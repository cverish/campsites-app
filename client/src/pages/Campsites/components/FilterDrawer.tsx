import React from "react";
import { Button, Drawer, Divider } from "@mantine/core";
import { CampsiteFilters } from "models";
import { Filters } from ".";
import { defaultFilterState } from "constants/defaultFilterState";

type FilterDrawerProps = {
  filterState: CampsiteFilters;
  setFilterState: (val: CampsiteFilters) => void;
  numResults: number | undefined;
  open: boolean;
  setClosed: () => void;
};

const FilterDrawer = (props: FilterDrawerProps): JSX.Element => {
  const resetFiltersDisabled =
    JSON.stringify(props.filterState) === JSON.stringify(defaultFilterState);

  const handleClearFiltersClick = () => {
    props.setFilterState({ ...defaultFilterState });
  };

  return (
    <Drawer.Root opened={props.open} onClose={props.setClosed} position="right">
      <Drawer.Overlay />
      <Drawer.Content maw="calc(100vw - 10%)">
        <Drawer.Header sx={{ zIndex: 2000 }}>
          <Drawer.Title sx={{ fontSize: 22, fontWeight: 600 }}>
            Filters
          </Drawer.Title>
          <Drawer.CloseButton />
        </Drawer.Header>
        <Drawer.Body sx={{ paddingBottom: 0 }}>
          <Filters
            filterState={props.filterState}
            setFilterState={props.setFilterState}
          />
          <div
            style={{
              width: "100%",
              textAlign: "center",
              paddingBottom: 16,
              position: "sticky",
              bottom: 0,
              backgroundColor: "white",
              zIndex: 2000,
            }}
          >
            <Divider
              my="md"
              pt={4}
              labelPosition="center"
              label={
                props.numResults !== undefined
                  ? `${props.numResults} results`
                  : "Loading..."
              }
            />
            <Button
              variant="outline"
              disabled={resetFiltersDisabled}
              onClick={handleClearFiltersClick}
              w="100%"
            >
              Clear Filters
            </Button>
          </div>
        </Drawer.Body>
      </Drawer.Content>
    </Drawer.Root>
  );
};

export default FilterDrawer;
