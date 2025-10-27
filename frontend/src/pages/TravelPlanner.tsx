import React, { useState } from 'react';
import { TravelForm } from '../components/TravelForm';
import { ItineraryDisplay } from '../components/ItineraryDisplay';
import { AgentLogs } from '../components/AgentLogs';
import { api } from '../services/api';
import type { TravelRequest, ApiResponse, AgentLog } from '../types';

type AgentType = 'single' | 'agent-squad' | 'strands' | 'ap2';

interface AgentOption {
  id: AgentType;
  name: string;
  description: string;
  tags: string[];
  color: string;
  icon: string;
}

const AGENT_OPTIONS: AgentOption[] = [
  {
    id: 'single',
    name: 'Quick Planning',
    description: '',
    tags: ['Single Agent'],
    color: 'blue',
    icon: '',
  },
  {
    id: 'agent-squad',
    name: 'Smart Planning',
    description: '',
    tags: ['Agent Squad'],
    color: 'blue',
    icon: '',
  },
  {
    id: 'strands',
    name: 'Premium Planning',
    description: '',
    tags: ['Strands'],
    color: 'blue',
    icon: '',
  },
  {
    id: 'ap2',
    name: 'Instant Booking',
    description: '',
    tags: ['AP2'],
    color: 'blue',
    icon: '',
  },
];

