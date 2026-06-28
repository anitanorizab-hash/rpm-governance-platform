// ShadCN-style Button — premium restyle (V1.2). Variant names unchanged; new "gold" added.
// Ripple is purely presentational and does not alter the onClick contract.
import { useRef } from "react";
import { cn } from "../../lib/utils";

const VARIANTS = {
  primary: "bg-royal-600 text-white hover:bg-royal-700 shadow-sm shadow-royal-600/30",
  secondary: "bg-slate-100 text-navy-700 hover:bg-slate-200",
  ghost: "bg-transparent text-navy-700 hover:bg-slate-100",
  outline: "border border-slate-300 bg-white text-navy-700 hover:bg-slate-50",
  danger: "bg-danger text-white hover:bg-red-700",
  gold: "bg-gold-500 font-semibold text-navy-800 hover:bg-gold-600 shadow-sm shadow-gold-500/30",
};

export function Button({ variant = "primary", className, onClick, children, ...props }) {
  const ref = useRef(null);
  function handleClick(e) {
    const btn = ref.current;
    if (btn) {
      const d = Math.max(btn.clientWidth, btn.clientHeight);
      const rect = btn.getBoundingClientRect();
      const circle = document.createElement("span");
      circle.style.width = circle.style.height = `${d}px`;
      circle.style.left = `${e.clientX - rect.left - d / 2}px`;
      circle.style.top = `${e.clientY - rect.top - d / 2}px`;
      circle.className = "ripple-el pointer-events-none absolute rounded-full bg-white/40 animate-ripple";
      btn.querySelector("span.ripple-el")?.remove();
      btn.appendChild(circle);
      setTimeout(() => circle.remove(), 600);
    }
    onClick?.(e);
  }
  return (
    <button
      ref={ref}
      onClick={handleClick}
      className={cn(
        "relative inline-flex items-center justify-center overflow-hidden rounded-lg px-4 py-2 text-sm font-medium",
        "transition-all duration-200 active:scale-[.98] focus:outline-none focus-visible:ring-2 focus-visible:ring-royal/60 disabled:pointer-events-none disabled:opacity-50",
        VARIANTS[variant] || VARIANTS.primary, className,
      )}
      {...props}
    >
      {children}
    </button>
  );
}
