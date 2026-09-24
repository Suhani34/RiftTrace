import {
  NavLink,
  Outlet,
} from "react-router";


export default function Layout() {
  return (
    <div className="app-shell">
      <header className="topbar">
        <div>
          <h1>RiftTrace</h1>

          <p>
            Cyber Risk Simulation Platform
          </p>
        </div>
      </header>

      <nav className="main-nav">
        <NavLink to="/">
          Dashboard
        </NavLink>

        <NavLink to="/zones">
          Network Zones
        </NavLink>

        <NavLink to="/organizations">
          Organizations
        </NavLink>

        <NavLink to="/assets">
          Assets
        </NavLink>

        <NavLink to="/relationships">
          Relationships
        </NavLink>
      </nav>

      <main className="page-container">
        <Outlet />
      </main>
    </div>
  );
}
