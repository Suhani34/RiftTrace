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
  createVulnerability,
  deleteVulnerability,
  listVulnerabilities,
} from "../api/vulnerabilities";

import type {
  Asset,
  Organization,
} from "../types/models";

import type {
  AttackVector,
  GrantedPrivilege,
  PrivilegeLevel,
  Vulnerability,
} from "../types/security";


export default function VulnerabilitiesPage() {
  const [
    organizations,
    setOrganizations,
  ] = useState<Organization[]>([]);

  const [
    selectedOrganization,
    setSelectedOrganization,
  ] = useState("");

  const [
    assets,
    setAssets,
  ] = useState<Asset[]>([]);

  const [
    vulnerabilities,
    setVulnerabilities,
  ] = useState<Vulnerability[]>([]);

  const [
    selectedAsset,
    setSelectedAsset,
  ] = useState("");

  const [
    referenceId,
    setReferenceId,
  ] = useState("");

  const [
    title,
    setTitle,
  ] = useState("");

  const [
    cvssScore,
    setCvssScore,
  ] = useState("");

  const [
    attackVector,
    setAttackVector,
  ] = useState<AttackVector>(
    "NETWORK",
  );

  const [
    privilegesRequired,
    setPrivilegesRequired,
  ] = useState<PrivilegeLevel>(
    "NONE",
  );

  const [
    grantsPrivilege,
    setGrantsPrivilege,
  ] = useState<GrantedPrivilege>(
    "LOW",
  );

  const [
    bypassesAuthentication,
    setBypassesAuthentication,
  ] = useState(false);

  const [
    isExploitable,
    setIsExploitable,
  ] = useState(true);

  const [
    description,
    setDescription,
  ] = useState("");

  const [
    error,
    setError,
  ] = useState("");


  async function loadOrganizationData(
    organizationId: number,
  ) {
    const [
      topology,
      vulnerabilityData,
    ] = await Promise.all([
      getOrganizationTopology(
        organizationId,
      ),

      listVulnerabilities(
        organizationId,
      ),
    ]);

    setAssets(
      topology.nodes,
    );

    setVulnerabilities(
      vulnerabilityData,
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
          organizationData,
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
            initial.id,
          ),
        );

        const [
          topology,
          vulnerabilityData,
        ] = await Promise.all([
          getOrganizationTopology(
            initial.id,
          ),

          listVulnerabilities(
            initial.id,
          ),
        ]);

        if (cancelled) {
          return;
        }

        setAssets(
          topology.nodes,
        );

        setVulnerabilities(
          vulnerabilityData,
        );
      } catch {
        if (!cancelled) {
          setError(
            "Unable to load "
            + "vulnerabilities.",
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

    setSelectedAsset("");

    setError("");

    if (!value) {
      setAssets([]);
      setVulnerabilities([]);

      return;
    }

    try {
      await loadOrganizationData(
        Number(value),
      );
    } catch {
      setError(
        "Unable to load selected "
        + "organization security data.",
      );
    }
  }


  async function handleSubmit(
    event:
      React.FormEvent<HTMLFormElement>,
  ) {
    event.preventDefault();

    if (!selectedAsset) {
      setError(
        "Select an asset.",
      );

      return;
    }

    if (!title.trim()) {
      setError(
        "Enter a vulnerability title.",
      );

      return;
    }

    try {
      setError("");

      await createVulnerability({
        asset:
          Number(
            selectedAsset
          ),

        reference_id:
          referenceId.trim(),

        title:
          title.trim(),

        cvss_score:
          cvssScore.trim()
            ? cvssScore.trim()
            : null,

        attack_vector:
          attackVector,

        privileges_required:
          privilegesRequired,

        grants_privilege:
          grantsPrivilege,

        bypasses_authentication:
          bypassesAuthentication,

        is_exploitable:
          isExploitable,

        description:
          description.trim(),
      });

      setReferenceId("");
      setTitle("");
      setCvssScore("");
      setDescription("");

      await loadOrganizationData(
        Number(
          selectedOrganization
        ),
      );
    } catch {
      setError(
        "Unable to create "
        + "vulnerability.",
      );
    }
  }


  async function handleDelete(
    vulnerability: Vulnerability,
  ) {
    const confirmed =
      window.confirm(
        `Delete ${vulnerability.title}?`,
      );

    if (!confirmed) {
      return;
    }

    try {
      await deleteVulnerability(
        vulnerability.id,
      );

      await loadOrganizationData(
        Number(
          selectedOrganization
        ),
      );
    } catch {
      setError(
        "Unable to delete "
        + "vulnerability.",
      );
    }
  }


  return (
    <>
      <div className="page-heading">
        <div>
          <h2>
            Vulnerabilities
          </h2>

          <p>
            Model security weaknesses used
            by RiftTrace propagation
            scenarios.
          </p>
        </div>
      </div>


      {error && (
        <div className="error-box">
          {error}
        </div>
      )}


      <section className="panel">
        <h3>
          Security Model
        </h3>

        <label>
          Organization

          <select
            value={
              selectedOrganization
            }
            onChange={(event) =>
              void handleOrganizationChange(
                event.target.value,
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
          Add Vulnerability
        </h3>

        <form
          className="form-grid"
          onSubmit={handleSubmit}
        >
          <label>
            Asset

            <select
              value={selectedAsset}
              onChange={(event) =>
                setSelectedAsset(
                  event.target.value,
                )
              }
            >
              <option value="">
                Select asset
              </option>

              {assets.map(
                (asset) => (
                  <option
                    key={asset.id}
                    value={asset.id}
                  >
                    {asset.name}
                  </option>
                ),
              )}
            </select>
          </label>


          <label>
            Reference ID

            <input
              value={referenceId}
              placeholder="CVE or internal ID"
              onChange={(event) =>
                setReferenceId(
                  event.target.value,
                )
              }
            />
          </label>


          <label>
            Title

            <input
              value={title}
              onChange={(event) =>
                setTitle(
                  event.target.value,
                )
              }
            />
          </label>


          <label>
            CVSS Score

            <input
              type="number"
              min="0"
              max="10"
              step="0.1"
              value={cvssScore}
              onChange={(event) =>
                setCvssScore(
                  event.target.value,
                )
              }
            />
          </label>


          <label>
            Attack Vector

            <select
              value={attackVector}
              onChange={(event) =>
                setAttackVector(
                  event.target.value as AttackVector,
                )
              }
            >
              <option value="NETWORK">
                Network
              </option>

              <option value="ADJACENT">
                Adjacent
              </option>

              <option value="LOCAL">
                Local
              </option>

              <option value="PHYSICAL">
                Physical
              </option>
            </select>
          </label>


          <label>
            Privileges Required

            <select
              value={
                privilegesRequired
              }
              onChange={(event) =>
                setPrivilegesRequired(
                  event.target.value as PrivilegeLevel,
                )
              }
            >
              <option value="NONE">
                None
              </option>

              <option value="LOW">
                Low
              </option>

              <option value="HIGH">
                High
              </option>
            </select>
          </label>


          <label>
            Privilege Gained

            <select
              value={grantsPrivilege}
              onChange={(event) =>
                setGrantsPrivilege(
                  event.target.value as GrantedPrivilege,
                )
              }
            >
              <option value="LOW">
                Low
              </option>

              <option value="HIGH">
                High
              </option>
            </select>
          </label>


          <label className="checkbox-label">
            <input
              type="checkbox"
              checked={
                bypassesAuthentication
              }
              onChange={(event) =>
                setBypassesAuthentication(
                  event.target.checked,
                )
              }
            />

            Bypasses Authentication
          </label>


          <label className="checkbox-label">
            <input
              type="checkbox"
              checked={isExploitable}
              onChange={(event) =>
                setIsExploitable(
                  event.target.checked,
                )
              }
            />

            Exploitable in Model
          </label>


          <label className="full-width">
            Description

            <textarea
              value={description}
              onChange={(event) =>
                setDescription(
                  event.target.value,
                )
              }
            />
          </label>


          <button type="submit">
            Add Vulnerability
          </button>
        </form>
      </section>


      <section className="panel">
        <h3>
          Vulnerabilities
        </h3>

        {vulnerabilities.length
        === 0 ? (
          <p>
            No vulnerabilities modeled.
          </p>
        ) : (
          <div className="vulnerability-grid">
            {vulnerabilities.map(
              (vulnerability) => (
                <article
                  className="vulnerability-card"
                  key={
                    vulnerability.id
                  }
                >
                  <div>
                    <strong>
                      {
                        vulnerability
                          .title
                      }
                    </strong>

                    <span>
                      {
                        vulnerability
                          .reference_id
                        || "No reference"
                      }
                    </span>
                  </div>

                  <p>
                    Asset:{" "}
                    {
                      vulnerability
                        .asset_name
                    }
                  </p>

                  <p>
                    Attack Vector:{" "}
                    {
                      vulnerability
                        .attack_vector_display
                    }
                  </p>

                  <p>
                    Privileges Required:{" "}
                    {
                      vulnerability
                        .privileges_required_display
                    }
                  </p>

                  <p>
                    Grants:{" "}
                    {
                      vulnerability
                        .grants_privilege_display
                    }
                  </p>

                  <p>
                    CVSS:{" "}
                    {
                      vulnerability
                        .cvss_score
                      ?? "Not specified"
                    }
                  </p>

                  <p>
                    Authentication bypass:{" "}
                    {
                      vulnerability
                        .bypasses_authentication
                      ? "Yes"
                      : "No"
                    }
                  </p>

                  <p>
                    Simulation status:{" "}
                    {
                      vulnerability
                        .is_exploitable
                      ? "Exploitable"
                      : "Disabled"
                    }
                  </p>

                  <button
                    type="button"
                    onClick={() =>
                      void handleDelete(
                        vulnerability,
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
