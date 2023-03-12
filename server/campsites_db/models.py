from enum import Enum
import uuid
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class CampsiteTypeEnum(str, Enum):
    AMC = "AMC"
    AUTH = "AUTH"
    BLM = "BLM"
    BOR = "BOR"
    CNP = "CNP"
    COE = "COE"
    CP = "CP"
    MIL = "MIL"
    NF = "NF"
    NM = "NM"
    NP = "NP"
    NRA = "NRA"
    NS = "NS"
    NWR = "NWR"
    PP = "PP"
    PR = "PR"
    RES = "RES"
    SB = "SB"
    SCA = "SCA"
    SF = "SF"
    SFW = "SFW"
    SP = "SP"
    SPR = "SPR"
    SR = "SR"
    SRVA = "SRVA"
    SRA = "SRA"
    TVA = "TVA"
    USFW = "USFW"
    UTIL = "UTIL"


class BearingEnum(str, Enum):
    N = "N"
    NE = "NE"
    E = "E"
    SE = "SE"
    S = "S"
    SW = "SW"
    W = "W"
    NW = "NW"


class ToiletTypeEnum(str, Enum):
    flush = "flush"
    vault = "vault"
    mixed = "mixed"
    pit = "pit"


class Campsite(Base):
    __tablename__ = "campsites"

    id = sa.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    code = sa.Column(sa.String, nullable=True)
    name = sa.Column(sa.String, nullable=False)
    state = sa.Column(sa.String, nullable=False)
    campsite_type = sa.Column(sa.Enum(CampsiteTypeEnum), nullable=True)
    lon = sa.Column(sa.DOUBLE_PRECISION, nullable=False)
    lat = sa.Column(sa.DOUBLE_PRECISION, nullable=False)
    composite = sa.Column(sa.Text, nullable=False)
    comments = sa.Column(sa.Text, nullable=True)
    phone = sa.Column(sa.String, nullable=True)
    month_open = sa.Column(sa.Integer, nullable=True)
    month_close = sa.Column(sa.Integer, nullable=True)
    elevation_ft = sa.Column(sa.Integer, nullable=True)
    num_campsites = sa.Column(sa.Integer, nullable=True)
    nearest_town = sa.Column(sa.String, nullable=True)
    nearest_town_distance = sa.Column(sa.Float, nullable=True)
    nearest_town_bearing = sa.Column(sa.Enum(BearingEnum), nullable=True)
    # amenities
    has_water_hookup = sa.Column(sa.Boolean, nullable=True)
    has_electric_hookup = sa.Column(sa.Boolean, nullable=True)
    has_sewer_hookup = sa.Column(sa.Boolean, nullable=True)
    has_sanitary_dump = sa.Column(sa.Boolean, nullable=True)
    max_rv_length = sa.Column(sa.Integer, nullable=True)
    has_toilets = sa.Column(sa.Boolean, nullable=True)
    toilet_type = sa.Column(sa.Enum(ToiletTypeEnum), nullable=True)
    has_drinking_water = sa.Column(sa.Boolean, nullable=True)
    has_showers = sa.Column(sa.Boolean, nullable=True)
    accepts_reservations = sa.Column(sa.Boolean, nullable=True)
    accepts_pets = sa.Column(sa.Boolean, nullable=True)
    low_no_fee = sa.Column(sa.Boolean, nullable=True)
