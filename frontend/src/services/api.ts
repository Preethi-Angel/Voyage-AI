import axios from 'axios';
import type { TravelRequest, ApiResponse } from '../types';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const api = {
  // Health check
  health: async () => {
    const response = await apiClient.get('/health');
    return response.data;
  },

  // Single Agent endpoint
  planTripSingleAgent: async (request: TravelRequest): Promise<ApiResponse> => {
    const response = await apiClient.post<ApiResponse>('/api/single', request);
    return response.data;
  },

  // Single Agent with streaming (SSE)
  planTripSingleAgentStream: async (
    request: TravelRequest,
    onLog: (log: { agent_name: string; message: string; timestamp: string }) => void,
    onResult: (result: ApiResponse) => void,
    onError: (error: string) => void
  ): Promise<void> => {
    const url = `${API_BASE_URL}/api/single/stream`;

    try {
      const response = await fetch(url, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(request),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const reader = response.body?.getReader();
      const decoder = new TextDecoder();

      if (!reader) {
        throw new Error('Failed to get response stream');
      }

      let buffer = '';

      while (true) {
        const { done, value } = await reader.read();
        if (done) break;

        buffer += decoder.decode(value, { stream: true });
        const lines = buffer.split('\n');

        // Keep the last incomplete line in the buffer
        buffer = lines.pop() || '';

        for (const line of lines) {
          if (line.startsWith('data: ')) {
            const data = line.substring(6).trim();
            if (!data) continue;

            try {
              const event = JSON.parse(data);

              if (event.type === 'log') {
                onLog({
                  agent_name: event.agent_name,
                  message: event.message,
                  timestamp: event.timestamp,
                });
              } else if (event.type === 'result') {
                onResult(event.data);
              } else if (event.type === 'error') {
                onError(event.message);
              }
            } catch (e) {
              console.error('Failed to parse SSE event:', data, e);
            }
          }
        }
      }
    } catch (error: any) {
      onError(error.message || 'Failed to plan trip');
    }
  },

  // Multi-Agent with AWS SDK endpoint
  planTripMultiAgent: async (request: TravelRequest): Promise<ApiResponse> => {
    const response = await apiClient.post<ApiResponse>('/api/multi', request);
    return response.data;
  },

  // Get stage explanation
  getStageExplanation: async (stage: 'single' | 'multi') => {
    const endpoint = stage === 'single' ? '/api/single/demo-explanation' : '/api/multi/demo-explanation';
    const response = await apiClient.get(endpoint);
    return response.data;
  },

  // Multi-Agent with streaming (SSE)
  planTripMultiAgentStream: async (
    request: TravelRequest,
    onLog: (log: { agent_name: string; message: string; timestamp: string }) => void,
    onResult: (result: ApiResponse) => void,
    onError: (error: string) => void
  ): Promise<void> => {
    const url = `${API_BASE_URL}/api/multi/stream`;

    try {
      const response = await fetch(url, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(request),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const reader = response.body?.getReader();
      const decoder = new TextDecoder();

      if (!reader) {
        throw new Error('Failed to get response stream');
      }

      let buffer = '';

      while (true) {
        const { done, value } = await reader.read();
        if (done) break;

        buffer += decoder.decode(value, { stream: true });
        const lines = buffer.split('\n');

        // Keep the last incomplete line in the buffer
        buffer = lines.pop() || '';

        for (const line of lines) {
          if (line.startsWith('data: ')) {
            const data = line.substring(6).trim();
            if (!data) continue;

            try {
              const event = JSON.parse(data);

              if (event.type === 'log') {
                onLog({
                  agent_name: event.agent_name,
                  message: event.message,
                  timestamp: event.timestamp,
                });
              } else if (event.type === 'result') {
                onResult(event.data);
              } else if (event.type === 'error') {
                onError(event.message);
              }
            } catch (e) {
              console.error('Failed to parse SSE event:', data, e);
            }
          }
        }
      }
    } catch (error: any) {
      onError(error.message || 'Failed to plan trip');
    }
  },

  // Strands with streaming (SSE) - Stage 3
  planTripStrandsStream: async (
    request: TravelRequest,
    onLog: (log: { agent_name: string; message: string; timestamp: string; data?: any }) => void,
    onResult: (result: ApiResponse) => void,
    onError: (error: string) => void
  ): Promise<void> => {
    const url = `${API_BASE_URL}/api/strands/stream`;

    try {
      const response = await fetch(url, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(request),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const reader = response.body?.getReader();
      const decoder = new TextDecoder();

      if (!reader) {
        throw new Error('Failed to get response stream');
      }

      let buffer = '';

      while (true) {
        const { done, value } = await reader.read();
        if (done) break;

        buffer += decoder.decode(value, { stream: true });
        const lines = buffer.split('\n');

        // Keep the last incomplete line in the buffer
        buffer = lines.pop() || '';

        for (const line of lines) {
          if (line.startsWith('data: ')) {
            const data = line.substring(6).trim();
            if (!data) continue;

            try {
              const event = JSON.parse(data);

              if (event.type === 'log') {
                onLog({
                  agent_name: event.agent_name,
                  message: event.message,
                  timestamp: event.timestamp,
                  data: event.data,
                });
              } else if (event.type === 'result') {
                onResult(event.data);
              } else if (event.type === 'error') {
                onError(event.message);
              }
            } catch (e) {
              console.error('Failed to parse SSE event:', data, e);
            }
          }
        }
      }
    } catch (error: any) {
      onError(error.message || 'Failed to plan trip');
    }
  },

  // AP2 with streaming (SSE) - Stage 4
  planTripAP2Stream: async (
    request: TravelRequest,
    onLog: (log: { agent_name: string; message: string; timestamp: string; data?: any }) => void,
    onResult: (result: ApiResponse) => void,
    onError: (error: string) => void
  ): Promise<void> => {
    const url = `${API_BASE_URL}/api/ap2/stream`;

    try {
      const response = await fetch(url, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(request),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const reader = response.body?.getReader();
      const decoder = new TextDecoder();

      if (!reader) {
        throw new Error('Failed to get response stream');
      }

      let buffer = '';

      while (true) {
        const { done, value } = await reader.read();
        if (done) break;

        buffer += decoder.decode(value, { stream: true });
        const lines = buffer.split('\n');

        // Keep the last incomplete line in the buffer
        buffer = lines.pop() || '';

        for (const line of lines) {
          if (line.startsWith('data: ')) {
            const data = line.substring(6).trim();
            if (!data) continue;

            try {
              const event = JSON.parse(data);

              if (event.type === 'log') {
                onLog({
                  agent_name: event.agent_name,
                  message: event.message,
                  timestamp: event.timestamp,
                  data: event.data,
                });
              } else if (event.type === 'result') {
                onResult(event.data);
              } else if (event.type === 'error') {
                onError(event.message);
              }
            } catch (e) {
              console.error('Failed to parse SSE event:', data, e);
            }
          }
        }
      }
    } catch (error: any) {
      onError(error.message || 'Failed to plan trip with AP2');
    }
  },
};

export default api;
