import { useState } from "react";
import { api } from "../services/api";

export default function Login() {
  const [username, setUsername] = useState("admin");
  const [password, setPassword] = useState("Admin@12345");
  const [message, setMessage] = useState("");

  async function handleLogin() {
    try {
      const res = await api.post("/auth/login", {
        username,
        password,
      });

      localStorage.setItem("token", res.data.access_token);
      setMessage("Login successful");
      window.location.href = "/dashboard";
    } catch {
      setMessage("Login failed");
    }
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-slate-950">
      <div className="w-full max-w-md bg-slate-900 border border-slate-700 rounded-2xl p-8 shadow-xl">
        <h1 className="text-3xl font-bold text-white mb-2">SISTECH NEXUS</h1>
        <p className="text-slate-400 mb-6">Enterprise Network Operations Platform</p>

        <input
          className="w-full mb-4 px-4 py-3 rounded-lg bg-slate-800 border border-slate-700 text-white"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          placeholder="Username"
        />

        <input
          className="w-full mb-4 px-4 py-3 rounded-lg bg-slate-800 border border-slate-700 text-white"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          placeholder="Password"
          type="password"
        />

        <button
          onClick={handleLogin}
          className="w-full bg-blue-600 hover:bg-blue-700 py-3 rounded-lg font-semibold"
        >
          Login
        </button>

        {message && <p className="mt-4 text-sm text-slate-300">{message}</p>}
      </div>
    </div>
  );
}