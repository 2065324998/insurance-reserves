"""Loss triangle construction and manipulation."""

from .models import LossTriangle


def build_triangle(
    origin_labels: list[str],
    dev_periods: list[int],
    data: list[list[float]],
) -> LossTriangle:
    """Build a loss triangle from ragged data.

    Each row in data may be shorter than dev_periods; missing entries
    are padded with None to form the lower-right triangle shape.
    """
    n_dev = len(dev_periods)
    values = []
    for row in data:
        padded = list(row) + [None] * (n_dev - len(row))
        values.append(padded[:n_dev])
    return LossTriangle(
        origin_labels=origin_labels,
        dev_periods=dev_periods,
        values=values,
    )


def to_incremental(triangle: LossTriangle) -> list[list[float | None]]:
    """Convert cumulative triangle to incremental losses."""
    incremental = []
    for i in range(triangle.n_origins):
        row = []
        for j in range(triangle.n_dev):
            val = triangle.values[i][j]
            if val is None:
                row.append(None)
            elif j == 0:
                row.append(val)
            else:
                prev = triangle.values[i][j - 1]
                if prev is None:
                    row.append(None)
                else:
                    row.append(round(val - prev, 2))
        incremental.append(row)
    return incremental