export const TravelPlanner: React.FC = () => {
  const [selectedAgent, setSelectedAgent] = useState<AgentType>('agent-squad');
  const [loading, setLoading] = useState(false);
  const [response, setResponse] = useState<ApiResponse | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [streamingLogs, setStreamingLogs] = useState<AgentLog[]>([]);
  const [startTime, setStartTime] = useState<number>(0);
  const [elapsedTime, setElapsedTime] = useState<number>(0);
  const [paymentStatus, setPaymentStatus] = useState<'idle' | 'processing' | 'authorized' | 'completed' | 'failed'>('idle');
  const [walletBalance, setWalletBalance] = useState<number>(10000);

  const selectedOption = AGENT_OPTIONS.find(opt => opt.id === selectedAgent)!;

  const handleSubmit = async (request: TravelRequest) => {
    setLoading(true);
    setError(null);
    setResponse(null);
    setStreamingLogs([]);
    setStartTime(Date.now());

    try {
      if (selectedAgent === 'single') {
        // Streaming single agent
        await api.planTripSingleAgentStream(
          request,
          (log) => {
            setStreamingLogs((prev) => [...prev, log]);
            setElapsedTime(Date.now() - startTime);
          },
          (result) => {
            setResponse(result);
            setLoading(false);
            setElapsedTime(Date.now() - startTime);
          },
          (errorMsg) => {
            setError(errorMsg);
            setLoading(false);
          }
        );
      } else if (selectedAgent === 'agent-squad') {
        // Streaming multi-agent
        await api.planTripMultiAgentStream(
          request,
          (log) => {
            setStreamingLogs((prev) => [...prev, log]);
            setElapsedTime(Date.now() - startTime);
          },
          (result) => {
            setResponse(result);
            setLoading(false);
            setElapsedTime(Date.now() - startTime);
          },
          (errorMsg) => {
            setError(errorMsg);
            setLoading(false);
          }
        );
      } else if (selectedAgent === 'strands') {
        // Strands streaming
        await api.planTripStrandsStream(
          request,
          (log) => {
            setStreamingLogs((prev) => [...prev, log]);
            setElapsedTime(Date.now() - startTime);
          },
          (result) => {
            setResponse(result);
            setLoading(false);
            setElapsedTime(Date.now() - startTime);
          },
          (errorMsg) => {
            setError(errorMsg);
            setLoading(false);
          }
        );
      } else if (selectedAgent === 'ap2') {
        // AP2 streaming with payment tracking
        setPaymentStatus('processing');
        await api.planTripAP2Stream(
          request,
          (log) => {
            setStreamingLogs((prev) => [...prev, log]);
            setElapsedTime(Date.now() - startTime);

            if (log.message.includes('Payment authorized')) {
              setPaymentStatus('authorized');
            } else if (log.message.includes('Transaction executed')) {
              setPaymentStatus('completed');
            } else if (log.message.includes('Payment denied')) {
              setPaymentStatus('failed');
            }
          },
          (result) => {
            setResponse(result);
            setLoading(false);
            setElapsedTime(Date.now() - startTime);
            if (result.wallet_balance !== undefined) {
              setWalletBalance(result.wallet_balance);
            }
          },
          (errorMsg) => {
            setError(errorMsg);
            setLoading(false);
            setPaymentStatus('failed');
          }
        );
      }
    } catch (err: any) {
      setError(err.response?.data?.detail || err.message || 'Failed to plan trip');
      setLoading(false);
    }
  };

  const getColorClasses = (color: string) => {
    const colorMap: Record<string, { bg: string; border: string; text: string; hover: string; tag: string }> = {
      gray: { bg: 'bg-gray-50', border: 'border-gray-300', text: 'text-gray-700', hover: 'hover:border-gray-500', tag: 'bg-gray-100 text-gray-700' },
      blue: { bg: 'bg-blue-50', border: 'border-blue-300', text: 'text-blue-700', hover: 'hover:border-blue-500', tag: 'bg-blue-100 text-blue-700' },
      purple: { bg: 'bg-purple-50', border: 'border-purple-300', text: 'text-purple-700', hover: 'hover:border-purple-500', tag: 'bg-purple-100 text-purple-700' },
      emerald: { bg: 'bg-emerald-50', border: 'border-emerald-300', text: 'text-emerald-700', hover: 'hover:border-emerald-500', tag: 'bg-emerald-100 text-emerald-700' },
    };
    return colorMap[color] || colorMap.gray;
  };

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
      {/* Header */}
      <div className="mb-12 text-center">
        <h1 className="text-5xl font-bold mb-4 text-blue-600">
          Plan Your Perfect Trip
        </h1>
        <p className="text-gray-600 text-xl max-w-3xl mx-auto">
          Choose your planning style and let our AI create the perfect itinerary for you
        </p>
      </div>

      {/* Agent Selection */}
      <div className="bg-white rounded-2xl p-8 shadow-lg mb-8 border border-gray-100">
        <h2 className="text-2xl font-bold mb-6 text-gray-900">Select Planning Style</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          {AGENT_OPTIONS.map((option) => {
            const colors = getColorClasses(option.color);
            const isSelected = selectedAgent === option.id;

            return (
              <button
                key={option.id}
                onClick={() => setSelectedAgent(option.id)}
                disabled={loading}
                className={`
                  text-left p-4 rounded-lg border-2 transition-all
                  ${isSelected
                    ? `${colors.bg} ${colors.border} shadow-lg`
                    : `bg-white border-gray-200 ${colors.hover}`
                  }
                  ${loading ? 'opacity-50 cursor-not-allowed' : 'cursor-pointer hover:shadow-md'}
                `}
              >
                <div className="flex items-center justify-between mb-2">
                  <h3 className={`font-bold text-lg ${isSelected ? colors.text : 'text-gray-900'}`}>
                    {option.name}
                  </h3>
                  {isSelected && (
                    <svg className={`w-5 h-5 ${colors.text} flex-shrink-0`} fill="currentColor" viewBox="0 0 20 20">
                      <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                    </svg>
                  )}
                </div>
                <div className="flex flex-wrap gap-2">
                  {option.tags.map((tag) => (
                    <span
                      key={tag}
                      className={`text-xs px-3 py-1 rounded-full font-medium ${
                        isSelected ? colors.tag : 'bg-gray-100 text-gray-600'
                      }`}
                    >
                      {tag}
                    </span>
                  ))}
                </div>
              </button>
            );
          })}
        </div>
      </div>

      {/* AP2 Wallet Balance (only show when AP2 is selected) */}
      {selectedAgent === 'ap2' && (
        <div className="card bg-gradient-to-br from-emerald-50 to-teal-50 border-2 border-emerald-200">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-4">
              <div className="bg-emerald-600 rounded-full p-3">
                <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 10h18M7 15h1m4 0h1m-7 4h12a3 3 0 003-3V8a3 3 0 00-3-3H6a3 3 0 00-3 3v8a3 3 0 003 3z" />
                </svg>
              </div>
              <div>
                <div className="text-xs text-gray-600 font-medium mb-1">AP2 Wallet Balance</div>
                <div className="text-2xl font-bold text-emerald-700">
                  ${walletBalance.toLocaleString('en-US', {minimumFractionDigits: 2, maximumFractionDigits: 2})}
                </div>
              </div>
            </div>
            {paymentStatus !== 'idle' && (
              <div className={`flex items-center gap-2 px-4 py-2 rounded-lg border ${
                paymentStatus === 'processing' ? 'bg-amber-100 text-amber-800 border-amber-300' :
                paymentStatus === 'authorized' ? 'bg-blue-100 text-blue-800 border-blue-300' :
                paymentStatus === 'completed' ? 'bg-green-100 text-green-800 border-green-300' :
                'bg-red-100 text-red-800 border-red-300'
              }`}>
                <span className="font-semibold capitalize">{paymentStatus}</span>
              </div>
            )}
          </div>
        </div>
      )}

      {/* Travel Form */}
      <div className={`card bg-gradient-to-br from-white to-${selectedOption.color}-50`}>
        <h2 className="text-2xl font-bold mb-6">Travel Requirements</h2>
        <TravelForm onSubmit={handleSubmit} loading={loading} />
      </div>

      {/* Loading State */}
      {loading && (
        <div className={`card py-12 bg-gradient-to-br from-${selectedOption.color}-50 to-white border-2 border-${selectedOption.color}-300`}>
          <div className="text-center mb-8">
            <div className="animate-spin rounded-full h-20 w-20 border-b-4 border-${selectedOption.color}-600 mx-auto mb-6"></div>
            <p className="text-gray-800 font-bold text-2xl mb-2">{selectedOption.name} Working</p>
            <p className="text-gray-600">{selectedOption.description}</p>
            {elapsedTime > 0 && (
              <div className="mt-4 text-2xl font-mono font-bold text-${selectedOption.color}-600">
                {(elapsedTime / 1000).toFixed(1)}s
              </div>
            )}
          </div>

          {/* Streaming Logs - Compact Timeline */}
          {streamingLogs.length > 0 && (
            <div className="mt-6 max-w-3xl mx-auto">
              <h3 className="font-bold text-blue-900 mb-4 text-center text-lg">
                Live Agent Activity
              </h3>
              <div className="relative bg-white rounded-lg border border-blue-200 p-4 max-h-96 overflow-y-auto">
                {/* Timeline vertical line */}
                <div className="absolute left-6 top-4 bottom-4 w-px bg-blue-200"></div>

                {/* Timeline items */}
                <div className="space-y-2">
                  {streamingLogs.map((log, idx) => (
                    <div
                      key={idx}
                      className="relative pl-12 animate-fade-in"
                    >
                      {/* Timeline dot */}
                      <div className="absolute left-4 top-1 w-4 h-4 rounded-full bg-blue-500 border-2 border-white shadow z-10"></div>

                      {/* Timeline content */}
                      <div className="flex items-start gap-2 py-1">
                        <span className="px-2 py-0.5 bg-blue-100 text-blue-700 rounded text-xs font-semibold whitespace-nowrap">
                          {log.agent_name}
                        </span>
                        <p className="text-sm text-gray-700 leading-snug">
                          {log.message.replace(/[🚀📍💰✈️🏨🎯🧮✅⚠️🎉🧠📊🔧⚡💳🔐📋🛒📧❌🤖🎭]/g, '').trim()}
                        </p>
                      </div>
                    </div>
                  ))}
                </div>

                {/* Loading indicator at the end */}
                <div className="relative pl-12 mt-2 py-1">
                  <div className="absolute left-4 top-1 w-4 h-4 rounded-full bg-blue-300 border-2 border-white animate-pulse"></div>
                  <p className="text-sm text-blue-600 font-medium flex items-center gap-2">
                    <svg className="animate-spin h-3 w-3" fill="none" viewBox="0 0 24 24">
                      <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                      <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                    </svg>
                    Processing...
                  </p>
                </div>
              </div>
            </div>
          )}
        </div>
      )}

      {/* Error Display */}
      {error && (
        <div className="card bg-red-50 border-2 border-red-200">
          <div className="flex items-start gap-3">
            <svg className="w-6 h-6 text-red-600 flex-shrink-0 mt-0.5" fill="currentColor" viewBox="0 0 20 20">
              <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
            </svg>
            <div>
              <h3 className="font-bold text-red-900 text-xl mb-1">Error</h3>
              <p className="text-red-700">{error}</p>
            </div>
          </div>
        </div>
      )}

      {/* Results */}
      {response && response.itinerary && (
        <div className="space-y-6">
          {/* Budget Status */}
          {response.itinerary.within_budget ? (
            <div className="card bg-gradient-to-br from-green-50 via-emerald-50 to-green-50 border-2 border-green-300 shadow-lg">
              <div className="text-center py-8">
                <div className="flex justify-center mb-4">
                  <div className="bg-green-500 rounded-full p-4">
                    <svg className="w-12 h-12 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                    </svg>
                  </div>
                </div>
                <h3 className="text-3xl font-bold text-green-800 mb-2">Within Budget!</h3>
                <p className="text-gray-600 mb-6">Great choice! Your trip fits perfectly within budget</p>

                <div className="max-w-md mx-auto space-y-4">
                  <div className="bg-white rounded-lg p-4 shadow-sm">
                    <div className="flex justify-between items-center mb-2">
                      <span className="text-sm text-gray-600">Your Budget</span>
                      <span className="text-lg font-semibold text-gray-900">${(response.itinerary.total_budget || 0).toLocaleString()}</span>
                    </div>
                    <div className="flex justify-between items-center mb-2">
                      <span className="text-sm text-gray-600">Total Cost</span>
                      <span className="text-lg font-semibold text-green-600">${(response.itinerary.actual_cost || 0).toLocaleString()}</span>
                    </div>
                    <div className="border-t-2 border-green-200 pt-2 mt-2">
                      <div className="flex justify-between items-center">
                        <span className="text-sm font-bold text-green-700">You Saved</span>
                        <span className="text-2xl font-bold text-green-700">${((response.itinerary.total_budget || 0) - (response.itinerary.actual_cost || 0)).toLocaleString()}</span>
                      </div>
                    </div>
                  </div>

                  <div className="bg-green-50 border border-green-200 rounded-lg p-4 text-left">
                    <div className="flex items-start gap-2">
                      <svg className="w-5 h-5 text-green-600 mt-0.5 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
                        <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                      </svg>
                      <p className="text-sm text-green-800">Your trip is optimized! You have extra budget for spontaneous activities or souvenirs.</p>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          ) : (
            <div className="card bg-gradient-to-br from-red-50 via-orange-50 to-red-50 border-2 border-red-300 shadow-lg">
              <div className="text-center py-8">
                <div className="flex justify-center mb-4">
                  <div className="bg-red-500 rounded-full p-4">
                    <svg className="w-12 h-12 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
                    </svg>
                  </div>
                </div>
                <h3 className="text-3xl font-bold text-red-800 mb-2">Over Budget</h3>
                <p className="text-gray-600 mb-6">The trip exceeds your budget</p>

                <div className="max-w-md mx-auto space-y-4">
                  <div className="bg-white rounded-lg p-4 shadow-sm">
                    <div className="flex justify-between items-center mb-2">
                      <span className="text-sm text-gray-600">Your Budget</span>
                      <span className="text-lg font-semibold text-gray-900">${(response.itinerary.total_budget || 0).toLocaleString()}</span>
                    </div>
                    <div className="flex justify-between items-center mb-2">
                      <span className="text-sm text-gray-600">Total Cost</span>
                      <span className="text-lg font-semibold text-red-600">${(response.itinerary.actual_cost || 0).toLocaleString()}</span>
                    </div>
                    <div className="border-t-2 border-red-200 pt-2 mt-2">
                      <div className="flex justify-between items-center">
                        <span className="text-sm font-bold text-red-700">Amount Over</span>
                        <span className="text-2xl font-bold text-red-700">${((response.itinerary.actual_cost || 0) - (response.itinerary.total_budget || 0)).toLocaleString()}</span>
                      </div>
                    </div>
                  </div>

                  <div className="bg-amber-50 border border-amber-200 rounded-lg p-4 text-left">
                    <div className="flex items-start gap-2">
                      <svg className="w-5 h-5 text-amber-600 mt-0.5 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
                        <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clipRule="evenodd" />
                      </svg>
                      <p className="text-sm text-amber-800">Try reducing the number of activities or selecting a lower budget hotel to stay within your budget.</p>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          )}

          {/* Agent Activity Logs */}
          {response.agent_logs && response.agent_logs.length > 0 && selectedAgent !== 'single' && (
            <AgentLogs logs={response.agent_logs} executionTime={response.execution_time_ms} />
          )}

          {/* Itinerary */}
          <ItineraryDisplay itinerary={response.itinerary} />

          {/* AP2 Payment Details */}
          {selectedAgent === 'ap2' && response.ap2_mandates && (
            <div className="card border-2 border-emerald-200">
              <h2 className="text-2xl font-bold mb-6 text-gray-900 flex items-center gap-2">
                <svg className="w-6 h-6 text-emerald-600" fill="currentColor" viewBox="0 0 20 20">
                  <path fillRule="evenodd" d="M2.166 4.999A11.954 11.954 0 0010 1.944 11.954 11.954 0 0017.834 5c.11.65.166 1.32.166 2.001 0 5.225-3.34 9.67-8 11.317C5.34 16.67 2 12.225 2 7c0-.682.057-1.35.166-2.001zm11.541 3.708a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                </svg>
                AP2 Verification Details
              </h2>

              {/* Payment Receipt */}
              {response.payment_details && (
                <div className="mb-4 p-4 bg-emerald-50 rounded-lg border border-emerald-200">
                  <div className="font-semibold text-emerald-900 mb-3">Payment Receipt</div>
                  <div className="space-y-2 text-sm">
                    <div className="flex justify-between">
                      <span className="text-gray-600">Receipt ID:</span>
                      <span className="font-mono text-gray-900">{response.payment_details.receipt_id}</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-gray-600">Amount Paid:</span>
                      <span className="font-bold text-emerald-700">${response.payment_details.amount_paid.toFixed(2)}</span>
                    </div>
                    <div className="flex justify-between items-start">
                      <span className="text-gray-600">Blockchain Hash:</span>
                      <span className="font-mono text-xs text-gray-600 break-all max-w-xs text-right">
                        {response.payment_details.blockchain_hash.substring(0, 32)}...
                      </span>
                    </div>
                  </div>
                </div>
              )}

              {/* Mandate Details */}
              <details className="mb-2 group">
                <summary className="cursor-pointer font-semibold text-gray-700 hover:text-emerald-600 p-3 bg-gray-50 rounded-lg transition-colors">
                  Intent Mandate (Step 1)
                </summary>
                <pre className="mt-2 text-xs bg-gray-50 p-4 rounded-lg overflow-x-auto border border-gray-200 font-mono">
                  {JSON.stringify(response.ap2_mandates.intent_mandate, null, 2)}
                </pre>
              </details>

              <details className="mb-2 group">
                <summary className="cursor-pointer font-semibold text-gray-700 hover:text-emerald-600 p-3 bg-gray-50 rounded-lg transition-colors">
                  Cart Mandate (Step 2)
                </summary>
                <pre className="mt-2 text-xs bg-gray-50 p-4 rounded-lg overflow-x-auto border border-gray-200 font-mono">
                  {JSON.stringify(response.ap2_mandates.cart_mandate, null, 2)}
                </pre>
              </details>

              <details className="mb-2 group">
                <summary className="cursor-pointer font-semibold text-gray-700 hover:text-emerald-600 p-3 bg-gray-50 rounded-lg transition-colors">
                  Payment Mandate (Step 3)
                </summary>
                <pre className="mt-2 text-xs bg-gray-50 p-4 rounded-lg overflow-x-auto border border-gray-200 font-mono">
                  {JSON.stringify(response.ap2_mandates.payment_mandate, null, 2)}
                </pre>
              </details>
            </div>
          )}
        </div>
      )}
    </div>
  );
};
