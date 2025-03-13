import React from "react";
import {
  Button,
  Container,
  Divider,
  Grid,
  Pagination,
  Text,
} from "@mantine/core";
import { ScrollToTopButton, CampsiteCard, ListActions, SkeletonCards } from ".";
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
  itemsPerPage: number;
};

type CampsitesListProps = {
  isFetching: boolean;
  isError: boolean;
  campsites: Campsite[] | undefined;
  numResults: number | undefined;
  filterState: CampsiteFilters;
  handleFilterStateChange: (filters: CampsiteFilters) => void;
  handleClearFilters: () => void;
  pageProps: PageProps;
  sortProps: SortProps;
};

const CampsitesList = (props: CampsitesListProps): JSX.Element => {
  const { totalPages, page, setPage } = props.pageProps;
  const [, scrollTo] = useWindowScroll();

  const showPagination =
    !(props.isFetching || props.isError) &&
    !!props.campsites &&
    !!props.numResults;

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
            pageProps={props.pageProps}
            filterState={props.filterState}
            handleFilterStateChange={props.handleFilterStateChange}
            handleClearFilters={props.handleClearFilters}
          />
        }
      />
      {props.isFetching || props.isError ? (
        <SkeletonCards numCards={4} />
      ) : props.campsites && props.numResults ? (
        <Grid>
          {props.campsites.map((campsite) => (
            <Grid.Col sm={6} key={campsite.id}>
              <CampsiteCard campsite={campsite} />
            </Grid.Col>
          ))}
        </Grid>
      ) : (
        <div style={{ height: 225, width: "100%", textAlign: "center" }}>
          <Text size="16px">No Results.</Text>
          <Button mt={10} onClick={props.handleClearFilters}>
            Reset Filters
          </Button>
        </div>
      )}
      {showPagination && (
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
      )}
      <ScrollToTopButton />
    </Container>
  );
};

export default CampsitesList;
