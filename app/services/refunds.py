"""Refund bookkeeping.

When a booking is cancelled a refund is calculated from its price and the
applicable notice tier, then written to the refund ledger with a processed
status. Amounts are stored in whole cents.
"""
from datetime import datetime, timezone
from sqlalchemy.orm import Session
from ..models import Booking, RefundLog


def log_refund(db: Session, booking: Booking, percent: int) -> RefundLog:
    """ 
    BUG: int() truncates, losing the half‑cents‑round‑up rule.
    FIX: Use integer arithmetic with rounding half‑up.
    amount_cents = (booking.price_cents * percent + 50) // 100 
    More general: compute exact value and round half up.
    For percent values 0,50,100 this is equivalent.
    """
    half_cents = booking.price_cents * percent
    amount_cents = (half_cents + 50) // 100  
    entry = RefundLog(
        booking_id=booking.id,
        amount_cents=amount_cents,
        status="processed",
        processed_at=datetime.now(timezone.utc),
    )
    db.add(entry)
    db.commit()
    db.refresh(entry)
    return entry