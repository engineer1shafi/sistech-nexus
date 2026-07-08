import React from "react";

type Props = {
  children: React.ReactNode;
  className?: string;
  title?: string;
  footer?: React.ReactNode;
};

export default function Card({ children, className = "", title, footer }: Props) {
  return (
    <div className={`bg-slate-900 border border-slate-800 rounded-2xl p-6 ${className}`}>
      {title && (
        <div className="mb-4 flex items-center justify-between">
          <h3 className="text-lg font-semibold">{title}</h3>
        </div>
      )}
      <div>{children}</div>
      {footer && <div className="mt-4">{footer}</div>}
    </div>
  );
}
