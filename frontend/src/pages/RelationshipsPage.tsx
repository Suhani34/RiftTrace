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
        description:
          description.trim(),
      });

      setSource("");
      setTarget("");
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
                </article>
              ),
            )}
          </div>
        )}
      </section>
    </>
  );
}

