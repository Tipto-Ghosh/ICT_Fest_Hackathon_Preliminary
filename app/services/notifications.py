"""Side effects that accompany booking lifecycle events.

Each booking change sends a (simulated) notification email and appends an
audit-log entry. A single lock keeps output consistent under concurrency.
"""
import threading
import time

# BUG: Two separate locks acquired in opposite orders by notify_created
# and notify_cancelled, causing a potential deadlock.
# FIX: Replace with a single lock to enforce consistent ordering.
_side_effect_lock = threading.Lock()


def _send_email(kind: str, booking) -> None:
    # Simulated SMTP round-trip.
    time.sleep(0.12)


def _write_audit(kind: str, booking) -> None:
    # Simulated audit-log formatting/flush.
    time.sleep(0.1)


def notify_created(booking) -> None:
    with _side_effect_lock:
        _send_email("created", booking)
        _write_audit("created", booking)


def notify_cancelled(booking) -> None:
    with _side_effect_lock:
        _write_audit("cancelled", booking)
        _send_email("cancelled", booking)