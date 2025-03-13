import React from "react";
import { useWindowScroll } from "@mantine/hooks";
import { ActionIcon, Affix, Transition, rem } from "@mantine/core";
import { Icon } from "@iconify/react";

const ScrollToTopButton = (): JSX.Element => {
  const [scroll, scrollTo] = useWindowScroll();

  return (
    <Affix position={{ bottom: rem(20), right: rem(20) }}>
      <Transition transition="slide-up" mounted={scroll.y > 0}>
        {(transitionStyles) => (
          <ActionIcon
            variant="filled"
            color="blue"
            style={transitionStyles}
            onClick={() => scrollTo({ y: 0 })}
          >
            <Icon icon="mdi:arrow-up" height={18} width={18} />
          </ActionIcon>
        )}
      </Transition>
    </Affix>
  );
};

export default ScrollToTopButton;
