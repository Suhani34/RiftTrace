import {
  useEffect,
  useState,
} from "react";

import {
  listOrganizations,
} from "../api/organizations";

import {
  listCredentialExposures,
  listIdentities,
  listIdentityAccess,
  listIdentityLinks,
} from "../api/identities";

import type {
  Organization,
} from "../types/models";

import type {
  CredentialExposure,
  Identity,
  IdentityAccess,
  IdentityLink,
} from "../types/identity";


export default function IdentityGraphPage() {
  const [
    organizations,
    setOrganizations,
  ] = useState<
    Organization[]
  >([]);


  const [
    organizationId,
    setOrganizationId,
  ] = useState("");


  const [
    identities,
    setIdentities,
  ] = useState<
    Identity[]
  >([]);


  const [
    credentials,
    setCredentials,
  ] = useState<
    CredentialExposure[]
  >([]);


  const [
    accesses,
    setAccesses,
  ] = useState<
    IdentityAccess[]
  >([]);


  const [
    links,
    setLinks,
  ] = useState<
    IdentityLink[]
  >([]);


  const [
    error,
    setError,
  ] = useState("");


  async function loadIdentityData(
    id: number,
  ) {
    const [
      identitiesResult,
      credentialsResult,
      accessesResult,
      linksResult,
    ] = await Promise.all([
      listIdentities(id),

      listCredentialExposures(id),

      listIdentityAccess(id),

      listIdentityLinks(id),
    ]);


    setIdentities(
      identitiesResult
    );

    setCredentials(
      credentialsResult
    );

    setAccesses(
      accessesResult
    );

    setLinks(
      linksResult
    );
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


        await loadIdentityData(
          preferred.id
        );
      } catch (
        caught
      ) {
        if (!cancelled) {
          setError(
            caught instanceof Error
              ? caught.message
              : "Unable to load identities.",
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
    setOrganizationId(
      value
    );


    if (!value) {
      return;
    }


    try {
      setError("");

      await loadIdentityData(
        Number(value)
      );
    } catch (
      caught
    ) {
      setError(
        caught instanceof Error
          ? caught.message
          : "Unable to load identities.",
      );
    }
  }


  return (
    <>
      <div className="page-heading">
        <div>
          <h2>
            Identity Graph
          </h2>

          <p>
            Model users, service
            accounts, roles, credential
            exposure and asset access.
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
              organizationId
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
          Identities
        </h3>

        <div className="identity-card-grid">
          {identities.map(
            (identity) => (
              <article
                key={
                  identity.id
                }
                className="identity-card"
              >
                <strong>
                  {
                    identity.name
                  }
                </strong>

                <span>
                  {
                    identity
                      .identity_type_display
                  }
                </span>

                <span>
                  Privilege:
                  {" "}
                  {
                    identity
                      .privilege_level
                  }
                </span>

                <span>
                  {
                    identity.enabled
                      ? "Enabled"
                      : "Disabled"
                  }
                </span>
              </article>
            ),
          )}
        </div>
      </section>


      <section className="panel">
        <h3>
          Credential Exposure
        </h3>

        {credentials.map(
          (credential) => (
            <div
              key={
                credential.id
              }
              className="identity-row"
            >
              <strong>
                {
                  credential.name
                }
              </strong>

              <span>
                {
                  credential
                    .stored_on_asset_name
                }
                {" → "}
                {
                  credential
                    .identity_name
                }
              </span>

              <span>
                {
                  credential
                    .credential_type
                }
              </span>
            </div>
          ),
        )}
      </section>


      <section className="panel">
        <h3>
          Identity Links
        </h3>

        {links.map(
          (link) => (
            <div
              key={
                link.id
              }
              className="identity-row"
            >
              <strong>
                {
                  link
                    .source_identity_name
                }
                {" → "}
                {
                  link
                    .target_identity_name
                }
              </strong>

              <span>
                {
                  link.link_type
                }
              </span>

              <span>
                MFA:
                {" "}
                {
                  link.requires_mfa
                    ? "Required"
                    : "No"
                }
              </span>
            </div>
          ),
        )}
      </section>


      <section className="panel">
        <h3>
          Asset Access
        </h3>

        {accesses.map(
          (access) => (
            <div
              key={
                access.id
              }
              className="identity-row"
            >
              <strong>
                {
                  access
                    .identity_name
                }
                {" → "}
                {
                  access.asset_name
                }
              </strong>

              <span>
                {
                  access.access_type
                }
              </span>

              <span>
                Privilege:
                {" "}
                {
                  access
                    .granted_privilege
                }
              </span>

              <span>
                MFA:
                {" "}
                {
                  access.requires_mfa
                    ? "Required"
                    : "No"
                }
              </span>
            </div>
          ),
        )}
      </section>
    </>
  );
}
