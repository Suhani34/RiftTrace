from scenarios.services import (
    compare_scenario_runs,
)


def build_experiment_comparison(
    experiment,
):
    return compare_scenario_runs(
        experiment.baseline_run,
        experiment.treatment_run,
    )


def build_evaluation_summary(
    experiments,
):
    experiments = list(
        experiments
    )


    metric_state = {}

    improved_observations = 0
    worsened_observations = 0
    unchanged_observations = 0
    metric_observation_count = 0


    for experiment in experiments:
        differences = (
            build_experiment_comparison(
                experiment
            )
        )


        for difference in differences:
            metric_observation_count += 1


            interpretation = (
                difference[
                    "interpretation"
                ]
            )


            if (
                interpretation
                == "IMPROVED"
            ):
                improved_observations += 1

            elif (
                interpretation
                == "WORSENED"
            ):
                worsened_observations += 1

            else:
                unchanged_observations += 1


            metric_key = (
                difference[
                    "metric"
                ]
            )


            if (
                metric_key
                not in metric_state
            ):
                metric_state[
                    metric_key
                ] = {
                    "metric":
                        metric_key,

                    "label":
                        difference[
                            "label"
                        ],

                    "observations":
                        0,

                    "before_sum":
                        0,

                    "after_sum":
                        0,

                    "reduction_sum":
                        0,

                    "improved":
                        0,

                    "worsened":
                        0,

                    "unchanged":
                        0,
                }


            state = (
                metric_state[
                    metric_key
                ]
            )


            state[
                "observations"
            ] += 1

            state[
                "before_sum"
            ] += difference[
                "before"
            ]

            state[
                "after_sum"
            ] += difference[
                "after"
            ]

            state[
                "reduction_sum"
            ] += difference[
                "reduction"
            ]


            if (
                interpretation
                == "IMPROVED"
            ):
                state[
                    "improved"
                ] += 1

            elif (
                interpretation
                == "WORSENED"
            ):
                state[
                    "worsened"
                ] += 1

            else:
                state[
                    "unchanged"
                ] += 1


    metric_summaries = []


    for metric_key in sorted(
        metric_state
    ):
        state = (
            metric_state[
                metric_key
            ]
        )


        observations = (
            state[
                "observations"
            ]
        )


        metric_summaries.append(
            {
                "metric":
                    state[
                        "metric"
                    ],

                "label":
                    state[
                        "label"
                    ],

                "observations":
                    observations,

                "mean_before":
                    round(
                        (
                            state[
                                "before_sum"
                            ]
                            / observations
                        ),
                        2,
                    ),

                "mean_after":
                    round(
                        (
                            state[
                                "after_sum"
                            ]
                            / observations
                        ),
                        2,
                    ),

                "mean_reduction":
                    round(
                        (
                            state[
                                "reduction_sum"
                            ]
                            / observations
                        ),
                        2,
                    ),

                "improved":
                    state[
                        "improved"
                    ],

                "worsened":
                    state[
                        "worsened"
                    ],

                "unchanged":
                    state[
                        "unchanged"
                    ],
            }
        )


    return {
        "experiment_count":
            len(
                experiments
            ),

        "metric_observation_count":
            metric_observation_count,

        "improved_observations":
            improved_observations,

        "worsened_observations":
            worsened_observations,

        "unchanged_observations":
            unchanged_observations,

        "metrics":
            metric_summaries,

        "disclaimer":
            (
                "These results describe "
                "differences between modeled "
                "simulation runs. They are "
                "descriptive model-evaluation "
                "results and do not establish "
                "real-world attack probability "
                "or guaranteed control efficacy."
            ),
    }


def build_evaluation_rows(
    experiments,
):
    rows = []


    for experiment in experiments:
        differences = (
            build_experiment_comparison(
                experiment
            )
        )


        for difference in differences:
            rows.append(
                {
                    "experiment_id":
                        experiment.id,

                    "experiment_name":
                        experiment.name,

                    "organization":
                        experiment
                        .organization
                        .name,

                    "scenario":
                        experiment
                        .scenario
                        .name,

                    "simulation_type":
                        experiment
                        .scenario
                        .simulation_type,

                    "intervention":
                        experiment
                        .intervention_label,

                    "baseline_run":
                        experiment
                        .baseline_run
                        .run_number,

                    "treatment_run":
                        experiment
                        .treatment_run
                        .run_number,

                    "metric":
                        difference[
                            "metric"
                        ],

                    "metric_label":
                        difference[
                            "label"
                        ],

                    "before":
                        difference[
                            "before"
                        ],

                    "after":
                        difference[
                            "after"
                        ],

                    "reduction":
                        difference[
                            "reduction"
                        ],

                    "interpretation":
                        difference[
                            "interpretation"
                        ],
                }
            )


    return rows
