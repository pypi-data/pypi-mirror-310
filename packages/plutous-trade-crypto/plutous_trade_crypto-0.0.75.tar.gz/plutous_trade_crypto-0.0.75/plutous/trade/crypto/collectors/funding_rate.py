import asyncio
from datetime import datetime, timedelta

from plutous import database as db
from plutous.trade.crypto.enums import CollectorType
from plutous.trade.crypto.models import FundingRate, FundingSettlement

from .base import BaseCollector, BaseCollectorConfig

TIMEOUT = timedelta(minutes=2)


class FundingRateCollectorConfig(BaseCollectorConfig):
    symbol_type: str = "swap"
    sleep_time: int = 30


class FundingRateCollector(BaseCollector):
    COLLECTOR_TYPE = CollectorType.FUNDING_RATE
    TABLE = FundingRate

    config: FundingRateCollectorConfig

    async def _collect(self):
        active_symbols = await self.fetch_active_symbols()
        while True:
            await self.exchange.load_markets(reload=True)
            if hasattr(self.exchange, "fetch_funding_rates"):
                funding_rates = list(
                    (await self.exchange.fetch_funding_rates(active_symbols)).values()
                )
            else:
                funding_rates = await asyncio.gather(
                    *[
                        self.exchange.fetch_funding_rate(symbol)
                        for symbol in active_symbols
                    ]
                )
            if funding_rates[0]["timestamp"] < int(
                (datetime.now() - TIMEOUT).timestamp() * 1000
            ):
                raise RuntimeError(
                    f"Data is stale, last updated at {funding_rates[0]['timestamp']}"
                )
            fr = [
                FundingRate(
                    symbol=funding_rate["symbol"],
                    exchange=self._exchange,
                    timestamp=self.round_milliseconds(funding_rate["timestamp"]),
                    funding_rate=funding_rate["fundingRate"] * 100,
                    datetime=self.exchange.iso8601(
                        self.round_milliseconds(funding_rate["timestamp"])
                    ),
                    settlement_timestamp=funding_rate["fundingTimestamp"],
                    settlement_datetime=funding_rate["fundingDatetime"],
                    funding_interval=(
                        funding_rate["interval"][:-1]
                        if funding_rate["interval"]
                        else None
                    ),
                )
                for funding_rate in funding_rates
                if funding_rate["fundingRate"] is not None
            ]

            fs = [
                FundingSettlement(
                    symbol=funding_rate.symbol,
                    exchange=self._exchange,
                    funding_rate=funding_rate.funding_rate * 100,
                    timestamp=funding_rate.settlement_timestamp,
                    datetime=funding_rate.settlement_datetime,
                )
                for funding_rate in fr
                if (
                    funding_rate.settlement_timestamp - funding_rate.timestamp
                    < 60 * 1000
                )
            ]
            with db.Session() as session:
                self._insert(fr, session, FundingRate)
                self._insert(fs, session, FundingSettlement)
                session.commit()
            await asyncio.sleep(self.config.sleep_time)
