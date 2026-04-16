"""Unit tests for data models."""

import pytest
from insurance_reserves.models import (
    LossTriangle,
    DevelopmentFactors,
    ReserveEstimate,
    ReserveSummary,
)


class TestLossTriangle:
    """Test LossTriangle model."""

    @pytest.fixture
    def small_triangle(self):
        return LossTriangle(
            origin_labels=["2020", "2021", "2022"],
            dev_periods=[1, 2, 3],
            values=[
                [100, 200, 250],
                [120, 240, None],
                [110, None, None],
            ],
        )

    def test_n_origins(self, small_triangle):
        assert small_triangle.n_origins == 3

    def test_n_dev(self, small_triangle):
        assert small_triangle.n_dev == 3

    def test_at_valid(self, small_triangle):
        assert small_triangle.at(0, 0) == 100
        assert small_triangle.at(0, 2) == 250
        assert small_triangle.at(1, 1) == 240

    def test_at_none(self, small_triangle):
        assert small_triangle.at(1, 2) is None
        assert small_triangle.at(2, 1) is None

    def test_latest_diagonal(self, small_triangle):
        diag = small_triangle.latest_diagonal()
        assert diag == [250, 240, 110]

    def test_latest_dev_index(self, small_triangle):
        assert small_triangle.latest_dev_index(0) == 2
        assert small_triangle.latest_dev_index(1) == 1
        assert small_triangle.latest_dev_index(2) == 0


class TestDevelopmentFactors:
    """Test DevelopmentFactors model."""

    def test_creation(self):
        df = DevelopmentFactors(factors=[1.5, 1.2, 1.1])
        assert len(df.factors) == 3
        assert df.tail_factor == 1.0

    def test_with_tail(self):
        df = DevelopmentFactors(factors=[1.5, 1.2], tail_factor=1.05)
        assert df.tail_factor == 1.05


class TestReserveSummary:
    """Test ReserveSummary aggregation."""

    def test_total_ibnr(self):
        estimates = [
            ReserveEstimate("2020", 100, 120, 20, 115, 15, 17),
            ReserveEstimate("2021", 80, 110, 30, 105, 25, 27),
        ]
        summary = ReserveSummary(
            estimates=estimates,
            development_factors=DevelopmentFactors(factors=[1.2]),
            cdfs=[1.2],
        )
        assert summary.total_ibnr_cl == 50
        assert summary.total_ibnr_bf == 40
        assert summary.total_ibnr_blended == 44
