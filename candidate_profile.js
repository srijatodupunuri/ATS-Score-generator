let allCandidates = [];

document.addEventListener("DOMContentLoaded", loadProfiles);

async function loadProfiles() {
  const response = await fetch("/api/candidates");

  const result = await response.json();

  allCandidates = result.data;

  renderProfiles(allCandidates);

  document
    .getElementById("candidateSearch")
    .addEventListener("input", filterProfiles);
}

function filterProfiles() {
  const value = document.getElementById("candidateSearch").value.toLowerCase();

  const filtered = allCandidates.filter((candidate) =>
    candidate.candidate_profile.name.toLowerCase().includes(value),
  );

  renderProfiles(filtered);
}

function renderProfiles(candidates) {
  document.getElementById("profilesContainer").innerHTML = candidates
    .map(
      (candidate) =>
        `
        <div class="glass-card profile-card">

            <h2>
                ${candidate.candidate_profile.name}
            </h2>

            <p>
                ATS Score:
                <strong>
                    ${candidate.ats_result.ats_percentage}%
                </strong>
            </p>

            <p>
                Status:
                ${candidate.ats_result.decision.status}
            </p>

            <p>
                Experience:
                ${candidate.candidate_profile.experience.years}
                Years
            </p>

            <p>
                Education:
                ${candidate.candidate_profile.education.degree}
            </p>

            <div class="skill-container">
            <p>
                Skills:
            </p>

                ${candidate.candidate_profile.skills

                  .map((skill) => `<span class="skill-chip">${skill}</span>`)

                  .join("")}

            </div>

            <h4>
                ✅ Matched Skills
            </h4>

            <p>
                ${candidate.ats_result.matched_skills.join(", ")}
            </p>

            <h4>
                ⚠ Missing Skills
            </h4>

            <p>
                ${candidate.ats_result.missing_skills.join(", ") || "None"}
            </p>

        </div>
        `,
    )
    .join("");
}
