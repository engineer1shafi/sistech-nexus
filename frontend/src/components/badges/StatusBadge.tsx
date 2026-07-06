type Props = {
  status?: string | null;
};

export default function StatusBadge({ status }: Props) {
  const value = status || "unknown";

  const styleMap: Record<string, string> = {
    online: "bg-green-500/10 text-green-400 border-green-500/30",
    offline: "bg-red-500/10 text-red-400 border-red-500/30",
    warning: "bg-yellow-500/10 text-yellow-400 border-yellow-500/30",
    unknown: "bg-slate-500/10 text-slate-400 border-slate-500/30",
  };

  const className = styleMap[value] || styleMap.unknown;

  return (
    <span className={`px-3 py-1 rounded-full text-xs border ${className}`}>
      {value.toUpperCase()}
    </span>
  );
}