import React from "react";
import { Link } from "react-router-dom";
import { Card, Text, Stack, Group } from "@mantine/core";
import { Campsite } from "models";
import {
  CampsiteCountryStringMap,
  CampsiteStateStringMap,
} from "constants/campsiteLocations";
import { AmenityIcon, CampsiteTypeBadge } from "components";
import { AmenityIconMap } from "constants/amenities";

const Amenities = (props: { campsite: Campsite }): JSX.Element => {
  const {
    has_rv_hookup,
    has_drinking_water,
    has_toilets,
    has_showers,
    accepts_pets,
    low_no_fee,
    accepts_reservations,
  } = props.campsite;

  return (
    <Group spacing={5}>
      <AmenityIcon
        icon={AmenityIconMap.HAS_DRINKING_WATER}
        status={has_drinking_water}
        description="Is there potable water on site?"
        size="lg"
      />
      <AmenityIcon
        icon={AmenityIconMap.HAS_TOILETS}
        status={has_toilets}
        description="Are toilets of any kind present on site?"
        size="lg"
      />
      <AmenityIcon
        icon={AmenityIconMap.HAS_SHOWERS}
        status={has_showers}
        description="Are showers present on site?"
        size="lg"
      />
      <AmenityIcon
        icon={AmenityIconMap.HAS_RV_HOOKUP}
        status={has_rv_hookup}
        description="Does this site have amenities related to RVs (electric hookups, sewer hookups, water hookups, sanitary dumps)?"
        size="lg"
      />
      <AmenityIcon
        icon={AmenityIconMap.ACCEPTS_PETS}
        status={accepts_pets}
        description="Are pets allowed?"
        size="lg"
      />
      <AmenityIcon
        icon={AmenityIconMap.LOW_NO_FEE}
        status={low_no_fee}
        description="Does this site charge low/no fee (less than $12)?"
        size="lg"
      />
      <AmenityIcon
        icon={AmenityIconMap.ACCEPTS_RESERVATIONS}
        status={accepts_reservations}
        description="Does this site accept reservations?"
        size="lg"
      />
    </Group>
  );
};

const CampsiteCard = (props: { campsite: Campsite }): JSX.Element => {
  const {
    id,
    name,
    state,
    country,
    nearest_town,
    nearest_town_distance,
    nearest_town_bearing,
    campsite_type,
  } = props.campsite;

  return (
    <Card shadow="md" radius="md" padding="lg" mt="sm" withBorder>
      <Stack align="flex-start" mih={225} justify="space-between">
        <div>
          <div>
            <Text
              weight={600}
              size="22px"
              component={Link}
              to={`/campsite/${id}`}
            >
              {name}
            </Text>
          </div>
          <div>
            <Text size="16px">
              {CampsiteStateStringMap[state]},{" "}
              {CampsiteCountryStringMap[country]}
            </Text>
          </div>
          <div>
            <Text span size="14px">
              Closest town:{" "}
            </Text>
            {nearest_town ? (
              <>
                <Text span weight={600} size="14px">
                  {nearest_town}{" "}
                </Text>
                {nearest_town_distance && (
                  <Text span size="14px">
                    ({nearest_town_distance} miles {nearest_town_bearing})
                  </Text>
                )}
              </>
            ) : (
              <Text span c="dimmed" fs="italic" size="14px">
                Unknown
              </Text>
            )}
          </div>
        </div>
        <div>
          <div style={{ margin: "10px 0px" }}>
            <CampsiteTypeBadge campsiteType={campsite_type} />
          </div>
          <Amenities campsite={props.campsite} />
        </div>
      </Stack>
    </Card>
  );
};

export default CampsiteCard;
