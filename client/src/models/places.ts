import { CampsiteCountryEnum, CampsiteStateEnum } from "models";

export type Place = {
  id: string;
  govt_id: string;
  name: string;
  generic_category: string;
  generic_term: string;
  county: string | null;
  state_province: CampsiteStateEnum;
  country: CampsiteCountryEnum;
  lat: number;
  lon: number;
  priority_order: number;
};

export type PlaceFilters = {
  state_province: CampsiteStateEnum[] | null;
  country: CampsiteCountryEnum | null;
  search_str__ct: string | null;
};
