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

import {
  MemoryRouter,
  Route,
  Routes,
} from "react-router";

import Layout
  from "./Layout";


vi.mock(
  "./SessionControls",
  () => {
    return {
      default:
        () => (
          <div>
            Session controls
          </div>
        ),
    };
  },
);


function renderLayout() {
  return render(
    <MemoryRouter
      initialEntries={[
        "/",
      ]}
    >
      <Routes>
        <Route
          element={
            <Layout />
          }
        >
          <Route
            index
            element={
              <div>
                Dashboard content
              </div>
            }
          />

          <Route
            path="organizations"
            element={
              <div>
                Organizations content
              </div>
            }
          />
        </Route>
      </Routes>
    </MemoryRouter>,
  );
}


describe(
  "Layout navigation",
  () => {
    test(
      (
        "keeps navigation hidden "
        + "until the menu is opened"
      ),
      () => {
        renderLayout();


        expect(
          screen.queryByRole(
            "navigation",
            {
              name:
                "RiftTrace sections",
            },
          ),
        ).not.toBeInTheDocument();


        expect(
          screen.getByText(
            "Dashboard content"
          ),
        ).toBeInTheDocument();
      },
    );


    test(
      (
        "opens the navigation drawer "
        + "from the menu button"
      ),
      async () => {
        const user =
          userEvent.setup();


        renderLayout();


        await user.click(
          screen.getByRole(
            "button",
            {
              name:
                "Open navigation menu",
            },
          ),
        );


        expect(
          screen.getByRole(
            "navigation",
            {
              name:
                "RiftTrace sections",
            },
          ),
        ).toBeInTheDocument();


        expect(
          screen.getByRole(
            "link",
            {
              name:
                "Organizations",
            },
          ),
        ).toBeInTheDocument();
      },
    );


    test(
      (
        "closes the drawer after "
        + "navigation"
      ),
      async () => {
        const user =
          userEvent.setup();


        renderLayout();


        await user.click(
          screen.getByRole(
            "button",
            {
              name:
                "Open navigation menu",
            },
          ),
        );


        await user.click(
          screen.getByRole(
            "link",
            {
              name:
                "Organizations",
            },
          ),
        );


        expect(
          screen.getByText(
            "Organizations content"
          ),
        ).toBeInTheDocument();


        expect(
          screen.queryByRole(
            "navigation",
            {
              name:
                "RiftTrace sections",
            },
          ),
        ).not.toBeInTheDocument();
      },
    );


    test(
      "closes the drawer with Escape",
      async () => {
        const user =
          userEvent.setup();


        renderLayout();


        await user.click(
          screen.getByRole(
            "button",
            {
              name:
                "Open navigation menu",
            },
          ),
        );


        await user.keyboard(
          "{Escape}"
        );


        expect(
          screen.queryByRole(
            "navigation",
            {
              name:
                "RiftTrace sections",
            },
          ),
        ).not.toBeInTheDocument();
      },
    );
  },
);
