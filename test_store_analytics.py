"""
test_store_analytics.py

Starter file for the "write your own tests" exercise.

pytest and the module under test are already imported below, and there's
one fully-worked example test to show you the pattern. Everything after
that is up to you: add your own test functions (name them test_something)
that check store_analytics.py against its docstrings.

Run your tests from this folder with:
    pytest -v
"""

import pytest
from store_analytics import (
    parse_order_row,
    compute_line_total,
    summarize_by_product,
    top_n_products,
    apply_bulk_discount,
    loyalty_tier,
    load_orders_from_csv,
    write_top_products_report,
)


# --- Example test (already written for you) -------------------------------

def test_parse_order_row_valid_row():
    row = ["1001", "Widget", "4", "9.99", "alice@example.com"]
    order = parse_order_row(row)
    assert order == {
        "order_id": "1001",
        "product": "widget",
        "quantity": 4,
        "unit_price": 9.99,
        "customer_email": "alice@example.com",
    }


# --- Your tests go below here ----------------------------------------------
#
# The example above checks the happy path. The interesting behavior in a
# parser, though, lives in the *transformations* it promises and the bad
# input it promises to reject -- so most of what follows targets those.


# --- parse_order_row: the cleaning promises --------------------------------

def test_parse_order_row_strips_and_lowercases_product():
    """The docstring promises product is stripped AND lowercased. Worth its
    own test because the example row ("Widget") only exercised the casing --
    it had no surrounding whitespace, so stripping was never actually
    checked. Here the product has both leading/trailing spaces and mixed
    case, so a regression in either transformation fails this."""
    row = ["1002", "  Super WIDGET  ", "1", "5.00", "x@y.com"]
    order = parse_order_row(row)
    assert order["product"] == "super widget"


def test_parse_order_row_rounds_unit_price_to_two_decimals():
    """unit_price is documented as rounded to 2 decimals. A raw price with
    more precision must not leak through unrounded."""
    row = ["1003", "widget", "2", "3.14159", "x@y.com"]
    order = parse_order_row(row)
    assert order["unit_price"] == 3.14


# --- parse_order_row: the rejection promises -------------------------------

def test_parse_order_row_rejects_wrong_field_count():
    """Fewer than 5 fields must raise -- this guards against a malformed CSV
    row silently producing a half-built dict."""
    with pytest.raises(ValueError):
        parse_order_row(["1004", "widget", "2", "3.00"])  # only 4 fields


def test_parse_order_row_rejects_empty_order_id():
    """order_id is checked *after* stripping, so a field of pure whitespace
    must still be treated as empty and rejected."""
    with pytest.raises(ValueError):
        parse_order_row(["   ", "widget", "2", "3.00", "x@y.com"])


def test_parse_order_row_rejects_empty_product():
    """Same stripping rule, but for product -- a separate branch in the code,
    so it deserves its own case rather than being assumed from the order_id
    test."""
    with pytest.raises(ValueError):
        parse_order_row(["1005", "  ", "2", "3.00", "x@y.com"])


def test_parse_order_row_rejects_non_integer_quantity():
    """"2.5" parses fine as a float but not as a whole number. This is the
    sneaky case: int("2.5") raises, so the docstring's "whole number" rule
    must reject it rather than silently truncating to 2."""
    with pytest.raises(ValueError):
        parse_order_row(["1006", "widget", "2.5", "3.00", "x@y.com"])


def test_parse_order_row_rejects_zero_quantity():
    """quantity must be strictly positive. Zero is the boundary the "<= 0"
    check exists for, and it's easy to get wrong with a "< 0" typo."""
    with pytest.raises(ValueError):
        parse_order_row(["1007", "widget", "0", "3.00", "x@y.com"])


def test_parse_order_row_rejects_negative_unit_price():
    """A negative price is nonsensical for an order and is explicitly
    forbidden. (Note 0.0 is allowed, so we test the negative side.)"""
    with pytest.raises(ValueError):
        parse_order_row(["1008", "widget", "2", "-1.00", "x@y.com"])


