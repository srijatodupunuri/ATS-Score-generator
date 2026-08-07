let reportsData = {};

document.addEventListener("DOMContentLoaded", loadReports);

async function loadReports() {
  const response = await fetch("/api/reports");

  reportsData = await response.json();

  document.getElementById("totalReports").innerText = reportsData.summary.total;

  document.getElementById("acceptedReports").innerText =
    reportsData.summary.accepted;

  document.getElementById("rejectedReports").innerText =
    reportsData.summary.rejected;

  document.getElementById("reviewReports").innerText =
    reportsData.summary.review;

  showHistory();
}

function renderReports(data) {
  const html = data
    .map(
      (candidate) =>
        `
            <div class="report-card">

                <h3>

                    #${candidate.rank}

                    ${candidate.candidate_profile.name}

                </h3>

                <p>

                    ATS:
                    ${candidate.ats_result.ats_percentage}%

                </p>

                <p>

                    Status:
                    ${candidate.ats_result.decision.status}

                </p>

                <p>

                    Priority:
                    ${candidate.ats_result.decision.priority}

                </p>

            </div>
            `,
    )
    .join("");

  document.getElementById("reportContent").innerHTML = html;
}
function activateTab(tabId) {
  document
    .querySelectorAll(".report-tab")
    .forEach((tab) => tab.classList.remove("active-tab"));

  document.getElementById(tabId).classList.add("active-tab");
}
function showAccepted() {
  activateTab("acceptedTab");

  renderReports(reportsData.accepted_reports);
}

function showRejected() {
  activateTab("rejectedTab");
  renderReports(reportsData.rejected_reports);
}

function showReview() {
  activateTab("reviewTab");
  renderReports(reportsData.review_reports);
}

function showHistory() {
  activateTab("historyTab");
  renderReports(reportsData.history);
}
document
  .getElementById("reportSearch")
  .addEventListener("input", searchReports);
function searchReports() {
  const value = document.getElementById("reportSearch").value.toLowerCase();

  const filtered = reportsData.history.filter((candidate) =>
    candidate.candidate_profile.name.toLowerCase().includes(value),
  );

  renderReports(filtered);
}
