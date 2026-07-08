import type { InterfaceItem } from "../../services/deviceApi";

type Props = {
  interfaces: InterfaceItem[];
};

export default function InterfaceTable({ interfaces }: Props) {
  return (
    <div className="overflow-hidden rounded-2xl border border-slate-800 bg-slate-900 shadow-xl">
      <table className="w-full text-left">
        <thead className="bg-slate-950 text-slate-400 text-sm">
          <tr>
            <th className="px-6 py-3">Name</th>
            <th className="px-6 py-3">Description</th>
            <th className="px-6 py-3">Admin Status</th>
            <th className="px-6 py-3">Oper Status</th>
            <th className="px-6 py-3">Speed</th>
            <th className="px-6 py-3">MTU</th>
            <th className="px-6 py-3">MAC Address</th>
          </tr>
        </thead>

        <tbody>
          {interfaces.length === 0 ? (
            <tr>
              <td colSpan={7} className="px-6 py-16 text-center">
                <div className="text-slate-400 font-medium">No interfaces found</div>
                <div className="text-slate-600 text-sm mt-1">Run discovery to populate interfaces.</div>
              </td>
            </tr>
          ) : (
            interfaces.map((it) => (
              <tr key={it.id} className="border-t border-slate-800 hover:bg-slate-800/40 transition">
                <td className="px-6 py-4 font-medium text-white">{it.if_name ?? `if${it.if_index}`}</td>
                <td className="px-6 py-4 text-slate-300">{it.if_descr ?? it.if_alias ?? "-"}</td>
                <td className="px-6 py-4 text-slate-300">{it.admin_status ?? "-"}</td>
                <td className="px-6 py-4 text-slate-300">{it.oper_status ?? "-"}</td>
                <td className="px-6 py-4 text-slate-300">{it.speed ?? "-"}</td>
                <td className="px-6 py-4 text-slate-300">{it.mtu ?? "-"}</td>
                <td className="px-6 py-4 text-slate-300 font-mono">{it.mac_address ?? "-"}</td>
              </tr>
            ))
          )}
        </tbody>
      </table>
    </div>
  );
}
