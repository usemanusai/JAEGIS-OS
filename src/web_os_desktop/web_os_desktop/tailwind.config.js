/** @type {import('tailwindcss').Config} */
export default {
  darkMode: ["class"],
  content: [
    './pages/**/*.{js,jsx}',
    './components/**/*.{js,jsx}',
    './app/**/*.{js,jsx}',
    './src/**/*.{js,jsx}',
  ],
  prefix: "",
  theme: {
    container: {
      center: true,
      padding: "2rem",
      screens: {
        "2xl": "1400px",
      },
    },
    extend: {
      colors: {
        border: "var(--color-border)", // slate-400 with opacity
        input: "var(--color-input)", // slate-800
        ring: "var(--color-ring)", // indigo-500
        background: "var(--color-background)", // slate-900
        foreground: "var(--color-foreground)", // slate-50
        primary: {
          DEFAULT: "var(--color-primary)", // indigo-500
          foreground: "var(--color-primary-foreground)", // slate-50
        },
        secondary: {
          DEFAULT: "var(--color-secondary)", // violet-500
          foreground: "var(--color-secondary-foreground)", // slate-50
        },
        destructive: {
          DEFAULT: "var(--color-destructive)", // red-500
          foreground: "var(--color-destructive-foreground)", // slate-50
        },
        muted: {
          DEFAULT: "var(--color-muted)", // slate-700
          foreground: "var(--color-muted-foreground)", // slate-400
        },
        accent: {
          DEFAULT: "var(--color-accent)", // cyan-500
          foreground: "var(--color-accent-foreground)", // slate-50
        },
        popover: {
          DEFAULT: "var(--color-popover)", // slate-800
          foreground: "var(--color-popover-foreground)", // slate-50
        },
        card: {
          DEFAULT: "var(--color-card)", // slate-800
          foreground: "var(--color-card-foreground)", // slate-50
        },
        surface: "var(--color-surface)", // slate-800
        success: {
          DEFAULT: "var(--color-success)", // emerald-500
          foreground: "var(--color-success-foreground)", // slate-50
        },
        warning: {
          DEFAULT: "var(--color-warning)", // amber-500
          foreground: "var(--color-warning-foreground)", // slate-900
        },
        error: {
          DEFAULT: "var(--color-error)", // red-500
          foreground: "var(--color-error-foreground)", // slate-50
        },
      },
      borderRadius: {
        lg: "12px",
        md: "8px",
        sm: "6px",
      },
      fontFamily: {
        heading: ['Inter', 'system-ui', 'sans-serif'],
        body: ['Inter', 'system-ui', 'sans-serif'],
        caption: ['Inter', 'system-ui', 'sans-serif'],
        mono: ['JetBrains Mono', 'Consolas', 'Monaco', 'monospace'],
      },
      fontSize: {
        'xs': ['0.75rem', { lineHeight: '1rem' }],
        'sm': ['0.875rem', { lineHeight: '1.25rem' }],
        'base': ['1rem', { lineHeight: '1.5rem' }],
        'lg': ['1.125rem', { lineHeight: '1.75rem' }],
        'xl': ['1.25rem', { lineHeight: '1.75rem' }],
        '2xl': ['1.5rem', { lineHeight: '2rem' }],
        '3xl': ['1.875rem', { lineHeight: '2.25rem' }],
        '4xl': ['2.25rem', { lineHeight: '2.5rem' }],
      },
      spacing: {
        '18': '4.5rem',
        '88': '22rem',
        '128': '32rem',
      },
      zIndex: {
        '1': '1',
        '10': '10',
        '100': '100',
        '1000': '1000',
        '2000': '2000',
      },
      backdropBlur: {
        xs: '2px',
        sm: '4px',
        md: '12px',
        lg: '16px',
        xl: '20px',
      },
      boxShadow: {
        'window': '0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04)',
        'window-focused': '0 25px 50px -12px rgba(0, 0, 0, 0.25)',
        'glass': '0 8px 32px 0 rgba(31, 38, 135, 0.37)',
      },
      animation: {
        "fade-in": "fadeIn 150ms ease-out",
        "slide-up": "slideUp 300ms cubic-bezier(0.4, 0, 0.2, 1)",
        "scale-in": "scaleIn 150ms cubic-bezier(0.4, 0, 0.2, 1)",
        "accordion-down": "accordion-down 0.2s ease-out",
        "accordion-up": "accordion-up 0.2s ease-out",
      },
      keyframes: {
        fadeIn: {
          "0%": { opacity: "0" },
          "100%": { opacity: "1" },
        },
        slideUp: {
          "0%": { opacity: "0", transform: "translateY(10px)" },
          "100%": { opacity: "1", transform: "translateY(0)" },
        },
        scaleIn: {
          "0%": { opacity: "0", transform: "scale(0.95)" },
          "100%": { opacity: "1", transform: "scale(1)" },
        },
        "accordion-down": {
          from: { height: "0" },
          to: { height: "var(--radix-accordion-content-height)" },
        },
        "accordion-up": {
          from: { height: "var(--radix-accordion-content-height)" },
          to: { height: "0" },
        },
      },
      transitionTimingFunction: {
        'smooth': 'cubic-bezier(0.4, 0, 0.2, 1)',
      },
      transitionDuration: {
        '150': '150ms',
        '300': '300ms',
      },
    },
  },
  plugins: [
    require("tailwindcss-animate"),
  ],
}