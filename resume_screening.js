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

loadResumes();
