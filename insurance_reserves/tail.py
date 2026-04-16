"""Tail factor estimation via curve fitting."""

from .models import DevelopmentFactors


def estimate_tail(
    link_ratios: list[float],
    fit_start: int = 4,
    max_extrap: int = 100,
    threshold: float = 0.0001,
) -> DevelopmentFactors:
    """Estimate tail factor by fitting a decay curve to development factors.

    Fits a regression to the later (more stable) development factors
    and extrapolates to estimate remaining development beyond the
    observed triangle.

    Parameters:
        link_ratios: observed age-to-age factors
        fit_start: index of first factor to use for fitting (0-based)
        max_extrap: maximum number of periods to extrapolate
        threshold: stop when projected development increment falls below this

    Returns:
        DevelopmentFactors with the original link ratios and estimated tail.
    """
    n = len(link_ratios)
    fit_start = min(fit_start, max(0, n - 2))
    selected = list(range(fit_start, n))

    xs = []
    ys = []
    for k in selected:
        excess = link_ratios[k] - 1.0
        if excess > 0:
            xs.append(float(k))
            ys.append(excess)

    if len(xs) < 2:
        return DevelopmentFactors(factors=link_ratios, tail_factor=1.0)

    n_pts = len(xs)
    x_mean = sum(xs) / n_pts
    y_mean = sum(ys) / n_pts

    ss_xy = sum((x - x_mean) * (y - y_mean) for x, y in zip(xs, ys))
    ss_xx = sum((x - x_mean) ** 2 for x in xs)

    if ss_xx == 0:
        return DevelopmentFactors(factors=link_ratios, tail_factor=1.0)

    b = ss_xy / ss_xx
    a = y_mean - b * x_mean

    tail = 1.0
    for period in range(n, n + max_extrap):
        projected = a + b * period
        if projected < threshold:
            break
        tail *= (1.0 + projected)

    return DevelopmentFactors(factors=link_ratios, tail_factor=tail)
