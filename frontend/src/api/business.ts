import {
  apiRequest,
} from "./client";

import type {
  BusinessProcess,
  BusinessProcessDependency,
  CreateBusinessDependencyInput,
  CreateBusinessProcessInput,
} from "../types/business";


export function listBusinessProcesses(
  organizationId: number,
) {
  return apiRequest<
    BusinessProcess[]
  >(
    "/business-processes/"
    + `?organization=${organizationId}`,
  );
}


export function createBusinessProcess(
  input:
    CreateBusinessProcessInput,
) {
  return apiRequest<
    BusinessProcess
  >(
    "/business-processes/",
    {
      method: "POST",

      body: JSON.stringify(
        input,
      ),
    },
  );
}


export function deleteBusinessProcess(
  id: number,
) {
  return apiRequest<void>(
    `/business-processes/${id}/`,
    {
      method: "DELETE",
    },
  );
}


export function listBusinessDependencies(
  organizationId: number,
) {
  return apiRequest<
    BusinessProcessDependency[]
  >(
    "/business-dependencies/"
    + `?organization=${organizationId}`,
  );
}


export function createBusinessDependency(
  input:
    CreateBusinessDependencyInput,
) {
  return apiRequest<
    BusinessProcessDependency
  >(
    "/business-dependencies/",
    {
      method: "POST",

      body: JSON.stringify(
        input,
      ),
    },
  );
}


export function deleteBusinessDependency(
  id: number,
) {
  return apiRequest<void>(
    `/business-dependencies/${id}/`,
    {
      method: "DELETE",
    },
  );
}
