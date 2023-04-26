"""Adding geospacial column

Revision ID: 578280956c02
Revises: 79e7e8b01bfb
Create Date: 2023-04-26 03:45:33.656287

"""
from alembic import op
import sqlalchemy as sa
from geoalchemy2 import Geometry
from geoalchemy2.shape import from_shape
from shapely.geometry import Point


# revision identifiers, used by Alembic.
revision = "578280956c02"
down_revision = "79e7e8b01bfb"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # setting nullable to True first, so upgrading the table doesn't
    # throw errors.
    op.add_column(
        "campsites",
        sa.Column(
            "geo",
            Geometry(
                geometry_type="POINT",
                srid=4326,
                from_text="ST_GeomFromEWKT",
                name="geometry",
            ),
            nullable=True,
        ),
    )

    # use the existing `lat` and `lon` columns for each Campsite to
    # populate the `geo` column
    conn = op.get_bind()
    results = conn.execute(sa.text("select id, lat, lon from campsites")).fetchall()

    # update all rows
    for result in results:
        id, lat, lon = result
        conn.execute(
            sa.text(
                f"UPDATE campsites SET geo = ST_SetSRID(ST_MakePoint({lon}, {lat}), 4326) WHERE id = '{id}'"
            )
        )

    # set column as non-nullable
    op.alter_column("campsites", "geo", nullable=False)


def downgrade() -> None:
    op.drop_column("campsites", "geo")
