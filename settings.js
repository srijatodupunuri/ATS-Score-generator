document.addEventListener("DOMContentLoaded", loadSettings);

function loadSettings() {
  const savedSettings = localStorage.getItem("atsSettings");

  if (!savedSettings) {
    return;
  }

  const settings = JSON.parse(savedSettings);

  document.getElementById("recruiterName").value = settings.recruiterName || "";

  document.getElementById("acceptThreshold").value =
    settings.acceptThreshold || 70;

  document.getElementById("reviewThreshold").value =
    settings.reviewThreshold || 50;
}

function saveSettings() {
  const settings = {
    recruiterName: document.getElementById("recruiterName").value,

    acceptThreshold: document.getElementById("acceptThreshold").value,

    reviewThreshold: document.getElementById("reviewThreshold").value,
  };

  localStorage.setItem(
    "atsSettings",

    JSON.stringify(settings),
  );

  alert("Settings saved successfully!");
}
