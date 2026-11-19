import {
  StrictMode,
} from "react";

import {
  createRoot,
} from "react-dom/client";

import {
  BrowserRouter,
} from "react-router";

import {
  AuthProvider,
} from "./auth/AuthProvider";

import {
  AppErrorBoundary,
} from "./components/AppErrorBoundary";

import App from "./App.tsx";

import "@xyflow/react/dist/style.css";
import "./index.css";


createRoot(
  document.getElementById(
    "root"
  )!
).render(
  <StrictMode>
    <AppErrorBoundary>
      <BrowserRouter>
        <AuthProvider>
          <App />
        </AuthProvider>
      </BrowserRouter>
    </AppErrorBoundary>
  </StrictMode>,
);
