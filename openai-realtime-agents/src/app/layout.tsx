import type { Metadata } from "next";
import "./globals.css";
import { useEffect } from 'react';
import { ThemeProvider } from "./contexts/ThemeContext";

// Suppress hydration warnings
if (typeof window !== 'undefined') {
  const originalConsoleError = console.error;
  console.error = (...args) => {
    if (args[0]?.includes('Hydration failed because')) {
      return;
    }
    if (args[0]?.includes('There was an error while hydrating')) {
      return;
    }
    originalConsoleError(...args);
  };
}

export const metadata: Metadata = {
  title: "CrunchByte",
  description: "OpenAI agentic wellness coach",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" className="dark">
      <body className={`antialiased`}>
        <ThemeProvider>
          {children}
        </ThemeProvider>
      </body>
    </html>
  );
}
