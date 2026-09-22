import {
  useEffect,
  useState,
} from "react";

import {
  createOrganization,
  deleteOrganization,
  listOrganizations,
} from "../api/organizations";

import type {
  Organization,
} from "../types/models";


export default function OrganizationsPage() {
  const [
    organizations,
    setOrganizations,
  ] = useState<Organization[]>([]);

  const [
    name,
    setName,
  ] = useState("");

  const [
    description,
    setDescription,
  ] = useState("");

  const [
    error,
    setError,
  ] = useState("");

  const [
    saving,
    setSaving,
  ] = useState(false);


  useEffect(() => {
    let cancelled = false;

    async function loadInitialOrganizations() {
      try {
        const data =
          await listOrganizations();

        if (!cancelled) {
          setOrganizations(data);
          setError("");
        }
      } catch {
        if (!cancelled) {
          setError(
            "Unable to load organizations.",
          );
        }
      }
    }

    void loadInitialOrganizations();

    return () => {
      cancelled = true;
    };
  }, []);

  async function handleSubmit(
    event: React.FormEvent<HTMLFormElement>,
  ) {
    event.preventDefault();

    if (!name.trim()) {
      setError(
        "Organization name is required.",
      );

      return;
    }

    try {
      setSaving(true);
      setError("");

      await createOrganization({
        name: name.trim(),
        description: description.trim(),
      });

      setName("");
      setDescription("");

      await refreshOrganizations();
    } catch {
      setError(
        "Unable to create organization. "
        + "The name may already exist.",
      );
    } finally {
      setSaving(false);
    }
  }

  async function refreshOrganizations() {
    const data =
      await listOrganizations();

    setOrganizations(data);
  }

  async function handleDelete(
    organization: Organization,
  ) {
    const confirmed = window.confirm(
      `Delete ${organization.name}? `
      + "Its assets will also be deleted.",
    );
 
    if (!confirmed) {
      return;
    } 

    try {
      setError("");

      await deleteOrganization(
        organization.id,
      );

      await refreshOrganizations();
    } catch {
      setError(
        "Unable to delete organization.",
      );
    }
  }

  return (
    <>
      <div className="page-heading">
        <div>
          <h2>Organizations</h2>

          <p>
            Manage organizations modelled
            inside RiftTrace.
          </p>
        </div>
      </div>

      {error && (
        <div className="error-box">
          {error}
        </div>
      )}

      <section className="panel">
        <h3>Create Organization</h3>

        <form
          className="form-grid"
          onSubmit={handleSubmit}
        >
          <label>
            Name

            <input
              value={name}
              onChange={(event) =>
                setName(event.target.value)
              }
              placeholder="ExampleCorp"
            />
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
              placeholder="Organization description"
            />
          </label>

          <button
            type="submit"
            disabled={saving}
          >
            {saving
              ? "Creating..."
              : "Create Organization"}
          </button>
        </form>
      </section>

      <section className="panel">
        <h3>
          Existing Organizations
        </h3>

        {organizations.length === 0 ? (
          <p>
            No organizations found.
          </p>
        ) : (
          <div className="card-list">
            {organizations.map(
              (organization) => (
                <article
                  className="simple-card"
                  key={organization.id}
                >
                  <div>
                    <strong>
                      {organization.name}
                    </strong>

                    <p>
                      {organization.description
                        || "No description"}
                    </p>
                  </div>

                  <button
                    className="danger-button"
                    onClick={() =>
                      void handleDelete(
                        organization,
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

