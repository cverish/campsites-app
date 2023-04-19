import React from "react";
import {
  AppShell,
  Container,
  Header,
  Title,
  Image,
  useMantineTheme,
  Group,
  UnstyledButton,
} from "@mantine/core";
import { Outlet, useNavigate } from "react-router-dom";
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
    >
      <Outlet />
    </AppShell>
  );
};

export default Layout;
