// ShadCN-style Input + Label — premium restyle (V1.2).
import { cn } from "../../lib/utils";

export function Input({ className, ...props }) {
  return (
    <input
      className={cn(
        "w-full rounded-lg border border-slate-300 bg-white px-3 py-2 text-sm transition-colors",
        "focus:border-royal focus:outline-none focus:ring-2 focus:ring-royal/30", className,
      )}
      {...props}
    />
  );
}

export function Label({ className, ...props }) {
  return <label className={cn("mb-1 block text-sm font-medium text-slate-700", className)} {...props} />;
}
