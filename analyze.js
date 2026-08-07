const analyzeButton = document.querySelector(".analyze-btn");

const resultsContainer = document.getElementById("analysisResults");

async function analyzeCandidates() {
  if (!jdState.fileName) {
    alert("Please upload a Job Description.");

    return;
  }

  if (resumeState.uploadedFiles.length === 0) {
    alert("Please upload resumes.");

    return;
  }

  analyzeButton.disabled = true;

  analyzeButton.innerHTML = "Analyzing...";

  try {
    const response = await fetch("/api/ats/analyze-all", {
      method: "POST",

      headers: {
        "Content-Type": "application/json",
      },

      body: JSON.stringify({
        jd_filename: jdState.fileName,

        resumes: resumeState.uploadedFiles,
      }),
    });

    const result = await response.json();

    if (result.success) {
      window.location = "/analysis-results";
    } else {
      alert(result.message);
    }
  } catch (error) {
    console.error(error);

    alert("Analysis failed.");
  } finally {
    analyzeButton.disabled = false;

    analyzeButton.innerHTML = "Analyze Candidates";
  }
}

function renderResults(results) {
  let html = `
        <h2>
            ATS Analysis Results
        </h2>

        <table
            style="
            width:100%;
            margin-top:20px;
            text-align:left;
            "
        >

        <thead>

        <tr>

            <th>Rank</th>

            <th>Candidate</th>

            <th>ATS Score</th>

            <th>Status</th>

            <th>Priority</th>

        </tr>

        </thead>

        <tbody>
    `;

  results.forEach((candidate) => {
    html += `

            <tr>

                <td>
                    ${candidate.rank}
                </td>

                <td>
                    ${candidate.candidate_profile.name}
                </td>

                <td>
                    ${candidate.ats_result.ats_percentage}%
                </td>

                <td>
                    ${candidate.ats_result.decision.status}
                </td>

                <td>
                    ${candidate.ats_result.decision.priority}
                </td>

            </tr>
            `;
  });

  html += `
        </tbody>
        </table>
    `;

  resultsContainer.innerHTML = html;
}

analyzeButton.addEventListener("click", analyzeCandidates);
