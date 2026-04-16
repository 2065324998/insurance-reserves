"""Unit tests for development factor computation."""

import pytest
from insurance_reserves.triangle import build_triangle
from insurance_reserves.development import compute_link_ratios


class TestLinkRatios:
    """Test link ratio computation."""

    def test_count(self):
        tri = build_triangle(
            ["2020", "2021", "2022"],
            [1, 2, 3],
            [[100, 200, 250], [120, 240], [110]],
        )
        factors = compute_link_ratios(tri)
        assert len(factors) == 2

    def test_factors_greater_than_one(self):
        tri = build_triangle(
            ["2020", "2021"],
            [1, 2, 3],
            [[100, 200, 250], [120, 280]],
        )
        factors = compute_link_ratios(tri)
        assert all(f > 1.0 for f in factors)

    def test_uniform_triangle(self):
        """When all rows have the same ratios, factor equals that ratio."""
        tri = build_triangle(
            ["A", "B"],
            [1, 2],
            [[100, 200], [100, 200]],
        )
        factors = compute_link_ratios(tri)
        assert factors[0] == pytest.approx(2.0)
