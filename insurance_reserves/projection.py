"""Loss projection and IBNR computation."""

from .models import LossTriangle, DevelopmentFactors


def compute_cdfs(dev_factors: DevelopmentFactors) -> list[float]:
    """Build cumulative development factors from link ratios.

    Each CDF entry represents the cumulative product of development
    factors, incorporating the tail factor at the final position.
    """
    n = len(dev_factors.factors)
    cdfs = [1.0] * (n + 1)

    cdfs[0] = dev_factors.factors[0]
    for k in range(1, n):
        cdfs[k] = cdfs[k - 1] * dev_factors.factors[k]
    cdfs[n] = cdfs[n - 1] * dev_factors.tail_factor

    return cdfs


def project_ultimate_cl(
    triangle: LossTriangle,
    cdfs: list[float],
) -> list[float]:
    """Project ultimate losses using chain-ladder method.

    Ultimate_i = Reported_i * CDF from latest development period.
    """
    ultimates = []
    for i in range(triangle.n_origins):
        d = triangle.latest_dev_index(i)
        reported = triangle.values[i][d]
        ultimates.append(reported * cdfs[d])
    return ultimates


def compute_ibnr_cl(
    triangle: LossTriangle,
    ultimates: list[float],
) -> list[float]:
    """Compute chain-ladder IBNR = Ultimate - Reported."""
    diagonal = triangle.latest_diagonal()
    return [round(ult - rep, 2) for ult, rep in zip(ultimates, diagonal)]


def compute_ibnr_bf(
    triangle: LossTriangle,
    cdfs: list[float],
    earned_premiums: list[float],
    expected_loss_ratio: float,
) -> list[float]:
    """Compute IBNR using Bornhuetter-Ferguson method.

    IBNR_BF = Expected_Ultimate * Pct_Unreported
    where:
        Expected_Ultimate = EarnedPremium * ExpectedLossRatio
        Pct_Unreported = 1 - 1/CDF
    """
    ibnr = []
    for i in range(triangle.n_origins):
        d = triangle.latest_dev_index(i)
        expected_ult = earned_premiums[i] * expected_loss_ratio
        pct_unreported = 1.0 - 1.0 / cdfs[d]
        ibnr.append(round(expected_ult * pct_unreported, 2))
    return ibnr


def blend_reserves(
    ibnr_cl: list[float],
    ibnr_bf: list[float],
    triangle: LossTriangle,
    full_cred_at: float = 0.90,
) -> list[float]:
    """Blend CL and BF reserves using credibility weighting.

    More mature origin periods receive higher credibility (more weight
    to chain-ladder). Credibility increases with the square of the
    maturity ratio, reflecting that early development periods carry
    less predictive value.

    credibility = min((d / n_dev)^2 * full_cred_at, 1.0)
    blended = credibility * CL + (1 - credibility) * BF
    """
    blended = []
    n_dev = triangle.n_dev
    for i in range(triangle.n_origins):
        d = triangle.latest_dev_index(i) + 1
        maturity = d / n_dev
        cred = min(maturity * maturity * full_cred_at, 1.0)
        b = cred * ibnr_cl[i] + (1.0 - cred) * ibnr_bf[i]
        blended.append(round(b, 2))
    return blended
