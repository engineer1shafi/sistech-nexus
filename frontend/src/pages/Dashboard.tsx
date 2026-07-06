import { useEffect, useState } from "react";
import { Activity, Database, Router, ShieldAlert, Wifi } from "lucide-react";
import AppLayout from "../layouts/AppLayout";
import StatCard from "../components/StatCard";
import { api } from "../services/api";

export default function Dashboard() {
  const [health, setHealth] = useState<any>(null);

  useEffect(() => {
    api.get("/health")
      .then((res) => setHealth(res.data))
      .catch(() => setHealth({ status: "offline" }));
  }, []);

  return (
    <AppLayout>
      <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-5 gap-6">
        <StatCard title="Total Devices" value="0" subtitle="Inventory devices" icon={Router} />
        <StatCard title="Online" value="0" subtitle="Healthy devices" icon={Activity} />
        <StatCard title="Offline" value="0" subtitle="Unreachable devices" icon={Wifi} />
        <StatCard title="Critical Alerts" value="0" subtitle="Need attention" icon={ShieldAlert} />
        <StatCard title="Database" value={health?.status || "checking"} subtitle="Backend health" icon={Database} />
      </div>

      <div className="grid grid-cols-1 xl:grid-cols-3 gap-6 mt-8">
        <section className="xl:col-span-2 bg-slate-900 border border-slate-800 rounded-2xl p-6">
          <div className="flex items-center justify-between mb-5">
            <div>
              <h3 className="text-xl font-semibold">Live Network Topology</h3>
              <p className="text-sm text-slate-500">Digital twin preview</p>
            </div>
            <span className="px-3 py-1 rounded-full text-xs bg-blue-600/20 text-blue-300">
              Preview
            </span>
          </div>

          <div className="h-[420px] rounded-2xl bg-slate-950 border border-slate-800 relative overflow-hidden">
            <div className="absolute inset-0 opacity-20 bg-[radial-gradient(circle_at_center,_#38bdf8_1px,_transparent_1px)] [background-size:28px_28px]" />

            <div className="relative h-full flex items-center justify-center">
              <div className="text-center">
                <div className="mx-auto mb-6 h-20 w-20 rounded-2xl bg-blue-600/20 border border-blue-500/30 flex items-center justify-center">
                  <Router size={42} className="text-blue-400" />
                </div>
                <h4 className="text-2xl font-bold">Topology Canvas Coming Next</h4>
                <p className="text-slate-500 mt-2">
                  Router → Firewall → Core Switch → Access Switch → Server
                </p>
              </div>
            </div>
          </div>
        </section>

        <section className="bg-slate-900 border border-slate-800 rounded-2xl p-6">
          <h3 className="text-xl font-semibold mb-4">System Status</h3>
          <div className="bg-slate-950 rounded-xl p-4 border border-slate-800">
            <pre className="text-xs text-green-400 overflow-auto">
              {JSON.stringify(health, null, 2)}
            </pre>
          </div>

          <h3 className="text-xl font-semibold mt-8 mb-4">Recent Alarms</h3>
          <div className="space-y-3">
            {["No critical alarm", "SNMP engine ready", "Dashboard online"].map((item) => (
              <div key={item} className="p-4 rounded-xl bg-slate-950 border border-slate-800">
                <p className="text-sm text-slate-300">{item}</p>
                <p className="text-xs text-slate-600 mt-1">Just now</p>
              </div>
            ))}
          </div>
        </section>
      </div>
    </AppLayout>
  );
}