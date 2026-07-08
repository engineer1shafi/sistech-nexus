import { useEffect, useState } from "react";
import { useParams, Link } from "react-router-dom";
import AppLayout from "../layouts/AppLayout";
import DeviceInfoCard from "../components/device/DeviceInfoCard";
import InterfaceTable from "../components/device/InterfaceTable";
import DiscoveryButton from "../components/device/DiscoveryButton";
import PollButton from "../components/device/PollButton";
import { getDevice, getDeviceInterfaces, type InterfaceItem } from "../services/deviceApi";
import type { Device } from "../types/device";
import PageHeader from "../components/ui/PageHeader";
import Card from "../components/ui/Card";
import EmptyState from "../components/ui/EmptyState";
import LoadingState from "../components/ui/LoadingState";

export default function DeviceDetails() {
  const { id } = useParams();
  const [device, setDevice] = useState<Device | null>(null);
  const [interfaces, setInterfaces] = useState<InterfaceItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [interfacesLoading, setInterfacesLoading] = useState(false);

  useEffect(() => {
    if (!id) return;
    setLoading(true);
    getDevice(id)
      .then(setDevice)
      .finally(() => setLoading(false));
  }, [id]);

  const loadInterfaces = async () => {
    if (!id) return;
    setInterfacesLoading(true);
    try {
      const resp = await getDeviceInterfaces(id);
      setInterfaces(resp);
    } finally {
      setInterfacesLoading(false);
    }
  };

  useEffect(() => {
    loadInterfaces();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [id]);

  return (
    <AppLayout>
      <PageHeader title="Device Details" subtitle="Device and interface details" actions={<Link to="/devices" className="text-sm text-slate-400 hover:underline">Back to devices</Link>} />

      {loading || !device ? (
        <Card>
          <LoadingState message="Loading device..." />
        </Card>
      ) : (
        <div className="grid gap-6 lg:grid-cols-[1fr_2fr]">
          <div>
            <DeviceInfoCard device={device} />
            <div className="mt-4 flex items-center gap-3">
              <DiscoveryButton deviceId={device.id} onSuccess={loadInterfaces} />
              <PollButton deviceId={device.id} onSuccess={() => { loadInterfaces(); /* refresh device */ getDevice(id!).then(setDevice).catch(()=>{}); }} />
            </div>
          </div>

          <div>
            <Card title={`Interfaces (${interfaces.length})`}>
              {interfacesLoading ? (
                <LoadingState message="Refreshing interfaces..." />
              ) : interfaces.length === 0 ? (
                <EmptyState title="No interfaces found" subtitle="Run discovery to populate interfaces." />
              ) : (
                <InterfaceTable interfaces={interfaces} />
              )}
            </Card>
          </div>
        </div>
      )}
    </AppLayout>
  );
}