def test_parse_order_row_accepts_zero_unit_price():
    """The flip side of the rule above: zero is documented as valid ("zero or
    positive"), so a free item must NOT raise. Pins down the boundary so a
    stricter-than-spec check can't creep in."""
    order = parse_order_row(["1009", "freebie", "1", "0", "x@y.com"])
    assert order["unit_price"] == 0.0


# --- compute_line_total ----------------------------------------------------

def test_compute_line_total_multiplies_and_rounds():
    """quantity * unit_price, rounded to 2 dp. 7 * 3.333 = 23.331, whose
    third decimal forces the rounding step to actually run -- a plain
    multiply-without-round would return 23.331 and fail here."""
    order = {"quantity": 7, "unit_price": 3.333}
    assert compute_line_total(order) == 23.33


# --- summarize_by_product --------------------------------------------------

def test_summarize_by_product_aggregates_repeated_products():
    """The whole point of the summary is aggregation across rows. Two orders
    of the same product must fold into one entry with summed quantity,
    summed revenue, and an order_count of 2 -- while a different product
    stays separate."""
    orders = [
        {"product": "widget", "quantity": 2, "unit_price": 10.0},
        {"product": "widget", "quantity": 3, "unit_price": 10.0},
        {"product": "gadget", "quantity": 1, "unit_price": 4.0},
    ]
    summary = summarize_by_product(orders)
    assert summary["widget"] == {
        "total_quantity": 5,
        "total_revenue": 50.0,
        "order_count": 2,
    }
    assert summary["gadget"]["order_count"] == 1


def test_summarize_by_product_empty_input_returns_empty_dict():
    """Documented edge case: no orders -> {}. A common off-by-one is to
    return None or raise on empty input."""
    assert summarize_by_product([]) == {}


# --- top_n_products --------------------------------------------------------

def test_top_n_products_ranks_by_revenue_with_alphabetical_tiebreak():
    """Two things at once, because they interact: highest revenue first, and
    when revenue ties, product name ascending. "apple" and "zebra" share
    revenue 100, so the tiebreak must put apple before zebra even though
    zebra was inserted first."""
    summary = {
        "zebra": {"total_quantity": 1, "total_revenue": 100.0, "order_count": 1},
        "middle": {"total_quantity": 1, "total_revenue": 250.0, "order_count": 1},
        "apple": {"total_quantity": 1, "total_revenue": 100.0, "order_count": 1},
    }
    result = top_n_products(summary, n=3)
    products = [name for name, _ in result]
    assert products == ["middle", "apple", "zebra"]


def test_top_n_products_n_larger_than_available_returns_all():
    """Asking for more than exist must return everything, not pad or error."""
    summary = {
        "a": {"total_quantity": 1, "total_revenue": 10.0, "order_count": 1},
        "b": {"total_quantity": 1, "total_revenue": 20.0, "order_count": 1},
    }
    result = top_n_products(summary, n=10)
    assert len(result) == 2


def test_top_n_products_negative_n_raises():
    """n < 0 is explicitly a ValueError. n == 0 is NOT (it's a valid empty
    slice), so we test the negative side only."""
    with pytest.raises(ValueError):
        top_n_products({}, n=-1)


# --- apply_bulk_discount ---------------------------------------------------

def test_apply_bulk_discount_applies_only_at_or_above_threshold():
    """The threshold is inclusive (>=), so an order exactly at min_quantity
    gets the discount while one just below is untouched. Checks both the
    discounted price and the pass-through."""
    orders = [
        {"order_id": "1", "product": "w", "quantity": 5, "unit_price": 10.0},
        {"order_id": "2", "product": "w", "quantity": 4, "unit_price": 10.0},
    ]
    result = apply_bulk_discount(orders, min_quantity=5, discount_rate=0.1)
    assert result[0]["unit_price"] == 9.0   # 5 >= 5 -> 10% off
    assert result[1]["unit_price"] == 10.0  # 4 < 5 -> unchanged


