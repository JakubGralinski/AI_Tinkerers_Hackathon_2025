import type { Metadata } from "next";
import "./globals.css";
import { useEffect } from 'react';

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
  title: "Realtime API Agents",
  description: "A demo app from OpenAI.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className={`antialiased`}>{children}</body>
    </html>
  );
}
