// ShadCN-style Button (CP19).
import { cn } from "../../lib/utils";

const VARIANTS = {
  primary: "bg-blue-700 text-white hover:bg-blue-800",
  secondary: "bg-slate-100 text-slate-800 hover:bg-slate-200",
  ghost: "bg-transparent text-slate-700 hover:bg-slate-100",
  outline: "border border-slate-300 bg-white text-slate-700 hover:bg-slate-50",
  danger: "bg-red-600 text-white hover:bg-red-700",
};

export function Button({ variant = "primary", className, ...props }) {
  return (
    <button
      className={cn(
        "inline-flex items-center justify-center rounded-md px-4 py-2 text-sm font-medium",
        "transition-colors focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:opacity-50",
        VARIANTS[variant], className,
      )}
      {...props}
    />
  );
}
