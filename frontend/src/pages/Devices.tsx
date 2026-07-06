import { useEffect, useState } from "react";
import { Plus, Search } from "lucide-react";

import AppLayout from "../layouts/AppLayout";
import DeviceFormModal from "../components/forms/DeviceFormModal";
import DeviceTable from "../components/tables/DeviceTable";
import { getDevices } from "../services/deviceApi";
import type { Device } from "../types/device";

export default function Devices() {
  const [devices, setDevices] = useState<Device[]>([]);
  const [search, setSearch] = useState("");
  const [loading, setLoading] = useState(true);
  const [modalOpen, setModalOpen] = useState(false);

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

  return (
    <AppLayout>
      <div className="flex items-center justify-between mb-6">
        <div>
          <h1 className="text-2xl font-bold">Device Inventory</h1>
          <p className="text-slate-500">Manage network devices, servers and security appliances</p>
        </div>

        <button
          onClick={() => setModalOpen(true)}
          className="flex items-center gap-2 bg-blue-600 hover:bg-blue-700 px-5 py-3 rounded-xl font-semibold"
        >
          <Plus size={18} />
          Add Device
        </button>
      </div>

      <div className="bg-slate-900 border border-slate-800 rounded-2xl p-5 mb-6">
        <div className="relative">
          <Search className="absolute left-4 top-3.5 text-slate-500" size={20} />
          <input
            className="w-full bg-slate-950 border border-slate-800 rounded-xl py-3 pl-12 pr-4 outline-none focus:border-blue-600"
            placeholder="Search by hostname, IP or vendor..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
          />
        </div>
      </div>

      {loading ? (
        <div className="bg-slate-900 border border-slate-800 rounded-2xl p-10 text-center text-slate-500">
          Loading devices...
        </div>
      ) : (
        <DeviceTable devices={filteredDevices} />
      )}

      <DeviceFormModal
        open={modalOpen}
        onClose={() => setModalOpen(false)}
        onCreated={(device) => setDevices((prev) => [device, ...prev])}
      />
    </AppLayout>
  );
}