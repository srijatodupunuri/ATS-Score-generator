/* ==========================================
   RESUME MODULE
========================================== */

const browseResumeButton = document.getElementById("browseResumeButton");
const uploadResumeButton = document.getElementById("uploadResumeButton");
const resumeFileInput = document.getElementById("resumeFileInput");
const resumeUploadZone = document.getElementById("resumeUploadZone");
const resumeList = document.getElementById("resumeList");
const resumePlaceholder = document.getElementById("resumePlaceholder");
const resumeStatus = document.getElementById("resumeStatus");

/* ==========================================
   RESUME MODULE STATE
========================================== */

const resumeState = {
  selectedFiles: [],
  uploadedFiles: [],
  failedFiles: [],
  totalFiles: 0,
  uploadCompleted: false,
};

/* ==========================================
   RESUME VALIDATION
========================================== */

const ALLOWED_RESUME_EXTENSIONS = ["pdf", "docx", "txt"];

const MAX_RESUME_FILE_SIZE = 16 * 1024 * 1024;

/* ==========================================
   INITIALIZATION
========================================== */

function updateResumeStatus(message, success = true) {
  resumeStatus.textContent = message;

  if (success) {
    resumeStatus.style.color = "#22C55E";
  } else {
    resumeStatus.style.color = "#EF4444";
  }
}

function initializeResumeModule() {
  uploadResumeButton.disabled = true;

  updateResumeStatus("Waiting for resumes...");
}
["dragenter", "dragover", "dragleave", "drop"].forEach((eventName) => {
  resumeUploadZone.addEventListener(eventName, preventDefaultDragBehavior);
});
function highlightResumeUploadZone() {
  resumeUploadZone.classList.add("drag-active");
}

function unhighlightResumeUploadZone() {
  resumeUploadZone.classList.remove("drag-active");
}
["dragenter", "dragover"].forEach((eventName) => {
  resumeUploadZone.addEventListener(eventName, highlightResumeUploadZone);
});
["dragleave", "drop"].forEach((eventName) => {
  resumeUploadZone.addEventListener(eventName, unhighlightResumeUploadZone);
});

function openResumeFileBrowser() {
  resumeFileInput.click();
}

browseResumeButton.addEventListener("click", openResumeFileBrowser);

initializeResumeModule();

