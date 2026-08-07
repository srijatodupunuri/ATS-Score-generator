def rank_candidates(results):

    ranked = sorted(
        results,
        key=lambda candidate:
        candidate["ats_result"][
            "ats_percentage"
        ],
        reverse=True
    )

    for position, candidate in enumerate(
        ranked,
        start=1
    ):
        candidate["rank"] = position

    return ranked
