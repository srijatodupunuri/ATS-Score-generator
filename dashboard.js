document.addEventListener("DOMContentLoaded", loadDashboard);

async function loadDashboard() {
  const response = await fetch("/api/dashboard");

  const data = await response.json();

  document.getElementById("totalCandidates").innerText = data.total;

  document.getElementById("acceptedCount").innerText = data.accepted;

  document.getElementById("rejectedCount").innerText = data.rejected;

  document.getElementById("reviewCount").innerText = data.review;

  document.getElementById("averageATS").innerText = data.average + "%";

  if (data.top_candidate) {
    document.getElementById("topCandidate").innerHTML = `

            <h2>
                ${data.top_candidate.candidate_profile.name}
            </h2>

            <p>
                ATS Score:
                ${data.top_candidate.ats_result.ats_percentage}%
            </p>

            <p>
                Status:
                ${data.top_candidate.ats_result.decision.status}
            </p>

            <p>
                Experience:
                ${data.top_candidate.candidate_profile.experience.years}
                Years
            </p>

        `;
  }
}

const darkModeBtn = document.getElementById("darkModeBtn");

if (darkModeBtn) {
  darkModeBtn.addEventListener("click", () => {
    document.body.classList.toggle("dark-theme");
  });
}
