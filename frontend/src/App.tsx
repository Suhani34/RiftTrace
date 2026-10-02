import {
  Route,
  Routes,
} from "react-router";

import Layout from "./components/Layout";

import AssetsPage from "./pages/AssetsPage";
import DashboardPage from "./pages/DashboardPage";
import OrganizationsPage from "./pages/OrganizationsPage";
import RelationshipsPage from "./pages/RelationshipsPage";
import TopologyPage from "./pages/TopologyPage";
import NetworkZonesPage from "./pages/NetworkZonesPage";
import VulnerabilitiesPage
  from "./pages/VulnerabilitiesPage";
import BusinessProcessesPage
  from "./pages/BusinessProcessesPage";

function NotFoundPage() {
  return (
    <section className="panel">
      <h2>Page not found</h2>

      <p>
        The requested RiftTrace page
        does not exist.
      </p>
    </section>
  );
}


export default function App() {
  return (
    <Routes>
      <Route element={<Layout />}>
        <Route
          index
          element={<DashboardPage />}
        />

        <Route
          path="organizations"
          element={<OrganizationsPage />}
        />

	<Route
          path="zones"
          element={<NetworkZonesPage />}
        />

        <Route
          path="assets"
          element={<AssetsPage />}
        />

	<Route
	  path="business-processes"
	  element={
	    <BusinessProcessesPage />
	  }
	/>

        <Route
          path="relationships"
          element={<RelationshipsPage />}
        />

	<Route
	  path="vulnerabilities"
	  element={
	    <VulnerabilitiesPage />
	  }
	/>

	<Route
	  path="topology"
	  element={<TopologyPage />}
	/>

        <Route
          path="*"
          element={<NotFoundPage />}
        />
      </Route>
    </Routes>
  );
}
