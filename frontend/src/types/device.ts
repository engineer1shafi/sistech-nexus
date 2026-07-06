export type DeviceStatus = "online" | "offline" | "unknown" | "warning";

export type Device = {
  id: string;
  organization_id: string;
  hostname: string;
  ip_address: string;
  vendor?: string | null;
  model?: string | null;
  serial_number?: string | null;
  device_type?: string | null;
  snmp_version?: string | null;
  snmp_port?: number | null;
  status?: DeviceStatus | string;
  is_enabled?: boolean;
};