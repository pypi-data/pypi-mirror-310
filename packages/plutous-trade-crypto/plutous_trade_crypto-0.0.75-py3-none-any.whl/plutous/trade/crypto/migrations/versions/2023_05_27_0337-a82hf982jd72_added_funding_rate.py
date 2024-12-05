"""init

Revision ID: a82hf982jd72
Revises: h283gd092hd8
Create Date: 2023-05-27 03:37:07.240615

"""

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "a82hf982jd72"
down_revision = "h283gd092hd8"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    exchange_enum = postgresql.ENUM(name="exchange", schema="public", create_type=False)
    op.create_table(
        "funding_rate",
        sa.Column("funding_rate", sa.DECIMAL(precision=7, scale=6), nullable=False),
        sa.Column("settlement_datetime", sa.DateTime(), nullable=False),
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
        "ix_funding_rate_created_at",
        "funding_rate",
        ["created_at"],
        unique=False,
        schema="crypto",
    )
    op.create_index(
        "ix_funding_rate_exchange_symbol_timestamp",
        "funding_rate",
        ["exchange", "symbol", "timestamp"],
        unique=True,
        schema="crypto",
    )
    op.create_index(
        "ix_funding_rate_timestamp",
        "funding_rate",
        ["timestamp"],
        unique=False,
        schema="crypto",
    )
    op.create_index(
        "ix_funding_rate_time_of_minute",
        "funding_rate",
        [sa.text("EXTRACT(minute from datetime)")],
        unique=False,
        schema="crypto",
    )
    op.create_index(
        "ix_funding_rate_updated_at",
        "funding_rate",
        ["updated_at"],
        unique=False,
        schema="crypto",
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    # FundingRate
    op.drop_index(
        "ix_funding_rate_updated_at", table_name="funding_rate", schema="crypto"
    )
    op.drop_index(
        "ix_funding_rate_time_of_minute", table_name="funding_rate", schema="crypto"
    )
    op.drop_index(
        "ix_funding_rate_timestamp_exchange_symbol",
        table_name="funding_rate",
        schema="crypto",
    )
    op.drop_index(
        "ix_funding_rate_created_at", table_name="funding_rate", schema="crypto"
    )
    op.drop_table("funding_rate", schema="crypto")
    # ### end Alembic commands ###
