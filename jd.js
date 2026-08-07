const pasteOption = document.getElementById("pasteOption");
const uploadOption = document.getElementById("uploadOption");

const pasteContainer = document.getElementById("pasteContainer");
const uploadContainer = document.getElementById("uploadContainer");

// Upload Elements

const browseJDButton = document.getElementById("browseJDButton");

const jdFileInput = document.getElementById("jdFileInput");

const jdFileName = document.getElementById("jdFileName");

const jdFileDetails = document.getElementById("jdFileDetails");

const jdStatus = document.getElementById("jdStatus");

const removeButton = document.getElementById("removeJDButton");

const jdTextarea = document.getElementById("jdTextarea");

const clipboardButton = document.getElementById("clipboardButton");

const wordCount = document.getElementById("wordCount");

const charCount = document.getElementById("charCount");

const clearJDButton = document.getElementById("clearJDButton");

const jdUploadZone = document.getElementById("jdUploadZone");

const uploadJDButton = document.getElementById("uploadJDButton");

function toggleJDInput() {
  if (pasteOption.checked) {
    pasteContainer.style.display = "block";
    uploadContainer.style.display = "none";
  } else if (uploadOption.checked) {
    pasteContainer.style.display = "none";
    uploadContainer.style.display = "block";
  }
}
pasteOption.addEventListener("change", toggleJDInput);

uploadOption.addEventListener("change", toggleJDInput);

function initializeJDModule() {
  toggleJDInput();
}

function openJDFileBrowser() {
  jdFileInput.click();
}
browseJDButton.addEventListener(
  "click",

  openJDFileBrowser,
);
function formatFileSize(fileSize) {
  const sizeInKB = fileSize / 1024;

  if (sizeInKB < 1024) {
    return sizeInKB.toFixed(1) + " KB";
  }

  const sizeInMB = sizeInKB / 1024;

  return sizeInMB.toFixed(2) + " MB";
}
function updateJDFileCard(file) {
  const extension = file.name.split(".").pop().toUpperCase();

  jdFileName.textContent = file.name;

  jdFileDetails.textContent = extension + " • " + formatFileSize(file.size);
}
function updateJDStatus(message, success = true) {
  jdStatus.textContent = message;

  if (success) {
    jdStatus.style.color = "#22C55E";
  } else {
    jdStatus.style.color = "#EF4444";
  }
}
const allowedFileTypes = ["pdf", "docx", "txt"];
const MAX_FILE_SIZE = 10 * 1024 * 1024;
function validateJDFile(file) {
  const extension = file.name.split(".").pop().toLowerCase();

  if (!allowedFileTypes.includes(extension)) {
    return {
      valid: false,

      message: "Only PDF, DOCX and TXT files are allowed.",
    };
  }

  if (file.size > MAX_FILE_SIZE) {
    return {
      valid: false,

      message: "Maximum file size is 10 MB.",
    };
  }

  return {
    valid: true,

    message: "Valid",
  };
}
function handleJDFileSelection(event) {
  const selectedFile = event.target.files[0];

  if (!selectedFile) {
    updateJDStatus(
      "No file selected.",

      false,
    );

    return;
  }

  const validation = validateJDFile(selectedFile);

  if (!validation.valid) {
    updateJDStatus(
      validation.message,

      false,
    );

    return;
  }

  updateJDStatus("JD selected. Click Upload Job Description.");
  jdState.uploadedFile = selectedFile;

  jdState.fileName = selectedFile.name;

  jdState.fileType = selectedFile.type;

  jdState.fileSize = selectedFile.size;

  jdState.isUploaded = true;

  uploadJDToServer(selectedFile);
}
jdFileInput.addEventListener(
  "change",

  handleJDFileSelection,
);
console.log("JD Module Loaded Successfully");
removeButton.addEventListener(
  "click",

  removeJDFile,
);
/* ==========================================
   JD MODULE STATE
========================================== */

