import { clsx } from "clsx";
import { twMerge } from "tailwind-merge";

/** cn — class name helper (ShadCN UI convention). Ready for ShadCN components added later. */
export function cn(...inputs) {
  return twMerge(clsx(inputs));
}