def test_apply_bulk_discount_does_not_mutate_input():
    """A headline promise: the input list and its dicts are never modified.
    This is exactly the kind of aliasing bug (.copy() forgotten) that a
    happy-path test would miss, so we assert the original is pristine after
    the call returns a discounted copy."""
    original = [{"order_id": "1", "product": "w", "quantity": 5, "unit_price": 10.0}]
    apply_bulk_discount(original, min_quantity=1, discount_rate=0.5)
    assert original[0]["unit_price"] == 10.0


def test_apply_bulk_discount_rejects_rate_above_one():
    """discount_rate must be within [0, 1]. A rate > 1 would imply a negative
    price, so it must raise rather than silently producing one."""
    with pytest.raises(ValueError):
        apply_bulk_discount([], min_quantity=1, discount_rate=1.5)


# --- loyalty_tier ----------------------------------------------------------

@pytest.mark.parametrize("spend,expected", [
    (0, "none"),         # bottom of the range
    (99.99, "none"),     # just under the first cutoff
    (100, "silver"),     # exactly on the boundary -> the higher tier
    (499.99, "silver"),
    (500, "gold"),       # boundary
    (999.99, "gold"),
    (1000, "platinum"),  # boundary
    (5000, "platinum"),
])
def test_loyalty_tier_boundaries(spend, expected):
    """Tier logic is all about boundaries, and the docstring uses >= at each
    cutoff -- meaning the boundary value belongs to the *higher* tier. This
    parametrized set nails down every cutoff from both sides, which is where
    a '>' vs '>=' slip would show up."""
    assert loyalty_tier(spend) == expected


def test_loyalty_tier_negative_raises():
    """Negative lifetime spend is impossible and must raise."""
    with pytest.raises(ValueError):
        loyalty_tier(-0.01)


# --- Integration tests (multiple functions / real file I/O) ----------------

def test_load_orders_from_csv_parses_good_rows_and_reports_errors(tmp_path):
    """Integration test: exercises load_orders_from_csv -> parse_order_row
    against a real file. It mixes valid rows with two broken ones (a
    negative quantity and a non-numeric price) and checks that (a) only the
    good rows are returned, (b) each bad row produces exactly one error, and
    (c) the error's row number counts the header as row 1 -- the
    spreadsheet-style numbering the docstring promises."""
    csv_content = (
        "order_id,product,quantity,unit_price,customer_email\n"
        "1,widget,2,10.00,a@x.com\n"      # row 2 - ok
        "2,gadget,-1,5.00,b@x.com\n"       # row 3 - bad quantity
        "3,gizmo,1,notaprice,c@x.com\n"    # row 4 - bad price
        "4,widget,3,10.00,d@x.com\n"       # row 5 - ok
    )
    csv_file = tmp_path / "orders.csv"
    csv_file.write_text(csv_content)

    orders, errors = load_orders_from_csv(str(csv_file))

    assert len(orders) == 2
    assert [o["order_id"] for o in orders] == ["1", "4"]
    assert len(errors) == 2
    assert errors[0].startswith("row 3:")
    assert errors[1].startswith("row 4:")


def test_write_top_products_report_writes_expected_format(tmp_path):
    """Integration test: summarize_by_product -> top_n_products ->
    write_top_products_report, ending in a real file on disk. Verifies the
    exact line format ("<product>: $<revenue> (<qty> units)") and that n
    actually limits the output to the top 2 by revenue."""
    orders = [
        {"product": "widget", "quantity": 10, "unit_price": 10.0},  # rev 100
        {"product": "gadget", "quantity": 1, "unit_price": 5.0},    # rev 5
        {"product": "gizmo", "quantity": 5, "unit_price": 10.0},    # rev 50
    ]
    summary = summarize_by_product(orders)
    report_file = tmp_path / "report.txt"

    result = write_top_products_report(summary, str(report_file), n=2)

    assert result is None  # documented return value
    lines = report_file.read_text().splitlines()
    assert lines == [
        "widget: $100.0 (10 units)",
        "gizmo: $50.0 (5 units)",
    ]
