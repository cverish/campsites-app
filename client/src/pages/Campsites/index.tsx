import React, { useEffect, useState } from "react";
import { useSearchParams } from "react-router-dom";
import { useQuery } from "@tanstack/react-query";
import { Alert, Anchor, Container, Dialog, Tabs } from "@mantine/core";
import { Icon } from "@iconify/react";
import { CampsitesList } from "./components";
import { getCampsites } from "http/campsites";
import { CampsiteFilters, CampsiteList, SortByEnum, SortDirEnum } from "models";
import { defaultFilterState } from "constants/defaultFilterState";
import { filterNullValuesFromObject } from "utils/filterNullValues";
import QueryString from "query-string";

const Campsites = (): JSX.Element => {
  const [searchParams, setSearchParams] = useSearchParams();

  const [page, setPage] = useState<number>(0);
  const [totalPages, setTotalPages] = useState(0);
  const [filterState, setFilterState] = useState<CampsiteFilters>({
    ...defaultFilterState,
  });

  const itemsPerPage = 20;

  // set filter state and page based on search params on load.
  // page is set to 0 on load to indicate this should run.
  useEffect(() => {
    if (page === 0) {
      const params = QueryString.parse(searchParams.toString());
      try {
        setFilterState({
          ...defaultFilterState,
          ...JSON.parse(params.filters as string),
        });
      } catch {
        setFilterState({ ...defaultFilterState });
      }
      setPage(Number(params.page) || 1);
    }
  }, [searchParams, page]);

  // update search params when filter state or page number changes
  useEffect(() => {
    if (page > 0) {
      const params = new URLSearchParams({
        page: page.toString(),
        filters: JSON.stringify(
          filterNullValuesFromObject<CampsiteFilters>(filterState)
        ),
      });
      setSearchParams(params);
    }
  }, [page, filterState, setSearchParams]);

  // react-query handler for fetching data. Handles loading and error states
  // as well as refetching when filter state or page changes.
  // disabled when page is 0, that is, page has not yet been determined
  // from the query params
  const {
    data: campsites,
    isError,
    isFetching,
  } = useQuery<CampsiteList, Error>(
    [
      "campsites",
      page,
      ...Object.keys(filterState).map(
        (key) => filterState[key as keyof CampsiteFilters]
      ),
    ],
    async () => getCampsites(page, itemsPerPage, filterState),
    {
      enabled: page > 0,
      retry: 1,
    }
  );

  // determine the number of pages to render in pagination based on results
  useEffect(() => {
    if (campsites) {
      setTotalPages(Math.ceil(campsites?.num_total_results / itemsPerPage));
    }
  }, [campsites]);

  // function to toggle the sort direction between asc and desc
  // reset page to 1 when sort direction changes
  const toggleSortDir = () => {
    const newSortDir =
      filterState.sort_dir === SortDirEnum.ASC
        ? SortDirEnum.DESC
        : SortDirEnum.ASC;
    setFilterState({ ...filterState, sort_dir: newSortDir });
    setPage(1);
  };

  // function to change the sort by value
  // reset page to 1 when sort by changes
  const setSortBy = (newSortBy: SortByEnum) => {
    setFilterState({ ...filterState, sort_by: newSortBy });
    setPage(1);
  };

  // function to handle filter state change
  // reset page to 1 when filters change
  const handleFilterStateChange = (newFilterState: CampsiteFilters) => {
    setFilterState({ ...newFilterState });
    setPage(1);
  };

  const handleClearFilters = () => {
    setFilterState({ ...defaultFilterState });
    setPage(1);
  };

  return (
    <Container>
      <Tabs defaultValue="list">
        <Tabs.List>
          <Tabs.Tab
            value="list"
            icon={
              <Icon icon={"radix-icons:card-stack"} width={18} height={18} />
            }
          >
            List View
          </Tabs.Tab>
          <Tabs.Tab
            value="map"
            icon={
              <Icon icon={"mdi:map-marker-outline"} width={18} height={18} />
            }
          >
            Map View
          </Tabs.Tab>
        </Tabs.List>
        <>
          <Tabs.Panel value="list" pt="xs">
            <CampsitesList
              isFetching={isFetching}
              isError={isError}
              campsites={campsites?.items}
              numResults={campsites?.num_total_results}
              filterState={filterState}
              handleFilterStateChange={handleFilterStateChange}
              handleClearFilters={handleClearFilters}
              pageProps={{
                totalPages,
                page,
                setPage,
                itemsPerPage,
              }}
              sortProps={{
                sortDir: filterState.sort_dir,
                sortBy: filterState.sort_by,
                toggleSortDir,
                setSortBy,
              }}
            />
          </Tabs.Panel>
          <Tabs.Panel value="map" pt="xs">
            Map View - Coming soon 😉
          </Tabs.Panel>
        </>
      </Tabs>
      <Dialog opened={isError} p={0}>
        <Alert
          icon={<Icon icon="material-symbols:error-rounded" />}
          title="Problem loading campsites"
          color="red"
          variant="outline"
        >
          Something went wrong and the campsites could not be loaded. Try{" "}
          <Anchor href="/">refreshing the page.</Anchor>
        </Alert>
      </Dialog>
    </Container>
  );
};

export default Campsites;