console.log("Resume Module Loaded Successfully");
function handleResumeSelection(event) {
  const selectedFiles = Array.from(event.target.files);

  processSelectedResumes(selectedFiles);

  resumeFileInput.value = "";
}
function isAllowedResumeType(file) {
  const fileName = file.name.toLowerCase();

  const extension = fileName.split(".").pop();

  return ALLOWED_RESUME_EXTENSIONS.includes(extension);
}
function isValidResumeSize(file) {
  return file.size <= MAX_RESUME_FILE_SIZE;
}
function isDuplicateResume(file) {
  return resumeState.selectedFiles.some((existingFile) => {
    return existingFile.name === file.name && existingFile.size === file.size;
  });
}
function validateResume(file) {
  if (!isAllowedResumeType(file)) {
    return {
      valid: false,
      message: `${file.name} has an unsupported file type.`,
    };
  }

  if (!isValidResumeSize(file)) {
    return {
      valid: false,
      message: `${file.name} exceeds the 16 MB size limit.`,
    };
  }

  if (isDuplicateResume(file)) {
    return {
      valid: false,
      message: `${file.name} has already been selected.`,
    };
  }

  return {
    valid: true,
  };
}
function handleResumeDrop(event) {
  const droppedFiles = Array.from(event.dataTransfer.files);

  processSelectedResumes(droppedFiles);
}
resumeUploadZone.addEventListener("drop", handleResumeDrop);
function formatResumeFileSize(fileSize) {
  const sizeInKB = fileSize / 1024;

  if (sizeInKB < 1024) {
    return `${sizeInKB.toFixed(1)} KB`;
  }

  const sizeInMB = sizeInKB / 1024;

  return `${sizeInMB.toFixed(2)} MB`;
}
function getResumeUploadStatus(file) {
  const uploaded = resumeState.uploadedFiles.find((item) => {
    return item.original_filename === file.name;
  });

  if (uploaded) {
    return {
      success: true,
      message: "Uploaded Successfully",
    };
  }

  const failed = resumeState.failedFiles.find((item) => {
    return item.original_filename === file.name;
  });

  if (failed) {
    return {
      success: false,
      message: failed.error,
    };
  }

  return null;
}
function createResumeCard(file, index) {
  const uploadStatus = getResumeUploadStatus(file);

  let statusHTML = "";

  if (uploadStatus) {
    statusHTML = `
      <div class="${
        uploadStatus.success ? "resume-upload-success" : "resume-upload-error"
      }">
        ${uploadStatus.success ? "✓" : "✗"}
        ${uploadStatus.message}
      </div>
    `;
  }

  return `
    <div class="resume-file-card">

      <div class="resume-file-info">

        <div class="resume-file-icon">
          <i class="fa-solid fa-file-lines"></i>
        </div>

        <div class="resume-file-text">

          <div class="resume-file-name">
            ${file.name}
          </div>

          <div class="resume-file-size">
            ${formatResumeFileSize(file.size)}
          </div>

          ${statusHTML}

        </div>

      </div>

      <button
        class="remove-resume-btn"
        data-index="${index}"
      >
        Remove
      </button>

    </div>
  `;
}
function renderResumeList() {
  if (resumeState.selectedFiles.length === 0) {
    resumeList.innerHTML = `
            <p
                id="resumePlaceholder"
                class="resume-placeholder"
            >
                No resumes selected.
            </p>
        `;

    return;
  }

  resumeList.innerHTML = "";

  resumeState.selectedFiles.forEach((file, index) => {
    resumeList.innerHTML += createResumeCard(file, index);
  });
}
function processSelectedResumes(files) {
  if (files.length === 0) {
    updateResumeStatus("No resumes selected.", false);
    return;
  }

  let validFilesAdded = 0;

  files.forEach((file) => {
    const validation = validateResume(file);

    if (!validation.valid) {
      updateResumeStatus(validation.message, false);
      return;
    }

    resumeState.selectedFiles.push(file);

    validFilesAdded++;
  });

  resumeState.totalFiles = resumeState.selectedFiles.length;

  renderResumeList();
  uploadResumeButton.disabled = resumeState.selectedFiles.length === 0;

  if (validFilesAdded > 0) {
    updateResumeStatus(`${resumeState.totalFiles} resume(s) selected.`);
  }
}
function removeResume(index) {
  resumeState.selectedFiles.splice(index, 1);

  resumeState.totalFiles = resumeState.selectedFiles.length;

  renderResumeList();

  // Always update button state
  uploadResumeButton.disabled = resumeState.selectedFiles.length === 0;

  if (resumeState.totalFiles === 0) {
    updateResumeStatus("Waiting for resumes...");

    return;
  }

  updateResumeStatus(`${resumeState.totalFiles} resume(s) selected.`);
}
async function uploadResumes() {
  if (resumeState.selectedFiles.length === 0) {
    updateResumeStatus("Please select at least one resume.", false);
    return;
  }

  updateResumeStatus("Uploading resumes...");

  const formData = new FormData();

  resumeState.selectedFiles.forEach((file) => {
    formData.append("resumes", file);
  });

  try {
    const response = await fetch("/api/resume/upload", {
      method: "POST",
      body: formData,
    });

    const result = await response.json();

    if (result.success) {
      resumeState.uploadCompleted = true;

      updateResumeStatus(
        `${result.data.uploaded_files.length} resume(s) uploaded successfully.`,
      );

      resumeState.uploadedFiles = result.data.uploaded_files;
      resumeState.failedFiles = result.data.failed_files;
      renderResumeList();
      console.log(resumeState.uploadedFiles);
    } else {
      if (result.data.failed_files.length > 0) {
        console.warn(result.data.failed_files);
      }
      updateResumeStatus(result.message, false);
    }
  } catch (error) {
    console.error(error);

    updateResumeStatus("Unable to connect to the server.", false);
  }
}
uploadResumeButton.addEventListener("click", uploadResumes);
resumeList.addEventListener("click", (event) => {
  const removeButton = event.target.closest(".remove-resume-btn");

  if (!removeButton) {
    return;
  }

  const index = Number(removeButton.dataset.index);

  removeResume(index);
});
function preventDefaultDragBehavior(event) {
  event.preventDefault();

  event.stopPropagation();
}
