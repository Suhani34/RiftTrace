import type {
  Asset,
  Relationship,
} from "../../types/models";


interface GraphDetailsPanelProps {
  asset: Asset | null;
  relationship: Relationship | null;
}


export default function GraphDetailsPanel({
  asset,
  relationship,
}: GraphDetailsPanelProps) {
  if (asset) {
    return (
      <aside className="graph-details-panel">
        <div className="details-heading">
          <span className="details-eyebrow">
            Asset
          </span>

          <h3>
            {asset.name}
          </h3>
        </div>

        <dl className="details-list">
          <div>
            <dt>Type</dt>
            <dd>
              {asset.asset_type_display}
            </dd>
          </div>

          <div>
            <dt>Criticality</dt>
            <dd>
              {asset.criticality_display}
            </dd>
          </div>

          <div>
            <dt>Environment</dt>
            <dd>
              {asset.environment_display}
            </dd>
          </div>

          <div>
            <dt>Network Zone</dt>
            <dd>
              {asset.network_zone_name
                ?? "Unassigned"}
            </dd>
          </div>

          <div>
            <dt>Hostname</dt>
            <dd>
              {asset.hostname
                || "Not specified"}
            </dd>
          </div>

          <div>
            <dt>IP Address</dt>
            <dd>
              {asset.ip_address
                ?? "Not specified"}
            </dd>
          </div>

          <div>
            <dt>Internet Exposed</dt>
            <dd>
              {asset.is_internet_exposed
                ? "Yes"
                : "No"}
            </dd>
          </div>

          <div>
            <dt>Description</dt>
            <dd>
              {asset.description
                || "No description"}
            </dd>
          </div>
        </dl>
      </aside>
    );
  }


  if (relationship) {
    return (
      <aside className="graph-details-panel">
        <div className="details-heading">
          <span className="details-eyebrow">
            Relationship
          </span>

          <h3>
            {relationship
              .relationship_type_display}
          </h3>
        </div>

        <dl className="details-list">
          <div>
            <dt>Source</dt>
            <dd>
              {relationship.source_name}
            </dd>
          </div>

          <div>
            <dt>Target</dt>
            <dd>
              {relationship.target_name}
            </dd>
          </div>

          <div>
            <dt>Relationship</dt>
            <dd>
              {
                relationship
                  .relationship_type_display
              }
            </dd>
          </div>

          <div>
            <dt>Protocol</dt>
            <dd>
              {relationship.protocol
                || "Not specified"}
            </dd>
          </div>

          <div>
            <dt>Port</dt>
            <dd>
              {relationship.port
                ?? "Not specified"}
            </dd>
          </div>

          <div>
            <dt>
              Authentication Required
            </dt>
            <dd>
              {
                relationship
                  .requires_authentication
                  ? "Yes"
                  : "No"
              }
            </dd>
          </div>

          <div>
            <dt>Description</dt>
            <dd>
              {relationship.description
                || "No description"}
            </dd>
          </div>
        </dl>
      </aside>
    );
  }


  return (
    <aside className="graph-details-panel">
      <div className="details-empty">
        <h3>Graph Details</h3>

        <p>
          Select an asset or relationship
          in the topology to inspect it.
        </p>
      </div>
    </aside>
  );
}
