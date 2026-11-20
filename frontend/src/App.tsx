import {
  Route,
  Routes,
} from "react-router";

import {
  ProtectedRoute,
} from "./auth/ProtectedRoute";

import Layout
  from "./components/Layout";

import PageState
  from "./components/PageState";

import AssetsPage
  from "./pages/AssetsPage";

import AttackMappingPage
  from "./pages/AttackMappingPage";

import BenchmarkingPage
  from "./pages/BenchmarkingPage";

import BusinessProcessesPage
  from "./pages/BusinessProcessesPage";

import ControlSimulationPage
  from "./pages/ControlSimulationPage";

import CounterfactualPage
  from "./pages/CounterfactualPage";

import DashboardPage
  from "./pages/DashboardPage";

import EvaluationPage
  from "./pages/EvaluationPage";

import IdentityGraphPage
  from "./pages/IdentityGraphPage";

import IdentityPropagationPage
  from "./pages/IdentityPropagationPage";

import IngestionPage
  from "./pages/IngestionPage";

import LoginPage
  from "./pages/LoginPage";

import NetworkZonesPage
  from "./pages/NetworkZonesPage";

import OrganizationsPage
  from "./pages/OrganizationsPage";

import PathIntelligencePage
  from "./pages/PathIntelligencePage";

import RelationshipsPage
  from "./pages/RelationshipsPage";

import RemediationRankingPage
  from "./pages/RemediationRankingPage";

import ReportsPage
  from "./pages/ReportsPage";

import ScenarioHistoryPage
  from "./pages/ScenarioHistoryPage";

import SecurityControlsPage
  from "./pages/SecurityControlsPage";

import TopologyPage
  from "./pages/TopologyPage";

import VulnerabilitiesPage
  from "./pages/VulnerabilitiesPage";


function NotFoundPage() {
  return (
    <PageState
      kind="empty"
      title="Page not found"
      message={
        (
          "The requested RiftTrace "
          + "page does not exist."
        )
      }
    />
  );
}


function ProtectedApplication() {
  return (
    <ProtectedRoute>
      <Layout />
    </ProtectedRoute>
  );
}


export default function App() {
  return (
    <Routes>
      <Route
        path="login"
        element={
          <LoginPage />
        }
      />


      <Route
        element={
          <ProtectedApplication />
        }
      >
        <Route
          index
          element={
            <DashboardPage />
          }
        />

        <Route
          path="organizations"
          element={
            <OrganizationsPage />
          }
        />

        <Route
          path="zones"
          element={
            <NetworkZonesPage />
          }
        />

        <Route
          path="assets"
          element={
            <AssetsPage />
          }
        />

        <Route
          path="identity-graph"
          element={
            <IdentityGraphPage />
          }
        />

        <Route
          path="identity-propagation"
          element={
            <IdentityPropagationPage />
          }
        />

        <Route
          path="remediation-ranking"
          element={
            <RemediationRankingPage />
          }
        />

        <Route
          path="relationships"
          element={
            <RelationshipsPage />
          }
        />

        <Route
          path="ingestion"
          element={
            <IngestionPage />
          }
        />

        <Route
          path="attack-mapping"
          element={
            <AttackMappingPage />
          }
        />

        <Route
          path="scenario-history"
          element={
            <ScenarioHistoryPage />
          }
        />

        <Route
          path="evaluation"
          element={
            <EvaluationPage />
          }
        />

        <Route
          path="benchmarking"
          element={
            <BenchmarkingPage />
          }
        />

        <Route
          path="reports"
          element={
            <ReportsPage />
          }
        />

        <Route
          path="vulnerabilities"
          element={
            <VulnerabilitiesPage />
          }
        />

        <Route
          path="topology"
          element={
            <TopologyPage />
          }
        />

        <Route
          path="business-processes"
          element={
            <BusinessProcessesPage />
          }
        />

        <Route
          path="counterfactual"
          element={
            <CounterfactualPage />
          }
        />

        <Route
          path="path-intelligence"
          element={
            <PathIntelligencePage />
          }
        />

        <Route
          path="security-controls"
          element={
            <SecurityControlsPage />
          }
        />

        <Route
          path="control-simulation"
          element={
            <ControlSimulationPage />
          }
        />

        <Route
          path="*"
          element={
            <NotFoundPage />
          }
        />
      </Route>
    </Routes>
  );
}
