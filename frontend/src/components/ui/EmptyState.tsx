import React from "react";

type Props = {
  title?: string;
  subtitle?: string;
  icon?: React.ReactNode;
};

export default function EmptyState({ title = "No data", subtitle = "Nothing to show.", icon }: Props) {
  return (
    <div className="text-center py-12">
      <div className="mx-auto mb-4 h-20 w-20 rounded-2xl bg-slate-800 flex items-center justify-center">{icon}</div>
      <h3 className="text-lg font-semibold mt-4">{title}</h3>
      <p className="text-slate-500 mt-2">{subtitle}</p>
    </div>
  );
}
