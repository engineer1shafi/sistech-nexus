import React from "react";

type ButtonProps = React.ButtonHTMLAttributes<HTMLButtonElement> & {
  variant?: "primary" | "secondary" | "ghost";
};

export default function Button({ variant = "primary", className = "", ...props }: ButtonProps) {
  const base = "inline-flex items-center gap-2 rounded-xl px-4 py-2 font-semibold focus:outline-none";
  const styles =
    variant === "secondary"
      ? "bg-slate-800 border border-slate-700 text-slate-100 hover:bg-slate-700"
      : variant === "ghost"
      ? "bg-transparent text-slate-100 hover:bg-slate-800"
      : "bg-blue-600 hover:bg-blue-700 text-white";

  return <button className={`${base} ${styles} ${className}`} {...props} />;
}
