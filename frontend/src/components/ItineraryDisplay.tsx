import React from 'react';
import type { TravelItinerary } from '../types';

interface ItineraryDisplayProps {
  itinerary: TravelItinerary;
}

export const ItineraryDisplay: React.FC<ItineraryDisplayProps> = ({ itinerary }) => {
  const {
    destination,
    duration_days,
    total_budget,
    actual_cost,
    within_budget,
    flights,
    hotel,
    activities,
    cost_breakdown,
  } = itinerary;

  return (
    <div className="space-y-6">
      {/* Trip Overview Header */}
      <div className="card bg-gradient-to-r from-blue-50 to-indigo-50 border-2 border-blue-200">
        <div className="flex items-center justify-between mb-6">
          <div>
            <div className="flex items-center gap-3 mb-2">
              <svg className="w-8 h-8 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3.055 11H5a2 2 0 012 2v1a2 2 0 002 2 2 2 0 012 2v2.945M8 3.935V5.5A2.5 2.5 0 0010.5 8h.5a2 2 0 012 2 2 2 0 104 0 2 2 0 012-2h1.064M15 20.488V18a2 2 0 012-2h3.064M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              <h3 className="text-3xl font-bold text-gray-900">{destination}</h3>
            </div>
            <p className="text-lg text-gray-600">{duration_days} day adventure</p>
          </div>
          <div className={`px-6 py-3 rounded-xl font-bold text-lg ${within_budget ? 'bg-green-100 text-green-700 border-2 border-green-300' : 'bg-red-100 text-red-700 border-2 border-red-300'}`}>
            {within_budget ? '✓ Within Budget' : '⚠ Over Budget'}
          </div>
        </div>

        <div className="grid grid-cols-3 gap-6">
          <div className="bg-white rounded-lg p-4 text-center shadow-sm">
            <p className="text-sm text-gray-500 mb-1">Your Budget</p>
            <p className="text-2xl font-bold text-gray-900">${total_budget.toLocaleString()}</p>
          </div>
          <div className="bg-white rounded-lg p-4 text-center shadow-sm">
            <p className="text-sm text-gray-500 mb-1">Total Cost</p>
            <p className={`text-2xl font-bold ${within_budget ? 'text-green-600' : 'text-red-600'}`}>
              ${actual_cost.toLocaleString()}
            </p>
          </div>
          <div className="bg-white rounded-lg p-4 text-center shadow-sm">
            <p className="text-sm text-gray-500 mb-1">{within_budget ? 'Savings' : 'Over Budget'}</p>
            <p className={`text-2xl font-bold ${within_budget ? 'text-green-600' : 'text-red-600'}`}>
              ${Math.abs(total_budget - actual_cost).toLocaleString()}
            </p>
          </div>
        </div>
      </div>

      {/* Flight & Hotel - 2 Column Grid */}
      <div className="grid md:grid-cols-2 gap-6">
        {/* Flight */}
        <div className="card bg-gradient-to-br from-sky-50 to-blue-50 border-2 border-blue-200">
          <div className="flex items-center gap-3 mb-4">
            <div className="bg-blue-600 rounded-lg p-2">
              <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 12h14M12 5l7 7-7 7" />
              </svg>
            </div>
            <h3 className="text-2xl font-bold text-gray-900">Flight</h3>
          </div>
          {flights ? (
            <div className="bg-white rounded-lg p-4 space-y-3">
              <div className="flex justify-between items-center pb-2 border-b">
                <span className="text-gray-600">Airline</span>
                <span className="font-semibold text-gray-900">{flights.airline}</span>
              </div>
              <div className="flex justify-between items-center pb-2 border-b">
                <span className="text-gray-600">Duration</span>
                <span className="font-semibold text-gray-900">{flights.duration}</span>
              </div>
              <div className="flex justify-between items-center pb-2 border-b">
                <span className="text-gray-600">Stops</span>
                <span className="font-semibold text-gray-900">{flights.stops === 0 ? 'Non-stop ✈️' : `${flights.stops} stop(s)`}</span>
              </div>
              <div className="flex justify-between items-center pt-2">
                <span className="text-gray-600 font-medium">Price per person</span>
                <span className="font-bold text-xl text-blue-600">${flights.price}</span>
              </div>
            </div>
          ) : (
            <div className="bg-white rounded-lg p-8 text-center">
              <svg className="w-12 h-12 text-gray-300 mx-auto mb-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              <p className="text-gray-500">No flights available</p>
            </div>
          )}
        </div>

        {/* Hotel */}
        <div className="card bg-gradient-to-br from-purple-50 to-pink-50 border-2 border-purple-200">
          <div className="flex items-center gap-3 mb-4">
            <div className="bg-purple-600 rounded-lg p-2">
              <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6" />
              </svg>
            </div>
            <h3 className="text-2xl font-bold text-gray-900">Hotel</h3>
          </div>
          <div className="bg-white rounded-lg p-4 space-y-3">
            <div className="pb-3 border-b">
              <p className="text-xl font-bold text-gray-900">{hotel.name}</p>
              <p className="text-sm text-gray-600 mt-1">{hotel.location}</p>
            </div>
            <div className="flex justify-between items-center pb-2 border-b">
              <span className="text-gray-600">Rating</span>
              <span className="font-semibold text-yellow-600">⭐ {hotel.rating}/5</span>
            </div>
            <div className="flex justify-between items-center pb-2 border-b">
              <span className="text-gray-600">Per Night</span>
              <span className="font-semibold text-gray-900">${hotel.price_per_night}</span>
            </div>
            <div className="flex justify-between items-center pb-3 border-b">
              <span className="text-gray-600">{duration_days} nights</span>
              <span className="font-bold text-xl text-purple-600">${hotel.total_price}</span>
            </div>
            <div>
              <p className="font-semibold text-gray-700 mb-2">Amenities</p>
              <div className="flex flex-wrap gap-2">
                {hotel.amenities.map((amenity, idx) => (
                  <span key={idx} className="px-3 py-1 bg-purple-100 text-purple-700 rounded-full text-xs font-medium">
                    {amenity}
                  </span>
                ))}
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Activities */}
      <div className="card bg-gradient-to-br from-orange-50 to-amber-50 border-2 border-orange-200">
        <div className="flex items-center gap-3 mb-4">
          <div className="bg-orange-600 rounded-lg p-2">
            <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M14.828 14.828a4 4 0 01-5.656 0M9 10h.01M15 10h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
          </div>
          <h3 className="text-2xl font-bold text-gray-900">Activities & Experiences</h3>
          <span className="ml-auto bg-orange-600 text-white px-3 py-1 rounded-full text-sm font-bold">{activities.length} activities</span>
        </div>
        <div className="grid md:grid-cols-2 gap-4">
          {activities.map((activity, idx) => (
            <div key={idx} className="bg-white rounded-lg p-4 border-l-4 border-orange-500 shadow-sm hover:shadow-md transition-shadow">
              <div className="flex items-start justify-between mb-2">
                <p className="font-bold text-lg text-gray-900 flex-1">{activity.name}</p>
                <span className="bg-orange-100 text-orange-700 px-3 py-1 rounded-full text-sm font-bold ml-2">${activity.cost}</span>
              </div>
              <p className="text-sm text-gray-600 mb-3">{activity.description}</p>
              <div className="flex items-center gap-4 text-sm">
                <span className="flex items-center gap-1 text-blue-600">
                  <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 7h.01M7 3h5c.512 0 1.024.195 1.414.586l7 7a2 2 0 010 2.828l-7 7a2 2 0 01-2.828 0l-7-7A1.994 1.994 0 013 12V7a4 4 0 014-4z" />
                  </svg>
                  {activity.category}
                </span>
                <span className="flex items-center gap-1 text-gray-600">
                  <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                  {activity.duration}
                </span>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Cost Breakdown */}
      <div className="card bg-gradient-to-br from-green-50 to-emerald-50 border-2 border-green-200">
        <div className="flex items-center gap-3 mb-4">
          <div className="bg-green-600 rounded-lg p-2">
            <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 7h6m0 10v-3m-3 3h.01M9 17h.01M9 14h.01M12 14h.01M15 11h.01M12 11h.01M9 11h.01M7 21h10a2 2 0 002-2V5a2 2 0 00-2-2H7a2 2 0 00-2 2v14a2 2 0 002 2z" />
            </svg>
          </div>
          <h3 className="text-2xl font-bold text-gray-900">Cost Breakdown</h3>
        </div>
        <div className="bg-white rounded-lg p-4">
          <div className="space-y-3">
            {Object.entries(cost_breakdown).map(([category, cost]) => (
              <div key={category} className="flex justify-between items-center py-2 border-b border-gray-100">
                <span className="capitalize font-medium text-gray-700">{category}</span>
                <span className="font-semibold text-gray-900">${(cost as number).toLocaleString()}</span>
              </div>
            ))}
            <div className="flex justify-between items-center pt-3 text-xl">
              <span className="font-bold text-gray-900">Total Cost</span>
              <span className={`font-bold ${within_budget ? 'text-green-600' : 'text-red-600'}`}>
                ${actual_cost.toLocaleString()}
              </span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
