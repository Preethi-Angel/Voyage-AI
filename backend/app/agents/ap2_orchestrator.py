"""
Stage 4: AP2 (Agents Payments Protocol) Integration
Demonstrates how AI agents can handle autonomous payments with user verification.

AP2 Concepts Demonstrated:
1. Intent Mandate - Agent declares purchase intent
2. Cart Mandate - Itemized breakdown with costs
3. Payment Mandate - Cryptographically signed payment authorization
4. Transaction Execution - Actual payment processing with audit trail
"""

import asyncio
import json
import os
from datetime import datetime
from typing import List, Dict, Any, AsyncGenerator
from dataclasses import dataclass, asdict
import hashlib
import uuid

from app.models.requests import MultiAgentRequest


@dataclass
class IntentMandate:
    """
    AP2 Intent Mandate - Declares what the agent intends to purchase.
    This is the first step in the AP2 protocol.
    """
    intent_id: str
    agent_id: str
    user_id: str
    description: str
    timestamp: str
    items_to_purchase: List[str]
    estimated_total: float

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class CartItem:
    """Individual item in the shopping cart."""
    item_id: str
    name: str
    description: str
    quantity: int
    unit_price: float
    total_price: float
    vendor: str


@dataclass
class CartMandate:
    """
    AP2 Cart Mandate - Itemized breakdown of all purchases.
    Provides transparency before payment authorization.
    """
    cart_id: str
    intent_id: str
    items: List[CartItem]
    subtotal: float
    taxes: float
    fees: float
    total: float
    timestamp: str

    def to_dict(self) -> Dict[str, Any]:
        return {
            "cart_id": self.cart_id,
            "intent_id": self.intent_id,
            "items": [asdict(item) for item in self.items],
            "subtotal": self.subtotal,
            "taxes": self.taxes,
            "fees": self.fees,
            "total": self.total,
            "timestamp": self.timestamp
        }


@dataclass
class PaymentMandate:
    """
    AP2 Payment Mandate - Cryptographically signed authorization.
    Non-repudiable proof of user's intent to pay.
    """
    mandate_id: str
    cart_id: str
    user_id: str
    amount: float
    currency: str
    payment_method: str
    timestamp: str
    signature: str  # In production, this would be a real cryptographic signature
    status: str  # pending, authorized, denied, executed, failed

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class TransactionReceipt:
    """Transaction receipt with full audit trail."""
    receipt_id: str
    mandate_id: str
    amount_paid: float
    currency: str
    timestamp: str
    items_purchased: List[Dict[str, Any]]
    status: str
    blockchain_hash: str  # Simulated blockchain verification


