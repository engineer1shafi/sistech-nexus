import type { Device } from "../../types/device";

type Props = {
  device: Device;
};

export default function DeviceInfoCard({ device }: Props) {
  return (
    <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6">
      <h2 className="text-xl font-semibold">{device.hostname}</h2>
      <div className="text-slate-400 text-sm mt-1">{device.ip_address}</div>

      <div className="grid grid-cols-2 gap-4 mt-4 text-sm text-slate-300">
        <div>
          <div className="text-slate-500">Vendor</div>
          <div>{device.vendor ?? "-"}</div>
        </div>
        <div>
          <div className="text-slate-500">Model</div>
          <div>{device.model ?? "-"}</div>
        </div>
        <div>
          <div className="text-slate-500">SNMP</div>
          <div>{device.snmp_version ?? "-"}</div>
        </div>
        <div>
          <div className="text-slate-500">Port</div>
          <div>{device.snmp_port ?? "-"}</div>
        </div>
      </div>
    </div>
  );
}
