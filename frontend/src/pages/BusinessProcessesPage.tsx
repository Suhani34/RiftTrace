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
  createBusinessDependency,
  createBusinessProcess,
  deleteBusinessDependency,
  deleteBusinessProcess,
  listBusinessDependencies,
  listBusinessProcesses,
} from "../api/business";

import type {
  Asset,
  Organization,
} from "../types/models";

import type {
  BusinessCriticality,
  BusinessProcess,
  BusinessProcessDependency,
  DependencyLevel,
} from "../types/business";


export default function BusinessProcessesPage() {
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
    processes,
    setProcesses,
  ] = useState<
    BusinessProcess[]
  >([]);

  const [
    dependencies,
    setDependencies,
  ] = useState<
    BusinessProcessDependency[]
  >([]);

  const [
    processName,
    setProcessName,
  ] = useState("");

  const [
    processCriticality,
    setProcessCriticality,
  ] = useState<
    BusinessCriticality
  >("MEDIUM");

  const [
    processDescription,
    setProcessDescription,
  ] = useState("");

  const [
    impactDescription,
    setImpactDescription,
  ] = useState("");

  const [
    selectedProcess,
    setSelectedProcess,
  ] = useState("");

  const [
    selectedAsset,
    setSelectedAsset,
  ] = useState("");

  const [
    dependencyLevel,
    setDependencyLevel,
  ] = useState<
    DependencyLevel
  >("IMPORTANT");

  const [
    dependencyDescription,
    setDependencyDescription,
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
      processData,
      dependencyData,
    ] = await Promise.all([
      getOrganizationTopology(
        organizationId,
      ),

      listBusinessProcesses(
        organizationId,
      ),

      listBusinessDependencies(
        organizationId,
      ),
    ]);


    setAssets(
      topology.nodes,
    );

    setProcesses(
      processData,
    );

    setDependencies(
      dependencyData,
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
          processData,
          dependencyData,
        ] = await Promise.all([
          getOrganizationTopology(
            initial.id,
          ),

          listBusinessProcesses(
            initial.id,
          ),

          listBusinessDependencies(
            initial.id,
          ),
        ]);


        if (cancelled) {
          return;
        }


        setAssets(
          topology.nodes,
        );

        setProcesses(
          processData,
        );

        setDependencies(
          dependencyData,
        );
      } catch {
        if (!cancelled) {
          setError(
            "Unable to load business data.",
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

    setSelectedProcess("");
    setSelectedAsset("");

    setError("");


    if (!value) {
      setAssets([]);
      setProcesses([]);
      setDependencies([]);

      return;
    }


    try {
      await loadOrganizationData(
        Number(value),
      );
    } catch {
      setError(
        "Unable to load the selected "
        + "organization business data.",
      );
    }
  }


  async function handleCreateProcess(
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


    if (!processName.trim()) {
      setError(
        "Enter a business process name.",
      );

      return;
    }


    try {
      setError("");


      await createBusinessProcess({
        organization:
          Number(
            selectedOrganization
          ),

        name:
          processName.trim(),

        criticality:
          processCriticality,

        description:
          processDescription.trim(),

        impact_description:
          impactDescription.trim(),
      });


      setProcessName("");

      setProcessCriticality(
        "MEDIUM",
      );

      setProcessDescription("");

      setImpactDescription("");


      await loadOrganizationData(
        Number(
          selectedOrganization
        ),
      );
    } catch {
      setError(
        "Unable to create "
        + "business process.",
      );
    }
  }


  async function handleCreateDependency(
    event:
      React.FormEvent<HTMLFormElement>,
  ) {
    event.preventDefault();


    if (
      !selectedProcess
      || !selectedAsset
    ) {
      setError(
        "Select both a business "
        + "process and an asset.",
      );

      return;
    }


    try {
      setError("");


      await createBusinessDependency({
        business_process:
          Number(
            selectedProcess
          ),

        asset:
          Number(
            selectedAsset
          ),

        dependency_level:
          dependencyLevel,

        description:
          dependencyDescription.trim(),
      });


      setSelectedAsset("");

      setDependencyLevel(
        "IMPORTANT",
      );

      setDependencyDescription("");


      await loadOrganizationData(
        Number(
          selectedOrganization
        ),
      );
    } catch {
      setError(
        "Unable to create "
        + "business dependency.",
      );
    }
  }


  async function handleDeleteProcess(
    process: BusinessProcess,
  ) {
    const confirmed =
      window.confirm(
        `Delete ${process.name}?`,
      );


    if (!confirmed) {
      return;
    }


    try {
      await deleteBusinessProcess(
        process.id,
      );


      await loadOrganizationData(
        Number(
          selectedOrganization
        ),
      );
    } catch {
      setError(
        "Unable to delete "
        + "business process.",
      );
    }
  }


  async function handleDeleteDependency(
    dependency:
      BusinessProcessDependency,
  ) {
    const confirmed =
      window.confirm(
        "Delete dependency "
        + `${dependency.business_process_name}`
        + " → "
        + `${dependency.asset_name}?`,
      );


    if (!confirmed) {
      return;
    }


    try {
      await deleteBusinessDependency(
        dependency.id,
      );


      await loadOrganizationData(
        Number(
          selectedOrganization
        ),
      );
    } catch {
      setError(
        "Unable to delete dependency.",
      );
    }
  }


  return (
    <>
      <div className="page-heading">
        <div>
          <h2>
            Business Processes
          </h2>

          <p>
            Model organizational processes
            and the technical assets they
            depend on.
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
          Add Business Process
        </h3>

        <form
          className="form-grid"
          onSubmit={
            handleCreateProcess
          }
        >
          <label>
            Process Name

            <input
              value={processName}
              onChange={(event) =>
                setProcessName(
                  event.target.value,
                )
              }
            />
          </label>


          <label>
            Criticality

            <select
              value={
                processCriticality
              }
              onChange={(event) =>
                setProcessCriticality(
                  event.target.value as BusinessCriticality,
                )
              }
            >
              <option value="LOW">
                Low
              </option>

              <option value="MEDIUM">
                Medium
              </option>

              <option value="HIGH">
                High
              </option>

              <option value="CRITICAL">
                Critical
              </option>
            </select>
          </label>


          <label className="full-width">
            Description

            <textarea
              value={
                processDescription
              }
              onChange={(event) =>
                setProcessDescription(
                  event.target.value,
                )
              }
            />
          </label>


          <label className="full-width">
            Potential Impact Description

            <textarea
              value={
                impactDescription
              }
              onChange={(event) =>
                setImpactDescription(
                  event.target.value,
                )
              }
            />
          </label>


          <button type="submit">
            Add Business Process
          </button>
        </form>
      </section>


      <section className="panel">
        <h3>
          Add Asset Dependency
        </h3>

        <form
          className="form-grid"
          onSubmit={
            handleCreateDependency
          }
        >
          <label>
            Business Process

            <select
              value={selectedProcess}
              onChange={(event) =>
                setSelectedProcess(
                  event.target.value,
                )
              }
            >
              <option value="">
                Select process
              </option>

              {processes.map(
                (process) => (
                  <option
                    key={process.id}
                    value={process.id}
                  >
                    {process.name}
                  </option>
                ),
              )}
            </select>
          </label>


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
            Dependency Level

            <select
              value={dependencyLevel}
              onChange={(event) =>
                setDependencyLevel(
                  event.target.value as DependencyLevel,
                )
              }
            >
              <option value="SUPPORTING">
                Supporting
              </option>

              <option value="IMPORTANT">
                Important
              </option>

              <option value="ESSENTIAL">
                Essential
              </option>
            </select>
          </label>


          <label className="full-width">
            Dependency Description

            <textarea
              value={
                dependencyDescription
              }
              onChange={(event) =>
                setDependencyDescription(
                  event.target.value,
                )
              }
            />
          </label>


          <button type="submit">
            Add Dependency
          </button>
        </form>
      </section>


      <section className="panel">
        <h3>
          Business Processes
        </h3>

        {processes.length === 0 ? (
          <p>
            No business processes modeled.
          </p>
        ) : (
          <div className="business-process-grid">
            {processes.map(
              (process) => {
                const processDependencies =
                  dependencies.filter(
                    (dependency) =>
                      dependency
                        .business_process
                      === process.id,
                  );


                return (
                  <article
                    className="business-process-card"
                    key={process.id}
                  >
                    <div className="business-process-card-header">
                      <div>
                        <strong>
                          {process.name}
                        </strong>

                        <span>
                          {
                            process
                              .criticality_display
                          }
                        </span>
                      </div>

                      <button
                        type="button"
                        onClick={() =>
                          void handleDeleteProcess(
                            process,
                          )
                        }
                      >
                        Delete
                      </button>
                    </div>


                    <p>
                      {
                        process.description
                        || "No description"
                      }
                    </p>


                    <p>
                      <strong>
                        Potential consequence:
                      </strong>
                      {" "}
                      {
                        process
                          .impact_description
                        || "Not specified"
                      }
                    </p>


                    <div className="business-dependency-list">
                      <strong>
                        Asset Dependencies
                      </strong>

                      {
                        processDependencies
                        .length === 0
                      ? (
                        <p>
                          No assets linked.
                        </p>
                      )
                      : (
                        processDependencies
                        .map(
                          (dependency) => (
                            <div
                              className="business-dependency-row"
                              key={
                                dependency.id
                              }
                            >
                              <span>
                                {
                                  dependency
                                    .asset_name
                                }

                                {" — "}

                                {
                                  dependency
                                    .dependency_level_display
                                }
                              </span>

                              <button
                                type="button"
                                onClick={() =>
                                  void handleDeleteDependency(
                                    dependency,
                                  )
                                }
                              >
                                Remove
                              </button>
                            </div>
                          ),
                        )
                      )
		     }
                    </div>
                  </article>
                );
              },
            )}
          </div>
        )}
      </section>
    </>
  );
}

