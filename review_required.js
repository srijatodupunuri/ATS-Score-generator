document.addEventListener("DOMContentLoaded", loadReviewQueue);

async function loadReviewQueue() {
  const response = await fetch("/api/candidates");

  const result = await response.json();

  const reviewData = result.data.filter(
    (candidate) =>
      candidate.ats_result.ats_percentage >= 40 &&
      candidate.ats_result.ats_percentage <= 65,
  );

  document.getElementById("reviewContainer").innerHTML = reviewData
    .map(
      (candidate) =>
        `
        <div class="glass-card review-card">

            <h2>
                ${candidate.candidate_profile.name}
            </h2>

            <p>
                ATS:
                ${candidate.ats_result.ats_percentage}%
            </p>

            <p>
                Status:
                ${candidate.ats_result.decision.status}
            </p>

            <p>
                Reason:
                ${candidate.ats_result.decision.reason}
            </p>

            <p>
                Missing Skills:
                ${candidate.ats_result.missing_skills.join(", ")}
            </p>

            <button>
                Review Candidate
            </button>

        </div>
        `,
    )
    .join("");
}
