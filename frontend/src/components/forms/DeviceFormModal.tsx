import { X } from "lucide-react";
import { useState } from "react";
import { createDevice } from "../../services/deviceApi";
import type { Device } from "../../types/device";

type Props = {
  open: boolean;
  onClose: () => void;
  onCreated: (device: Device) => void;
};

export default function DeviceFormModal({ open, onClose, onCreated }: Props) {
  const [form, setForm] = useState({
    organization_id: "",
    hostname: "",
    ip_address: "",
    vendor: "Huawei",
    model: "",
    serial_number: "",
    device_type: "Switch",
    snmp_version: "v2c",
    snmp_port: 161,
  });

  const [saving, setSaving] = useState(false);
  const [message, setMessage] = useState("");

  if (!open) return null;

  function updateField(key: string, value: string | number) {
    setForm((prev) => ({ ...prev, [key]: value }));
  }

  async function handleSubmit() {
    setSaving(true);
    setMessage("");

    try {
      const created = await createDevice(form);
      onCreated(created);
      setMessage("Device created successfully");
      onClose();
    } catch (error: any) {
      setMessage(error?.response?.data?.detail || "Failed to create device");
    } finally {
      setSaving(false);
    }
  }

  return (
    <div className="fixed inset-0 z-50 bg-black/70 flex items-center justify-center p-6">
      <div className="w-full max-w-3xl bg-slate-900 border border-slate-800 rounded-2xl shadow-2xl">
        <div className="flex items-center justify-between px-6 py-5 border-b border-slate-800">
          <div>
            <h2 className="text-xl font-bold">Add Device</h2>
            <p className="text-sm text-slate-500">Register a network device into inventory</p>
          </div>

          <button onClick={onClose} className="p-2 rounded-lg hover:bg-slate-800">
            <X size={22} />
          </button>
        </div>

        <div className="p-6 grid grid-cols-1 md:grid-cols-2 gap-4">
          <Input label="Organization ID" value={form.organization_id} onChange={(v) => updateField("organization_id", v)} />
          <Input label="Hostname" value={form.hostname} onChange={(v) => updateField("hostname", v)} />
          <Input label="IP Address" value={form.ip_address} onChange={(v) => updateField("ip_address", v)} />
          <Input label="Vendor" value={form.vendor} onChange={(v) => updateField("vendor", v)} />
          <Input label="Model" value={form.model} onChange={(v) => updateField("model", v)} />
          <Input label="Serial Number" value={form.serial_number} onChange={(v) => updateField("serial_number", v)} />
          <Input label="Device Type" value={form.device_type} onChange={(v) => updateField("device_type", v)} />
          <Input label="SNMP Version" value={form.snmp_version} onChange={(v) => updateField("snmp_version", v)} />
          <Input
            label="SNMP Port"
            value={String(form.snmp_port)}
            onChange={(v) => updateField("snmp_port", Number(v))}
          />
        </div>

        {message && (
          <div className="px-6 pb-2 text-sm text-yellow-400">
            {message}
          </div>
        )}

        <div className="flex items-center justify-end gap-3 px-6 py-5 border-t border-slate-800">
          <button onClick={onClose} className="px-5 py-3 rounded-xl bg-slate-800 hover:bg-slate-700">
            Cancel
          </button>
          <button
            onClick={handleSubmit}
            disabled={saving}
            className="px-5 py-3 rounded-xl bg-blue-600 hover:bg-blue-700 disabled:opacity-50 font-semibold"
          >
            {saving ? "Saving..." : "Save Device"}
          </button>
        </div>
      </div>
    </div>
  );
}

function Input({
  label,
  value,
  onChange,
}: {
  label: string;
  value: string;
  onChange: (value: string) => void;
}) {
  return (
    <label className="block">
      <span className="text-sm text-slate-400">{label}</span>
      <input
        className="mt-2 w-full bg-slate-950 border border-slate-800 rounded-xl px-4 py-3 outline-none focus:border-blue-600"
        value={value}
        onChange={(e) => onChange(e.target.value)}
      />
    </label>
  );
}