import {
  afterEach,
  describe,
  expect,
  test,
  vi,
} from "vitest";

import {
  ensureCsrf,
  getCsrfToken,
} from "./csrf";


describe(
  "CSRF helpers",
  () => {
    afterEach(
      () => {
        document.cookie =
          (
            "csrftoken=; "
            + "expires=Thu, "
            + "01 Jan 1970 00:00:00 GMT; "
            + "path=/"
          );


        vi.unstubAllGlobals();
      },
    );


    test(
      "reads the Django CSRF cookie",
      () => {
        document.cookie =
          (
            "csrftoken="
            + "rifttrace-test-token; "
            + "path=/"
          );


        expect(
          getCsrfToken(),
        ).toBe(
          "rifttrace-test-token"
        );
      },
    );


    test(
      (
        "requests the CSRF endpoint "
        + "with credentials"
      ),
      async () => {
        const fetchMock =
          vi.fn()
            .mockResolvedValue({
              ok: true,
            });


        vi.stubGlobal(
          "fetch",
          fetchMock,
        );


        await ensureCsrf();


        expect(
          fetchMock,
        ).toHaveBeenCalledWith(
          "/api/auth/csrf/",
          {
            method:
              "GET",

            credentials:
              "include",
          },
        );
      },
    );


    test(
      (
        "throws when CSRF initialization "
        + "fails"
      ),
      async () => {
        const fetchMock =
          vi.fn()
            .mockResolvedValue({
              ok: false,
            });


        vi.stubGlobal(
          "fetch",
          fetchMock,
        );


        await expect(
          ensureCsrf(),
        ).rejects.toThrow(
          "Unable to initialize CSRF."
        );
      },
    );
  },
);
