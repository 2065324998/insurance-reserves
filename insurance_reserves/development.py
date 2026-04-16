"""Age-to-age development factor calculation."""

from .models import LossTriangle


def compute_link_ratios(triangle: LossTriangle) -> list[float]:
    """Compute age-to-age development factors from the loss triangle.

    For each development period transition k -> k+1, computes the
    average ratio of losses at period k+1 to losses at period k,
    using all origin periods where both values are available.

    Returns a list of development factors, one per transition.
    """
    factors = []
    for k in range(triangle.n_dev - 1):
        n_pairs = 0
        ratio_sum = 0.0
        for i in range(triangle.n_origins):
            c_k = triangle.at(i, k)
            c_k1 = triangle.at(i, k + 1)
            if c_k is not None and c_k1 is not None and c_k > 0:
                ratio_sum += c_k1 / c_k
                n_pairs += 1
        if n_pairs == 0:
            factors.append(1.0)
        else:
            factors.append(ratio_sum / n_pairs)
    return factors
