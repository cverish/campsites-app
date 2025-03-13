import React from "react";
import { Grid, Skeleton } from "@mantine/core";


const SkeletonCards = (props: { numCards: number }): JSX.Element => {
  return (
    <Grid>
      {[...Array(props.numCards)].map((e, i) => (
        <Grid.Col sm={6} key={i}>
          <Skeleton height={225} mt="sm" radius="md" />
        </Grid.Col>
      ))}
    </Grid>
  );
};

export default SkeletonCards;
