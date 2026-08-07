let allJDs = [];

async function loadJobDescriptions() {
  const response = await fetch("/api/job-descriptions");

  const data = await response.json();

  allJDs = data.data;

  renderJDs(allJDs);
}

function renderJDs(files) {
  const container = document.getElementById("jdContainer");

  container.innerHTML = files
    .map(
      (file) =>
        `
            <div class="glass-card library-card">

                <h3>📄 ${file}</h3>

            </div>
            `,
    )
    .join("");
}

document.getElementById("jdSearch").addEventListener("input", function () {
  const value = this.value.toLowerCase();

  const filtered = allJDs.filter((file) => file.toLowerCase().includes(value));

  renderJDs(filtered);
});

loadJobDescriptions();
async function loadResumes() {
  const response = await fetch("/api/resumes");

  const data = await response.json();

  document.getElementById("resumeContainer").innerHTML = data.data
    .map(
      (file) =>
        `
        <div class="glass-card">

            <h3>

                📑 ${file}

            </h3>

        </div>
        `,
    )
    .join("");
}
