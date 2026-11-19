import {
  beforeEach,
  describe,
  expect,
  test,
  vi,
} from "vitest";

import {
  render,
  screen,
} from "@testing-library/react";

import {
  MemoryRouter,
  Route,
  Routes,
} from "react-router";

import {
  ProtectedRoute,
} from "./ProtectedRoute";


const {
  mockUseAuth,
} = vi.hoisted(
  () => {
    return {
      mockUseAuth:
        vi.fn(),
    };
  },
);


vi.mock(
  "./authContext",
  () => {
    return {
      useAuth:
        () => mockUseAuth(),
    };
  },
);


describe(
  "ProtectedRoute",
  () => {
    beforeEach(
      () => {
        mockUseAuth.mockReset();
      },
    );


    test(
      (
        "redirects an unauthenticated "
        + "user to login"
      ),
      () => {
        mockUseAuth.mockReturnValue({
          user: null,
          loading: false,
        });


        render(
          <MemoryRouter
            initialEntries={[
              "/assets",
            ]}
          >
            <Routes>
              <Route
                path="/login"
                element={
                  <div>
                    Login page
                  </div>
                }
              />

              <Route
                path="/assets"
                element={
                  <ProtectedRoute>
                    <div>
                      Assets page
                    </div>
                  </ProtectedRoute>
                }
              />
            </Routes>
          </MemoryRouter>,
        );


        expect(
          screen.getByText(
            "Login page"
          ),
        ).toBeInTheDocument();
      },
    );


    test(
      (
        "renders a loading state while "
        + "authentication is checked"
      ),
      () => {
        mockUseAuth.mockReturnValue({
          user: null,
          loading: true,
        });


        render(
          <MemoryRouter>
            <ProtectedRoute>
              <div>
                Protected content
              </div>
            </ProtectedRoute>
          </MemoryRouter>,
        );


        expect(
          screen.getByText(
            "Loading RiftTrace"
          ),
        ).toBeInTheDocument();


        expect(
          screen.queryByText(
            "Protected content"
          ),
        ).not.toBeInTheDocument();
      },
    );


    test(
      (
        "renders protected content for "
        + "an authenticated user"
      ),
      () => {
        mockUseAuth.mockReturnValue({
          user: {
            username:
              "admin",
          },

          loading:
            false,
        });


        render(
          <MemoryRouter>
            <ProtectedRoute>
              <div>
                Protected content
              </div>
            </ProtectedRoute>
          </MemoryRouter>,
        );


        expect(
          screen.getByText(
            "Protected content"
          ),
        ).toBeInTheDocument();
      },
    );
  },
);
