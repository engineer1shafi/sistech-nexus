import type { LucideIcon } from "lucide-react";

type Props = {
  title: string;
  value: string;
  subtitle: string;
  icon: LucideIcon;
};

export default function StatCard({ title, value, subtitle, icon: Icon }: Props) {
  return (
    <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6 shadow-lg">
      <div className="flex items-start justify-between">
        <div>
          <p className="text-slate-400 text-sm">{title}</p>
          <h3 className="text-4xl font-bold mt-3 text-white">{value}</h3>
          <p className="text-xs text-slate-500 mt-2">{subtitle}</p>
        </div>
        <div className="h-12 w-12 rounded-xl bg-blue-600/20 flex items-center justify-center">
          <Icon className="text-blue-400" size={26} />
        </div>
      </div>
    </div>
  );
}