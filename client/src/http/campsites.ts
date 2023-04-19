import { Campsite, CampsiteFilters, CampsiteList } from "models";
import http from "http/http";
import { filterNullValuesFromObject } from "utils/filterNullValues";
import QueryString from "query-string";

export const getCampsites = async (
  page: number,
  limit: number = 25,
  filterState: CampsiteFilters
): Promise<CampsiteList> => {
  // calculate the offset to give to the API based on the page and limit
  // pagination component has index of 1, so we need to index it to 0 instead
  const offset = (page - 1) * limit;
  // remove null filters from filterState
  const nonNullFilters =
    filterNullValuesFromObject<CampsiteFilters>(filterState);
  const query = QueryString.stringify(nonNullFilters);
  const results = await http.get<CampsiteList>(
    `/campsites?offset=${offset}&limit=${limit}&${query}`
  );
  return results.data;
};

export const getCampsite = async (campsiteId: string): Promise<Campsite> => {
  const result = await http.get<Campsite>(`/campsites/campsite/${campsiteId}`);
  return result.data;
};
