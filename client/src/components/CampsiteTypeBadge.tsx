import React from "react";
import { Badge } from "@mantine/core";
import { campsiteTypeColors, campsiteTypeMap } from "constants/campsiteTypes";
import { CampsiteTypeEnum } from "models";

const CampsiteTypeBadge = (props: {
  campsiteType: CampsiteTypeEnum | null;
}): JSX.Element => {
  const color =
    campsiteTypeColors[campsiteTypeMap[props.campsiteType ?? "UNK"].category];
  return (
    <Badge color={color} variant="outline">
      <div>{campsiteTypeMap[props.campsiteType ?? "UNK"].label}</div>
    </Badge>
  );
};

export default CampsiteTypeBadge;
