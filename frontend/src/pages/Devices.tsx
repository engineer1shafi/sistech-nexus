import { useEffect, useState } from "react";
import { Plus, Search } from "lucide-react";

import AppLayout from "../layouts/AppLayout";
import DeviceFormModal from "../components/forms/DeviceFormModal";
import DeviceTable from "../components/tables/DeviceTable";
import { getDevices, runSNMPWalk, type SNMPWalkResponse } from "../services/deviceApi";
import type { Device } from "../types/device";
import PageHeader from "../components/ui/PageHeader";
import Button from "../components/ui/Button";
import Card from "../components/ui/Card";
import EmptyState from "../components/ui/EmptyState";
import LoadingState from "../components/ui/LoadingState";

export default function Devices() {
  const [devices, setDevices] = useState<Device[]>([]);
  const [search, setSearch] = useState("");
  const [loading, setLoading] = useState(true);
  const [modalOpen, setModalOpen] = useState(false);
  const [walkIp, setWalkIp] = useState("");
  const [walkOid, setWalkOid] = useState("1.3.6.1.2.1.2.2");
  const [walkResult, setWalkResult] = useState<SNMPWalkResponse | null>(null);
  const [walkLoading, setWalkLoading] = useState(false);

  useEffect(() => {
    getDevices()
      .then(setDevices)
      .finally(() => setLoading(false));
  }, []);

  const filteredDevices = devices.filter((device) => {
    const keyword = search.toLowerCase();

    return (
      device.hostname.toLowerCase().includes(keyword) ||
      device.ip_address.toLowerCase().includes(keyword) ||
      (device.vendor || "").toLowerCase().includes(keyword)
    );
  });

  const handleWalk = async () => {
    if (!walkIp || !walkOid) return;

    setWalkLoading(true);
    try {
      const response = await runSNMPWalk({
        ip_address: walkIp,
        oid: walkOid,
        community: "public",
        port: 161,
        timeout: 3,
        limit: 10,
      });
      setWalkResult(response);
    } finally {
      setWalkLoading(false);
    }
  };

  return (
    <AppLayout>
      <PageHeader
        title="Device Inventory"
        subtitle="Manage network devices, servers and security appliances"
        actions={<Button onClick={() => setModalOpen(true)}><Plus size={16} /> Add Device</Button>}
      />

      <Card>
        <div className="relative">
          <Search className="absolute left-4 top-3.5 text-slate-500" size={20} />
          <input
            className="w-full bg-slate-950 border border-slate-800 rounded-xl py-3 pl-12 pr-4 outline-none focus:border-blue-600"
            placeholder="Search by hostname, IP or vendor..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
          />
        </div>
      </Card>

      <Card title="SNMP Walk Engine" className="mt-6">
        <div className="grid gap-4 md:grid-cols-[1.2fr_1.2fr_auto]">
          <input
            className="bg-slate-950 border border-slate-800 rounded-xl px-4 py-3 outline-none focus:border-cyan-500"
            placeholder="Device IP"
            value={walkIp}
            onChange={(e) => setWalkIp(e.target.value)}
          />
          <input
            className="bg-slate-950 border border-slate-800 rounded-xl px-4 py-3 outline-none focus:border-cyan-500"
            placeholder="SNMP OID"
            value={walkOid}
            onChange={(e) => setWalkOid(e.target.value)}
          />
          <Button onClick={handleWalk} disabled={walkLoading} className="justify-center">{walkLoading ? "Running..." : "Run Walk"}</Button>
        </div>

        {walkResult && (
          <div className="mt-4 rounded-xl border border-slate-800 bg-slate-950 p-4">
            <div className="text-sm text-slate-400 mb-2">Result for {walkResult.ip_address}</div>
            {walkResult.error ? (
              <div className="text-red-400">{walkResult.error}</div>
            ) : (
              <ul className="space-y-2 text-sm text-slate-300">
                {walkResult.results.map((entry, index) => (
                  <li key={`${entry.oid}-${index}`} className="flex justify-between gap-4 rounded-lg bg-slate-900 px-3 py-2">
                    <span className="font-mono text-xs break-all">{entry.oid}</span>
                    <span className="text-slate-400 text-right">{entry.value ?? "-"}</span>
                  </li>
                ))}
              </ul>
            )}
          </div>
        )}
      </Card>

      <div className="mt-6">
        {loading ? (
          <Card>
            <LoadingState message="Loading devices..." />
          </Card>
        ) : filteredDevices.length === 0 ? (
          <Card>
            <EmptyState title="No devices" subtitle="Add devices using the Add Device button." />
          </Card>
        ) : (
          <DeviceTable devices={filteredDevices} />
        )}
      </div>

      <DeviceFormModal
        open={modalOpen}
        onClose={() => setModalOpen(false)}
        onCreated={(device) => setDevices((prev) => [device, ...prev])}
      />
    </AppLayout>
  );
}