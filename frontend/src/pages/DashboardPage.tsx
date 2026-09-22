import {
  useEffect,
  useState,
} from "react";

import { listAssets } from "../api/assets";
import { listOrganizations } from "../api/organizations";
import { listRelationships } from "../api/relationships";

import type {
  Asset,
  Organization,
  Relationship,
} from "../types/models";


export default function DashboardPage() {
  const [
    organizations,
    setOrganizations,
  ] = useState<Organization[]>([]);

  const [
    assets,
    setAssets,
  ] = useState<Asset[]>([]);

  const [
    relationships,
    setRelationships,
  ] = useState<Relationship[]>([]);

  const [
    loading,
    setLoading,
  ] = useState(true);

  const [
    error,
    setError,
  ] = useState("");


  useEffect(() => {
    async function loadDashboard() {
      try {
        const [
          organizationData,
          assetData,
          relationshipData,
        ] = await Promise.all([
          listOrganizations(),
          listAssets(),
          listRelationships(),
        ]);

        setOrganizations(
          organizationData,
        );

        setAssets(
          assetData,
        );

        setRelationships(
          relationshipData,
        );
      } catch {
        setError(
          "Unable to load RiftTrace data.",
        );
      } finally {
        setLoading(false);
      }
    }

    void loadDashboard();
  }, []);


  if (loading) {
    return <p>Loading dashboard...</p>;
  }


  if (error) {
    return (
      <div className="error-box">
        {error}
      </div>
    );
  }


  const criticalAssets = assets.filter(
    (asset) =>
      asset.criticality === "CRITICAL",
  );

  const exposedAssets = assets.filter(
    (asset) =>
      asset.is_internet_exposed,
  );


  return (
    <>
      <div className="page-heading">
        <div>
          <h2>Dashboard</h2>

          <p>
            Current RiftTrace environment overview.
          </p>
        </div>
      </div>

      <section className="metric-grid">
        <article className="metric-card">
          <span>Organizations</span>
          <strong>
            {organizations.length}
          </strong>
        </article>

        <article className="metric-card">
          <span>Assets</span>
          <strong>
            {assets.length}
          </strong>
        </article>

        <article className="metric-card">
          <span>Relationships</span>
          <strong>
            {relationships.length}
          </strong>
        </article>

        <article className="metric-card">
          <span>Critical Assets</span>
          <strong>
            {criticalAssets.length}
          </strong>
        </article>

        <article className="metric-card">
          <span>Internet Exposed</span>
          <strong>
            {exposedAssets.length}
          </strong>
        </article>
      </section>

      <section className="panel">
        <h3>Critical Assets</h3>

        {criticalAssets.length === 0 ? (
          <p>
            No critical assets are currently defined.
          </p>
        ) : (
          <div className="card-list">
            {criticalAssets.map(
              (asset) => (
                <article
                  className="simple-card"
                  key={asset.id}
                >
                  <strong>
                    {asset.name}
                  </strong>

                  <span>
                    {asset.organization_name}
                  </span>

                  <span>
                    {asset.asset_type_display}
                  </span>
                </article>
              ),
            )}
          </div>
        )}
      </section>
    </>
  );
}
