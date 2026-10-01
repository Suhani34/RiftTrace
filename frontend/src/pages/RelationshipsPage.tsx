import {
  useEffect,
  useMemo,
  useState,
} from "react";

import {
  listAssets,
} from "../api/assets";

import {
  listOrganizations,
} from "../api/organizations";

import {
  createRelationship,
  deleteRelationship,
  listRelationships,
} from "../api/relationships";

import type {
  Asset,
  Organization,
  Relationship,
  RelationshipType,
  RequiredSourcePrivilege,
} from "../types/models";


const RELATIONSHIP_TYPES: Array<{
  value: RelationshipType;
  label: string;
}> = [
  {
    value: "CONNECTS_TO",
    label: "Connects To",
  },
  {
    value: "CALLS",
    label: "Calls",
  },
  {
    value: "READS",
    label: "Reads",
  },
  {
    value: "WRITES",
    label: "Writes",
  },
  {
    value: "AUTHENTICATES_TO",
    label: "Authenticates To",
  },
  {
    value: "DEPENDS_ON",
    label: "Depends On",
  },
];


export default function RelationshipsPage() {
  const [
    organizations,
    setOrganizations,
  ] = useState<Organization[]>([]);

  const [
    allAssets,
    setAllAssets,
  ] = useState<Asset[]>([]);

  const [
    relationships,
    setRelationships,
  ] = useState<Relationship[]>([]);

  const [
    protocol,
    setProtocol,
  ] = useState("");

  const [
    port,
    setPort,
  ] = useState("");

  const [
    requiresAuthentication,
    setRequiresAuthentication,
  ] = useState(false);

  const [
    requiredSourcePrivilege,
    setRequiredSourcePrivilege,
  ] = useState<
    RequiredSourcePrivilege
  >("LOW");

  const [
    selectedOrganization,
    setSelectedOrganization,
  ] = useState("");

  const [
    source,
    setSource,
  ] = useState("");

  const [
    target,
    setTarget,
  ] = useState("");

  const [
    relationshipType,
    setRelationshipType,
  ] = useState<RelationshipType>(
    "CONNECTS_TO",
  );

  const [
    description,
    setDescription,
  ] = useState("");

  const [
    error,
    setError,
  ] = useState("");


  useEffect(() => {
    async function initialize() {
      try {
        const [
          orgData,
          assetData,
        ] = await Promise.all([
          listOrganizations(),
          listAssets(),
        ]);

        setOrganizations(orgData);
        setAllAssets(assetData);

        if (orgData.length > 0) {
          setSelectedOrganization(
            String(orgData[0].id),
          );
        }
      } catch {
        setError(
          "Unable to load relationship data.",
        );
      }
    }

    void initialize();
  }, []);


useEffect(() => {
  async function load() {
    if (!selectedOrganization) {
      return;
    }

    try {
      const data =
        await listRelationships(
          Number(selectedOrganization),
        );

      setRelationships(data);
      setError("");
    } catch {
      setError(
        "Unable to load relationships.",
      );
    }
  }

  void load();
}, [selectedOrganization]);


  const availableAssets = useMemo(
    () =>
      allAssets.filter(
        (asset) =>
          asset.organization
          === Number(
            selectedOrganization,
          ),
      ),
    [
      allAssets,
      selectedOrganization,
    ],
  );

  function handleOrganizationChange(
    value: string,
  ) {
    setSelectedOrganization(value);
    setSource("");
    setTarget("");
    setDescription("");
  }

  async function handleSubmit(
    event: React.FormEvent<HTMLFormElement>,
  ) {
    event.preventDefault();

    if (!source || !target) {
      setError(
        "Select both source and target assets.",
      );

      return;
    }

    try {
      setError("");

      await createRelationship({
        source: Number(source),
        target: Number(target),
        relationship_type:
          relationshipType,
	protocol: protocol.trim(),

	port:
	  port.trim()
	    ? Number(port)
	    : null,

	requires_authentication:
	  requiresAuthentication,
	required_source_privilege:
	  requiredSourcePrivilege,
        description:
          description.trim(),
      });

      setSource("");
      setTarget("");
      setProtocol("");
      setPort("");
      setRequiresAuthentication(false);
      setDescription("");

      const data =
        await listRelationships(
          Number(selectedOrganization),
        );

      setRelationships(data);
    } catch {
      setError(
        "Unable to create relationship. "
        + "Check that source and target "
        + "are different and belong to "
        + "the same organization.",
      );
    }
  }


  async function handleDelete(
    relationship: Relationship,
  ) {
    const confirmed = window.confirm(
      `Delete relationship from `
      + `${relationship.source_name} to `
      + `${relationship.target_name}?`,
    );

    if (!confirmed) {
      return;
    }

    try {
      await deleteRelationship(
        relationship.id,
      );

      const data =
        await listRelationships(
          Number(selectedOrganization),
        );

      setRelationships(data);
    } catch {
      setError(
        "Unable to delete relationship.",
      );
    }
  }


  return (
    <>
      <div className="page-heading">
        <div>
          <h2>Relationships</h2>

          <p>
            Define directed technical
            relationships between assets.
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
            value={selectedOrganization}
            onChange={(event) =>
              handleOrganizationChange(
                event.target.value,
              )
            }
          >
            {organizations.map(
              (organization) => (
                <option
                  key={organization.id}
                  value={organization.id}
                >
                  {organization.name}
                </option>
              ),
            )}
          </select>
        </label>
      </section>

      <section className="panel">
        <h3>Create Relationship</h3>

        <form
          className="form-grid"
          onSubmit={handleSubmit}
        >
          <label>
            Source Asset

            <select
              value={source}
              onChange={(event) =>
                setSource(
                  event.target.value,
                )
              }
            >
              <option value="">
                Select source
              </option>

              {availableAssets.map(
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
            Relationship

            <select
              value={relationshipType}
              onChange={(event) =>
                setRelationshipType(
                  event.target.value as RelationshipType,
                )
              }
            >
              {RELATIONSHIP_TYPES.map(
                (type) => (
                  <option
                    key={type.value}
                    value={type.value}
                  >
                    {type.label}
                  </option>
                ),
              )}
            </select>
          </label>

	  <label>
	    Protocol

	    <input
	      value={protocol}
	      onChange={(event) =>
	        setProtocol(
	          event.target.value,
	        )
	      }
	      placeholder="HTTPS"
	    />
	  </label>

	  <label>
	    Port

	    <input
	      type="number"
	      min="1"
	      max="65535"
	      value={port}
	      onChange={(event) =>
	        setPort(
	          event.target.value,
	        )
	      }
	      placeholder="443"
	    />
	  </label>

	  <label className="checkbox-label">
	    <input
	      type="checkbox"
	      checked={requiresAuthentication}
	      onChange={(event) =>
	        setRequiresAuthentication(
	          event.target.checked,
	        )
	      }
	    />

	    Requires authentication
	  </label>

	  <label>
	    Required Source Privilege

	    <select
	      value={
	        requiredSourcePrivilege
	      }
	      onChange={(event) =>
	        setRequiredSourcePrivilege(
	          event.target.value as RequiredSourcePrivilege,
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
            Target Asset

            <select
              value={target}
              onChange={(event) =>
                setTarget(
                  event.target.value,
                )
              }
            >
              <option value="">
                Select target
              </option>

              {availableAssets.map(
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
            Create Relationship
          </button>
        </form>
      </section>

      <section className="panel">
        <h3>Relationships</h3>

        {relationships.length === 0 ? (
          <p>
            No relationships defined yet.
          </p>
        ) : (
          <div className="card-list">
            {relationships.map(
              (relationship) => (
                <article
                  className="relationship-card"
                  key={relationship.id}
                >
                  <div>
                    <strong>
                      {relationship.source_name}
                    </strong>

                    <span className="relationship-arrow">
                      {" "}
                      →{" "}
                      {
                        relationship
                          .relationship_type_display
                      }
                      {" "}
                      →{" "}
                    </span>

                    <strong>
                      {relationship.target_name}
                    </strong>

                    {relationship.description && (
                      <p>
                        {
                          relationship.description
                        }
                      </p>
                    )}
                  </div>

                  <button
                    className="danger-button"
                    onClick={() =>
                      void handleDelete(
                        relationship,
                      )
                    }
                  >
                    Delete
                  </button>

		  <p>
		    Protocol:
		    {" "}
		    {relationship.protocol || "Unspecified"}

		    {relationship.port
		      ? ` / ${relationship.port}`
		      : ""}
		  </p>

		  <p>
		    Authentication:
		    {" "}
		    {relationship.requires_authentication
		      ? "Required"
		      : "Not specified"}
		  </p>

                </article>
              ),
            )}
          </div>
        )}
      </section>
    </>
  );
}

