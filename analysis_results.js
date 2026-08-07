document.addEventListener("DOMContentLoaded", loadResults);

function goBack() {
  window.location = "/analysis";
}

async function loadResults() {
  const response = await fetch("/api/candidates");

  const result = await response.json();

  renderResults(result.data);
}

function renderResults(results) {
  const container = document.getElementById("resultsContainer");

  container.innerHTML = results
    .map((candidate) => createCandidateCard(candidate))
    .join("");
}

function createCandidateCard(candidate) {
  const ats = candidate.ats_result;

  return `

    <div class="premium-result-card">

        <div class="candidate-header">

            <div>

                <h2>

                    #${candidate.rank}

                    ${candidate.candidate_profile.name}

                </h2>

                <p>

                    Experience:

                    ${candidate.candidate_profile.experience.years}

                    Years

                </p>

            </div>

            <div class="ats-score-circle">

                ${ats.ats_percentage}%

            </div>

        </div>

        <div class="status-section">

            <span class="status-badge">

                ${ats.decision.status}

            </span>

            <span class="priority-badge">

                Priority:

                ${ats.decision.priority}

            </span>

        </div>

        <div class="section-block">

            <h3>

                ✅ Matched Skills

            </h3>

            <div class="skill-container">

                ${ats.matched_skills
                  .map(
                    (skill) =>
                      `
                    <span class="skill-chip">

                        ${skill}

                    </span>
                    `,
                  )
                  .join("")}

            </div>

        </div>

        <div class="section-block">

            <h3>

                ⚠ Missing Skills

            </h3>

            <div class="skill-container">

                ${
                  ats.missing_skills.length > 0
                    ? ats.missing_skills
                        .map(
                          (skill) =>
                            `
                        <span class="missing-chip">

                            ${skill}

                        </span>
                        `,
                        )
                        .join("")
                    : "<span class='success-text'>No Missing Skills</span>"
                }

            </div>

        </div>

        <div class="section-block">

            <h3>

                📊 ATS Breakdown

            </h3>

            ${buildBreakdown(ats.section_scores)}

        </div>

        <div class="section-block">

            <h3>
                ✅ Strengths
            </h3>

            <ul>

                ${ats.strengths

                  .filter(Boolean)

                  .map((item) => `<li>${item}</li>`)

                  .join("")}

            </ul>

        </div>

        <div class="section-block">

            <h3>
                ⚠ Weaknesses
            </h3>

            <ul>

                ${ats.weaknesses

                  .filter(Boolean)

                  .map((item) => `<li>${item}</li>`)

                  .join("")}

            </ul>

        </div>

        <div class="recommendation-box">

            <h3>

                Recruiter Recommendation

            </h3>

            <p>

                ${ats.decision.reason}

            </p>

        </div>

    </div>

    `;
}

function buildBreakdown(scores) {
  let html = "";

  Object.entries(scores).forEach(([key, value]) => {
    html += `

            <div class="score-row">

                <span>

                    ${key.toUpperCase()}

                </span>

                <span>

                    ${value.score}

                    /

                    ${value.max_score}

                </span>

            </div>

            `;
  });

  return html;
}
