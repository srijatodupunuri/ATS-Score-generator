def dashboard_summary(results):

    total = len(results)

    accepted = len([
        candidate
        for candidate in results
        if candidate["ats_result"]["decision"]["status"]
        == "Accepted"
    ])

    rejected = len([
        candidate
        for candidate in results
        if candidate["ats_result"]["decision"]["status"]
        == "Rejected"
    ])

    review_required = len([
        candidate
        for candidate in results
        if candidate["ats_result"]["decision"]["status"]
        == "Review Required"
    ])

    average = 0

    if total > 0:

        average = round(

            sum(
                candidate["ats_result"]["ats_percentage"]
                for candidate in results
            )

            / total,

            2
        )

    scores = [

        candidate["ats_result"]["ats_percentage"]

        for candidate in results
    ]

    highest_score = 0

    lowest_score = 0

    if scores:

        highest_score = max(scores)

        lowest_score = min(scores)

    top_candidate = None

    if results:

        top_candidate = max(

            results,

            key=lambda candidate:

            candidate["ats_result"][
                "ats_percentage"
            ]
        )

    return {

        "total_candidates":
            total,

        "accepted":
            accepted,

        "rejected":
            rejected,

        "review_required":
            review_required,

        "average_score":
            average,

        "highest_score":
            highest_score,

        "lowest_score":
            lowest_score,

        "scores":
            scores,

        "top_candidate":
            top_candidate

    }
