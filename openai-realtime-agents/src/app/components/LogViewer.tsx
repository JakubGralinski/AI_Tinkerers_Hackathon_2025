"use client";

import React, { useState, useRef, useEffect } from "react";
import { useEvent } from "@/app/contexts/EventContext";
import { useTheme } from "@/app/contexts/ThemeContext";
import { LoggedEvent } from "@/app/types";
import Image from "next/image";

interface LogViewerProps {
  isVisible: boolean;
  onToggleVisibility: () => void;
}

const LogViewer: React.FC<LogViewerProps> = ({ isVisible, onToggleVisibility }) => {
  const { loggedEvents, toggleExpand } = useEvent();
  const { theme, toggleTheme } = useTheme();
  const [prevEventLogs, setPrevEventLogs] = useState<LoggedEvent[]>([]);
  const logContainerRef = useRef<HTMLDivElement | null>(null);
  const [searchTerm, setSearchTerm] = useState<string>("");
  const [filteredEvents, setFilteredEvents] = useState<LoggedEvent[]>([]);
  const [searchQuery, setSearchQuery] = useState<string>("");

  // Filter events based on search term
  useEffect(() => {
    if (searchTerm.trim() === "") {
      setFilteredEvents(loggedEvents);
    } else {
      const filtered = loggedEvents.filter(event => 
        event.eventName.toLowerCase().includes(searchTerm.toLowerCase()) ||
        JSON.stringify(event.eventData).toLowerCase().includes(searchTerm.toLowerCase())
      );
      setFilteredEvents(filtered);
    }
  }, [loggedEvents, searchTerm]);

  // Auto-scroll to bottom when new events arrive
  useEffect(() => {
    const hasNewEvent = loggedEvents.length > prevEventLogs.length;
    if (isVisible && hasNewEvent && logContainerRef.current) {
      logContainerRef.current.scrollTop = logContainerRef.current.scrollHeight;
    }
    setPrevEventLogs(loggedEvents);
  }, [loggedEvents, isVisible]);

  const getDirectionArrow = (direction: "incoming" | "outgoing") => {
    return {
      symbol: direction === "incoming" ? "←" : "→",
      color: direction === "incoming" ? "#6c71c4" : "#859900"
    };
  };

  const clearLogs = () => {
    // This would need to be implemented in the EventContext
    console.log("Clear logs clicked");
  };

  const handleClearSearch = () => {
    setSearchQuery("");
    setSearchTerm("");
  };

  return (
    <div className={`flex flex-col flex-1 bg-card-bg min-h-0 rounded-xl border border-card-border shadow-lg ${isVisible ? 'opacity-100' : 'opacity-0 hidden'}`}>
      <div className="p-4 flex items-center gap-x-2 flex-shrink-0 border-b border-card-border">
        <input
          type="text"
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
          className="flex-1 px-4 py-2 bg-background text-text-primary border border-card-border rounded focus:outline-none focus:border-accent placeholder-text-secondary"
          placeholder="Search logs..."
        />
        <button
          onClick={handleClearSearch}
          className="bg-background text-text-primary rounded-full px-2 py-2 hover:bg-card-border transition-colors duration-200"
        >
          <Image src="clear.svg" alt="Clear" width={24} height={24} className="invert-[0.8]" />
        </button>
        <button
          onClick={toggleTheme}
          className="bg-background text-text-primary rounded-full px-2 py-2 hover:bg-card-border transition-colors duration-200"
          title={`Switch to ${theme === 'light' ? 'dark' : 'light'} mode`}
        >
          {theme === 'light' ? '🌙' : '☀️'}
        </button>
      </div>

      <div className="flex-1 overflow-auto p-4">
        {filteredEvents.map((log, index) => {
          const arrowInfo = getDirectionArrow(log.direction as "incoming" | "outgoing");
          const isError = log.eventName.toLowerCase().includes("error") || 
            log.eventData?.response?.status_details?.error != null;

          return (
            <div
              key={index}
              className={`flex items-start gap-x-2 font-mono text-sm mb-2 ${
                isError ? "text-error" : "text-text-primary"
              }`}
            >
              <span className="text-accent">{arrowInfo.symbol}</span>
              <span className="text-text-secondary">{log.timestamp}</span>
              <pre className="whitespace-pre-wrap break-words flex-1">
                {JSON.stringify(log.eventData, null, 2)}
              </pre>
            </div>
          );
        })}
      </div>
    </div>
  );
};

export default LogViewer; 