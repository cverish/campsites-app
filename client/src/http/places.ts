import http from "http/http";
import { Place, PlaceFilters } from "models";
import { filterNullValuesFromObject } from "utils/filterNullValues";
import QueryString from "query-string";

export const getPlaces = async (
  filterState: PlaceFilters
): Promise<Place[]> => {
  // remove null filters from filterState
  const nonNullFilters =
    filterNullValuesFromObject<PlaceFilters>(filterState);
  const query = QueryString.stringify(nonNullFilters);
  const results = await http.get<Place[]>(
    `/places?offset=0&limit=25&${query}`
  );
  return results.data;
};