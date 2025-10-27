import React, { useState } from 'react';
import type { AgentLog } from '../types';

interface AgentLogsProps {
  logs: AgentLog[];
  executionTime: number;
  agentsUsed?: string[];
}

export const AgentLogs: React.FC<AgentLogsProps> = ({ logs, executionTime, agentsUsed }) => {
  const [expanded, setExpanded] = useState(true);

  if (!logs || logs.length === 0) {
    return null;
  }

  return (
    <div className="card bg-gray-50">
      <div
        className="flex items-center justify-between cursor-pointer"
        onClick={() => setExpanded(!expanded)}
      >
        <h3 className="text-xl font-bold">Agent Communication Logs</h3>
        <button className="text-blue-600 hover:text-blue-800">
          {expanded ? '▼ Hide' : '▶ Show'}
        </button>
      </div>

      {expanded && (
        <div className="mt-4 space-y-4">
          {/* Summary */}
          <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
            <div className="grid grid-cols-2 gap-4">
              <div>
                <p className="text-sm text-gray-600">Execution Time</p>
                <p className="text-lg font-semibold text-blue-600">
                  {(executionTime / 1000).toFixed(2)} seconds
                </p>
              </div>
              {agentsUsed && agentsUsed.length > 0 && (
                <div>
                  <p className="text-sm text-gray-600">Agents Used</p>
                  <p className="text-lg font-semibold text-blue-600">{agentsUsed.join(', ')}</p>
                </div>
              )}
            </div>
          </div>

          {/* Logs Timeline */}
          <div className="space-y-3">
            {logs.map((log, idx) => (
              <div
                key={idx}
                className="bg-white border-l-4 border-blue-500 rounded-r-lg p-4 shadow-sm hover:shadow-md transition-shadow"
              >
                <div className="flex items-start justify-between mb-2">
                  <div className="flex items-center gap-2">
                    <span className="px-2 py-1 bg-blue-100 text-blue-800 rounded text-sm font-semibold">
                      {log.agent_name}
                    </span>
                    <span className="text-xs text-gray-500">
                      {new Date(log.timestamp).toLocaleTimeString()}
                    </span>
                  </div>
                </div>

                <p className="text-gray-800 mb-2">{log.message}</p>

                {log.data && Object.keys(log.data).length > 0 && (
                  <details className="mt-2">
                    <summary className="cursor-pointer text-sm text-blue-600 hover:text-blue-800">
                      View Details
                    </summary>
                    <pre className="mt-2 p-3 bg-gray-100 rounded text-xs overflow-x-auto">
                      {JSON.stringify(log.data, null, 2)}
                    </pre>
                  </details>
                )}
              </div>
            ))}
          </div>

          {/* AWS SDK Indicator */}
          <div className="bg-green-50 border border-green-200 rounded-lg p-4">
            <div className="flex items-center gap-2">
              <div>
                <p className="font-semibold text-green-800">Using AWS Agent Squad Framework</p>
                <p className="text-sm text-green-600">
                  Intelligent intent classification and routing to specialized Bedrock agents
                </p>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
