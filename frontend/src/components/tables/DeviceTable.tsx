import { MoreHorizontal } from "lucide-react";
import StatusBadge from "../badges/StatusBadge";
import type { Device } from "../../types/device";

type Props = {
  devices: Device[];
};

export default function DeviceTable({ devices }: Props) {
  return (
    <div className="overflow-hidden rounded-2xl border border-slate-800 bg-slate-900 shadow-xl">
      <table className="w-full text-left">
        <thead className="bg-slate-950 text-slate-400 text-sm">
          <tr>
            <th className="px-6 py-4">Hostname</th>
            <th className="px-6 py-4">IP Address</th>
            <th className="px-6 py-4">Vendor</th>
            <th className="px-6 py-4">Model</th>
            <th className="px-6 py-4">Status</th>
            <th className="px-6 py-4">Enabled</th>
            <th className="px-6 py-4 text-right">Action</th>
          </tr>
        </thead>

        <tbody>
          {devices.length === 0 ? (
            <tr>
              <td colSpan={7} className="px-6 py-16 text-center">
                <div className="text-slate-400 font-medium">No devices found</div>
                <div className="text-slate-600 text-sm mt-1">
                  Add your first router, switch, firewall or server.
                </div>
              </td>
            </tr>
          ) : (
            devices.map((device) => (
              <tr
                key={device.id}
                className="border-t border-slate-800 hover:bg-slate-800/40 transition"
              >
                <td className="px-6 py-4">
                  <div className="font-medium text-white">{device.hostname}</div>
                  <div className="text-xs text-slate-500">{device.device_type || "Network Device"}</div>
                </td>
                <td className="px-6 py-4 text-slate-300 font-mono">{device.ip_address}</td>
                <td className="px-6 py-4 text-slate-300">{device.vendor || "-"}</td>
                <td className="px-6 py-4 text-slate-300">{device.model || "-"}</td>
                <td className="px-6 py-4">
                  <StatusBadge status={device.status} />
                </td>
                <td className="px-6 py-4 text-slate-300">
                  {device.is_enabled ? "Yes" : "No"}
                </td>
                <td className="px-6 py-4 text-right">
                  <button className="p-2 rounded-lg hover:bg-slate-700">
                    <MoreHorizontal size={20} />
                  </button>
                </td>
              </tr>
            ))
          )}
        </tbody>
      </table>
    </div>
  );
}