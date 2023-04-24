import React, { useEffect } from "react";
import { Text, Stack } from "@mantine/core";
import {
  CampsiteCountryEnum,
  CampsiteFilters,
  CampsiteStateEnum,
  CampsiteTypeEnum,
  ToiletTypeEnum,
} from "models";
import { AmenityIconMap } from "constants/amenities";
import {
  CampsiteCountryStringMap,
  CampsiteStateStringMap,
  countryStateMap,
} from "constants/campsiteLocations";
import {
  MonthRangeFilter,
  MultiselectFilter,
  NumberFilter,
  NumberRangeFilter,
  SelectFilter,
  TextFilter,
  ThreeStateFilter,
} from "components";
import { campsiteTypeMap } from "constants/campsiteTypes";

// component for filter title, with short name for ease of use
const FT = (props: { label: string }) => {
  return (
    <Text fz="md" weight={500}>
      {props.label}
    </Text>
  );
};

type FiltersProps = {
  filterState: CampsiteFilters;
  handleFilterStateChange: (filters: CampsiteFilters) => void;
};

const Filters = (props: FiltersProps): JSX.Element => {
  const { filterState, handleFilterStateChange } = props;

  // clear out states in the filterState that don't correspond
  // to currently-selected country
  useEffect(() => {
    if (filterState.state) {
      const newStates = filterState.state.filter(
        (s) =>
          !filterState.country ||
          countryStateMap[filterState.country].includes(s)
      );
      handleFilterStateChange({
        ...filterState,
        state: newStates.length ? newStates : null,
      });
    }
  }, [filterState.country]); // eslint-disable-line react-hooks/exhaustive-deps

  const countryOptions = Object.values(CampsiteCountryEnum).map((s) => ({
    value: s,
    label: CampsiteCountryStringMap[s],
  }));

  const stateOptions = Object.values(CampsiteStateEnum)
    .filter(
      (s) =>
        !filterState.country || countryStateMap[filterState.country].includes(s)
    )
    .map((s) => ({
      value: s,
      label: CampsiteStateStringMap[s],
    }));

  const campsiteTypeOptions = Object.values(CampsiteTypeEnum).map((t) => ({
    value: t,
    label: campsiteTypeMap[t].label,
    group: campsiteTypeMap[t].category,
  }));

  const toiletOptions = Object.values(ToiletTypeEnum).map((t) => ({
    value: t,
    label: t,
  }));

  const handleGenericFilterChange = (
    filterKey: keyof CampsiteFilters,
    value: string | number | null
  ) => {
    handleFilterStateChange({
      ...filterState,
      [filterKey]: value,
    });
  };

  // handle three state filter change: true, false, or null
  const handleThreeStateFilterChange = (filterKey: keyof CampsiteFilters) => {
    const valueOptions = [true, false, null];
    const currentValueIndex = valueOptions.indexOf(
      filterState[filterKey] as boolean | null
    );
    const newValIndex = (currentValueIndex + 1) % 3;
    handleFilterStateChange({
      ...filterState,
      [filterKey]: valueOptions[newValIndex],
    });
  };

  const handleMultiselectFilterChange = (
    filterKey: keyof CampsiteFilters,
    value: string[]
  ) => {
    const newValue = value.length ? value : null;
    handleFilterStateChange({
      ...filterState,
      [filterKey]: newValue,
    });
  };

  const handleMonthRangeFilterChange = (
    openValue: number | null,
    closeValue: number | null
  ) => {
    handleFilterStateChange({
      ...filterState,
      month_open__lt: openValue,
      month_close__gt: closeValue,
    });
  };

  return (
    <Stack>
      <div>
        <FT label="Name" />
        <TextFilter<CampsiteFilters>
          filterKey="name__ct"
          value={filterState.name__ct}
          placeholderText="All campsite names"
          onChange={handleGenericFilterChange}
        />
      </div>
      <div>
        <FT label="Country" />
        <SelectFilter<CampsiteFilters>
          filterKey="country"
          options={countryOptions}
          value={filterState.country}
          placeholderText="All countries"
          onChange={handleGenericFilterChange}
        />
      </div>
      <div>
        <FT label="State/Province" />
        <MultiselectFilter<CampsiteFilters>
          filterKey="state"
          options={stateOptions}
          values={filterState.state || []}
          placeholderText="All states/provinces"
          onChange={handleMultiselectFilterChange}
        />
      </div>
      <div>
        <FT label="Campsite Type" />
        <MultiselectFilter<CampsiteFilters>
          filterKey="campsite_type"
          options={campsiteTypeOptions}
          values={filterState.campsite_type || []}
          placeholderText="All types"
          onChange={handleMultiselectFilterChange}
        />
      </div>
      <div>
        <FT label="Campsite Open Between" />
        <MonthRangeFilter<CampsiteFilters>
          openFilterKey="month_open__lt"
          closeFilterKey="month_close__gt"
          openValue={filterState.month_open__lt}
          closeValue={filterState.month_close__gt}
          openPlaceholderText="Opens before"
          closePlaceholderText="Closes after"
          onChange={handleMonthRangeFilterChange}
        />
      </div>
      <div>
        <FT label="Amenities" />
        <Stack spacing={5}>
          <ThreeStateFilter<CampsiteFilters>
            filterKey="has_drinking_water"
            label="Has drinking water"
            value={filterState.has_drinking_water}
            icon={AmenityIconMap.HAS_DRINKING_WATER}
            onChange={handleThreeStateFilterChange}
          />
          <ThreeStateFilter<CampsiteFilters>
            filterKey="has_toilets"
            label="Has toilets"
            value={filterState.has_toilets}
            icon={AmenityIconMap.HAS_TOILETS}
            onChange={handleThreeStateFilterChange}
          />
          <div style={{ marginLeft: "32px" }}>
            <MultiselectFilter<CampsiteFilters>
              disabled={!filterState.has_toilets}
              filterKey="toilet_type"
              options={toiletOptions}
              values={filterState.toilet_type || []}
              placeholderText="All types"
              onChange={handleMultiselectFilterChange}
            />
          </div>
          <ThreeStateFilter<CampsiteFilters>
            filterKey="has_showers"
            label="Has showers"
            value={filterState.has_showers}
            icon={AmenityIconMap.HAS_SHOWERS}
            onChange={handleThreeStateFilterChange}
          />
          <ThreeStateFilter<CampsiteFilters>
            filterKey="has_rv_hookup"
            label="Has RV hookup"
            value={filterState.has_rv_hookup}
            icon={AmenityIconMap.HAS_RV_HOOKUP}
            onChange={handleThreeStateFilterChange}
          />
          <ThreeStateFilter<CampsiteFilters>
            filterKey="accepts_pets"
            label="Accepts pets"
            value={filterState.accepts_pets}
            icon={AmenityIconMap.ACCEPTS_PETS}
            onChange={handleThreeStateFilterChange}
          />
          <ThreeStateFilter<CampsiteFilters>
            filterKey="low_no_fee"
            label="Low or no fee (<$12)"
            value={filterState.low_no_fee}
            icon={AmenityIconMap.LOW_NO_FEE}
            onChange={handleThreeStateFilterChange}
          />
          <ThreeStateFilter<CampsiteFilters>
            filterKey="accepts_reservations"
            label="Accepts reservations"
            value={filterState.accepts_reservations}
            icon={AmenityIconMap.ACCEPTS_RESERVATIONS}
            onChange={handleThreeStateFilterChange}
          />
        </Stack>
      </div>
      <div>
        <FT label="Number of Campsites" />
        <NumberRangeFilter<CampsiteFilters>
          minFilterKey="num_campsites__gt"
          maxFilterKey="num_campsites__lt"
          minValue={filterState.num_campsites__gt}
          maxValue={filterState.num_campsites__lt}
          minPlaceholderText="No minimum"
          maxPlaceholderText="No maximum"
          onChange={handleGenericFilterChange}
        />
      </div>
      <div>
        <FT label="Minimum Allowed RV Length (ft)" />
        <NumberFilter<CampsiteFilters>
          filterKey="max_rv_length__gt"
          value={filterState.max_rv_length__gt}
          placeholderText="No specified minimum length"
          onChange={handleGenericFilterChange}
        />
      </div>
      <div>
        <FT label="Miles to Nearest Town" />
        <NumberFilter<CampsiteFilters>
          filterKey="nearest_town_distance__lt"
          value={filterState.nearest_town_distance__lt}
          placeholderText="Any distance"
          onChange={handleGenericFilterChange}
        />
      </div>
      <div>
        <FT label="Campsite Elevation (ft)" />
        <NumberRangeFilter<CampsiteFilters>
          minFilterKey="elevation_ft__gt"
          maxFilterKey="elevation_ft__lt"
          minValue={filterState.elevation_ft__gt}
          maxValue={filterState.elevation_ft__lt}
          minPlaceholderText="No minimum"
          maxPlaceholderText="No maximum"
          onChange={handleGenericFilterChange}
        />
      </div>
    </Stack>
  );
};

export default Filters;
