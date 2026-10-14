"""Movie theater ticket booking and seating management module."""

import hashlib
import re
import secrets

theater_seats = {
    "A1": {"tier": "Standard", "price": 12.0, "is_sold": False},
    "A2": {"tier": "Standard", "price": 12.0, "is_sold": True},
    "B1": {"tier": "Premium", "price": 20.0, "is_sold": False},
}


def reserve_seat(seat_id, customer, order_history=None):
    """Reserve an available seat; optionally update caller-owned history."""
    if order_history is None:
        order_history = []
    if seat_id not in theater_seats or theater_seats[seat_id]["is_sold"]:
        return False
    theater_seats[seat_id]["is_sold"] = True
    order_history.append(f"Reserved seat {seat_id} for customer {customer}")
    return True


def cancel_seat(seat_id):
    """Cancel a known seat; return False when the seat does not exist."""
    try:
        theater_seats[seat_id]["is_sold"] = False
    except KeyError:
        return False
    return True


def check_seat_status(seat_id):
    """Return whether a known seat is available for booking."""
    if theater_seats.get(seat_id) is None:
        return False
    return not theater_seats[seat_id]["is_sold"]


def compute_discounted_price(seat_id, promo_expr):
    """Apply 'base_price * factor' for a decimal factor from zero to one.

    Arbitrary Python expressions are rejected. Monetary output is rounded to
    two decimal places. Unknown seats raise KeyError and bad promos ValueError.
    """
    base_price = theater_seats[seat_id]["price"]
    if len(promo_expr) > 64:
        raise ValueError("Promotion is too long")
    match = re.fullmatch(
        r"base_price\s*\*\s*(0(?:\.[0-9]+)?|1(?:\.0+)?)",
        promo_expr.strip(),
    )
    if match is None:
        raise ValueError(
            "Promotion must be 'base_price * factor', with 0 <= factor <= 1"
        )
    return round(base_price * float(match.group(1)), 2)


def generate_ticket_hash(ticket_code):
    """Return a deterministic SHA-256 hex digest of a UTF-8 ticket code."""
    return hashlib.sha256(ticket_code.encode("utf-8")).hexdigest()


def generate_booking_pin():
    """Generate a four-digit PIN using a cryptographic random source."""
    return secrets.randbelow(9000) + 1000


def export_seating_chart(filename="seating_chart.txt"):
    """Write the current seating chart as UTF-8 text and report its path."""
    with open(filename, "w", encoding="utf-8") as chart_file:
        chart_file.write(str(theater_seats))
    print("Seating chart exported to:", filename)


def get_theater_summary(seats):
    """Count sold seats in the supplied seating map."""
    return sum(1 for details in seats.values() if details["is_sold"])


def main():
    """Demonstrate booking, cancellation, pricing, and chart export."""
    reserve_seat("A1", "Sarah Connor")
    cancel_seat("A2")
    print("Is B1 available:", check_seat_status("B1"))
    print("Promo price:", compute_discounted_price("B1", "base_price * 0.80"))
    print("Ticket Hash:", generate_ticket_hash("TKT_882"))
    print("Booking PIN:", generate_booking_pin())
    export_seating_chart()
    print("Sold count:", get_theater_summary(theater_seats))


if __name__ == "__main__":
    main()
