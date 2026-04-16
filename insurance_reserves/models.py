"""Data models for loss triangle and reserve estimation."""

from dataclasses import dataclass


@dataclass
class LossTriangle:
    """A loss development triangle with cumulative losses.

    Attributes:
        origin_labels: Labels for origin periods (e.g., accident years).
        dev_periods: Development period labels (integers).
        values: 2D list of cumulative losses. None for unavailable cells
                in the lower-right portion of the triangle.
    """
    origin_labels: list[str]
    dev_periods: list[int]
    values: list[list[float | None]]

    @property
    def n_origins(self) -> int:
        return len(self.origin_labels)

    @property
    def n_dev(self) -> int:
        return len(self.dev_periods)

    def at(self, origin_idx: int, dev_idx: int) -> float | None:
        """Get cumulative loss at given origin and development indices."""
        return self.values[origin_idx][dev_idx]

    def latest_diagonal(self) -> list[float]:
        """Return the latest available cumulative value for each origin."""
        result = []
        for i in range(self.n_origins):
            for j in range(self.n_dev - 1, -1, -1):
                if self.values[i][j] is not None:
                    result.append(self.values[i][j])
                    break
        return result

    def latest_dev_index(self, origin_idx: int) -> int:
        """Return the index of the latest development period with data."""
        for j in range(self.n_dev - 1, -1, -1):
            if self.values[origin_idx][j] is not None:
                return j
        raise ValueError(f"No data for origin index {origin_idx}")


@dataclass
class DevelopmentFactors:
    """Age-to-age development factors with tail."""
    factors: list[float]
    tail_factor: float = 1.0


@dataclass
class ReserveEstimate:
    """IBNR reserve estimates for a single origin period."""
    origin_label: str
    reported: float
    ultimate_cl: float
    ibnr_cl: float
    ultimate_bf: float
    ibnr_bf: float
    ibnr_blended: float


@dataclass
class ReserveSummary:
    """Complete reserve estimation results."""
    estimates: list[ReserveEstimate]
    development_factors: DevelopmentFactors
    cdfs: list[float]

    @property
    def total_ibnr_cl(self) -> float:
        return sum(e.ibnr_cl for e in self.estimates)

    @property
    def total_ibnr_bf(self) -> float:
        return sum(e.ibnr_bf for e in self.estimates)

    @property
    def total_ibnr_blended(self) -> float:
        return sum(e.ibnr_blended for e in self.estimates)
