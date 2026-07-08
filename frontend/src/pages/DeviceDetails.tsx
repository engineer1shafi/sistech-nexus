import { useEffect, useState } from "react";
import { useParams, Link } from "react-router-dom";
import AppLayout from "../layouts/AppLayout";
import DeviceInfoCard from "../components/device/DeviceInfoCard";
import InterfaceTable from "../components/device/InterfaceTable";
import DiscoveryButton from "../components/device/DiscoveryButton";
import { getDevice, getDeviceInterfaces, type InterfaceItem } from "../services/deviceApi";
import type { Device } from "../types/device";

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
      <div className="flex items-center justify-between mb-6">
        <div>
          <h1 className="text-2xl font-bold">Device Details</h1>
          <p className="text-slate-500">Device and interface details</p>
        </div>
        <Link to="/devices" className="text-sm text-slate-400 hover:underline">Back to devices</Link>
      </div>

      {loading || !device ? (
        <div className="bg-slate-900 border border-slate-800 rounded-2xl p-10 text-center text-slate-500">Loading device...</div>
      ) : (
        <div className="grid gap-6 lg:grid-cols-[1fr_2fr]">
          <div>
            <DeviceInfoCard device={device} />
            <div className="mt-4">
              <DiscoveryButton deviceId={device.id} onSuccess={loadInterfaces} />
            </div>
          </div>

          <div>
            <div className="flex items-center justify-between mb-4">
              <h2 className="text-lg font-semibold">Interfaces</h2>
              <div className="text-sm text-slate-400">{interfacesLoading ? "Refreshing..." : `${interfaces.length} interfaces`}</div>
            </div>

            <InterfaceTable interfaces={interfaces} />
          </div>
        </div>
      )}
    </AppLayout>
  );
}
