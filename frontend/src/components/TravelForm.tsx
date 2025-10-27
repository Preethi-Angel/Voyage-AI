import React, { useState } from 'react';
import type { TravelRequest } from '../types';

interface FormErrors {
  [key: string]: string;
}

interface TravelFormProps {
  onSubmit: (request: TravelRequest) => void;
  loading: boolean;
  initialValues?: Partial<TravelRequest>;
}

const INTERESTS_OPTIONS = [
  { value: 'food', label: 'Food & Dining' },
  { value: 'tech', label: 'Technology' },
  { value: 'temples', label: 'Temples & Culture' },
  { value: 'shopping', label: 'Shopping' },
  { value: 'nightlife', label: 'Nightlife' },
  { value: 'culture', label: 'Cultural Activities' },
];

export const TravelForm: React.FC<TravelFormProps> = ({ onSubmit, loading, initialValues }) => {
  const [formData, setFormData] = useState<TravelRequest>({
    destination: initialValues?.destination || 'Paris, France',
    duration_days: initialValues?.duration_days || 5,
    budget: initialValues?.budget || 3000,
    travelers: initialValues?.travelers || 2,
    interests: initialValues?.interests || ['food', 'culture'],
    hotel_preference: initialValues?.hotel_preference || 'mid-range',
    activity_level: initialValues?.activity_level || 'moderate',
    enable_logging: initialValues?.enable_logging ?? true,
  });

  const [errors, setErrors] = useState<FormErrors>({});

  const validate = (): boolean => {
    const newErrors: FormErrors = {};

    if (!formData.destination.trim()) {
      newErrors.destination = 'Destination is required';
    }

    if (formData.duration_days < 1 || formData.duration_days > 30) {
      newErrors.duration_days = 'Duration must be between 1 and 30 days';
    }

    if (formData.budget < 500) {
      newErrors.budget = 'Budget must be at least $500';
    }

    if (formData.travelers < 1 || formData.travelers > 10) {
      newErrors.travelers = 'Number of travelers must be between 1 and 10';
    }

    if (formData.interests.length === 0) {
      newErrors.interests = 'Select at least one interest';
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (validate()) {
      onSubmit(formData);
    }
  };

  const handleInterestToggle = (interest: string) => {
    setFormData(prev => ({
      ...prev,
      interests: prev.interests.includes(interest)
        ? prev.interests.filter(i => i !== interest)
        : [...prev.interests, interest]
    }));
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-6">
      {/* Top Row: Destination and Travelers */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2">
          <label className="label">Destination</label>
          <input
            type="text"
            value={formData.destination}
            onChange={(e) => setFormData({ ...formData, destination: e.target.value })}
            className="input-field"
            placeholder="e.g., Tokyo, Japan"
          />
          {errors.destination && <p className="text-red-500 text-sm mt-1">{errors.destination}</p>}
        </div>

        <div>
          <label className="label">Travelers</label>
          <input
            type="number"
            value={formData.travelers}
            onChange={(e) => setFormData({ ...formData, travelers: parseInt(e.target.value) })}
            className="input-field"
            min="1"
            max="10"
          />
          {errors.travelers && <p className="text-red-500 text-sm mt-1">{errors.travelers}</p>}
        </div>
      </div>

      {/* Second Row: Duration, Budget, Hotel, Activity */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <div>
          <label className="label">Duration (days)</label>
          <input
            type="number"
            value={formData.duration_days}
            onChange={(e) => setFormData({ ...formData, duration_days: parseInt(e.target.value) })}
            className="input-field"
            min="1"
            max="30"
          />
          {errors.duration_days && <p className="text-red-500 text-sm mt-1">{errors.duration_days}</p>}
        </div>

        <div>
          <label className="label">Budget (USD)</label>
          <input
            type="number"
            value={formData.budget}
            onChange={(e) => setFormData({ ...formData, budget: parseFloat(e.target.value) })}
            className="input-field"
            min="500"
            step="100"
          />
          {errors.budget && <p className="text-red-500 text-sm mt-1">{errors.budget}</p>}
        </div>

        <div>
          <label className="label">Hotel Preference</label>
          <select
            value={formData.hotel_preference}
            onChange={(e) => setFormData({ ...formData, hotel_preference: e.target.value as any })}
            className="select-field"
          >
            <option value="budget">Budget</option>
            <option value="mid-range">Mid-Range</option>
            <option value="luxury">Luxury</option>
          </select>
        </div>

        <div>
          <label className="label">Activity Level</label>
          <select
            value={formData.activity_level}
            onChange={(e) => setFormData({ ...formData, activity_level: e.target.value as any })}
            className="select-field"
          >
            <option value="low">Low</option>
            <option value="moderate">Moderate</option>
            <option value="high">High</option>
          </select>
        </div>
      </div>

      {/* Interests - Full Width */}
      <div>
        <label className="label">Interests</label>
        <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-3">
          {INTERESTS_OPTIONS.map(option => (
            <label
              key={option.value}
              className="flex items-center gap-2 cursor-pointer bg-white border-2 border-gray-200 rounded-lg px-4 py-3 hover:border-blue-500 hover:bg-blue-50 transition-all"
            >
              <input
                type="checkbox"
                checked={formData.interests.includes(option.value)}
                onChange={() => handleInterestToggle(option.value)}
                className="w-4 h-4 text-blue-600 rounded focus:ring-blue-500"
              />
              <span className="text-sm font-medium">{option.label}</span>
            </label>
          ))}
        </div>
        {errors.interests && <p className="text-red-500 text-sm mt-1">{errors.interests}</p>}
      </div>

      {/* Enable Logging */}
      <div className="flex items-center gap-3 bg-gray-50 border border-gray-200 rounded-lg px-4 py-3">
        <input
          type="checkbox"
          id="enable_logging"
          checked={formData.enable_logging}
          onChange={(e) => setFormData({ ...formData, enable_logging: e.target.checked })}
          className="w-4 h-4 text-blue-600 rounded focus:ring-blue-500"
        />
        <label htmlFor="enable_logging" className="text-sm cursor-pointer font-medium">
          Show agent communication logs
        </label>
      </div>

      {/* Submit Button */}
      <div className="flex justify-end">
        <button
          type="submit"
          disabled={loading}
          className="btn-primary py-3 px-8 text-lg"
        >
          {loading ? 'Planning your trip...' : 'Plan My Trip'}
        </button>
      </div>
    </form>
  );
};
