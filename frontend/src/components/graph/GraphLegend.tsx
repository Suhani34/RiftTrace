export default function GraphLegend() {
  return (
    <div className="graph-legend">
      <strong>Criticality</strong>

      <div className="legend-items">
        <span>
          <i className="legend-dot legend-low" />
          Low
        </span>

        <span>
          <i className="legend-dot legend-medium" />
          Medium
        </span>

        <span>
          <i className="legend-dot legend-high" />
          High
        </span>

        <span>
          <i className="legend-dot legend-critical" />
          Critical
        </span>
      </div>

      <p>
        Zone colors indicate visual
        grouping only, not risk.
      </p>
    </div>
  );
}
