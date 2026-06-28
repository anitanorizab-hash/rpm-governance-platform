// App router (CP19/CP20A): public pages + protected /app shell.
// CP20A: /app/dashboard renders the real Dashboard; other modules keep the placeholder.
import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import { AuthProvider } from "./context/AuthContext";
import ProtectedRoute from "./routes/ProtectedRoute";
import Layout from "./components/Layout";
import Landing from "./pages/Landing";
import Login from "./pages/Login";
import Register from "./pages/Register";
import AppShell from "./pages/AppShell";
import Dashboard from "./pages/Dashboard";
import KpiManagement from "./pages/KpiManagement";
import KpiDetail from "./pages/KpiDetail";
import MonthlyUpdate from "./pages/MonthlyUpdate";
import FDS from "./pages/FDS";
import Reports from "./pages/Reports";
import ReportDetail from "./pages/ReportDetail";
import Notifications from "./pages/Notifications";
import Chatbot from "./pages/Chatbot";
import ExecutiveCopilot from "./pages/ExecutiveCopilot";
import AdminRoute from "./routes/AdminRoute";
import Admin from "./pages/Admin";
import AdminUsers from "./pages/AdminUsers";
import AdminPics from "./pages/AdminPics";
import AdminKnowledge from "./pages/AdminKnowledge";
import AdminAudit from "./pages/AdminAudit";
import AdminSystemHealth from "./pages/AdminSystemHealth";

export default function App() {
  return (
    <AuthProvider>
      <BrowserRouter future={{ v7_startTransition: true, v7_relativeSplatPath: true }}>
        <Routes>
          {/* Public */}
          <Route path="/" element={<Landing />} />
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />

          {/* Protected app shell */}
          <Route element={<ProtectedRoute />}>
            <Route path="/app" element={<Layout />}>
              <Route index element={<Navigate to="/app/dashboard" replace />} />
              <Route path="dashboard" element={<Dashboard />} />
              <Route path="kpis" element={<KpiManagement />} />
              <Route path="kpis/:id" element={<KpiDetail />} />
              <Route path="monthly-updates" element={<MonthlyUpdate />} />
              <Route path="fds" element={<FDS />} />
              <Route path="reports" element={<Reports />} />
              <Route path="reports/:id" element={<ReportDetail />} />
              <Route path="notifications" element={<Notifications />} />
              <Route path="chatbot" element={<Chatbot />} />
              <Route path="copilot" element={<ExecutiveCopilot />} />

              {/* Admin module — gated to super_admin / jpn_admin */}
              <Route path="admin" element={<AdminRoute />}>
                <Route index element={<Admin />} />
                <Route path="users" element={<AdminUsers />} />
                <Route path="pics" element={<AdminPics />} />
                <Route path="knowledge" element={<AdminKnowledge />} />
                <Route path="audit" element={<AdminAudit />} />
                <Route path="system" element={<AdminSystemHealth />} />
              </Route>

              <Route path=":module" element={<AppShell />} />
            </Route>
          </Route>

          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </BrowserRouter>
    </AuthProvider>
  );
}
