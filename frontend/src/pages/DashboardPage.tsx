import {
  useEffect,
  useState,
} from "react";

import {
  Link,
} from "react-router-dom";

import {
  Bar,
  BarChart,
  CartesianGrid,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";

import {
  getDashboardSummary,
} from "../api/dashboard";

import {
  listOrganizations,
} from "../api/organizations";

import type {
  DashboardSummary,
} from "../types/dashboard";

import type {
  Organization,
} from "../types/models";


export default function DashboardPage() {
  const [
    organizations,
    setOrganizations,
  ] = useState<Organization[]>([]);


  const [
    selectedOrganization,
    setSelectedOrganization,
  ] = useState("");


  const [
    summary,
    setSummary,
  ] = useState<
    DashboardSummary
    | null
  >(null);


  const [
    error,
    setError,
  ] = useState("");


  async function loadSummary(
    organizationId: number,
  ) {
    const data =
      await getDashboardSummary(
        organizationId
      );


    setSummary(
      data
    );
  }


  useEffect(() => {
    let cancelled = false;


    async function initialize() {
      try {
        const organizationData =
          await listOrganizations();


        if (cancelled) {
          return;
        }


        setOrganizations(
          organizationData
        );


        if (
          organizationData.length
          === 0
        ) {
          return;
        }


        const initial =
          organizationData.find(
            (organization) =>
              organization.name
              === "RiftTrace Labs",
          )
          ?? organizationData[0];


        setSelectedOrganization(
          String(
            initial.id
          )
        );


        const dashboardData =
          await getDashboardSummary(
            initial.id
          );


        if (!cancelled) {
          setSummary(
            dashboardData
          );
        }
      } catch {
        if (!cancelled) {
          setError(
            "Unable to load dashboard.",
          );
        }
      }
    }


    void initialize();


    return () => {
      cancelled = true;
    };
  }, []);


  async function handleOrganizationChange(
    value: string,
  ) {
    setSelectedOrganization(
      value
    );

    setSummary(null);

    setError("");


    if (!value) {
      return;
    }


    try {
      await loadSummary(
        Number(value)
      );
    } catch {
      setError(
        "Unable to load selected "
        + "organization dashboard.",
      );
    }
  }


  return (
    <>
      <div className="page-heading">
        <div>
          <h2>
            RiftTrace Dashboard
          </h2>

          <p>
            Organization-wide view of the
            modeled cyber environment,
            business dependencies and
            candidate defensive controls.
          </p>
        </div>
      </div>


      {error && (
        <div className="error-box">
          {error}
        </div>
      )}


      <section className="panel">
        <label>
          Organization

          <select
            value={
              selectedOrganization
            }

            onChange={(event) =>
              void handleOrganizationChange(
                event.target.value
              )
            }
          >
            {organizations.map(
              (organization) => (
                <option
                  key={
                    organization.id
                  }

                  value={
                    organization.id
                  }
                >
                  {
                    organization.name
                  }
                </option>
              ),
            )}
          </select>
        </label>
      </section>


      {!summary ? (
        <section className="panel">
          <p>
            Select an organization to load
            the dashboard.
          </p>
        </section>
      ) : (
        <>
          <section className="dashboard-stat-grid">
            <article className="dashboard-stat-card">
              <span>
                Assets
              </span>

              <strong>
                {
                  summary
                    .totals
                    .assets
                }
              </strong>
            </article>


            <article className="dashboard-stat-card">
              <span>
                Relationships
              </span>

              <strong>
                {
                  summary
                    .totals
                    .relationships
                }
              </strong>
            </article>


            <article className="dashboard-stat-card">
              <span>
                Vulnerabilities
              </span>

              <strong>
                {
                  summary
                    .totals
                    .vulnerabilities
                }
              </strong>

              <small>
                {
                  summary
                    .totals
                    .exploitable_vulnerabilities
                }
                {" exploitable"}
              </small>
            </article>


            <article className="dashboard-stat-card">
              <span>
                Business Processes
              </span>

              <strong>
                {
                  summary
                    .totals
                    .business_processes
                }
              </strong>
            </article>


            <article className="dashboard-stat-card">
              <span>
                Security Controls
              </span>

              <strong>
                {
                  summary
                    .totals
                    .security_controls
                }
              </strong>
            </article>


            <article className="dashboard-stat-card">
              <span>
                Network Zones
              </span>

              <strong>
                {
                  summary
                    .totals
                    .network_zones
                }
              </strong>
            </article>
          </section>


          <section className="dashboard-chart-grid">
            <article className="panel dashboard-chart-card">
              <h3>
                Asset Criticality
              </h3>

              <ResponsiveContainer
                width="100%"
                height={280}
              >
                <BarChart
                  data={
                    summary
                      .asset_criticality
                  }
                >
                  <CartesianGrid
                    strokeDasharray="3 3"
                  />

                  <XAxis
                    dataKey="name"
                  />

                  <YAxis
                    allowDecimals={
                      false
                    }
                  />

                  <Tooltip />

                  <Bar
                    dataKey="value"
                    fill="#7c3aed"
                  />
                </BarChart>
              </ResponsiveContainer>
            </article>


            <article className="panel dashboard-chart-card">
              <h3>
                Business Process Criticality
              </h3>

              <ResponsiveContainer
                width="100%"
                height={280}
              >
                <BarChart
                  data={
                    summary
                      .business_process_criticality
                  }
                >
                  <CartesianGrid
                    strokeDasharray="3 3"
                  />

                  <XAxis
                    dataKey="name"
                  />

                  <YAxis
                    allowDecimals={
                      false
                    }
                  />

                  <Tooltip />

                  <Bar
                    dataKey="value"
                    fill="#2563eb"
                  />
                </BarChart>
              </ResponsiveContainer>
            </article>
          </section>


          <section className="panel">
            <h3>
              RiftTrace Workflow
            </h3>

            <div className="dashboard-workflow-grid">
              <Link to="/topology">
                <strong>
                  1. Analyze Propagation
                </strong>

                <span>
                  Topology, security-aware
                  propagation and business
                  impact.
                </span>
              </Link>


              <Link to="/counterfactual">
                <strong>
                  2. Test What-If Changes
                </strong>

                <span>
                  Compare the current model
                  against temporary changes.
                </span>
              </Link>


              <Link to="/control-simulation">
                <strong>
                  3. Simulate Controls
                </strong>

                <span>
                  Apply modeled defensive
                  controls.
                </span>
              </Link>


              <Link to="/remediation-ranking">
                <strong>
                  4. Prioritize Fixes
                </strong>

                <span>
                  Rank controls by modeled
                  consequence reduction.
                </span>
              </Link>
            </div>
          </section>
        </>
      )}
    </>
  );
}
