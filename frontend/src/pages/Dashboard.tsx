import { useEffect, useState } from "react";
import { Activity, Database, Router, ShieldAlert } from "lucide-react";
import { api } from "../services/api";

export default function Dashboard() {
  const [health, setHealth] = useState<any>(null);

  useEffect(() => {
    api.get("/health").then((res) => setHealth(res.data)).catch(() => {
      setHealth({ status: "offline" });
    });
  }, []);

  const cards = [
    { title: "Total Devices", value: "0", icon: Router },
    { title: "Online", value: "0", icon: Activity },
    { title: "Alarms", value: "0", icon: ShieldAlert },
    { title: "Database", value: health?.status || "checking", icon: Database },
  ];

  return (
    <div className="min-h-screen bg-slate-950">
      <div className="border-b border-slate-800 px-8 py-5">
        <h1 className="text-2xl font-bold text-white">SISTECH NEXUS</h1>
        <p className="text-slate-400">NOC Dashboard</p>
      </div>

      <div className="p-8 grid grid-cols-1 md:grid-cols-4 gap-6">
        {cards.map((card) => {
          const Icon = card.icon;
          return (
            <div key={card.title} className="bg-slate-900 border border-slate-800 rounded-2xl p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-slate-400 text-sm">{card.title}</p>
                  <h2 className="text-3xl font-bold text-white mt-2">{card.value}</h2>
                </div>
                <Icon className="text-blue-500" size={36} />
              </div>
            </div>
          );
        })}
      </div>

      <div className="px-8 grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6">
          <h2 className="text-xl font-semibold mb-4">Network Topology Preview</h2>
          <div className="h-72 flex items-center justify-center text-slate-500 border border-dashed border-slate-700 rounded-xl">
            Live Topology Canvas Coming Next
          </div>
        </div>

        <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6">
          <h2 className="text-xl font-semibold mb-4">System Status</h2>
          <pre className="text-sm text-green-400 bg-slate-950 p-4 rounded-xl overflow-auto">
            {JSON.stringify(health, null, 2)}
          </pre>
        </div>
      </div>
    </div>
  );
}