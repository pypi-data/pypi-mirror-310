"""added orderbbook

Revision ID: 77203ed2c699
Revises: bf8hgsm873ff
Create Date: 2024-07-14 03:28:06.799955

"""

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "77203ed2c699"
down_revision = "bf8hgsm873ff"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    exchange_enum = postgresql.ENUM(name="exchange", schema="public", create_type=False)
    op.create_table(
        "orderbook",
        sa.Column("bids", postgresql.JSONB(), nullable=False),
        sa.Column("asks", postgresql.JSONB(), nullable=False),
        sa.Column("exchange", exchange_enum, nullable=False),
        sa.Column("symbol", sa.String(), nullable=False),
        sa.Column("timestamp", sa.BIGINT(), nullable=False),
        sa.Column("datetime", sa.DateTime(), nullable=False),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.TIMESTAMP(), nullable=False),
        sa.Column("updated_at", sa.TIMESTAMP(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        schema="crypto",
    )
    op.create_index(
        "ix_orderbook_created_at",
        "orderbook",
        ["created_at"],
        unique=False,
        schema="crypto",
    )
    op.create_index(
        "ix_orderbook_exchange_symbol_timestamp",
        "orderbook",
        ["exchange", "symbol", "timestamp"],
        unique=True,
        schema="crypto",
    )
    op.create_index(
        "ix_orderbook_time_of_minute",
        "orderbook",
        [sa.text("EXTRACT(minute from datetime)")],
        unique=False,
        schema="crypto",
    )
    op.create_index(
        "ix_orderbook_timestamp",
        "orderbook",
        ["timestamp"],
        unique=False,
        schema="crypto",
    )
    op.create_index(
        "ix_orderbook_updated_at",
        "orderbook",
        ["updated_at"],
        unique=False,
        schema="crypto",
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index("ix_orderbook_updated_at", table_name="orderbook", schema="crypto")
    op.drop_index("ix_orderbook_timestamp", table_name="orderbook", schema="crypto")
    op.drop_index(
        "ix_orderbook_time_of_minute", table_name="orderbook", schema="crypto"
    )
    op.drop_index(
        "ix_orderbook_exchange_symbol_timestamp",
        table_name="orderbook",
        schema="crypto",
    )
    op.drop_index("ix_orderbook_created_at", table_name="orderbook", schema="crypto")
    op.drop_table("orderbook", schema="crypto")
    # ### end Alembic commands ###
