import {
  describe,
  expect,
  test,
  vi,
} from "vitest";

import {
  render,
  screen,
} from "@testing-library/react";

import userEvent
  from "@testing-library/user-event";

import PageState
  from "./PageState";


describe(
  "PageState",
  () => {
    test(
      "renders an error state",
      () => {
        render(
          <PageState
            kind="error"
            title="Unable to load"
            message={
              "The requested data could not be loaded."
            }
          />,
        );


        expect(
          screen.getByRole(
            "alert"
          ),
        ).toBeInTheDocument();


        expect(
          screen.getByText(
            "Unable to load"
          ),
        ).toBeInTheDocument();


        expect(
          screen.getByText(
            (
              "The requested data "
              + "could not be loaded."
            ),
          ),
        ).toBeInTheDocument();
      },
    );


    test(
      "calls the supplied action",
      async () => {
        const user =
          userEvent.setup();


        const onAction =
          vi.fn();


        render(
          <PageState
            kind="error"
            title="Unable to load"
            actionLabel="Retry"
            onAction={onAction}
          />,
        );


        await user.click(
          screen.getByRole(
            "button",
            {
              name: "Retry",
            },
          ),
        );


        expect(
          onAction,
        ).toHaveBeenCalledTimes(
          1
        );
      },
    );


    test(
      "renders an empty state",
      () => {
        render(
          <PageState
            kind="empty"
            title="No assets yet"
            message={
              "There are no assets to display."
            }
          />,
        );


        expect(
          screen.getByRole(
            "status"
          ),
        ).toBeInTheDocument();


        expect(
          screen.getByText(
            "No assets yet"
          ),
        ).toBeInTheDocument();
      },
    );
  },
);
