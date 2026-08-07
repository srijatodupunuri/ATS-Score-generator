def generate_ai_response(
    question,
    candidates
):

    question = question.lower().strip()

    # -------------------
    # Interview Recommendation
    # -------------------

    if any(

        text in question

        for text in [

            "interview",
            "shortlist",
            "best candidate",
            "hire",
            "top candidate"
        ]

    ):

        top_candidates = sorted(

            candidates,

            key=lambda c:

            c["ats_result"][
                "ats_percentage"
            ],

            reverse=True

        )[:3]

        answer = (
            "Recommended Candidates:\n\n"
        )

        for candidate in top_candidates:

            answer += f"""

{candidate['candidate_profile']['name']}

ATS:
{candidate['ats_result']['ats_percentage']}%

Experience:
{candidate['candidate_profile']['experience']['years']} Years

Status:
{candidate['ats_result']['decision']['status']}

-------------------

"""

        return answer

    # -------------------
    # Skill Search
    # -------------------

    skills = [

        "linux",
        "python",
        "git",
        "jenkins",
        "automation",
        "embedded c",
        "device driver",
        "gerrit"

    ]

    requested_skills = [

        skill

        for skill in skills

        if skill in question

    ]

    if requested_skills:

        matched = []

        for candidate in candidates:

            candidate_skills = [

                s.lower()

                for s in

                candidate[
                    "candidate_profile"
                ][
                    "skills"
                ]
            ]

            if all(

                skill in candidate_skills

                for skill in requested_skills

            ):

                matched.append(
                    candidate
                )

        if not matched:

            return (
                "No candidate found with those skills."
            )

        answer = (
            "Matching Candidates:\n\n"
        )

        for candidate in matched:

            answer += f"""

{candidate['candidate_profile']['name']}

ATS Score:
{candidate['ats_result']['ats_percentage']}%

Experience:
{candidate['candidate_profile']['experience']['years']} Years

Skills:
{", ".join(candidate['candidate_profile']['skills'])}

-------------------

"""

        return answer

    # -------------------
    # Rank Query
    # -------------------

    if "rank" in question:

        for candidate in candidates:

            name = candidate[
                "candidate_profile"
            ][
                "name"
            ].lower()

            if name in question:

                return f"""

Candidate:
{candidate['candidate_profile']['name']}

Current Rank:
#{candidate['rank']}

ATS Score:
{candidate['ats_result']['ats_percentage']}%

Status:
{candidate['ats_result']['decision']['status']}

"""

    # -------------------
    # Candidate Details
    # -------------------

    for candidate in candidates:

        name = candidate[
            "candidate_profile"
        ][
            "name"
        ].lower()

        first_name = name.split()[0]

        if (

            first_name in question

            or

            name in question

        ):

            return f"""

Candidate:

{candidate['candidate_profile']['name']}

Rank:
#{candidate['rank']}

ATS:
{candidate['ats_result']['ats_percentage']}%

Experience:
{candidate['candidate_profile']['experience']['years']} Years

Education:
{candidate['candidate_profile']['education']['degree']}

Skills:
{", ".join(candidate['candidate_profile']['skills'])}

Matched Skills:
{", ".join(candidate['ats_result']['matched_skills'])}

Missing Skills:
{", ".join(candidate['ats_result']['missing_skills']) if candidate['ats_result']['missing_skills'] else 'None'}

Decision:
{candidate['ats_result']['decision']['reason']}

"""

    # -------------------
    # Missing Skills Analysis
    # -------------------

    if (

        "missing skills" in question

        or

        "skill gap" in question

    ):

        skill_count = {}

        for candidate in candidates:

            for skill in candidate[
                "ats_result"
            ][
                "missing_skills"
            ]:

                skill_count[skill] = (

                    skill_count.get(
                        skill,
                        0
                    ) + 1
                )

        if not skill_count:

            return (
                "No major skill gaps detected."
            )

        sorted_skills = sorted(

            skill_count.items(),

            key=lambda x: x[1],

            reverse=True

        )

        answer = (
            "Top Missing Skills:\n\n"
        )

        for skill, count in sorted_skills:

            answer += (
                f"{skill}: {count}\n"
            )

        return answer

    # -------------------
    # ATS Summary
    # -------------------

    if any(

        word in question

        for word in [

            "summary",
            "overview",
            "analysis"
        ]

    ):

        accepted = len([

            c for c in candidates

            if

            c["ats_result"]["decision"]["status"]
            == "Accepted"

        ])

        rejected = len([

            c for c in candidates

            if

            c["ats_result"]["decision"]["status"]
            == "Rejected"

        ])

        average = round(

            sum(

                c["ats_result"]["ats_percentage"]

                for c in candidates

            ) / len(candidates),

            2

        )

        return f"""

Recruitment Summary

Total Candidates:
{len(candidates)}

Accepted:
{accepted}

Rejected:
{rejected}

Average ATS:
{average}%

Recommendation:

Focus on top ranked candidates
for technical interviews.

"""

    # -------------------
    # Fallback
    # -------------------

    return """

I can help with:

• Who should I interview first?

• Best candidate

• Candidate ranking

• Candidate details

• Linux candidates

• Python candidates

• Linux and Python candidates

• Skill gap analysis

• Recruitment summary

• Candidate ATS score

Try asking:

Who is the best candidate?

Show Linux and Python candidates

Tell me about Mukesh Kumar K

Show recruitment summary

"""
