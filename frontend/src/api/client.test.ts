import {
  afterEach,
  beforeEach,
  describe,
  expect,
  test,
  vi,
} from "vitest";


const {
  ensureCsrfMock,
  getCsrfTokenMock,
} = vi.hoisted(
  () => {
    return {
      ensureCsrfMock:
        vi.fn(),

      getCsrfTokenMock:
        vi.fn(),
    };
  },
);


vi.mock(
  "./csrf",
  () => {
    return {
      ensureCsrf:
        ensureCsrfMock,

      getCsrfToken:
        getCsrfTokenMock,
    };
  },
);


import {
  ApiError,
  apiRequest,
} from "./client";


function makeResponse(
  status: number,
  body: string,
): Response {
  return new Response(
    body,
    {
      status,

      headers: {
        "Content-Type":
          "application/json",
      },
    },
  );
}


describe(
  "apiRequest",
  () => {
    beforeEach(
      () => {
        ensureCsrfMock
          .mockReset();

        getCsrfTokenMock
          .mockReset();
      },
    );


    afterEach(
      () => {
        vi.unstubAllGlobals();
      },
    );


    test(
      (
        "uses the same-origin API "
        + "with credentials"
      ),
      async () => {
        const fetchMock =
          vi.fn()
            .mockResolvedValue(
              makeResponse(
                200,
                '{"ok":true}',
              ),
            );


        vi.stubGlobal(
          "fetch",
          fetchMock,
        );


        const result =
          await apiRequest<{
            ok: boolean;
          }>(
            "/example/",
          );


        expect(
          result,
        ).toEqual({
          ok: true,
        });


        expect(
          fetchMock,
        ).toHaveBeenCalledTimes(
          1
        );


        expect(
          fetchMock.mock.calls[
            0
          ][0],
        ).toBe(
          "/api/example/"
        );


        expect(
          fetchMock.mock.calls[
            0
          ][1],
        ).toEqual(
          expect.objectContaining({
            method:
              "GET",

            credentials:
              "include",
          }),
        );


        expect(
          ensureCsrfMock,
        ).not.toHaveBeenCalled();
      },
    );


    test(
      (
        "adds CSRF protection to "
        + "unsafe requests"
      ),
      async () => {
        ensureCsrfMock
          .mockResolvedValue(
            undefined
          );


        getCsrfTokenMock
          .mockReturnValue(
            "csrf-test-token"
          );


        const fetchMock =
          vi.fn()
            .mockResolvedValue(
              makeResponse(
                200,
                '{"saved":true}',
              ),
            );


        vi.stubGlobal(
          "fetch",
          fetchMock,
        );


        await apiRequest(
          "/example/",
          {
            method:
              "POST",

            body:
              JSON.stringify({
                name:
                  "example",
              }),
          },
        );


        expect(
          ensureCsrfMock,
        ).toHaveBeenCalledTimes(
          1
        );


        const options =
          fetchMock.mock.calls[
            0
          ][1] as RequestInit;


        const headers =
          new Headers(
            options.headers
          );


        expect(
          headers.get(
            "X-CSRFToken"
          ),
        ).toBe(
          "csrf-test-token"
        );


        expect(
          headers.get(
            "Content-Type"
          ),
        ).toBe(
          "application/json"
        );


        expect(
          options.credentials,
        ).toBe(
          "include"
        );
      },
    );


    test(
      (
        "throws ApiError using the "
        + "backend detail message"
      ),
      async () => {
        const fetchMock =
          vi.fn()
            .mockResolvedValue(
              makeResponse(
                400,
                (
                  '{"detail":'
                  + '"Invalid request."}'
                ),
              ),
            );


        vi.stubGlobal(
          "fetch",
          fetchMock,
        );


        try {
          await apiRequest(
            "/example/",
          );


          throw new Error(
            "Expected request to fail."
          );
        } catch (
          error
        ) {
          expect(
            error,
          ).toBeInstanceOf(
            ApiError
          );


          if (
            !(error instanceof ApiError)
          ) {
            throw error;
          }


          expect(
            error.status,
          ).toBe(
            400
          );


          expect(
            error.message,
          ).toBe(
            "Invalid request."
          );


          expect(
            error.details,
          ).toEqual({
            detail:
              "Invalid request.",
          });
        }
      },
    );


    test(
      "handles a 204 response",
      async () => {
        const fetchMock =
          vi.fn()
            .mockResolvedValue(
              new Response(
                null,
                {
                  status: 204,
                },
              ),
            );


        vi.stubGlobal(
          "fetch",
          fetchMock,
        );


        const result =
          await apiRequest<void>(
            "/example/",
            {
              method:
                "DELETE",
            },
          );


        expect(
          result,
        ).toBeUndefined();


        expect(
          ensureCsrfMock,
        ).toHaveBeenCalledTimes(
          1
        );
      },
    );
  },
);