class AP2Orchestrator:
    """
    AP2 Payment Protocol Orchestrator

    Demonstrates the complete AP2 flow:
    1. Agent analyzes travel request
    2. Creates Intent Mandate (what to buy)
    3. Builds Cart Mandate (itemized costs)
    4. Requests Payment Mandate (user approval)
    5. Executes transaction (with verification)
    6. Returns receipt (with audit trail)
    """

    def __init__(self, region_name: str = None):
        self.region_name = region_name or os.getenv("AWS_REGION", "us-east-1")
        self.user_id = "demo_user_001"
        self.agent_id = "ap2_travel_agent_001"
        self.mock_wallet_balance = float(os.getenv("AP2_WALLET_BALANCE", "10000.00"))
        self.execution_logs = []

    def _log_event(self, event_type: str, agent_name: str, message: str, data: Dict[str, Any] = None):
        """Log events for streaming to frontend."""
        log_entry = {
            "type": event_type,
            "agent_name": agent_name,
            "message": message,
            "timestamp": datetime.utcnow().isoformat(),
        }
        if data:
            log_entry["data"] = data
        self.execution_logs.append(log_entry)

    def _generate_signature(self, data: str) -> str:
        """
        Generate a cryptographic signature (simulated).
        In production, this would use real cryptographic signing.
        """
        return hashlib.sha256(f"{data}{self.user_id}{datetime.utcnow().isoformat()}".encode()).hexdigest()

    def _create_intent_mandate(self, request: MultiAgentRequest) -> IntentMandate:
        """
        Step 1: Create Intent Mandate
        Agent declares its intention to make purchases.
        """
        intent_id = f"intent_{uuid.uuid4().hex[:8]}"

        items_to_purchase = [
            f"Round-trip flights to {request.destination}",
            f"{request.hotel_preference} hotel for {request.duration_days} nights",
            f"Activities: {', '.join(request.interests or ['general sightseeing'])}"
        ]

        intent = IntentMandate(
            intent_id=intent_id,
            agent_id=self.agent_id,
            user_id=self.user_id,
            description=f"{request.duration_days}-day trip to {request.destination} for {request.travelers} travelers",
            timestamp=datetime.utcnow().isoformat(),
            items_to_purchase=items_to_purchase,
            estimated_total=float(request.budget)
        )

        self._log_event(
            "log",
            "AP2 Intent Mandate",
            f"📋 Step 1/5: Intent declared - {intent.description}",
            intent.to_dict()
        )

        return intent

    def _build_cart_mandate(self, intent: IntentMandate, request: MultiAgentRequest) -> CartMandate:
        """
        Step 2: Build Cart Mandate
        Create itemized breakdown with actual pricing.
        """
        cart_id = f"cart_{uuid.uuid4().hex[:8]}"

        # Simulate pricing (in production, these would come from real vendors)
        flight_price = request.budget * 0.35
        hotel_price = request.budget * 0.30
        activities_price = request.budget * 0.20

        cart_items = [
            CartItem(
                item_id=f"flight_{uuid.uuid4().hex[:6]}",
                name=f"Round-trip flights to {request.destination}",
                description=f"Economy class for {request.travelers} travelers",
                quantity=request.travelers,
                unit_price=flight_price / request.travelers,
                total_price=flight_price,
                vendor="GlobalAir"
            ),
            CartItem(
                item_id=f"hotel_{uuid.uuid4().hex[:6]}",
                name=f"{request.hotel_preference.title()} Hotel",
                description=f"{request.duration_days} nights in {request.destination}",
                quantity=request.duration_days,
                unit_price=hotel_price / request.duration_days,
                total_price=hotel_price,
                vendor="TravelStay"
            ),
            CartItem(
                item_id=f"activities_{uuid.uuid4().hex[:6]}",
                name="Activities Package",
                description=f"Curated activities: {', '.join(request.interests or ['sightseeing'])}",
                quantity=1,
                unit_price=activities_price,
                total_price=activities_price,
                vendor="LocalExperiences"
            )
        ]

        subtotal = sum(item.total_price for item in cart_items)
        taxes = subtotal * 0.08  # 8% tax
        fees = 25.00  # Processing fee
        total = subtotal + taxes + fees

        cart = CartMandate(
            cart_id=cart_id,
            intent_id=intent.intent_id,
            items=cart_items,
            subtotal=subtotal,
            taxes=taxes,
            fees=fees,
            total=total,
            timestamp=datetime.utcnow().isoformat()
        )

        self._log_event(
            "log",
            "AP2 Cart Mandate",
            f"🛒 Step 2/5: Cart created with {len(cart_items)} items - Total: ${total:.2f}",
            cart.to_dict()
        )

        return cart

    def _request_payment_authorization(self, cart: CartMandate) -> PaymentMandate:
        """
        Step 3: Request Payment Authorization
        Create payment mandate and request user approval.
        """
        mandate_id = f"mandate_{uuid.uuid4().hex[:8]}"

        # Generate cryptographic signature
        signature_data = f"{mandate_id}{cart.cart_id}{cart.total}{self.user_id}"
        signature = self._generate_signature(signature_data)

        # Simulate user authorization check
        authorized = cart.total <= self.mock_wallet_balance

        mandate = PaymentMandate(
            mandate_id=mandate_id,
            cart_id=cart.cart_id,
            user_id=self.user_id,
            amount=cart.total,
            currency="USD",
            payment_method="AP2_Wallet",
            timestamp=datetime.utcnow().isoformat(),
            signature=signature,
            status="authorized" if authorized else "denied"
        )

        if authorized:
            self._log_event(
                "log",
                "AP2 Payment Mandate",
                f"🔐 Step 3/5: Payment authorized - ${cart.total:.2f} (Balance: ${self.mock_wallet_balance:.2f})",
                {"mandate": mandate.to_dict(), "signature": signature[:16] + "..."}
            )
        else:
            self._log_event(
                "log",
                "AP2 Payment Mandate",
                f"❌ Step 3/5: Payment denied - Insufficient funds (Required: ${cart.total:.2f}, Balance: ${self.mock_wallet_balance:.2f})",
                mandate.to_dict()
            )

        return mandate

    def _execute_transaction(self, mandate: PaymentMandate, cart: CartMandate) -> TransactionReceipt:
        """
        Step 4: Execute Transaction
        Process the payment and generate receipt with audit trail.
        """
        receipt_id = f"receipt_{uuid.uuid4().hex[:8]}"

        # Simulate blockchain verification hash
        blockchain_data = f"{receipt_id}{mandate.mandate_id}{mandate.amount}{datetime.utcnow().isoformat()}"
        blockchain_hash = hashlib.sha256(blockchain_data.encode()).hexdigest()

        receipt = TransactionReceipt(
            receipt_id=receipt_id,
            mandate_id=mandate.mandate_id,
            amount_paid=mandate.amount,
            currency=mandate.currency,
            timestamp=datetime.utcnow().isoformat(),
            items_purchased=[asdict(item) for item in cart.items],
            status="completed",
            blockchain_hash=blockchain_hash
        )

        self._log_event(
            "log",
            "AP2 Transaction",
            f"💳 Step 4/5: Transaction executed - ${mandate.amount:.2f} charged",
            {
                "receipt_id": receipt_id,
                "blockchain_hash": blockchain_hash[:16] + "...",
                "items_count": len(cart.items)
            }
        )

        # Update wallet balance
        self.mock_wallet_balance -= mandate.amount

        self._log_event(
            "log",
            "AP2 Receipt",
            f"📧 Step 5/5: Receipt generated - Blockchain verified",
            {
                "receipt_id": receipt_id,
                "blockchain_hash": blockchain_hash[:32] + "...",
                "wallet_balance": self.mock_wallet_balance
            }
        )

        return receipt

    async def plan_trip_with_ap2_stream(self, request: MultiAgentRequest) -> AsyncGenerator[Dict[str, Any], None]:
        """
        Stream the complete AP2 payment flow.
        Demonstrates autonomous agent payments with full transparency.
        """
        self.execution_logs = []

        try:
            # Header
            self._log_event(
                "log",
                "AP2 Protocol",
                f"🚀 Initiating AP2 Autonomous Payment Protocol for {request.destination} trip",
                {"protocol_version": "1.0", "agent_id": self.agent_id}
            )

            # Yield initial logs
            for log in self.execution_logs:
                yield log
                await asyncio.sleep(0.3)
            self.execution_logs = []

            # Step 1: Intent Mandate
            await asyncio.sleep(0.5)
            intent = self._create_intent_mandate(request)
            for log in self.execution_logs:
                yield log
                await asyncio.sleep(0.3)
            self.execution_logs = []

            # Step 2: Cart Mandate
            await asyncio.sleep(0.5)
            cart = self._build_cart_mandate(intent, request)
            for log in self.execution_logs:
                yield log
                await asyncio.sleep(0.3)
            self.execution_logs = []

            # Step 3: Payment Authorization
            await asyncio.sleep(0.5)
            mandate = self._request_payment_authorization(cart)
            for log in self.execution_logs:
                yield log
                await asyncio.sleep(0.3)
            self.execution_logs = []

            if mandate.status != "authorized":
                # Payment denied
                yield {
                    "type": "error",
                    "message": f"Payment authorization denied: Insufficient funds",
                    "timestamp": datetime.utcnow().isoformat()
                }
                return

            # Step 4: Execute Transaction
            await asyncio.sleep(0.5)
            receipt = self._execute_transaction(mandate, cart)
            for log in self.execution_logs:
                yield log
                await asyncio.sleep(0.3)
            self.execution_logs = []

            # Final Result
            await asyncio.sleep(0.5)
            result = {
                "type": "result",
                "data": {
                    "success": True,
                    "trip_details": {
                        "destination": request.destination,
                        "duration": request.duration_days,
                        "travelers": request.travelers,
                        "total_cost": cart.total
                    },
                    "payment_details": {
                        "receipt_id": receipt.receipt_id,
                        "amount_paid": receipt.amount_paid,
                        "currency": receipt.currency,
                        "blockchain_hash": receipt.blockchain_hash,
                        "timestamp": receipt.timestamp
                    },
                    "ap2_mandates": {
                        "intent_mandate": intent.to_dict(),
                        "cart_mandate": cart.to_dict(),
                        "payment_mandate": mandate.to_dict()
                    },
                    "items_purchased": receipt.items_purchased,
                    "wallet_balance": self.mock_wallet_balance
                },
                "timestamp": datetime.utcnow().isoformat()
            }

            yield result

        except Exception as e:
            yield {
                "type": "error",
                "message": f"AP2 orchestration error: {str(e)}",
                "timestamp": datetime.utcnow().isoformat()
            }
