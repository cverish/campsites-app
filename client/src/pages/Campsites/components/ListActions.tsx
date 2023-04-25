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
  Grid,
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

type PageProps = {
  totalPages: number;
  page: number;
  setPage: (newPage: number) => void;
  itemsPerPage: number;
};

type ListActionProps = {
  isFetching: boolean;
  filterState: CampsiteFilters;
  handleFilterStateChange: (filters: CampsiteFilters) => void;
  handleClearFilters: () => void;
  sortProps: SortProps;
  pageProps: PageProps;
  numResults: number | undefined;
};

const SortDropdown = (props: { sortProps: SortProps }): JSX.Element => {
  const { sortBy, setSortBy, sortDir, toggleSortDir } = props.sortProps;

  const directionIcon = `tabler:sort-${sortDir}ending-letters`;

  const sortByOptions = Object.keys(SortByEnum).map((option) => ({
    value: option.toLowerCase(),
    label: option.replace("_", " ").toLowerCase(),
  }));

  return (
    <Popover position="bottom-end" shadow="sm">
      <Popover.Target>
        <Tooltip
          label={`Sort by: ${sortBy
            .replace("_", " ")
            .toLowerCase()} (${sortDir})`}
        >
          <ActionIcon color="blue" size="md">
            <Icon icon="material-symbols:sort-rounded" width={24} height={24} />
          </ActionIcon>
        </Tooltip>
      </Popover.Target>
      <Popover.Dropdown>
        <Text size="14px" pb={6}>
          Sort Settings
        </Text>
        <Grid align="flex-end" gutter="xs">
          <Grid.Col span="auto">
            <Select
              w={200}
              value={sortBy}
              data={sortByOptions}
              onChange={setSortBy}
            />
          </Grid.Col>
          <Grid.Col span="content" pb={8}>
            <Tooltip label={`Sort direction: ${sortDir}ending`}>
              <ActionIcon onClick={toggleSortDir} color="blue" size="md">
                <Icon icon={directionIcon} width={36} height={36} />
              </ActionIcon>
            </Tooltip>
          </Grid.Col>
        </Grid>
      </Popover.Dropdown>
    </Popover>
  );
};

const ListActions = (props: ListActionProps): JSX.Element => {
  const [filtersOpen, setFiltersOpen] = useState(false);

  // calculating the start result number to build display string
  // e.g. 1-20 of 1000
  const { pageProps } = props;
  const startResultNum = (pageProps.page - 1) * pageProps.itemsPerPage + 1;
  const endResultNum = pageProps.page * pageProps.itemsPerPage;
  const resultsText = `${startResultNum}-${endResultNum} of ${props.numResults}`;

  // get the number of applied filters -- remove sort filters
  const numAppliedFilters = Object.keys(
    filterNullValuesFromObject<CampsiteFilters>(props.filterState)
  ).filter((key) => !["sort_by", "sort_dir"].includes(key)).length;

  const onResetFiltersClick = () => {
    props.handleFilterStateChange({ ...defaultFilterState });
  };

  return (
    <>
      <Group spacing={5}>
        <Divider orientation="vertical" />
        <Text c="dimmed" fz="sm" px={5}>
          {props.isFetching || props.numResults === undefined
            ? "Loading..."
            : resultsText}
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
            zIndex={99}
          >
            <ActionIcon color="blue" size="md">
              <Icon icon="mdi:filter-outline" width={24} height={24} />
            </ActionIcon>
          </Indicator>
        </Tooltip>
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
        <SortDropdown sortProps={props.sortProps} />
      </Group>
      <FilterDrawer
        filterState={props.filterState}
        handleFilterStateChange={props.handleFilterStateChange}
        handleClearFilters={props.handleClearFilters}
        numResults={props.numResults}
        open={filtersOpen}
        setClosed={() => setFiltersOpen(false)}
      />
    </>
  );
};

export default ListActions;
