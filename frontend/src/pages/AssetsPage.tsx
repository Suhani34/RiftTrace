import {
  useCallback,
  useEffect,
  useState,
} from "react";

import {
  createAsset,
  deleteAsset,
  listAssets,
} from "../api/assets";

import {
  listOrganizations,
} from "../api/organizations";

import {
  listZones,
} from "../api/zones";

import type {
  Asset,
  AssetType,
  Criticality,
  Environment,
  NetworkZone,
  Organization,
} from "../types/models";


const ASSET_TYPES: Array<{
  value: AssetType;
  label: string;
}> = [
  { value: "APPLICATION", label: "Application" },
  { value: "API", label: "API" },
  { value: "SERVER", label: "Server" },
  { value: "DATABASE", label: "Database" },
  { value: "WORKSTATION", label: "Workstation" },
  { value: "FILE_SERVER", label: "File Server" },
  { value: "VPN_GATEWAY", label: "VPN Gateway" },
  { value: "CLOUD_SERVICE", label: "Cloud Service" },
  { value: "CI_CD", label: "CI/CD System" },
  { value: "EMAIL_SERVER", label: "Email Server" },
  {
    value: "DOMAIN_CONTROLLER",
    label: "Domain Controller",
  },
  {
    value: "NETWORK_DEVICE",
    label: "Network Device",
  },
  { value: "OTHER", label: "Other" },
];


const CRITICALITIES: Criticality[] = [
  "LOW",
  "MEDIUM",
  "HIGH",
  "CRITICAL",
];

const ENVIRONMENTS: Array<{
  value: Environment;
  label: string;
}> = [
  {
    value: "PRODUCTION",
    label: "Production",
  },
  {
    value: "STAGING",
    label: "Staging",
  },
  {
    value: "TEST",
    label: "Test",
  },
  {
    value: "DEVELOPMENT",
    label: "Development",
  },
  {
    value: "OTHER",
    label: "Other",
  },
];

