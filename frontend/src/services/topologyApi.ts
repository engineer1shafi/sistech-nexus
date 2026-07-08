import { api } from "./api";

export async function getTopologyLinks(): Promise<{ nodes: any[]; links: any[] }> {
  const response = await api.get("/topology/links");
  return response.data;
}

export async function getDeviceNeighbors(deviceId: string): Promise<any[]> {
  const response = await api.get(`/topology/devices/${deviceId}/neighbors`);
  return response.data;
}