const jdState = {
  uploadedFile: null,

  fileName: "",

  fileType: "",

  fileSize: 0,

  extractedText: "",

  parsedData: null,

  isUploaded: false,
};
function removeJDFile() {
  jdState.uploadedFile = null;

  jdState.fileName = "";

  jdState.fileType = "";

  jdState.fileSize = 0;

  jdState.extractedText = "";

  jdState.parsedData = null;

  jdState.isUploaded = false;

  jdFileInput.value = "";

  jdFileName.textContent = "No Job Description Selected";

  jdFileDetails.textContent = "Waiting for upload...";

  updateJDStatus("Waiting for Job Description...");
}
function updateJDCounts() {
  const text = jdTextarea.value.trim();

  charCount.textContent = text.length;

  if (text === "") {
    wordCount.textContent = 0;

    return;
  }

  const words = text.split(/\s+/);

  wordCount.textContent = words.length;
}
jdTextarea.addEventListener(
  "input",

  updateJDCounts,
);
async function pasteFromClipboard() {
  try {
    const clipboardText = await navigator.clipboard.readText();

    if (clipboardText.trim() === "") {
      updateJDStatus(
        "Clipboard is empty.",

        false,
      );

      return;
    }

    jdTextarea.value = clipboardText;

    updateJDCounts();

    updateJDStatus("✅ Job Description pasted successfully.");
  } catch (error) {
    updateJDStatus(
      "Clipboard permission denied.",

      false,
    );
  }
}
clipboardButton.addEventListener(
  "click",

  pasteFromClipboard,
);
function resetJDModule() {
  jdTextarea.value = "";

  updateJDCounts();

  removeJDFile();

  updateJDStatus("Waiting for Job Description...");
}
function clearJDData() {
  const confirmed = confirm("Clear the current Job Description?");

  if (!confirmed) {
    return;
  }

  resetJDModule();
}
clearJDButton.addEventListener(
  "click",

  clearJDData,
);
function highlightUploadZone() {
  jdUploadZone.classList.add("drag-active");
}
function removeHighlightUploadZone() {
  jdUploadZone.classList.remove("drag-active");
}
function preventDefaults(event) {
  event.preventDefault();

  event.stopPropagation();
}
["dragenter", "dragover"].forEach((eventName) => {
  jdUploadZone.addEventListener(
    eventName,

    function (event) {
      preventDefaults(event);

      highlightUploadZone();
    },
  );

  ["dragleave", "drop"].forEach((eventName) => {
    jdUploadZone.addEventListener(
      eventName,

      function (event) {
        preventDefaults(event);

        removeHighlightUploadZone();
      },
    );
  });
});
jdUploadZone.addEventListener(
  "drop",

  function (event) {
    handleFileDrop(event);
  },
);
function handleFileDrop(event) {
  const droppedFile = event.dataTransfer.files[0];

  if (!droppedFile) {
    return;
  }

  const validation = validateJDFile(droppedFile);

  if (!validation.valid) {
    updateJDStatus(validation.message, false);
    return;
  }
  updateJDFileCard(droppedFile);

  jdState.uploadedFile = droppedFile;

  jdState.fileName = droppedFile.name;

  jdState.fileType = droppedFile.type;

  jdState.fileSize = droppedFile.size;

  jdState.isUploaded = true;

  uploadJDToServer(droppedFile);
}
function processJDFile(file) {}
async function validateJobDescription() {
  let jobDescription = "";

  if (pasteOption.checked) {
    jobDescription = jdTextarea.value.trim();
  } else {
    if (!jdState.uploadedFile) {
      updateJDStatus("Please upload a Job Description.", false);

      return;
    }

    jobDescription = jdState.fileName;
  }

  if (jobDescription === "") {
    updateJDStatus("Job Description cannot be empty.", false);

    return;
  }

  try {
    updateJDStatus("Connecting to Server...");

    const response = await fetch("/api/jd/validate", {
      method: "POST",

      headers: {
        "Content-Type": "application/json",
      },

      body: JSON.stringify({
        jd_text: jobDescription,
      }),
    });

    const result = await response.json();

    console.log(result);
  } catch (error) {
    console.error(error);

    updateJDStatus("Server Connection Failed.", false);
  }
}
async function uploadJDToServer(formData) {
  try {
    updateJDStatus("Uploading JD...");

    const response = await fetch("/api/job-description/upload", {
      method: "POST",
      body: formData,
    });

    const result = await response.json();

    if (result.success) {
      jdState.fileName = result.data.filename;

      jdState.isUploaded = true;

      updateJDStatus(result.message);
    } else {
      updateJDStatus(result.message, false);
    }
  } catch (error) {
    console.error(error);

    updateJDStatus("Unable to connect to server.", false);
  }
}
uploadJDButton.addEventListener("click", async function () {
  try {
    // ========= PASTE JD =========

    if (pasteOption.checked) {
      const jdText = jdTextarea.value.trim();

      if (!jdText) {
        updateJDStatus("Please enter Job Description.", false);

        return;
      }

      const formData = new FormData();

      formData.append("jd_text", jdText);

      await uploadJDToServer(formData);

      return;
    }

    // ========= FILE JD =========

    if (!jdState.uploadedFile) {
      updateJDStatus("Please select JD file.", false);

      return;
    }

    const formData = new FormData();

    formData.append("job_description", jdState.uploadedFile);

    await uploadJDToServer(formData);
  } catch (error) {
    console.error(error);

    updateJDStatus("Upload failed.", false);
  }
});
uploadJDPButton.addEventListener("click", async function () {
  try {
    // ========= PASTE JD =========

    if (pasteOption.checked) {
      const jdText = jdTextarea.value.trim();

      if (!jdText) {
        updateJDStatus("Please enter Job Description.", false);

        return;
      }

      const formData = new FormData();

      formData.append("jd_text", jdText);

      await uploadJDToServer(formData);

      return;
    }

    // ========= FILE JD =========

    if (!jdState.uploadedFile) {
      updateJDStatus("Please select JD file.", false);

      return;
    }

    const formData = new FormData();

    formData.append("job_description", jdState.uploadedFile);

    await uploadJDToServer(formData);
  } catch (error) {
    console.error(error);

    updateJDStatus("Upload failed.", false);
  }
});
