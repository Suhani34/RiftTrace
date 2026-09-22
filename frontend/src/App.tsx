import {
  Route,
  Routes,
} from "react-router";

import Layout from "./components/Layout";

import AssetsPage from "./pages/AssetsPage";
import DashboardPage from "./pages/DashboardPage";
import OrganizationsPage from "./pages/OrganizationsPage";
import RelationshipsPage from "./pages/RelationshipsPage";


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
          path="assets"
          element={<AssetsPage />}
        />

        <Route
          path="relationships"
          element={<RelationshipsPage />}
        />

        <Route
          path="*"
          element={<NotFoundPage />}
        />
      </Route>
    </Routes>
  );
}
