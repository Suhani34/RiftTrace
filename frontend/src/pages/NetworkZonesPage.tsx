import {
  useEffect,
  useState,
} from "react";

import {
  listOrganizations,
} from "../api/organizations";

import {
  createZone,
  deleteZone,
  listZones,
} from "../api/zones";

import type {
  NetworkZone,
  Organization,
  ZoneType,
} from "../types/models";


const ZONE_TYPES: Array<{
  value: ZoneType;
  label: string;
}> = [
  { value: "DMZ", label: "DMZ" },
  { value: "INTERNAL", label: "Internal" },
  {
    value: "RESTRICTED",
    label: "Restricted",
  },
  {
    value: "MANAGEMENT",
    label: "Management",
  },
  { value: "CLOUD", label: "Cloud" },
  { value: "ENDPOINT", label: "Endpoint" },
  { value: "OTHER", label: "Other" },
];


export default function NetworkZonesPage() {
  const [
    organizations,
    setOrganizations,
  ] = useState<Organization[]>([]);

  const [
    zones,
    setZones,
  ] = useState<NetworkZone[]>([]);

  const [
    selectedOrganization,
    setSelectedOrganization,
  ] = useState("");

  const [
    name,
    setName,
  ] = useState("");

  const [
    zoneType,
    setZoneType,
  ] = useState<ZoneType>("INTERNAL");

  const [
    description,
    setDescription,
  ] = useState("");

  const [
    error,
    setError,
  ] = useState("");


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

        if (organizationData.length === 0) {
          return;
        }

        const organizationId =
          organizationData[0].id;

        const zoneData =
          await listZones(
            organizationId,
          );

        if (cancelled) {
          return;
        }

        setSelectedOrganization(
          String(organizationId),
        );

        setZones(zoneData);
      } catch {
        if (!cancelled) {
          setError(
            "Unable to load network zones.",
          );
        }
      }
    }

    void initialize();

    return () => {
      cancelled = true;
    };
  }, []);


  async function refreshZones(
    organizationId: number,
  ) {
    const zoneData =
      await listZones(
        organizationId,
      );

    setZones(zoneData);
  }


  async function handleOrganizationChange(
    value: string,
  ) {
    setSelectedOrganization(value);

    if (!value) {
      setZones([]);
      return;
    }

    try {
      setError("");

      await refreshZones(
        Number(value),
      );
    } catch {
      setError(
        "Unable to load network zones.",
      );
    }
  }


  async function handleSubmit(
    event: React.FormEvent<HTMLFormElement>,
  ) {
    event.preventDefault();

    if (!selectedOrganization) {
      setError(
        "Select an organization first.",
      );

      return;
    }

    if (!name.trim()) {
      setError(
        "Network zone name is required.",
      );

      return;
    }

    try {
      setError("");

      await createZone({
        organization:
          Number(selectedOrganization),

        name: name.trim(),

        zone_type: zoneType,

        description:
          description.trim(),
      });

      setName("");
      setDescription("");

      await refreshZones(
        Number(selectedOrganization),
      );
    } catch {
      setError(
        "Unable to create network zone.",
      );
    }
  }


  async function handleDelete(
    zone: NetworkZone,
  ) {
    const confirmed = window.confirm(
      `Delete network zone ${zone.name}?`,
    );

    if (!confirmed) {
      return;
    }

    try {
      setError("");

      await deleteZone(zone.id);

      await refreshZones(
        Number(selectedOrganization),
      );
    } catch {
      setError(
        "Unable to delete network zone.",
      );
    }
  }


  return (
    <>
      <div className="page-heading">
        <div>
          <h2>Network Zones</h2>

          <p>
            Model security and network
            boundaries inside an organization.
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
              void handleOrganizationChange(
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
        <h3>Create Network Zone</h3>

        <form
          className="form-grid"
          onSubmit={handleSubmit}
        >
          <label>
            Name

            <input
              value={name}
              onChange={(event) =>
                setName(
                  event.target.value,
                )
              }
              placeholder="DMZ"
            />
          </label>

          <label>
            Zone Type

            <select
              value={zoneType}
              onChange={(event) =>
                setZoneType(
                  event.target.value as ZoneType,
                )
              }
            >
              {ZONE_TYPES.map(
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
            Create Zone
          </button>
        </form>
      </section>

      <section className="panel">
        <h3>Network Zones</h3>

        {zones.length === 0 ? (
          <p>No network zones found.</p>
        ) : (
          <div className="card-list">
            {zones.map((zone) => (
              <article
                className="simple-card"
                key={zone.id}
              >
                <div>
                  <strong>
                    {zone.name}
                  </strong>

                  <p>
                    {zone.zone_type_display}
                  </p>

                  {zone.description && (
                    <p>
                      {zone.description}
                    </p>
                  )}
                </div>

                <button
                  className="danger-button"
                  onClick={() =>
                    void handleDelete(zone)
                  }
                >
                  Delete
                </button>
              </article>
            ))}
          </div>
        )}
      </section>
    </>
  );
}
