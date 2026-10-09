import {
  useEffect,
  useState,
} from "react";

import {
  listOrganizations,
} from "../api/organizations";

import {
  getOrganizationTopology,
} from "../api/topology";

import {
  listVulnerabilities,
} from "../api/vulnerabilities";

import {
  createSecurityControl,
  deleteSecurityControl,
  listSecurityControls,
} from "../api/securityControls";

import type {
  Organization,
  OrganizationTopology,
} from "../types/models";

import type {
  Vulnerability,
} from "../types/security";

import type {
  SecurityControl,
  SecurityControlType,
} from "../types/securityControl";


export default function SecurityControlsPage() {
  const [
    organizations,
    setOrganizations,
  ] = useState<Organization[]>([]);


  const [
    selectedOrganization,
    setSelectedOrganization,
  ] = useState("");


  const [
    topology,
    setTopology,
  ] = useState<
    OrganizationTopology
    | null
  >(null);


  const [
    vulnerabilities,
    setVulnerabilities,
  ] = useState<
    Vulnerability[]
  >([]);


  const [
    controls,
    setControls,
  ] = useState<
    SecurityControl[]
  >([]);


  const [
    name,
    setName,
  ] = useState("");


  const [
    controlType,
    setControlType,
  ] = useState<
    SecurityControlType
  >("NETWORK_SEGMENTATION");


  const [
    targetRelationship,
    setTargetRelationship,
  ] = useState("");


  const [
    targetVulnerability,
    setTargetVulnerability,
  ] = useState("");


  const [
    description,
    setDescription,
  ] = useState("");


  const [
    error,
    setError,
  ] = useState("");


  function usesRelationship(
    type:
      SecurityControlType,
  ) {
    return (
      type
      !== "VULNERABILITY_REMEDIATION"
    );
  }


  async function loadData(
    organizationId: number,
  ) {
    const [
      topologyData,
      vulnerabilityData,
      controlData,
    ] = await Promise.all([
      getOrganizationTopology(
        organizationId,
      ),

      listVulnerabilities(
        organizationId,
      ),

      listSecurityControls(
        organizationId,
      ),
    ]);


    setTopology(
      topologyData
    );

    setVulnerabilities(
      vulnerabilityData
    );

    setControls(
      controlData
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


        const [
          topologyData,
          vulnerabilityData,
          controlData,
        ] = await Promise.all([
          getOrganizationTopology(
            initial.id,
          ),

          listVulnerabilities(
            initial.id,
          ),

          listSecurityControls(
            initial.id,
          ),
        ]);


        if (cancelled) {
          return;
        }


        setTopology(
          topologyData
        );

        setVulnerabilities(
          vulnerabilityData
        );

        setControls(
          controlData
        );
      } catch {
        if (!cancelled) {
          setError(
            "Unable to load "
            + "security controls.",
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
    setSelectedOrganization(value);

    setTargetRelationship("");

    setTargetVulnerability("");

    setError("");


    if (!value) {
      setTopology(null);

      setVulnerabilities([]);

      setControls([]);

      return;
    }


    try {
      await loadData(
        Number(value)
      );
    } catch {
      setError(
        "Unable to load selected "
        + "organization controls.",
      );
    }
  }


  async function handleSubmit(
    event:
      React.FormEvent<HTMLFormElement>,
  ) {
    event.preventDefault();


    if (!selectedOrganization) {
      setError(
        "Select an organization.",
      );

      return;
    }


    if (!name.trim()) {
      setError(
        "Enter a control name.",
      );

      return;
    }


    if (
      usesRelationship(
        controlType
      )
      && !targetRelationship
    ) {
      setError(
        "Select a target "
        + "relationship.",
      );

      return;
    }


    if (
      controlType
      === "VULNERABILITY_REMEDIATION"

      && !targetVulnerability
    ) {
      setError(
        "Select a target "
        + "vulnerability.",
      );

      return;
    }


    try {
      setError("");


      await createSecurityControl({
        organization:
          Number(
            selectedOrganization
          ),

        name:
          name.trim(),

        control_type:
          controlType,

        target_relationship:
          usesRelationship(
            controlType
          )
            ? Number(
                targetRelationship
              )
            : null,

        target_vulnerability:
          controlType
          === "VULNERABILITY_REMEDIATION"
            ? Number(
                targetVulnerability
              )
            : null,

        description:
          description.trim(),
      });


      setName("");

      setTargetRelationship("");

      setTargetVulnerability("");

      setDescription("");


      await loadData(
        Number(
          selectedOrganization
        )
      );
    } catch {
      setError(
        "Unable to create "
        + "security control.",
      );
    }
  }


  async function handleDelete(
    control:
      SecurityControl,
  ) {
    const confirmed =
      window.confirm(
        `Delete ${control.name}?`,
      );


    if (!confirmed) {
      return;
    }


    try {
      await deleteSecurityControl(
        control.id
      );


      await loadData(
        Number(
          selectedOrganization
        )
      );
    } catch {
      setError(
        "Unable to delete "
        + "security control.",
      );
    }
  }


  return (
    <>
      <div className="page-heading">
        <div>
          <h2>
            Security Controls
          </h2>

          <p>
            Model candidate defensive
            changes for counterfactual
            simulation.
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


      <section className="panel">
        <h3>
          Add Security Control
        </h3>


        <form
          className="form-grid"

          onSubmit={
            handleSubmit
          }
        >
          <label>
            Control Name

            <input
              value={name}

              onChange={(event) =>
                setName(
                  event.target.value
                )
              }
            />
          </label>


          <label>
            Control Type

            <select
              value={controlType}

              onChange={(event) => {
                const value =
                  event.target.value as SecurityControlType;


                setControlType(
                  value
                );


                setTargetRelationship("");

                setTargetVulnerability("");
              }}
            >
              <option
                value="NETWORK_SEGMENTATION"
              >
                Network Segmentation
              </option>

              <option
                value="VULNERABILITY_REMEDIATION"
              >
                Vulnerability Remediation
              </option>

              <option value="MFA">
                Multi-Factor Authentication
              </option>

              <option
                value="LEAST_PRIVILEGE"
              >
                Least Privilege
              </option>

              <option
                value="AUTHENTICATION_ENFORCEMENT"
              >
                Authentication Enforcement
              </option>
            </select>
          </label>


          {usesRelationship(
            controlType
          ) ? (
            <label>
              Target Relationship

              <select
                value={
                  targetRelationship
                }

                onChange={(event) =>
                  setTargetRelationship(
                    event.target.value
                  )
                }
              >
                <option value="">
                  Select relationship
                </option>

                {
                  topology?.edges.map(
                    (relationship) => (
                      <option
                        key={
                          relationship.id
                        }

                        value={
                          relationship.id
                        }
                      >
                        {
                          relationship
                            .source_name
                        }
                        {" → "}
                        {
                          relationship
                            .target_name
                        }
                        {" — "}
                        {
                          relationship
                            .relationship_type_display
                        }
                      </option>
                    ),
                  )
                }
              </select>
            </label>
          ) : (
            <label>
              Target Vulnerability

              <select
                value={
                  targetVulnerability
                }

                onChange={(event) =>
                  setTargetVulnerability(
                    event.target.value
                  )
                }
              >
                <option value="">
                  Select vulnerability
                </option>

                {
                  vulnerabilities.map(
                    (vulnerability) => (
                      <option
                        key={
                          vulnerability.id
                        }

                        value={
                          vulnerability.id
                        }
                      >
                        {
                          vulnerability
                            .reference_id
                          || vulnerability
                            .title
                        }

                        {" — "}

                        {
                          vulnerability
                            .asset_name
                        }
                      </option>
                    ),
                  )
                }
              </select>
            </label>
          )}


          <label className="full-width">
            Description

            <textarea
              value={description}

              onChange={(event) =>
                setDescription(
                  event.target.value
                )
              }
            />
          </label>


          <button type="submit">
            Add Security Control
          </button>
        </form>
      </section>


      <section className="panel">
        <h3>
          Candidate Controls
        </h3>


        {controls.length === 0 ? (
          <p>
            No security controls modeled.
          </p>
        ) : (
          <div className="security-control-grid">
            {controls.map(
              (control) => (
                <article
                  className="security-control-card"

                  key={
                    control.id
                  }
                >
                  <div>
                    <strong>
                      {control.name}
                    </strong>

                    <span>
                      {
                        control
                          .control_type_display
                      }
                    </span>
                  </div>


                  <p>
                    Target:
                    {" "}
                    {
                      control
                        .target_relationship_display

                      ?? control
                        .target_vulnerability_display

                      ?? "None"
                    }
                  </p>


                  <p>
                    {
                      control.description
                      || "No description"
                    }
                  </p>


                  <button
                    type="button"

                    onClick={() =>
                      void handleDelete(
                        control
                      )
                    }
                  >
                    Delete
                  </button>
                </article>
              ),
            )}
          </div>
        )}
      </section>
    </>
  );
}
