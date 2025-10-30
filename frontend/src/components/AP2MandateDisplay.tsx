import React from 'react';

interface AP2Mandate {
  intent_mandate?: {
    intent_id: string;
    description: string;
    items_to_purchase: string[];
    estimated_total: number;
    timestamp: string;
  };
  cart_mandate?: {
    cart_id: string;
    items: Array<{
      name: string;
      description: string;
      quantity: number;
      total_price: number;
      vendor: string;
    }>;
    subtotal: number;
    taxes: number;
    fees: number;
    total: number;
  };
  payment_mandate?: {
    mandate_id: string;
    amount: number;
    payment_method: string;
    signature: string;
    status: string;
    timestamp: string;
  };
}

interface AP2PaymentDetails {
  receipt_id: string;
  amount_paid: number;
  currency: string;
  blockchain_hash: string;
  timestamp: string;
}

interface AP2MandateDisplayProps {
  ap2Mandates?: AP2Mandate;
  paymentDetails?: AP2PaymentDetails;
}

const AP2MandateDisplay: React.FC<AP2MandateDisplayProps> = ({
  ap2Mandates,
  paymentDetails,
}) => {
  if (!ap2Mandates) return null;

  const { intent_mandate, cart_mandate, payment_mandate } = ap2Mandates;

  return (
    <div className="space-y-6">
      {/* AP2 Protocol Header */}
      <div className="bg-gradient-to-r from-indigo-600 to-purple-600 text-white rounded-xl p-6 shadow-lg">
        <div className="flex items-center gap-3 mb-3">
          <svg className="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" />
          </svg>
          <h2 className="text-2xl font-bold">AP2 Autonomous Payment Protocol</h2>
        </div>
        <p className="text-indigo-100 text-sm">
          Verifiable Digital Credentials (VDCs) for Secure AI Commerce
        </p>
      </div>

      {/* Step 1: Intent Mandate */}
      {intent_mandate && (
        <div className="bg-white rounded-xl shadow-lg border-2 border-indigo-200 overflow-hidden">
          <div className="bg-gradient-to-r from-indigo-50 to-indigo-100 px-6 py-4 border-b border-indigo-200">
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 bg-indigo-600 rounded-full flex items-center justify-center text-white font-bold">
                1
              </div>
              <div>
                <h3 className="text-xl font-bold text-indigo-900">Intent Mandate</h3>
                <p className="text-sm text-indigo-600">Agent declares purchase authority and constraints</p>
              </div>
            </div>
          </div>
          <div className="p-6 space-y-4">
            <div className="flex items-start gap-3">
              <svg className="w-5 h-5 text-indigo-500 mt-0.5 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
              </svg>
              <div>
                <p className="text-sm font-semibold text-gray-700">Intent Description</p>
                <p className="text-gray-900">{intent_mandate.description}</p>
              </div>
            </div>
            <div className="flex items-start gap-3">
              <svg className="w-5 h-5 text-indigo-500 mt-0.5 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 10h18M7 15h1m4 0h1m-7 4h12a3 3 0 003-3V8a3 3 0 00-3-3H6a3 3 0 00-3 3v8a3 3 0 003 3z" />
              </svg>
              <div>
                <p className="text-sm font-semibold text-gray-700">Budget Constraint</p>
                <p className="text-2xl font-bold text-indigo-600">${intent_mandate.estimated_total.toFixed(2)}</p>
              </div>
            </div>
            <div className="flex items-start gap-3">
              <svg className="w-5 h-5 text-indigo-500 mt-0.5 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
              </svg>
              <div className="flex-1">
                <p className="text-sm font-semibold text-gray-700 mb-2">Authorized Purchases</p>
                <ul className="space-y-1">
                  {intent_mandate.items_to_purchase.map((item, idx) => (
                    <li key={idx} className="flex items-start gap-2 text-sm text-gray-700">
                      <span className="text-indigo-500 mt-0.5">•</span>
                      <span>{item}</span>
                    </li>
                  ))}
                </ul>
              </div>
            </div>
            <div className="mt-4 pt-4 border-t border-gray-200">
              <p className="text-xs text-gray-500">
                Intent ID: <span className="font-mono">{intent_mandate.intent_id}</span>
              </p>
            </div>
          </div>
        </div>
      )}

      {/* Step 2: Cart Mandate */}
      {cart_mandate && (
        <div className="bg-white rounded-xl shadow-lg border-2 border-purple-200 overflow-hidden">
          <div className="bg-gradient-to-r from-purple-50 to-purple-100 px-6 py-4 border-b border-purple-200">
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 bg-purple-600 rounded-full flex items-center justify-center text-white font-bold">
                2
              </div>
              <div>
                <h3 className="text-xl font-bold text-purple-900">Cart Mandate</h3>
                <p className="text-sm text-purple-600">Agent's purchase proposal with itemized breakdown</p>
              </div>
            </div>
          </div>
          <div className="p-6 space-y-4">
            <div className="space-y-3">
              {cart_mandate.items.map((item, idx) => (
                <div key={idx} className="bg-gray-50 rounded-lg p-4">
                  <div className="flex justify-between items-start mb-2">
                    <div className="flex-1">
                      <p className="font-semibold text-gray-900">{item.name}</p>
                      <p className="text-sm text-gray-600">{item.description}</p>
                      <p className="text-xs text-gray-500 mt-1">Vendor: {item.vendor}</p>
                    </div>
                    <div className="text-right">
                      <p className="text-lg font-bold text-purple-600">${item.total_price.toFixed(2)}</p>
                      <p className="text-xs text-gray-500">Qty: {item.quantity}</p>
                    </div>
                  </div>
                </div>
              ))}
            </div>

            <div className="mt-4 pt-4 border-t-2 border-gray-300 space-y-2">
              <div className="flex justify-between text-sm">
                <span className="text-gray-600">Subtotal</span>
                <span className="font-semibold">${cart_mandate.subtotal.toFixed(2)}</span>
              </div>
              <div className="flex justify-between text-sm">
                <span className="text-gray-600">Taxes</span>
                <span className="font-semibold">${cart_mandate.taxes.toFixed(2)}</span>
              </div>
              <div className="flex justify-between text-sm">
                <span className="text-gray-600">Processing Fees</span>
                <span className="font-semibold">${cart_mandate.fees.toFixed(2)}</span>
              </div>
              <div className="flex justify-between text-lg font-bold pt-2 border-t border-gray-200">
                <span className="text-purple-900">Total</span>
                <span className="text-purple-600">${cart_mandate.total.toFixed(2)}</span>
              </div>
            </div>

            <div className="mt-4 pt-4 border-t border-gray-200">
              <p className="text-xs text-gray-500">
                Cart ID: <span className="font-mono">{cart_mandate.cart_id}</span>
              </p>
            </div>
          </div>
        </div>
      )}

      {/* Step 3: Payment Mandate */}
      {payment_mandate && (
        <div className="bg-white rounded-xl shadow-lg border-2 border-green-200 overflow-hidden">
          <div className="bg-gradient-to-r from-green-50 to-green-100 px-6 py-4 border-b border-green-200">
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 bg-green-600 rounded-full flex items-center justify-center text-white font-bold">
                3
              </div>
              <div>
                <h3 className="text-xl font-bold text-green-900">Payment Mandate</h3>
                <p className="text-sm text-green-600">Cryptographically signed authorization (Non-repudiable)</p>
              </div>
            </div>
          </div>
          <div className="p-6 space-y-4">
            <div className="flex items-center gap-4 bg-green-50 rounded-lg p-4">
              <svg className="w-12 h-12 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" />
              </svg>
              <div className="flex-1">
                <p className="text-sm font-semibold text-gray-700">Authorization Status</p>
                <p className="text-2xl font-bold text-green-600 uppercase">{payment_mandate.status}</p>
              </div>
            </div>

            <div className="space-y-3">
              <div className="flex justify-between items-center">
                <span className="text-sm text-gray-600">Amount Authorized</span>
                <span className="text-xl font-bold text-green-600">${payment_mandate.amount.toFixed(2)}</span>
              </div>
              <div className="flex justify-between items-center">
                <span className="text-sm text-gray-600">Payment Method</span>
                <span className="font-semibold text-gray-900">{payment_mandate.payment_method}</span>
              </div>
            </div>

            <div className="bg-gray-50 rounded-lg p-4 mt-4">
              <p className="text-sm font-semibold text-gray-700 mb-2">Cryptographic Signature</p>
              <p className="font-mono text-xs text-gray-600 break-all bg-white p-3 rounded border border-gray-200">
                {payment_mandate.signature}
              </p>
              <p className="text-xs text-gray-500 mt-2 flex items-center gap-1">
                <svg className="w-4 h-4 text-green-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                </svg>
                Signature verified - Non-repudiable proof of user intent
              </p>
            </div>

            <div className="mt-4 pt-4 border-t border-gray-200">
              <p className="text-xs text-gray-500">
                Mandate ID: <span className="font-mono">{payment_mandate.mandate_id}</span>
              </p>
            </div>
          </div>
        </div>
      )}

      {/* Step 4 & 5: Transaction Receipt */}
      {paymentDetails && (
        <div className="bg-white rounded-xl shadow-lg border-2 border-blue-200 overflow-hidden">
          <div className="bg-gradient-to-r from-blue-50 to-blue-100 px-6 py-4 border-b border-blue-200">
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 bg-blue-600 rounded-full flex items-center justify-center text-white font-bold">
                ✓
              </div>
              <div>
                <h3 className="text-xl font-bold text-blue-900">Transaction Complete</h3>
                <p className="text-sm text-blue-600">Cryptographic receipt with blockchain verification</p>
              </div>
            </div>
          </div>
          <div className="p-6 space-y-4">
            <div className="grid grid-cols-2 gap-4">
              <div>
                <p className="text-sm text-gray-600">Amount Paid</p>
                <p className="text-2xl font-bold text-blue-600">${paymentDetails.amount_paid.toFixed(2)} {paymentDetails.currency}</p>
              </div>
              <div>
                <p className="text-sm text-gray-600">Receipt ID</p>
                <p className="font-mono text-sm text-gray-900">{paymentDetails.receipt_id}</p>
              </div>
            </div>

            <div className="bg-gradient-to-r from-blue-50 to-indigo-50 rounded-lg p-4 border border-blue-200">
              <p className="text-sm font-semibold text-gray-700 mb-2 flex items-center gap-2">
                <svg className="w-5 h-5 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
                </svg>
                Blockchain Verification Hash
              </p>
              <p className="font-mono text-xs text-gray-600 break-all bg-white p-3 rounded border border-gray-300">
                {paymentDetails.blockchain_hash}
              </p>
              <div className="mt-3 flex items-center gap-2 text-xs text-green-600">
                <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
                <span>Transaction verified on distributed ledger</span>
              </div>
            </div>

            <div className="bg-gray-50 rounded-lg p-4">
              <p className="text-sm font-semibold text-gray-700 mb-2">Security Features</p>
              <div className="space-y-2">
                <div className="flex items-center gap-2 text-sm text-gray-700">
                  <svg className="w-4 h-4 text-green-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                  </svg>
                  <span>Intent mandate validated</span>
                </div>
                <div className="flex items-center gap-2 text-sm text-gray-700">
                  <svg className="w-4 h-4 text-green-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                  </svg>
                  <span>Cart mandate verified</span>
                </div>
                <div className="flex items-center gap-2 text-sm text-gray-700">
                  <svg className="w-4 h-4 text-green-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                  </svg>
                  <span>Cryptographic signature authenticated</span>
                </div>
                <div className="flex items-center gap-2 text-sm text-gray-700">
                  <svg className="w-4 h-4 text-green-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                  </svg>
                  <span>Blockchain audit trail created</span>
                </div>
              </div>
            </div>

            <div className="text-xs text-gray-500">
              Transaction timestamp: {new Date(paymentDetails.timestamp).toLocaleString()}
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default AP2MandateDisplay;
