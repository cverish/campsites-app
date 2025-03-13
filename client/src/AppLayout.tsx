import React from "react";
import { Outlet, useNavigate } from "react-router-dom";
import {
  AppShell,
  Container,
  Header,
  Title,
  Image,
  useMantineTheme,
  Group,
  UnstyledButton,
  Text,
  ActionIcon,
  Divider,
  Tooltip,
} from "@mantine/core";
import { Icon } from "@iconify/react";
import logo from "img/logo.png";

const Layout = (): JSX.Element => {
  const theme = useMantineTheme();
  const navigate = useNavigate();

  return (
    <AppShell
      styles={{
        main: {
          background: theme.colors.gray[0],
        },
      }}
      header={
        <Header height={60} p="xs">
          <Container>
            <UnstyledButton onClick={() => navigate("/")}>
              <Group>
                <Image src={logo} fit="contain" width={36} height={36} />
                <Title order={2}>Campsite Explorer</Title>
              </Group>
            </UnstyledButton>
          </Container>
        </Header>
      }
      footer={
        <Container
          p="xs"
          sx={(theme) => ({
            height: 45,
            borderTop: `1px solid ${theme.colors.gray[2]}`,
            display: "flex",
            justifyContent: "center",
            alignItems: "center",
          })}
        >
          <Group spacing={6}>
            <Text c="dimmed" size={14} pr={8}>
              © Clarissa Verish
            </Text>
            <Divider orientation="vertical" />
            <Group spacing={0}>
              <Tooltip label="Github">
                <ActionIcon
                  component="a"
                  href={"https://github.com/cverish/campsites-app"}
                  target="_blank"
                >
                  <Icon icon="ri:github-line" />
                </ActionIcon>
              </Tooltip>
              <Tooltip label="LinkedIn">
                <ActionIcon
                  component="a"
                  href={"http://linkedin.com/in/clarissa-verish"}
                  target="_blank"
                >
                  <Icon icon="ri:linkedin-fill" />
                </ActionIcon>
              </Tooltip>
              <Tooltip label="Personal website">
                <ActionIcon
                  component="a"
                  href={"https://www.clarissaverish.com/"}
                  target="_blank"
                >
                  <Icon icon="material-symbols:person-outline" />
                </ActionIcon>
              </Tooltip>
            </Group>
          </Group>
        </Container>
      }
    >
      <Outlet />
    </AppShell>
  );
};

export default Layout;
