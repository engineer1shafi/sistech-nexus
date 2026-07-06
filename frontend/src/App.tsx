import { BrowserRouter, Navigate, Route, Routes } from "react-router-dom";

import Dashboard from "./pages/Dashboard";
import Devices from "./pages/Devices";
import Login from "./pages/Login";

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Navigate to="/login" replace />} />
        <Route path="/login" element={<Login />} />
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/devices" element={<Devices />} />
      </Routes>
    </BrowserRouter>
  );
}