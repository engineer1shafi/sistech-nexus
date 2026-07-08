import { useEffect, useState } from "react";
import AppLayout from "../layouts/AppLayout";
import { getTopologyLinks } from "../services/topologyApi";

export default function Topology() {
  const [topology, setTopology] = useState<{ nodes: any[]; links: any[] }>({ nodes: [], links: [] });
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    setLoading(true);
    getTopologyLinks()
      .then(setTopology)
      .finally(() => setLoading(false));
  }, []);

  return (
    <AppLayout>
      <div className="flex items-center justify-between mb-6">
        <div>
          <h1 className="text-2xl font-bold">Network Topology</h1>
          <p className="text-slate-500">Topology preview and link summary</p>
        </div>
      </div>

      <div className="grid gap-4 md:grid-cols-3 mb-6">
        <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6">
          <div className="text-slate-400 text-sm">Nodes</div>
          <div className="text-2xl font-semibold mt-2">{topology.nodes.length}</div>
        </div>
        <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6">
          <div className="text-slate-400 text-sm">Links</div>
          <div className="text-2xl font-semibold mt-2">{topology.links.length}</div>
        </div>
        <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6">
          <div className="text-slate-400 text-sm">Status</div>
          <div className="text-2xl font-semibold mt-2">Preview</div>
        </div>
      </div>

      <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6">
        {loading ? (
          <div className="text-slate-400">Loading topology...</div>
        ) : topology.links.length === 0 ? (
          <div className="text-center py-10 text-slate-400">No topology links found. Run discovery to populate the topology.</div>
        ) : (
          <div>
            <div className="text-slate-300">Topology preview container (React Flow ready)</div>
            <div className="mt-4 h-96 border border-slate-800 rounded-lg" />
          </div>
        )}
      </div>
    </AppLayout>
  );
}
