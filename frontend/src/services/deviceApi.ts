import { api } from "./api";
import type { Device } from "../types/device";

export type CreateDevicePayload = {
  organization_id: string;
  hostname: string;
  ip_address: string;
  vendor: string;
  model?: string;
  serial_number?: string;
  device_type: string;
  snmp_version: string;
  snmp_port: number;
};

export async function getDevices(): Promise<Device[]> {
  const response = await api.get<Device[]>("/devices");
  return response.data;
}

export async function createDevice(payload: CreateDevicePayload): Promise<Device> {
  const response = await api.post<Device>("/devices", payload);
  return response.data;
}