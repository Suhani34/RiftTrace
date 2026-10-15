import {
  apiRequest,
} from "./client";

import type {
  DashboardSummary,
} from "../types/dashboard";


export function getDashboardSummary(
  organizationId: number,
) {
  return apiRequest<
    DashboardSummary
  >(
    "/dashboard/summary/"
    + `?organization=${organizationId}`,
  );
}
