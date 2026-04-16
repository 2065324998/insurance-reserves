"""Reserve estimation orchestrator."""

from .models import LossTriangle, ReserveEstimate, ReserveSummary
from .development import compute_link_ratios
from .tail import estimate_tail
from .projection import (
    compute_cdfs,
    project_ultimate_cl,
    compute_ibnr_cl,
    compute_ibnr_bf,
    blend_reserves,
)


def estimate_reserves(
    triangle: LossTriangle,
    earned_premiums: list[float],
    expected_loss_ratio: float,
    tail_fit_start: int = 4,
    full_cred_at: float = 0.90,
) -> ReserveSummary:
    """Estimate IBNR reserves using chain-ladder, BF, and blended methods.

    Pipeline:
        1. Compute age-to-age development factors from triangle
        2. Estimate tail factor via curve fitting
        3. Build cumulative development factors to ultimate
        4. Project ultimate losses (chain-ladder)
        5. Compute IBNR via chain-ladder and Bornhuetter-Ferguson
        6. Blend CL and BF using credibility weighting
    """
    link_ratios = compute_link_ratios(triangle)
    dev_factors = estimate_tail(link_ratios, fit_start=tail_fit_start)
    cdfs = compute_cdfs(dev_factors)

    ultimates_cl = project_ultimate_cl(triangle, cdfs)
    ibnr_cl = compute_ibnr_cl(triangle, ultimates_cl)
    ibnr_bf = compute_ibnr_bf(
        triangle, cdfs, earned_premiums, expected_loss_ratio
    )
    ibnr_blended = blend_reserves(
        ibnr_cl, ibnr_bf, triangle, full_cred_at
    )

    diagonal = triangle.latest_diagonal()
    estimates = []
    for i in range(triangle.n_origins):
        ult_bf = diagonal[i] + ibnr_bf[i]
        estimates.append(ReserveEstimate(
            origin_label=triangle.origin_labels[i],
            reported=diagonal[i],
            ultimate_cl=ultimates_cl[i],
            ibnr_cl=ibnr_cl[i],
            ultimate_bf=ult_bf,
            ibnr_bf=ibnr_bf[i],
            ibnr_blended=ibnr_blended[i],
        ))

    return ReserveSummary(
        estimates=estimates,
        development_factors=dev_factors,
        cdfs=cdfs,
    )
