"""Regression tests for ticket booking behavior and secure replacements."""

from contextlib import redirect_stdout
from copy import deepcopy
from io import StringIO
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

import ticket_booking_system as booking


class TicketBookingTests(unittest.TestCase):
    """Restore mutable seating state around every test."""

    def setUp(self):
        self.original_seats = deepcopy(booking.theater_seats)
        booking.theater_seats = {
            "A1": {"tier": "Standard", "price": 12.0, "is_sold": False},
            "A2": {"tier": "Standard", "price": 12.0, "is_sold": True},
            "B1": {"tier": "Premium", "price": 20.0, "is_sold": False},
        }

    def tearDown(self):
        booking.theater_seats = self.original_seats

    def test_reservation_updates_seat_and_history(self):
        history = []
        self.assertTrue(booking.reserve_seat("A1", "Customer", history))
        self.assertFalse(booking.check_seat_status("A1"))
        self.assertEqual(history, ["Reserved seat A1 for customer Customer"])

    def test_sold_and_unknown_seats_do_not_change_history(self):
        history = []
        self.assertFalse(booking.reserve_seat("A2", "Customer", history))
        self.assertFalse(booking.reserve_seat("Z9", "Customer", history))
        self.assertEqual(history, [])

    def test_no_shared_default_history(self):
        self.assertEqual(booking.reserve_seat.__defaults__, (None,))
        self.assertTrue(booking.reserve_seat("A1", "First"))
        history = []
        self.assertTrue(booking.reserve_seat("B1", "Second", history))
        self.assertEqual(history, ["Reserved seat B1 for customer Second"])

    def test_cancellation_makes_seat_available(self):
        self.assertTrue(booking.cancel_seat("A2"))
        self.assertTrue(booking.check_seat_status("A2"))

    def test_unknown_seat_cancellation_returns_false(self):
        self.assertFalse(booking.cancel_seat("Z9"))
        self.assertFalse(booking.check_seat_status("Z9"))

    def test_unexpected_data_errors_are_not_swallowed(self):
        booking.theater_seats["A2"] = None
        with self.assertRaises(TypeError):
            booking.cancel_seat("A2")

    def test_discount_and_rounding(self):
        self.assertEqual(
            booking.compute_discounted_price("B1", "base_price * 0.80"), 16.0
        )
        self.assertEqual(
            booking.compute_discounted_price("A1", "base_price * 0.333"), 4.0
        )

    def test_discount_boundaries(self):
        self.assertEqual(
            booking.compute_discounted_price("B1", "base_price * 0"), 0.0
        )
        self.assertEqual(
            booking.compute_discounted_price("B1", "base_price * 1.00"), 20.0
        )

    def test_bad_promotions_are_rejected(self):
        for expression in (
            "base_price * -0.2", "base_price * 1.2", "base_price + 1",
            "base_price / 0", "unknown_name * 0.8", "", "0" * 65,
        ):
            with self.subTest(expression=expression):
                with self.assertRaises(ValueError):
                    booking.compute_discounted_price("B1", expression)

    def test_discount_for_unknown_seat_raises_key_error(self):
        with self.assertRaises(KeyError):
            booking.compute_discounted_price("Z9", "base_price * 0.8")

    def test_sha256_ticket_digest(self):
        self.assertEqual(
            booking.generate_ticket_hash("abc"),
            "ba7816bf8f01cfea414140de5dae2223"
            "b00361a396177a9cb410ff61f20015ad",
        )
        self.assertNotEqual(
            booking.generate_ticket_hash("abc"),
            booking.generate_ticket_hash("abcd"),
        )

    def test_secure_pin_bounds(self):
        for random_value, expected in ((0, 1000), (8999, 9999)):
            with patch.object(booking.secrets, "randbelow",
                              return_value=random_value) as random_source:
                self.assertEqual(booking.generate_booking_pin(), expected)
                random_source.assert_called_once_with(9000)

    def test_chart_export_treats_filename_as_data(self):
        with tempfile.TemporaryDirectory() as temporary_dir:
            filename = Path(temporary_dir) / "seating chart & draft.txt"
            output = StringIO()
            with redirect_stdout(output):
                booking.export_seating_chart(filename)
            self.assertEqual(filename.read_text(encoding="utf-8"),
                             str(booking.theater_seats))
            self.assertIn(str(filename), output.getvalue())
            self.assertEqual(len(list(Path(temporary_dir).iterdir())), 1)

    def test_summary_for_supplied_map(self):
        self.assertEqual(booking.get_theater_summary(booking.theater_seats), 1)
        booking.reserve_seat("A1", "Customer")
        self.assertEqual(booking.get_theater_summary(booking.theater_seats), 2)
        self.assertEqual(booking.get_theater_summary({}), 0)

    def test_import_has_no_output_or_file_side_effects(self):
        module_dir = str(Path(booking.__file__).resolve().parent)
        with tempfile.TemporaryDirectory() as temporary_dir:
            result = subprocess.run(
                [sys.executable, "-c",
                 f"import sys; sys.path.insert(0, {module_dir!r}); "
                 "import ticket_booking_system"],
                cwd=temporary_dir, capture_output=True, text=True, check=True,
            )
            self.assertEqual(result.stdout, "")
            self.assertEqual(result.stderr, "")
            self.assertEqual(list(Path(temporary_dir).iterdir()), [])


if __name__ == "__main__":
    unittest.main()
