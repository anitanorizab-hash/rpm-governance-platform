// ShadCN-style Card — premium restyle (V1.2).
import { cn } from "../../lib/utils";

export function Card({ className, ...props }) {
  return <div className={cn("rounded-2xl border border-slate-200/70 bg-white shadow-card transition-shadow duration-300 hover:shadow-card-hover", className)} {...props} />;
}
export function CardHeader({ className, ...props }) {
  return <div className={cn("border-b border-slate-100 px-5 py-4", className)} {...props} />;
}
export function CardTitle({ className, ...props }) {
  return <h3 className={cn("font-display text-base font-semibold text-navy-700", className)} {...props} />;
}
export function CardContent({ className, ...props }) {
  return <div className={cn("px-5 py-4", className)} {...props} />;
}
