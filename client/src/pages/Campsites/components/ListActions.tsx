import React, { useState } from "react";
import {
  ActionIcon,
  Divider,
  Group,
  Popover,
  Select,
  Tooltip,
  Text,
  Indicator,
} from "@mantine/core";
import { CampsiteFilters, SortByEnum, SortDirEnum } from "models";
import { Icon } from "@iconify/react";
import { filterNullValuesFromObject } from "utils/filterNullValues";
import { defaultFilterState } from "constants/defaultFilterState";
import { FilterDrawer } from "./";

type SortProps = {
  sortBy: SortByEnum;
  sortDir: SortDirEnum;
  toggleSortDir: () => void;
  setSortBy: (newSortBy: SortByEnum) => void;
};

type ListActionProps = {
  isFetching: boolean;
  filterState: CampsiteFilters;
  handleFilterStateChange: (filters: CampsiteFilters) => void;
  handleClearFilters: () => void;
  sortProps: SortProps;
  numResults: number | undefined;
};

const ListActions = (props: ListActionProps): JSX.Element => {
  const { sortBy, sortDir, toggleSortDir, setSortBy } = props.sortProps;
  const [filtersOpen, setFiltersOpen] = useState(false);

  const directionIcon = `tabler:sort-${sortDir}ending-letters`;
  const sortByOptions = Object.keys(SortByEnum).map((option) => ({
    value: option.toLowerCase(),
    label: option.replace("_", " ").toLowerCase(),
  }));

  // get the number of applied filters -- remove sort filters
  const numAppliedFilters = Object.keys(
    filterNullValuesFromObject<CampsiteFilters>(props.filterState)
  ).filter((key) => !["sort_by", "sort_dir"].includes(key)).length;

  const onResetFiltersClick = () => {
    props.handleFilterStateChange({ ...defaultFilterState });
  };

  return (
    <Group spacing={5}>
      <Divider orientation="vertical" />
      <Text c="dimmed" fz="sm" px={5}>
        {props.isFetching || props.numResults === undefined
          ? "Loading..."
          : `${props.numResults} Results`}
      </Text>
      <Divider orientation="vertical" />
      <Tooltip
        label={`Filters: ${numAppliedFilters} applied`}
        onClick={() => setFiltersOpen(true)}
      >
        <Indicator
          size={8}
          position="bottom-end"
          offset={6}
          inline
          disabled={numAppliedFilters === 0}
        >
          <ActionIcon color="blue" size="md">
            <Icon icon="mdi:filter-outline" width={24} height={24} />
          </ActionIcon>
        </Indicator>
      </Tooltip>
      <FilterDrawer
        filterState={props.filterState}
        handleFilterStateChange={props.handleFilterStateChange}
        handleClearFilters={props.handleClearFilters}
        numResults={props.numResults}
        open={filtersOpen}
        setClosed={() => setFiltersOpen(false)}
      />
      <ActionIcon
        onClick={onResetFiltersClick}
        color="gray"
        size="md"
        disabled={numAppliedFilters === 0}
      >
        <Tooltip label={`Reset Filters`}>
          <Icon icon="mdi:filter-off-outline" width={24} height={24} />
        </Tooltip>
      </ActionIcon>
      <Divider orientation="vertical" />
      <Popover position="bottom-end" shadow="sm">
        <Popover.Target>
          <Tooltip label={`Sort by: ${sortBy.replace("_", " ").toLowerCase()}`}>
            <ActionIcon color="blue" size="md">
              <Icon
                icon="material-symbols:sort-rounded"
                width={24}
                height={24}
              />
            </ActionIcon>
          </Tooltip>
        </Popover.Target>
        <Popover.Dropdown>
          <div style={{ padding: "6px 6px 12px 6px" }}>
            <Select
              label="Sort by"
              w={200}
              value={sortBy}
              data={sortByOptions}
              onChange={setSortBy}
            />
          </div>
        </Popover.Dropdown>
      </Popover>
      <Tooltip label={`Sort direction: ${sortDir}ending`}>
        <ActionIcon onClick={toggleSortDir} color="blue" size="md">
          <Icon icon={directionIcon} width={24} height={24} />
        </ActionIcon>
      </Tooltip>
    </Group>
  );
};

export default ListActions;
