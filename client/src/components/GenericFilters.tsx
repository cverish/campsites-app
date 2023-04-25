import React, { useEffect, useState } from "react";
import { useDebouncedValue } from "@mantine/hooks";
import {
  Group,
  Text,
  UnstyledButton,
  MultiSelect,
  Select,
  TextInput,
  Grid,
  NumberInput,
  ActionIcon,
  Divider,
  Checkbox,
} from "@mantine/core";
import { AmenityIcon } from "components";
import { Icon } from "@iconify/react";
import { monthMap } from "constants/months";

type OptionValueType = {
  label: string;
  value: string;
  group?: string;
};

export const ThreeStateFilter = <T extends unknown>(props: {
  filterKey: keyof T;
  label: string;
  value: boolean | null;
  icon: string;
  onChange: (filterKey: keyof T) => void;
}): JSX.Element => {
  return (
    <UnstyledButton onClick={() => props.onChange(props.filterKey)}>
      <Group spacing={10}>
        <AmenityIcon icon={props.icon} status={props.value} size="md" />
        <Text fz="sm">{props.label}</Text>
      </Group>
    </UnstyledButton>
  );
};

export const SelectFilter = <T extends unknown>(props: {
  filterKey: keyof T;
  options: OptionValueType[];
  value: string | null;
  placeholderText: string;
  onChange: (filterKey: keyof T, val: string | null) => void;
}): JSX.Element => {
  return (
    <Select
      clearable
      searchable
      data={props.options}
      value={props.value}
      placeholder={props.placeholderText}
      onChange={(val) => props.onChange(props.filterKey, val)}
      nothingFound="Not found"
    />
  );
};

export const MultiselectFilter = <T extends unknown>(props: {
  filterKey: keyof T;
  options: OptionValueType[];
  values: string[];
  placeholderText: string;
  disabled?: boolean;
  onChange: (filterKey: keyof T, values: any[]) => void;
}): JSX.Element => {
  return (
    <MultiSelect
      disabled={!!props.disabled}
      sx={{
        ".mantine-MultiSelect-values": {
          marginRight: 0,
        },
      }}
      data={props.options}
      value={props.values}
      onChange={(vals) => props.onChange(props.filterKey, vals)}
      placeholder={props.placeholderText}
      searchable
      clearable
      nothingFound="No results"
    />
  );
};

export const TextFilter = <T extends unknown>(props: {
  filterKey: keyof T;
  value: string | null;
  placeholderText: string;
  onChange: (filterKey: keyof T, val: string | null) => void;
}): JSX.Element => {
  const [input, setInput] = useState(props.value);
  const [debounced] = useDebouncedValue(input, 250);

  // we need to disable the exhaustive deps eslint rule for debounces.
  // including `props` in the list of dependencies  causes the useEffect
  // to run again when props.value is set outside of this component
  // (namely, when filters are reset via a button).
  // The debounce causes the input to be refilled with the prior value
  // upon filter reset, causing the filter value to not be reset.
  useEffect(() => {
    if (debounced === input && input !== props.value) {
      props.onChange(props.filterKey, debounced);
    }
  }, [debounced, input]); // eslint-disable-line react-hooks/exhaustive-deps

  useEffect(() => {
    setInput(props.value);
  }, [props.value]);

  const handleClear = () => {
    setInput(null);
    props.onChange(props.filterKey, null);
  };

  return (
    <TextInput
      value={input ?? ""}
      onChange={(e) => setInput(e.target.value)}
      placeholder={props.placeholderText}
      rightSection={
        props.value && (
          <ActionIcon mr={10} onClick={handleClear}>
            <Icon icon="iconoir:cancel" />
          </ActionIcon>
        )
      }
    />
  );
};

export const NumberFilter = <T extends unknown>(props: {
  filterKey: keyof T;
  value: number | null;
  placeholderText: string;
  onChange: (filterKey: keyof T, val: number | null) => void;
}): JSX.Element => {
  const [input, setInput] = useState(props.value);
  const [debounced] = useDebouncedValue(input, 250);

  // we need to disable the exhaustive deps eslint rule for debounces.
  // including `props` in the list of dependencies  causes the useEffect
  // to run again when props.value is set outside of this component
  // (namely, when filters are reset via a button).
  // The debounce causes the input to be refilled with the prior value
  // upon filter reset, causing the filter value to not be reset.
  useEffect(() => {
    if (debounced === input && input !== props.value) {
      props.onChange(props.filterKey, debounced);
    }
  }, [debounced, input]); // eslint-disable-line react-hooks/exhaustive-deps

  useEffect(() => {
    setInput(props.value);
  }, [props.value]);

  const handleClear = () => {
    setInput(null);
    props.onChange(props.filterKey, null);
  };

  return (
    <NumberInput
      type="number"
      value={input ?? ""}
      min={0}
      placeholder={props.placeholderText}
      hideControls
      onChange={(newVal) => setInput(newVal !== "" ? newVal : null)}
      rightSection={
        props.value && (
          <ActionIcon mr={10} onClick={handleClear}>
            <Icon icon="iconoir:cancel" />
          </ActionIcon>
        )
      }
    />
  );
};

