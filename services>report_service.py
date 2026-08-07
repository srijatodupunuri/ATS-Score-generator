import pandas as pd


class ReportService:

    @staticmethod
    def generate_summary_report(results):

        rows = []

        for item in results:

            profile = item[
                "candidate_profile"
            ]

            ats = item[
                "ats_result"
            ]

            rows.append({

                "Rank":
                item["rank"],

                "Candidate":
                profile["name"],

                "ATS Score":
                ats["ats_percentage"],

                "Status":
                ats["decision"]["status"],

                "Priority":
                ats["decision"]["priority"],

                "Reason":
                ats["decision"]["reason"]

            })

        return pd.DataFrame(rows)

@staticmethod
def generate_accepted_report(results):

    data = []

    for item in results:

        if (
            item["ats_result"]
            ["decision"]["status"]
            == "Accepted"
        ):

            data.append({

                "Candidate":
                item[
                    "candidate_profile"
                ]["name"],

                "ATS Score":
                item[
                    "ats_result"
                ][
                    "ats_percentage"
                ],

                "Priority":
                item[
                    "ats_result"
                ][
                    "decision"
                ]["priority"]

            })

    return pd.DataFrame(data)
@staticmethod
def generate_rejected_report(results):

    data = []

    for item in results:

        if (
            item["ats_result"]
            ["decision"]["status"]
            == "Rejected"
        ):

            data.append({

                "Candidate":
                item[
                    "candidate_profile"
                ]["name"],

                "ATS":
                item[
                    "ats_result"
                ][
                    "ats_percentage"
                ],

                "Reason":
                item[
                    "ats_result"
                ]["decision"]["reason"]

            })

    return pd.DataFrame(data)
@staticmethod
def get_candidate_report(candidate):

    ats = candidate[
        "ats_result"
    ]

    return {

        "candidate_name":

            candidate[
                "candidate_profile"
            ]["name"],

        "ats_score":

            ats[
                "ats_percentage"
            ],

        "section_scores":

            ats[
                "section_scores"
            ],

        "matched_skills":

            ats[
                "matched_skills"
            ],

        "missing_skills":

            ats[
                "missing_skills"
            ],

        "decision":

            ats[
                "decision"
            ]
    }
