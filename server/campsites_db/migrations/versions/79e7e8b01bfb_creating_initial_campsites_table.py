"""creating initial campsites table

Revision ID: 79e7e8b01bfb
Revises:
Create Date: 2023-03-12 18:24:06.877618

"""
import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql as ps

# revision identifiers, used by Alembic.
revision = "79e7e8b01bfb"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # manual commands

    # creating enums
    campsite_state_enum = ps.ENUM(
        "AK",
        "AL",
        "AR",
        "AZ",
        "CA",
        "CO",
        "CT",
        "DC",
        "DE",
        "FL",
        "GA",
        "HI",
        "IA",
        "ID",
        "IL",
        "IN",
        "KS",
        "KY",
        "LA",
        "MA",
        "MD",
        "ME",
        "MI",
        "MN",
        "MO",
        "MS",
        "MT",
        "NC",
        "ND",
        "NE",
        "NH",
        "NJ",
        "NM",
        "NV",
        "NY",
        "OH",
        "OK",
        "OR",
        "PA",
        "RI",
        "SC",
        "SD",
        "TN",
        "TX",
        "UT",
        "VA",
        "VT",
        "WA",
        "WI",
        "WV",
        "WY",
        "AB",
        "BC",
        "MB",
        "NB",
        "NL",
        "NT",
        "NS",
        "NU",
        "ON",
        "PE",
        "QC",
        "SK",
        "YT",
        name="campsite_state_enum",
    )

    campsite_country_enum = ps.ENUM("CAN", "USA", name="campsite_country_enum")

    campsite_type_enum = ps.ENUM(
        "AMC",
        "AUTH",
        "BLM",
        "BOR",
        "CNP",
        "COE",
        "CP",
        "MIL",
        "NF",
        "NM",
        "NP",
        "NRA",
        "NS",
        "NWR",
        "PP",
        "PR",
        "RES",
        "SB",
        "SCA",
        "SF",
        "SFW",
        "SP",
        "SPR",
        "SR",
        "SRVA",
        "SRA",
        "TVA",
        "USFW",
        "UTIL",
        name="campsite_type_enum",
    )

    bearing_enum = ps.ENUM(
        "N", "NE", "E", "SE", "S", "SW", "W", "NW", name="bearing_enum"
    )

    toilet_type_enum = ps.ENUM(
        "flush", "vault", "mixed", "pit", name="toilet_type_enum"
    )

    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "campsites",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("code", sa.String(), nullable=True),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("country", campsite_country_enum, nullable=False),
        sa.Column("state", campsite_state_enum, nullable=False),
        sa.Column("campsite_type", campsite_type_enum, nullable=True),
        sa.Column("lon", sa.DOUBLE_PRECISION(), nullable=False),
        sa.Column("lat", sa.DOUBLE_PRECISION(), nullable=False),
        sa.Column("composite", sa.Text(), nullable=False),
        sa.Column("comments", sa.Text(), nullable=True),
        sa.Column("phone", sa.String(), nullable=True),
        sa.Column("month_open", sa.Integer(), nullable=True),
        sa.Column("month_close", sa.Integer(), nullable=True),
        sa.Column("elevation_ft", sa.Integer(), nullable=True),
        sa.Column("num_campsites", sa.Integer(), nullable=True),
        sa.Column("nearest_town", sa.String(), nullable=True),
        sa.Column("nearest_town_distance", sa.Float(), nullable=True),
        sa.Column("nearest_town_bearing", bearing_enum, nullable=True),
        sa.Column("has_water_hookup", sa.Boolean(), nullable=True),
        sa.Column("has_electric_hookup", sa.Boolean(), nullable=True),
        sa.Column("has_sewer_hookup", sa.Boolean(), nullable=True),
        sa.Column("has_sanitary_dump", sa.Boolean(), nullable=True),
        sa.Column("max_rv_length", sa.Integer(), nullable=True),
        sa.Column("has_toilets", sa.Boolean(), nullable=True),
        sa.Column("toilet_type", toilet_type_enum, nullable=True),
        sa.Column("has_drinking_water", sa.Boolean(), nullable=True),
        sa.Column("has_showers", sa.Boolean(), nullable=True),
        sa.Column("accepts_reservations", sa.Boolean(), nullable=True),
        sa.Column("accepts_pets", sa.Boolean(), nullable=True),
        sa.Column("low_no_fee", sa.Boolean(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("campsites")
    # ### end Alembic commands ###
    # manual enum drops
    bind = op.get_bind()
    sa.Enum(name="campsite_state_enum").drop(bind, checkfirst=False)
    sa.Enum(name="campsite_country_enum").drop(bind, checkfirst=False)
    sa.Enum(name="campsite_type_enum").drop(bind, checkfirst=False)
    sa.Enum(name="bearing_enum").drop(bind, checkfirst=False)
    sa.Enum(name="toilet_type_enum").drop(bind, checkfirst=False)
