"""Unit tests for triangle construction and manipulation."""

import pytest
from insurance_reserves.triangle import build_triangle, to_incremental


class TestBuildTriangle:
    """Test triangle construction from ragged data."""

    def test_shape(self):
        tri = build_triangle(
            ["2020", "2021", "2022"],
            [1, 2, 3],
            [[100, 200, 250], [120, 240], [110]],
        )
        assert tri.n_origins == 3
        assert tri.n_dev == 3

    def test_padding(self):
        tri = build_triangle(
            ["2020", "2021"],
            [1, 2, 3],
            [[100, 200, 250], [120]],
        )
        assert tri.at(1, 0) == 120
        assert tri.at(1, 1) is None
        assert tri.at(1, 2) is None

    def test_full_row(self):
        tri = build_triangle(
            ["2020"],
            [1, 2, 3],
            [[100, 200, 300]],
        )
        assert tri.at(0, 0) == 100
        assert tri.at(0, 1) == 200
        assert tri.at(0, 2) == 300

    def test_latest_diagonal(self):
        tri = build_triangle(
            ["2020", "2021", "2022"],
            [1, 2, 3],
            [[100, 200, 250], [120, 240], [110]],
        )
        assert tri.latest_diagonal() == [250, 240, 110]


class TestIncremental:
    """Test cumulative to incremental conversion."""

    def test_basic(self):
        tri = build_triangle(
            ["2020", "2021"],
            [1, 2, 3],
            [[100, 250, 300], [120, 280]],
        )
        inc = to_incremental(tri)
        assert inc[0] == [100, 150, 50]
        assert inc[1][0] == 120
        assert inc[1][1] == 160
        assert inc[1][2] is None

    def test_single_period(self):
        tri = build_triangle(["2022"], [1], [[500]])
        inc = to_incremental(tri)
        assert inc[0] == [500]
