import { useEffect, useState } from "react";
import AppLayout from "../layouts/AppLayout";
import { getTopologyLinks } from "../services/topologyApi";
import Card from "../components/ui/Card";
import PageHeader from "../components/ui/PageHeader";
import EmptyState from "../components/ui/EmptyState";
import LoadingState from "../components/ui/LoadingState";

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
      <PageHeader title="Network Topology" subtitle="Topology preview and link summary" />

      <div className="grid gap-4 md:grid-cols-3 mb-6">
        <Card>
          <div className="text-slate-400 text-sm">Nodes</div>
          <div className="text-2xl font-semibold mt-2">{topology.nodes.length}</div>
        </Card>
        <Card>
          <div className="text-slate-400 text-sm">Links</div>
          <div className="text-2xl font-semibold mt-2">{topology.links.length}</div>
        </Card>
        <Card>
          <div className="text-slate-400 text-sm">Status</div>
          <div className="text-2xl font-semibold mt-2">Preview</div>
        </Card>
      </div>

      <Card>
        {loading ? (
          <LoadingState message="Loading topology..." />
        ) : topology.links.length === 0 ? (
          <EmptyState title="No topology data" subtitle="Run LLDP discovery to populate topology." />
        ) : (
          <div>
            <div className="text-slate-300">Topology preview container (React Flow ready)</div>
            <div className="mt-4 h-96 border border-slate-800 rounded-lg" />
          </div>
        )}
      </Card>
    </AppLayout>
  );
}
