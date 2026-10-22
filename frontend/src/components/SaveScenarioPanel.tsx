import {
  useState,
} from "react";

import {
  createScenario,
  createScenarioRun,
} from "../api/scenarios";

import type {
  SimulationType,
} from "../types/scenarios";


interface SaveScenarioPanelProps {
  organizationId: number;

  simulationType:
    SimulationType;

  requestPayload:
    Record<string, unknown>;

  resultPayload: unknown;

  metrics:
    Record<string, number>;
}


export default function SaveScenarioPanel(
  {
    organizationId,
    simulationType,
    requestPayload,
    resultPayload,
    metrics,
  }: SaveScenarioPanelProps,
) {
  const [
    name,
    setName,
  ] = useState("");

  const [
    description,
    setDescription,
  ] = useState("");

  const [
    saving,
    setSaving,
  ] = useState(false);

  const [
    error,
    setError,
  ] = useState("");

  const [
    success,
    setSuccess,
  ] = useState("");


  async function handleSave() {
    const cleanName =
      name.trim();


    if (!cleanName) {
      setError(
        "Enter a scenario name."
      );

      return;
    }


    setSaving(true);
    setError("");
    setSuccess("");


    try {
      const scenario =
        await createScenario(
          {
            organization:
              organizationId,

            name:
              cleanName,

            simulation_type:
              simulationType,

            description:
              description.trim(),

            request_payload:
              requestPayload,
          },
        );


      await createScenarioRun(
        scenario.id,

        {
          label:
            "Initial saved run",

          status:
            "SUCCESS",

          request_payload:
            requestPayload,

          result_payload:
            resultPayload,

          metrics,
        },
      );


      setSuccess(
        (
          `Saved "${cleanName}" `
          + "with Run #1."
        )
      );

      setName("");
      setDescription("");

    } catch (caughtError) {
      setError(
        caughtError
          instanceof Error
          ? caughtError.message
          : (
              "Unable to save scenario."
            )
      );

    } finally {
      setSaving(false);
    }
  }


  return (
    <section className="panel scenario-save-panel">
      <h3>
        Save Simulation Scenario
      </h3>

      <p>
        Save this request and result so
        the same modeled scenario can
        be rerun and compared later.
      </p>

      <div className="form-grid">
        <label>
          Scenario Name

          <input
            value={
              name
            }

            onChange={(event) =>
              setName(
                event.target.value
              )
            }

            placeholder={
              "Example: Before MFA"
            }
          />
        </label>

        <label>
          Description

          <input
            value={
              description
            }

            onChange={(event) =>
              setDescription(
                event.target.value
              )
            }

            placeholder={
              (
                "Why are you saving "
                + "this scenario?"
              )
            }
          />
        </label>
      </div>

      <button
        type="button"

        onClick={
          handleSave
        }

        disabled={
          saving
        }
      >
        {
          saving
            ? "Saving..."
            : "Save Scenario"
        }
      </button>

      {error && (
        <div className="error-box">
          {error}
        </div>
      )}

      {success && (
        <div className="success-box">
          {success}
        </div>
      )}
    </section>
  );
}
