import React from "react";
import { Container, Divider, Grid, Pagination, Skeleton } from "@mantine/core";
import { ScrollToTopButton, CampsiteCard, ListActions } from ".";
import { Campsite, CampsiteFilters, SortByEnum, SortDirEnum } from "models";
import { useWindowScroll } from "@mantine/hooks";

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
};

type CampsitesListProps = {
  isFetching: boolean;
  isError: boolean;
  campsites: Campsite[] | undefined;
  numResults: number | undefined;
  filterState: CampsiteFilters;
  handleFilterStateChange: (filters: CampsiteFilters) => void;
  pageProps: PageProps;
  sortProps: SortProps;
};

const CampsitesList = (props: CampsitesListProps): JSX.Element => {
  const { totalPages, page, setPage } = props.pageProps;
  const [, scrollTo] = useWindowScroll();

  const handlePaginationChange = (newPage: number) => {
    setPage(newPage);
    scrollTo({ y: 0 });
  };

  return (
    <Container>
      <Divider
        my="md"
        labelPosition="right"
        label={
          <ListActions
            isFetching={props.isFetching}
            numResults={props.numResults}
            sortProps={props.sortProps}
            filterState={props.filterState}
            handleFilterStateChange={props.handleFilterStateChange}
          />
        }
      />
      <Grid>
        {props.isFetching || props.isError ? (
          [...Array(4)].map((e, i) => (
            <Grid.Col sm={6} key={i}>
              <Skeleton height={225} mt="sm" radius="md" />
            </Grid.Col>
          ))
        ) : props.campsites ? (
          props.campsites.map((campsite) => (
            <Grid.Col sm={6} key={campsite.id}>
              <CampsiteCard campsite={campsite} />
            </Grid.Col>
          ))
        ) : (
          <div />
        )}
      </Grid>
      <Divider
        my="md"
        labelPosition="center"
        label={
          <Pagination
            size="sm"
            total={totalPages}
            value={page}
            onChange={handlePaginationChange}
          />
        }
      />
      <ScrollToTopButton />
    </Container>
  );
};

export default CampsitesList;
