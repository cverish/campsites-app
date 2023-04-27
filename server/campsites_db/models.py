from typing import Optional
import uuid
from enum import Enum
from pydantic import UUID4

import sqlalchemy as sa
from geoalchemy2 import Geometry
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped
from sqlalchemy.dialects.postgresql import UUID


class Base(DeclarativeBase):
    pass

class CampsiteStateEnum(str, Enum):
    AK = "AK"
    AL = "AL"
    AR = "AR"
    AZ = "AZ"
    CA = "CA"
    CO = "CO"
    CT = "CT"
    DC = "DC"
    DE = "DE"
    FL = "FL"
    GA = "GA"
    HI = "HI"
    IA = "IA"
    ID = "ID"
    IL = "IL"
    IN = "IN"
    KS = "KS"
    KY = "KY"
    LA = "LA"
    MA = "MA"
    MD = "MD"
    ME = "ME"
    MI = "MI"
    MN = "MN"
    MO = "MO"
    MS = "MS"
    MT = "MT"
    NC = "NC"
    ND = "ND"
    NE = "NE"
    NH = "NH"
    NJ = "NJ"
    NM = "NM"
    NV = "NV"
    NY = "NY"
    OH = "OH"
    OK = "OK"
    OR = "OR"
    PA = "PA"
    RI = "RI"
    SC = "SC"
    SD = "SD"
    TN = "TN"
    TX = "TX"
    UT = "UT"
    VA = "VA"
    VT = "VT"
    WA = "WA"
    WI = "WI"
    WV = "WV"
    WY = "WY"
    AB = "AB"
    BC = "BC"
    MB = "MB"
    NB = "NB"
    NL = "NL"
    NT = "NT"
    NS = "NS"
    NU = "NU"
    ON = "ON"
    PE = "PE"
    QC = "QC"
    SK = "SK"
    YT = "YT"


class CampsiteCountryEnum(str, Enum):
    CAN = "CAN"
    USA = "USA"


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

    id: Mapped[UUID4] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    code: Mapped[Optional[str]]
    name: Mapped[str]
    state: Mapped[CampsiteStateEnum]
    country: Mapped[CampsiteCountryEnum]
    campsite_type: Mapped[Optional[CampsiteTypeEnum]]
    lon: Mapped[float]
    lat: Mapped[float]
    geo: Mapped[Geometry] = mapped_column(Geometry("POINT", srid=4326))
    composite: Mapped[str]
    comments: Mapped[Optional[str]]
    phone: Mapped[Optional[str]]
    month_open: Mapped[Optional[int]]
    month_close: Mapped[Optional[int]]
    elevation_ft: Mapped[Optional[int]]
    num_campsites: Mapped[Optional[int]]
    nearest_town: Mapped[Optional[str]]
    nearest_town_distance: Mapped[Optional[float]]
    nearest_town_bearing: Mapped[Optional[BearingEnum]]
    # amenities
    has_rv_hookup: Mapped[Optional[bool]]
    has_water_hookup: Mapped[Optional[bool]]
    has_electric_hookup: Mapped[Optional[bool]]
    has_sewer_hookup: Mapped[Optional[bool]]
    has_sanitary_dump: Mapped[Optional[bool]]
    max_rv_length: Mapped[Optional[int]]
    has_toilets: Mapped[Optional[bool]]
    toilet_type: Mapped[Optional[ToiletTypeEnum]]
    has_drinking_water: Mapped[Optional[bool]]
    has_showers: Mapped[Optional[bool]]
    accepts_reservations: Mapped[Optional[bool]]
    accepts_pets: Mapped[Optional[bool]]
    low_no_fee: Mapped[Optional[bool]]
