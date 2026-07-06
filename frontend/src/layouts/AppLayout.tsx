import {
  Activity,
  Bell,
  LayoutDashboard,
  Network,
  Router,
  Settings,
  ShieldAlert,
} from "lucide-react";
import { NavLink } from "react-router-dom";

type Props = {
  children: React.ReactNode;
};

const menu = [
  { name: "Dashboard", path: "/dashboard", icon: LayoutDashboard },
  { name: "Devices", path: "/devices", icon: Router },
  { name: "Topology", path: "/topology", icon: Network },
  { name: "Alerts", path: "/alerts", icon: ShieldAlert },
  { name: "Monitoring", path: "/monitoring", icon: Activity },
  { name: "Settings", path: "/settings", icon: Settings },
];

export default function AppLayout({ children }: Props) {
  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 flex">
      <aside className="w-72 border-r border-slate-800 bg-slate-950/90 p-5 hidden lg:block">
        <div className="mb-10">
          <h1 className="text-2xl font-bold tracking-wide">SISTECH</h1>
          <p className="text-blue-400 font-semibold">NEXUS</p>
          <p className="text-xs text-slate-500 mt-2">
            Enterprise Network Operations Platform
          </p>
        </div>

        <nav className="space-y-2">
          {menu.map((item) => {
            const Icon = item.icon;

            return (
              <NavLink
                key={item.name}
                to={item.path}
                className={({ isActive }) =>
                  `w-full flex items-center gap-3 px-4 py-3 rounded-xl transition ${
                    isActive
                      ? "bg-blue-600 text-white shadow-lg shadow-blue-900/30"
                      : "text-slate-300 hover:bg-slate-800 hover:text-white"
                  }`
                }
              >
                <Icon size={20} />
                <span>{item.name}</span>
              </NavLink>
            );
          })}
        </nav>
      </aside>

      <main className="flex-1">
        <header className="h-20 border-b border-slate-800 bg-slate-950/80 flex items-center justify-between px-8">
          <div>
            <h2 className="text-xl font-semibold">SISTECH NEXUS</h2>
            <p className="text-sm text-slate-500">Live NOC Operations Console</p>
          </div>

          <div className="flex items-center gap-4">
            <button className="relative p-3 rounded-xl bg-slate-900 border border-slate-800">
              <Bell size={20} />
              <span className="absolute -top-1 -right-1 h-3 w-3 bg-red-500 rounded-full" />
            </button>

            <div className="text-right">
              <p className="font-medium">Admin</p>
              <p className="text-xs text-slate-500">Super Admin</p>
            </div>

            <div className="h-11 w-11 rounded-xl bg-blue-600 flex items-center justify-center font-bold">
              A
            </div>
          </div>
        </header>

        <div className="p-8">{children}</div>
      </main>
    </div>
  );
}