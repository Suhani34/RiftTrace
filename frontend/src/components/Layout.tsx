import {
  useEffect,
  useState,
} from "react";

import {
  NavLink,
  Outlet,
} from "react-router";

import SessionControls
  from "./SessionControls";


interface NavigationItem {
  label: string;

  to: string;

  end?: boolean;
}


interface NavigationGroup {
  label: string;

  items: NavigationItem[];
}


const navigationGroups:
  NavigationGroup[] = [
    {
      label:
        "Overview",

      items: [
        {
          label:
            "Dashboard",

          to:
            "/",

          end:
            true,
        },
      ],
    },

    {
      label:
        "Environment",

      items: [
        {
          label:
            "Organizations",

          to:
            "/organizations",
        },

        {
          label:
            "Network Zones",

          to:
            "/zones",
        },

        {
          label:
            "Assets",

          to:
            "/assets",
        },

        {
          label:
            "Relationships",

          to:
            "/relationships",
        },

        {
          label:
            "Topology",

          to:
            "/topology",
        },

        {
          label:
            "Environment Ingestion",

          to:
            "/ingestion",
        },

        {
          label:
            "Reports",

          to:
            "/reports",
        },
      ],
    },

    {
      label:
        "Risk & Simulation",

      items: [
        {
          label:
            "Vulnerabilities",

          to:
            "/vulnerabilities",
        },

        {
          label:
            "Business Processes",

          to:
            "/business-processes",
        },

        {
          label:
            "Counterfactual",

          to:
            "/counterfactual",
        },

        {
          label:
            "Security Controls",

          to:
            "/security-controls",
        },

        {
          label:
            "Control Simulation",

          to:
            "/control-simulation",
        },

        {
          label:
            "Remediation Ranking",

          to:
            "/remediation-ranking",
        },

        {
          label:
            "Path Intelligence",

          to:
            "/path-intelligence",
        },
      ],
    },

    {
      label:
        "Identity & Mapping",

      items: [
        {
          label:
            "Identity Graph",

          to:
            "/identity-graph",
        },

        {
          label:
            "Identity Propagation",

          to:
            "/identity-propagation",
        },

        {
          label:
            "ATT&CK Mapping",

          to:
            "/attack-mapping",
        },
      ],
    },

    {
      label:
        "Research & Validation",

      items: [
        {
          label:
            "Scenario History",

          to:
            "/scenario-history",
        },

        {
          label:
            "Evaluation",

          to:
            "/evaluation",
        },

        {
          label:
            "Benchmarking",

          to:
            "/benchmarking",
        },
      ],
    },
  ];


export default function Layout() {
  const [
    menuOpen,
    setMenuOpen,
  ] = useState(false);

  useEffect(
    () => {
      function handleKeyDown(
        event: KeyboardEvent,
      ) {
        if (
          event.key
          === "Escape"
        ) {
          setMenuOpen(false);
        }
      }


      window.addEventListener(
        "keydown",
        handleKeyDown,
      );


      return () => {
        window.removeEventListener(
          "keydown",
          handleKeyDown,
        );
      };
    },
    [],
  );

  function closeMenu() {
    setMenuOpen(false);
  }


  return (
    <div
      className="app-shell"
    >
      <header
        className="app-topbar"
      >
        <div
          className="app-topbar__identity"
        >
          <button
            type="button"
            className="menu-button"
            aria-label={
              menuOpen
                ? "Close navigation menu"
                : "Open navigation menu"
            }
            aria-expanded={
              menuOpen
            }
            aria-controls={
              "rifttrace-navigation"
            }
            onClick={
              () => {
                setMenuOpen(
                  (current) =>
                    !current
                );
              }
            }
          >
            <span
              className="menu-icon"
              aria-hidden="true"
            >
              <span />

              <span />

              <span />
            </span>
          </button>


          <NavLink
            to="/"
            className="app-brand"
          >
            RiftTrace
          </NavLink>
        </div>


        <SessionControls />
      </header>


      {
        menuOpen
        && (
          <>
            <button
              type="button"
              className="navigation-backdrop"
              aria-label={
                "Close navigation menu"
              }
              onClick={
                closeMenu
              }
            />


            <aside
              id="rifttrace-navigation"
              className="navigation-drawer"
              aria-label={
                "RiftTrace navigation"
              }
            >
              <header
                className="navigation-drawer__header"
              >
                <div>
                  <strong>
                    RiftTrace
                  </strong>

                  <p>
                    Navigation
                  </p>
                </div>


                <button
                  type="button"
                  className={
                    "navigation-drawer__close"
                  }
                  aria-label={
                    "Close navigation menu"
                  }
                  onClick={
                    closeMenu
                  }
                >
                  ×
                </button>
              </header>


              <nav
                className="navigation-menu"
                aria-label={
                  "RiftTrace sections"
                }
              >
                {
                  navigationGroups.map(
                    (
                      group
                    ) => (
                      <section
                        key={
                          group.label
                        }
                        className={
                          "navigation-group"
                        }
                      >
                        <h2
                          className={
                            "navigation-group__title"
                          }
                        >
                          {group.label}
                        </h2>


                        <ul
                          className={
                            "navigation-group__list"
                          }
                        >
                          {
                            group.items.map(
                              (
                                item
                              ) => (
                                <li
                                  key={
                                    item.to
                                  }
                                >
                                  <NavLink
                                    to={
                                      item.to
                                    }
                                    end={
                                      item.end
                                    }
                                    onClick={
                                      closeMenu
                                    }
                                    className={
                                      (
                                        {
                                          isActive,
                                        },
                                      ) => (
                                        isActive
                                          ? (
                                            "navigation-link "
                                            + "navigation-link--active"
                                          )
                                          : "navigation-link"
                                      )
                                    }
                                  >
                                    {
                                      item.label
                                    }
                                  </NavLink>
                                </li>
                              ),
                            )
                          }
                        </ul>
                      </section>
                    ),
                  )
                }
              </nav>
            </aside>
          </>
        )
      }


      <main
        className="app-content"
      >
        <Outlet />
      </main>
    </div>
  );
}
