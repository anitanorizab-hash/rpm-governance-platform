/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,jsx}"],
  theme: {
    extend: {
      colors: {
        navy: {
          50: "#eaf0f7", 100: "#cdddec", 200: "#9bbad9", 300: "#6896c6", 400: "#3a6fa8",
          500: "#1d4e85", 600: "#143d6b", 700: "#0B2E59", 800: "#082241", 900: "#05172c",
          DEFAULT: "#0B2E59",
        },
        royal: {
          50: "#e8f1fb", 100: "#c9ddf5", 200: "#93bbeb", 300: "#5d99e0", 400: "#2e7ad4",
          500: "#1565C0", 600: "#1156a3", 700: "#0d4485", 800: "#0a3464", 900: "#062544",
          DEFAULT: "#1565C0",
        },
        gold: {
          50: "#fef6e6", 100: "#fde7b8", 200: "#fbd585", 300: "#fac352", 400: "#f9b53a",
          500: "#F9A825", 600: "#d68b16", 700: "#a96c10", 800: "#7c4e0b",
          DEFAULT: "#F9A825",
        },
        success: "#16a34a",
        warning: "#f59e0b",
        danger: "#dc2626",
      },
      fontFamily: {
        sans: ["Inter", "ui-sans-serif", "system-ui", "sans-serif"],
        display: ["Poppins", "Inter", "ui-sans-serif", "sans-serif"],
      },
      boxShadow: {
        card: "0 1px 3px rgba(11,46,89,0.06), 0 8px 24px -8px rgba(11,46,89,0.10)",
        "card-hover": "0 10px 34px -8px rgba(11,46,89,0.20)",
      },
      keyframes: {
        fadeUp: { "0%": { opacity: "0", transform: "translateY(12px)" }, "100%": { opacity: "1", transform: "translateY(0)" } },
        ripple: { "0%": { transform: "scale(0)", opacity: ".5" }, "100%": { transform: "scale(4)", opacity: "0" } },
      },
      animation: {
        "fade-up": "fadeUp .6s cubic-bezier(.16,.84,.44,1) both",
        ripple: "ripple .6s linear",
      },
    },
  },
  plugins: [],
};
