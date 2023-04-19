export enum CampsiteCountryEnum {
  CAN = "CAN",
  USA = "USA",
}

export enum CampsiteStateEnum {
  AK = "AK",
  AL = "AL",
  AR = "AR",
  AZ = "AZ",
  CA = "CA",
  CO = "CO",
  CT = "CT",
  DC = "DC",
  DE = "DE",
  FL = "FL",
  GA = "GA",
  HI = "HI",
  IA = "IA",
  ID = "ID",
  IL = "IL",
  IN = "IN",
  KS = "KS",
  KY = "KY",
  LA = "LA",
  MA = "MA",
  MD = "MD",
  ME = "ME",
  MI = "MI",
  MN = "MN",
  MO = "MO",
  MS = "MS",
  MT = "MT",
  NC = "NC",
  ND = "ND",
  NE = "NE",
  NH = "NH",
  NJ = "NJ",
  NM = "NM",
  NV = "NV",
  NY = "NY",
  OH = "OH",
  OK = "OK",
  OR = "OR",
  PA = "PA",
  RI = "RI",
  SC = "SC",
  SD = "SD",
  TN = "TN",
  TX = "TX",
  UT = "UT",
  VA = "VA",
  VT = "VT",
  WA = "WA",
  WI = "WI",
  WV = "WV",
  WY = "WY",
  AB = "AB",
  BC = "BC",
  MB = "MB",
  NB = "NB",
  NL = "NL",
  NT = "NT",
  NS = "NS",
  NU = "NU",
  ON = "ON",
  PE = "PE",
  QC = "QC",
  SK = "SK",
  YT = "YT",
}

export enum CampsiteTypeEnum {
  AMC = "AMC",
  AUTH = "AUTH",
  BLM = "BLM",
  BOR = "BOR",
  CNP = "CNP",
  COE = "COE",
  CP = "CP",
  MIL = "MIL",
  NF = "NF",
  NM = "NM",
  NP = "NP",
  NRA = "NRA",
  NS = "NS",
  NWR = "NWR",
  PP = "PP",
  PR = "PR",
  RES = "RES",
  SB = "SB",
  SCA = "SCA",
  SF = "SF",
  SFW = "SFW",
  SP = "SP",
  SPR = "SPR",
  SR = "SR",
  SRVA = "SRVA",
  SRA = "SRA",
  TVA = "TVA",
  USFW = "USFW",
  UTIL = "UTIL",
}

export enum BearingEnum {
  N = "N",
  NE = "NE",
  E = "E",
  SE = "SE",
  S = "S",
  SW = "SW",
  W = "W",
  NW = "NW",
}

export enum ToiletTypeEnum {
  FLUSH = "flush",
  VAULT = "vault",
  MIXED = "mixed",
  PIT = "pit",
}

export type Campsite = {
  id: string;
  code: string | null;
  name: string;
  country: CampsiteCountryEnum;
  state: CampsiteStateEnum;
  campsite_type: CampsiteTypeEnum | null;
  lon: number;
  lat: number;
  composite: string;
  comments: string | null;
  phone: string | null;
  month_open: number | null;
  month_close: number | null;
  elevation_ft: number | null;
  num_campsites: number | null;
  nearest_town: string | null;
  nearest_town_distance: number | null;
  nearest_town_bearing: BearingEnum | null;
  has_rv_hookup: boolean | null;
  has_water_hookup: boolean | null;
  has_electric_hookup: boolean | null;
  has_sewer_hookup: boolean | null;
  has_sanitary_dump: boolean | null;
  max_rv_length: number | null;
  has_toilets: boolean | null;
  toilet_type: ToiletTypeEnum | null;
  has_drinking_water: boolean | null;
  has_showers: boolean | null;
  accepts_reservations: boolean | null;
  accepts_pets: boolean | null;
  low_no_fee: boolean | null;
};

export type CampsiteList = {
  num_total_results: number;
  items: Campsite[];
};

export enum SortByEnum {
  CODE = "code",
  NAME = "name",
  STATE = "state",
  COUNTRY = "country",
  CAMPSITE_TYPE = "campsite_type",
}

export enum SortDirEnum {
  ASC = "asc",
  DESC = "desc",
}

export type CampsiteFilters = {
  sort_by: SortByEnum;
  sort_dir: SortDirEnum;
  code__ct: string | null;
  name__ct: string | null;
  state: CampsiteStateEnum[] | null;
  country: CampsiteCountryEnum | null;
  campsite_type: CampsiteTypeEnum[] | null;
  month_open__lt: number | null;
  month_close__gt: number | null;
  elevation_ft__gt: number | null;
  elevation_ft__lt: number | null;
  num_campsites__gt: number | null;
  num_campsites__lt: number | null;
  nearest_town_distance__lt: number | null;
  has_rv_hookup: boolean | null;
  has_water_hookup: boolean | null;
  has_electric_hookup: boolean | null;
  has_sewer_hookup: boolean | null;
  has_sanitary_dump: boolean | null;
  max_rv_length__gt: number | null;
  has_toilets: boolean | null;
  toilet_type: ToiletTypeEnum[] | null;
  has_drinking_water: boolean | null;
  has_showers: boolean | null;
  accepts_reservations: boolean | null;
  accepts_pets: boolean | null;
  low_no_fee: boolean | null;
};