export const NumberRangeFilter = <T extends unknown>(props: {
  minFilterKey: keyof T;
  maxFilterKey: keyof T;
  minValue: number | null;
  maxValue: number | null;
  minPlaceholderText: string;
  maxPlaceholderText: string;
  onChange: (filterKey: keyof T, val: number | null) => void;
}): JSX.Element => {
  return (
    <Grid align="center" columns={15} gutter="xs">
      <Grid.Col span={7}>
        <NumberFilter<T>
          filterKey={props.minFilterKey}
          value={props.minValue}
          placeholderText={props.minPlaceholderText}
          onChange={props.onChange}
        />
      </Grid.Col>
      <Grid.Col span={1}>
        <Divider />
      </Grid.Col>
      <Grid.Col span={7}>
        <NumberFilter<T>
          filterKey={props.maxFilterKey}
          value={props.maxValue}
          placeholderText={props.maxPlaceholderText}
          onChange={props.onChange}
        />
      </Grid.Col>
    </Grid>
  );
};

export const MonthRangeFilter = <T extends unknown>(props: {
  openFilterKey: keyof T;
  closeFilterKey: keyof T;
  openValue: number | null;
  closeValue: number | null;
  openPlaceholderText: string;
  closePlaceholderText: string;
  onChange: (openVal: number | null, closeVal: number | null) => void;
}): JSX.Element => {
  const [checked, setChecked] = useState(
    props.openValue === 1 && props.closeValue === 12
  );
  const dropdownOptions = monthMap.map((m) => ({
    value: m.number.toString(),
    label: m.label,
  }));

  const onCheckChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const isChecked = e.currentTarget.checked;
    if (isChecked) {
      props.onChange(1, 12);
    } else {
      props.onChange(null, null);
    }
    setChecked(isChecked);
  };

  // reset check state to false if months are anything besides (1, 12)
  useEffect(() => {
    if (checked && (props.openValue !== 1 || props.closeValue !== 12)) {
      setChecked(false);
    } else if (!checked && props.openValue === 1 && props.closeValue === 12) {
      setChecked(true);
    }
  }, [checked, props.openValue, props.closeValue]);

  const onChange = (filterKey: keyof T, stringVal: string | null) => {
    const val = stringVal ? Number(stringVal) : null;
    if (filterKey === "month_open__lt") {
      // toggle closeValue to null if the chosen open month is greater than
      // the currnet closeValue
      const newCloseValue =
        val && props.closeValue && props.closeValue < val
          ? null
          : props.closeValue;
      props.onChange(val, newCloseValue);
    } else if (filterKey === "month_close__gt") {
      // toggle openValue to null if the chosen close month is less than
      // the current openValue
      const newOpenValue =
        val && props.openValue && props.openValue > val
          ? null
          : props.openValue;
      props.onChange(newOpenValue, val);
    }
  };

  return (
    <Grid align="center" columns={15} gutter="xs">
      <Grid.Col span={15}>
        <Checkbox
          checked={checked}
          onChange={onCheckChange}
          label="Open all year"
        />
      </Grid.Col>
      <Grid.Col span={7}>
        <SelectFilter
          filterKey={props.openFilterKey}
          options={dropdownOptions}
          value={props.openValue ? props.openValue.toString() : null}
          placeholderText={props.openPlaceholderText}
          onChange={onChange}
        />
      </Grid.Col>
      <Grid.Col span={1}>
        <Divider />
      </Grid.Col>
      <Grid.Col span={7}>
        <SelectFilter
          filterKey={props.closeFilterKey}
          options={dropdownOptions}
          value={props.closeValue ? props.closeValue.toString() : null}
          placeholderText={props.closePlaceholderText}
          onChange={onChange}
        />
      </Grid.Col>
    </Grid>
  );
};
