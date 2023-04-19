import React from "react";
import { useParams } from "react-router";
import { useQuery } from "@tanstack/react-query";
import { Container, JsonInput, LoadingOverlay, Text, Title } from "@mantine/core";
import { Campsite } from "models";
import { getCampsite } from "http/campsites";

const CampsitesDetails = (): JSX.Element => {
  const { campsiteId } = useParams();

  const { data, isLoading, isError } = useQuery<Campsite, Error>(
    ["campsite", { id: campsiteId }],
    () => getCampsite(campsiteId as string),
    { retry: 1 }
  );

  if (isError) {
    throw new Response("Error", { status: 404 });
  }

  if (isLoading) return <LoadingOverlay visible={isLoading} overlayBlur={2} />;

  return (
    <Container>
      <Title order={1}>{data.name}</Title>
      <Text mt={10}>Detail page in progress. Raw campsite data:</Text>
      <JsonInput
        mt={10}
        autosize
        value={JSON.stringify(data, null, 4)}
      />
    </Container>
  );
};

export default CampsitesDetails;
