import {
  useEffect,
  useState,
} from "react";

import {
  listAttackMappingRules,
  listAttackTechniques,
} from "../api/attackMapping";

import type {
  AttackMappingRule,
  AttackTechnique,
} from "../types/attackMapping";


export default function AttackMappingPage() {
  const [
    techniques,
    setTechniques,
  ] = useState<
    AttackTechnique[]
  >([]);


  const [
    rules,
    setRules,
  ] = useState<
    AttackMappingRule[]
  >([]);


  const [
    error,
    setError,
  ] = useState("");


  useEffect(() => {
    let cancelled =
      false;


    async function load() {
      try {
        const [
          techniqueData,
          ruleData,
        ] = await Promise.all([
          listAttackTechniques(),

          listAttackMappingRules(),
        ]);


        if (cancelled) {
          return;
        }


        setTechniques(
          techniqueData
        );


        setRules(
          ruleData
        );
      } catch (
        caught
      ) {
        if (!cancelled) {
          setError(
            caught instanceof Error
              ? caught.message
              : (
                  "Unable to load "
                  + "ATT&CK mapping."
                ),
          );
        }
      }
    }


    void load();


    return () => {
      cancelled = true;
    };
  }, []);


  const version =
    techniques.length > 0
      ? techniques[0]
          .source_version
      : "—";


  return (
    <>
      <div className="page-heading">
        <div>
          <h2>
            MITRE ATT&CK Mapping
          </h2>

          <p>
            Explain modeled RiftTrace
            propagation events using a
            versioned ATT&CK knowledge
            layer.
          </p>
        </div>
      </div>


      {error && (
        <div className="error-box">
          {error}
        </div>
      )}


      <section className="panel attack-framework-summary">
        <div>
          <span>
            ATT&CK Release
          </span>

          <strong>
            v{version}
          </strong>
        </div>

        <div>
          <span>
            Curated Techniques
          </span>

          <strong>
            {techniques.length}
          </strong>
        </div>

        <div>
          <span>
            Mapping Rules
          </span>

          <strong>
            {rules.length}
          </strong>
        </div>
      </section>


      <section className="panel">
        <h3>
          Technique Catalog
        </h3>

        <p className="muted">
          These techniques are used as
          annotations for modeled
          simulation events. They do not
          indicate observed malicious
          activity.
        </p>


        <div className="attack-technique-grid">
          {techniques.map(
            (technique) => (
              <article
                key={
                  technique.attack_id
                }

                className="attack-technique-card"
              >
                <div className="attack-technique-heading">
                  <strong>
                    {
                      technique
                        .attack_id
                    }
                  </strong>

                  <span>
                    ATT&CK v
                    {
                      technique
                        .source_version
                    }
                  </span>
                </div>


                <h4>
                  {
                    technique.name
                  }
                </h4>


                <div className="attack-tactic-list">
                  {
                    technique
                      .tactics
                      .map(
                        (tactic) => (
                          <span
                            key={
                              tactic
                            }
                          >
                            {tactic}
                          </span>
                        ),
                      )
                  }
                </div>


                <a
                  href={
                    technique
                      .source_url
                  }

                  target="_blank"

                  rel="noreferrer"
                >
                  View official ATT&CK entry
                </a>
              </article>
            ),
          )}
        </div>
      </section>


      <section className="panel">
        <h3>
          RiftTrace Mapping Rules
        </h3>


        {rules.map(
          (rule) => (
            <article
              key={
                rule.rule_code
              }

              className="attack-rule-row"
            >
              <div>
                <strong>
                  {
                    rule.name
                  }
                </strong>

                <small>
                  {
                    rule.rule_code
                  }
                </small>
              </div>


              <div>
                <span>
                  Event
                </span>

                <strong>
                  {
                    rule.event_type
                  }
                </strong>
              </div>


              <div>
                <span>
                  ATT&CK
                </span>

                <strong>
                  {
                    rule
                      .technique_attack_id
                  }
                  {" — "}
                  {
                    rule
                      .technique_name
                  }
                </strong>
              </div>


              <div>
                <span>
                  Conditions
                </span>

                <code>
                  {
                    JSON.stringify(
                      rule.conditions
                    )
                  }
                </code>
              </div>


              <p>
                {
                  rule.rationale
                }
              </p>
            </article>
          ),
        )}
      </section>


      <section className="panel attack-disclaimer">
        <strong>
          Interpretation
        </strong>

        <p>
          ATT&CK annotations describe
          behavior that is consistent
          with a modeled RiftTrace event.
          They are not detections,
          incident evidence, or claims
          that an adversary performed
          the technique.
        </p>
      </section>
    </>
  );
}