export default function AssetsPage() {
  const [
    organizations,
    setOrganizations,
  ] = useState<Organization[]>([]);

  const [
    assets,
    setAssets,
  ] = useState<Asset[]>([]);

  const [
    selectedOrganization,
    setSelectedOrganization,
  ] = useState("");

  const [
    name,
    setName,
  ] = useState("");

  const [
    assetType,
    setAssetType,
  ] = useState<AssetType>("SERVER");

  const [
    criticality,
    setCriticality,
  ] = useState<Criticality>("MEDIUM");

  const [
    description,
    setDescription,
  ] = useState("");

  const [
    internetExposed,
    setInternetExposed,
  ] = useState(false);

  const [
    error,
    setError,
  ] = useState("");

  const [
    zones,
    setZones,
  ] = useState<NetworkZone[]>([]);

  const [
    selectedZone,
    setSelectedZone,
  ] = useState("");

  const [
    environment,
    setEnvironment,
  ] = useState<Environment>(
    "PRODUCTION",
  );

  const [
    hostname,
    setHostname,
  ] = useState("");

  const [
    ipAddress,
    setIpAddress,
  ] = useState("");

  const loadAssets = useCallback(
    async (organizationId?: number) => {
      try {
        setError("");

        const data = await listAssets(
          organizationId,
        );

        setAssets(data);
      } catch {
        setError(
          "Unable to load assets.",
        );
      }
    },
    [],
  );


  useEffect(() => {
    async function initialize() {
      try {
        const orgData =
          await listOrganizations();

        setOrganizations(orgData);

        if (orgData.length > 0) {
          const firstId =
            String(orgData[0].id);

          setSelectedOrganization(
            firstId,
          );

          await loadAssets(
            orgData[0].id,
          );

	  const zoneData =
  	    await listZones(
    	    orgData[0].id,
  	  );

          setZones(zoneData);

        }
      } catch {
        setError(
          "Unable to load organizations.",
        );
      }
    }

    void initialize();
  }, [loadAssets]);


  async function handleOrganizationChange(
    value: string,
  ) {
    setSelectedOrganization(value);

    const zoneData =
      await listZones(
        Number(value),
    );

    setZones(zoneData);
    setSelectedZone("");

    if (value) {
      await loadAssets(
        Number(value),
      );
    } else {
      setAssets([]);
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
        "Asset name is required.",
      );

      return;
    }

    try {
      setError("");

      await createAsset({
        organization:
          Number(selectedOrganization),

        name: name.trim(),

        asset_type: assetType,

        criticality,

	environment,

	network_zone:
	  selectedZone
	    ? Number(selectedZone)
	    : null,

	hostname: hostname.trim(),

	ip_address:
	  ipAddress.trim()
	    ? ipAddress.trim()
	    : null,

        description:
          description.trim(),

        is_internet_exposed:
          internetExposed,
      });

      setName("");
      setDescription("");
      setHostname("");
      setIpAddress("");
      setInternetExposed(false);

      await loadAssets(
        Number(selectedOrganization),
      );
    } catch {
      setError(
        "Unable to create asset. "
        + "Check for duplicate names "
        + "or invalid data.",
      );
    }
  }


  async function handleDelete(
    asset: Asset, 
  ) 
  {
    const confirmed = window.confirm(
      `Delete ${asset.name}?`,
    );

    if (!confirmed) {
      return;
    }

    try {
      await deleteAsset(asset.id);

      await loadAssets(
        Number(selectedOrganization),
      );
    } catch {
      setError(
        "Unable to delete asset.",
      );
    }
  }


  return (
    <>
      <div className="page-heading">
        <div>
          <h2>Assets</h2>

          <p>
            Model systems, applications,
            databases and infrastructure.
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
            {organizations.length === 0 && (
              <option value="">
                No organizations available
              </option>
            )}

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
        <h3>Create Asset</h3>

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
              placeholder="VPN Gateway"
            />
          </label>

	  <label>
	    Environment

	    <select
	      value={environment}
	      onChange={(event) =>
	        setEnvironment(
	          event.target.value as Environment,
	        )
	      }
	    >
	      {ENVIRONMENTS.map(
	        (item) => (
	          <option
	            key={item.value}
	            value={item.value}
	          >
	            {item.label}
	          </option>
	        ),
	      )}
	    </select>
	  </label>

	  <label>
	    Network Zone

	    <select
	      value={selectedZone}
	      onChange={(event) =>
	        setSelectedZone(
	          event.target.value,
	        )
	      }
	    >
	      <option value="">
	        No zone
	      </option>

	      {zones.map((zone) => (
	        <option
	          key={zone.id}
	          value={zone.id}
	        >
	          {zone.name}
	        </option>
	      ))}
	    </select>
	  </label>

	  <label>
	    Hostname

	    <input
	      value={hostname}
	      onChange={(event) =>
	        setHostname(
	          event.target.value,
	        )
	      }
	      placeholder="web01.example.local"
	    />
	  </label>

	  <label>
	    IP Address

	    <input
	      value={ipAddress}
	      onChange={(event) =>
	        setIpAddress(
	          event.target.value,
	        )
	      }
	      placeholder="10.10.10.10"
	    />
	  </label>

          <label>
            Asset Type

            <select
  		value={assetType}
  		onChange={(event) =>
    		setAssetType(
      		event.target.value as AssetType,
    		)
  		}
		>
              {ASSET_TYPES.map(
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
            Criticality

            <select
              value={criticality}
              onChange={(event) =>
                setCriticality(
                  event.target.value as Criticality,
                )
              }
            >
              {CRITICALITIES.map(
                (value) => (
                  <option
                    key={value}
                    value={value}
                  >
                    {value}
                  </option>
                ),
              )}
            </select>
          </label>

          <label className="checkbox-label">
            <input
              type="checkbox"
              checked={internetExposed}
              onChange={(event) =>
                setInternetExposed(
                  event.target.checked,
                )
              }
            />

            Internet exposed
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
            Create Asset
          </button>
        </form>
      </section>

      <section className="panel">
        <h3>Assets</h3>

        {assets.length === 0 ? (
          <p>
            No assets found for this organization.
          </p>
        ) : (
          <div className="card-list">
            {assets.map(
              (asset) => (
                <article
                  className="asset-card"
                  key={asset.id}
                >
                  <div>
                    <div className="card-title-row">
                      <strong>
                        {asset.name}
                      </strong>

                      <span
                        className={
                          `badge criticality-${asset.criticality.toLowerCase()}`
                        }
                      >
                        {asset.criticality_display}
                      </span>

		    <p>
		      Environment:
		      {" "}
		      {asset.environment_display}
		    </p>

		    <p>
		      Zone:
		      {" "}
		      {asset.network_zone_name ?? "Unassigned"}
		    </p>

		    {asset.hostname && (
		      <p>
		        Hostname: {asset.hostname}
		      </p>
		    )}

		    {asset.ip_address && (
		      <p>
		        IP: {asset.ip_address}
		      </p>
		    )}

                    </div>

                    <p>
                      {asset.asset_type_display}
                    </p>

                    {asset.is_internet_exposed && (
                      <span className="warning-text">
                        Internet exposed
                      </span>
                    )}
                  </div>

                  <button
                    className="danger-button"
                    onClick={() =>
                      void handleDelete(
                        asset,
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
