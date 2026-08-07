async function loadRanking() {
  const response = await fetch("/api/candidates");

  const result = await response.json();

  const sorted = result.data.sort(
    (a, b) => b.ats_result.ats_percentage - a.ats_result.ats_percentage,
  );

  document.getElementById("rankingContainer").innerHTML = sorted
    .map(
      (candidate, index) =>
        `
        <div class="glass-card ranking-card">

            <h2>

                #${index + 1}

                ${candidate.candidate_profile.name}

            </h2>

            <p>

                ATS Score :
                ${candidate.ats_result.ats_percentage}%

            </p>

            <p>

                Status :
                ${candidate.ats_result.decision.status}

            </p>

        </div>
        `,
    )
    .join("");
}

loadRanking();
