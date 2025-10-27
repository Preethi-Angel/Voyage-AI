// API Request Types
export interface TravelRequest {
  destination: string;
  duration_days: number;
  budget: number;
  travelers: number;
  interests: string[];
  hotel_preference?: 'budget' | 'mid-range' | 'luxury';
  activity_level?: 'low' | 'moderate' | 'high';
  enable_logging?: boolean;
}

// API Response Types
export interface FlightOption {
  airline: string;
  departure_time: string;
  arrival_time: string;
  duration: string;
  price: number;
  stops: number;
}

export interface HotelOption {
  name: string;
  location: string;
  price_per_night: number;
  total_price: number;
  rating: number;
  amenities: string[];
}

export interface ActivityOption {
  name: string;
  description: string;
  cost: number;
  duration: string;
  category: string;
}

export interface CostBreakdown {
  flights: number;
  accommodation: number;
  activities: number;
  food: number;
  misc: number;
}

export interface TravelItinerary {
  destination: string;
  duration_days: number;
  total_budget: number;
  actual_cost: number;
  within_budget: boolean;
  flights: FlightOption;
  hotel: HotelOption;
  activities: ActivityOption[];
  daily_plan: any | null;
  cost_breakdown: CostBreakdown;
}

export interface AgentLog {
  agent_name: string;
  timestamp: string;
  message: string;
  data?: Record<string, any>;
}

export type AgentStatus = 'success' | 'error' | 'warning';

export interface ApiResponse {
  success: boolean;
  message: string;
  execution_time_ms: number;
  timestamp: string;
  status: AgentStatus;
  itinerary: TravelItinerary | null;
  agent_logs?: AgentLog[];
  agents_used?: string[];
  collaboration_count?: number;
  // AP2-specific fields
  payment_details?: {
    receipt_id: string;
    amount_paid: number;
    currency: string;
    blockchain_hash: string;
    timestamp: string;
  };
  ap2_mandates?: {
    intent_mandate: any;
    cart_mandate: any;
    payment_mandate: any;
  };
  items_purchased?: any[];
  wallet_balance?: number;
}

// Form Types
export interface FormErrors {
  [key: string]: string;
}
