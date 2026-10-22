import {
  useEffect,
  useState,
} from "react";

import {
  listOrganizations,
} from "../api/organizations";

import {
  runIdentityPropagation,
} from "../api/identities";

import SaveScenarioPanel from "../components/SaveScenarioPanel";

import {
  extractComparableMetrics,
} from "../utils/scenarioMetrics";

import {
  listAssets,
} from "../api/assets";

import type {
  Asset,
  Organization,
} from "../types/models";

import type {
  IdentityPropagationResult,
} from "../types/identity";


export default function IdentityPropagationPage() {
  const [
    organizations,
    setOrganizations,
  ] = useState<
    Organization[]
  >([]);


  const [
    assets,
    setAssets,
  ] = useState<
    Asset[]
  >([]);


  const [
    organizationId,
    setOrganizationId,
  ] = useState("");


  const [
    assetId,
    setAssetId,
  ] = useState("");


  const [
    privilege,
    setPrivilege,
  ] = useState<
    "LOW" | "HIGH"
  >("LOW");


  const [
    result,
    setResult,
  ] = useState<
    IdentityPropagationResult
    | null
  >(null);


  const [
    error,
    setError,
  ] = useState("");


  const [
    working,
    setWorking,
  ] = useState(false);


  async function loadAssets(
    orgId: number,
  ) {
    const data =
      await listAssets(
        orgId
      );


    setAssets(
      data
    );


    if (
      data.length > 0
    ) {
      setAssetId(
        String(
          data[0].id
        )
      );
    }
  }


  useEffect(() => {
    let cancelled =
      false;


    async function initialize() {
      try {
        const orgs =
          await listOrganizations();


        if (
          cancelled
          || orgs.length === 0
        ) {
          return;
        }


        setOrganizations(
          orgs
        );


        const preferred =
          orgs.find(
            (item) =>
              item.name
              === "Import Demo Corp",
          )
          ?? orgs[0];


        setOrganizationId(
          String(
            preferred.id
          )
        );


        await loadAssets(
          preferred.id
        );
      } catch (
        caught
      ) {
        if (!cancelled) {
          setError(
            caught instanceof Error
              ? caught.message
              : "Initialization failed.",
          );
        }
      }
    }


    void initialize();


    return () => {
      cancelled = true;
    };
  }, []);


  async function handleRun() {
    if (
      !organizationId
      || !assetId
    ) {
      return;
    }


    try {
      setWorking(true);

      setError("");


      const data =
        await runIdentityPropagation(
          {
            organization:
              Number(
                organizationId
              ),

            compromised_assets: [
              {
                asset_id:
                  Number(
                    assetId
                  ),

                privilege,
              },
            ],
          }
        );


      setResult(
        data
      );
    } catch (
      caught
    ) {
      setError(
        caught instanceof Error
          ? caught.message
          : "Simulation failed.",
      );
    } finally {
      setWorking(false);
    }
  }

  const scenarioRequestPayload = {
    organization:
      Number(
        organizationId
      ),

    compromised_assets: [
      {
        asset_id:
          Number(
            assetId
          ),

        privilege,
      },
    ],
  };

  return (
    <>
      <div className="page-heading">
        <div>
          <h2>
            Identity Propagation
          </h2>

          <p>
            Analyze potential lateral
            movement through modeled
            credential and identity paths.
          </p>
        </div>
      </div>


      {error && (
        <div className="error-box">
          {error}
        </div>
      )}


      <section className="panel">
        <div className="form-grid">
          <label>
            Organization

            <select
              value={
                organizationId
              }

              onChange={async (
                event
              ) => {
                const value =
                  event.target.value;


                setOrganizationId(
                  value
                );

                setResult(null);


                await loadAssets(
                  Number(value)
                );
              }}
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


          <label>
            Initial Compromised Asset

            <select
              value={
                assetId
              }

              onChange={(event) =>
                setAssetId(
                  event.target.value
                )
              }
            >
              {assets.map(
                (asset) => (
                  <option
                    key={
                      asset.id
                    }

                    value={
                      asset.id
                    }
                  >
                    {
                      asset.name
                    }
                  </option>
                ),
              )}
            </select>
          </label>


          <label>
            Initial Privilege

            <select
              value={
                privilege
              }

              onChange={(event) =>
                setPrivilege(
                  event.target.value as
                    "LOW" | "HIGH"
                )
              }
            >
              <option value="LOW">
                LOW
              </option>

              <option value="HIGH">
                HIGH
              </option>
            </select>
          </label>
        </div>


        <button
          type="button"

          disabled={
            working
          }

          onClick={() => {
            void handleRun();
          }}
        >
          {
            working
              ? "Running..."
              : "Run Identity Simulation"
          }
        </button>
      </section>


      {result && (
        <>
          <section className="identity-summary-grid">
            <article>
              <strong>
                Acquired Identities
              </strong>

              <span>
                {
                  result
                    .summary
                    .acquired_identities
                }
              </span>
            </article>

            <article>
              <strong>
                New Assets
              </strong>

              <span>
                {
                  result
                    .summary
                    .new_assets_from_identity
                }
              </span>
            </article>

            <article>
              <strong>
                Successful Steps
              </strong>

              <span>
                {
                  result
                    .summary
                    .successful_identity_steps
                }
              </span>
            </article>

            <article>
              <strong>
                Blocked Steps
              </strong>

              <span>
                {
                  result
                    .summary
                    .blocked_identity_steps
                }
              </span>
            </article>
          </section>

          <SaveScenarioPanel
            organizationId={
              Number(
                organizationId
              )
            }

            simulationType={
              "IDENTITY_PROPAGATION"
            }

            requestPayload={
              scenarioRequestPayload
            }

            resultPayload={
              result
            }

            metrics={
              extractComparableMetrics(
                "IDENTITY_PROPAGATION",
                result,
              )
            }
          />

          <section className="panel">
            <h3>
              Identity Path
            </h3>

            {result.steps.map(
              (
                step,
                index,
              ) => (
                <div
                  key={
                    `${step.step_type}-${index}`
                  }

                  className="identity-path-step"
                >
                  <span>
                    {
                      step.source_name
                    }
                  </span>

                  <strong>
                    →
                    {" "}
                    {
                      step.reference_name
                    }
                    {" "}
                    →
                  </strong>

                  <span>
                    {
                      step.target_name
                    }
                  </span>

                  {step
                    .attack_annotations
                    .length > 0 && (
                      <div className="attack-annotation-list">
                        {step
                          .attack_annotations
                          .map(
                            (annotation) => (
                              <a
                                key={
                                  annotation.attack_id
                                }

                                className="attack-annotation-badge"

                                href={
                                  annotation.source_url
                                }

                                target="_blank"

                                rel="noreferrer"

                                title={
                                  annotation.basis
                                }
                              >
                                {
                                  annotation.attack_id
                                }
                                {" "}
                                {
                                  annotation.name
                                }
                              </a>
                            ),
                          )}
                      </div>
                    )}
                </div>
              ),
            )}
          </section>

          <section className="panel">
            <h3>
              Potentially Compromised Assets
            </h3>

            {result
              .compromised_assets
              .map(
                (asset) => (
                  <div
                    key={
                      asset.asset_id
                    }

                    className="identity-row"
                  >
                    <strong>
                      {
                        asset
                          .asset_name
                      }
                    </strong>

                    <span>
                      Privilege:
                      {" "}
                      {
                        asset
                          .privilege
                      }
                    </span>

                    <span>
                      {
                        asset.seed
                          ? "Initial"
                          : "Identity-mediated"
                      }
                    </span>
                  </div>
                ),
              )}
          </section>


          <section className="panel">
            <h3>
              Blocked Identity Paths
            </h3>

            {
              result
                .blocked_steps
                .length === 0
            ? (
              <p>
                No modeled identity path
                was blocked.
              </p>
            )
            : (
              result
                .blocked_steps
                .map(
                  (
                    step,
                    index,
                  ) => (
                    <div
                      key={
                        `${step.reference_id}-${index}`
                      }

                      className="identity-blocked-step"
                    >
                      <strong>
                        {
                          step.source_name
                        }
                        {" → "}
                        {
                          step.target_name
                        }
                      </strong>

                      <span>
                        {
                          step.reason
                        }
                      </span>
                    </div>
                  ),
                )
              )
	    }
          </section>
        </>
      )}
    </>
  );
}
