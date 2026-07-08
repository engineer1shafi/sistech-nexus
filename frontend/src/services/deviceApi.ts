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

export type SNMPWalkPayload = {
  ip_address: string;
  community?: string;
  port?: number;
  timeout?: number;
  oid: string;
  limit?: number | null;
};

export type SNMPWalkResult = {
  oid: string;
  value: string | null;
};

export type SNMPWalkResponse = {
  status: string;
  ip_address: string;
  oid: string;
  results: SNMPWalkResult[];
  error?: string | null;
};

export async function getDevices(): Promise<Device[]> {
  const response = await api.get<Device[]>("/devices");
  return response.data;
}

export async function createDevice(payload: CreateDevicePayload): Promise<Device> {
  const response = await api.post<Device>("/devices", payload);
  return response.data;
}

export async function runSNMPWalk(payload: SNMPWalkPayload): Promise<SNMPWalkResponse> {
  const response = await api.post<SNMPWalkResponse>("/snmp/walk", payload);
  return response.data;
}