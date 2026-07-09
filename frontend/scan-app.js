/* ===========================================================
   MatchScan frontend logic
   =========================================================== */

const API_BASE = "/api";
const GAUGE_CIRCUMFERENCE = 578; // 2 * PI * r(92), matches styles.css

// ---------- State ----------
let resumeSourceText = "";   // text ultimately sent to the backend
let jdSourceText = "";

// ---------- Tab switching ----------
document.querySelectorAll(".doc-tab").forEach((tab) => {
  tab.addEventListener("click", () => {
    const panelName = tab.dataset.panel; // "resume" or "jd"
    const targetId = tab.dataset.target;

    document
      .querySelectorAll(`.doc-tab[data-panel="${panelName}"]`)
      .forEach((t) => t.classList.remove("active"));
    tab.classList.add("active");

    const parentPanel = panelName === "resume" ? resumePanel : jdPanel;
    parentPanel.querySelectorAll(".doc-input").forEach((el) => el.classList.remove("active"));
    document.getElementById(targetId).classList.add("active");
  });
});

const resumePanel = document.getElementById("resumePanel");
const jdPanel = document.getElementById("jdPanel");

// ---------- File upload helpers ----------
function setupDropzone({ dropzoneEl, inputEl, chipEl, nameEl, clearBtn, statusEl, onFile, onClear }) {
  dropzoneEl.addEventListener("click", () => inputEl.click());

  dropzoneEl.addEventListener("dragover", (e) => {
    e.preventDefault();
    dropzoneEl.classList.add("drag-over");
  });
  dropzoneEl.addEventListener("dragleave", () => dropzoneEl.classList.remove("drag-over"));
  dropzoneEl.addEventListener("drop", (e) => {
    e.preventDefault();
    dropzoneEl.classList.remove("drag-over");
    if (e.dataTransfer.files.length) {
      inputEl.files = e.dataTransfer.files;
      onFile(e.dataTransfer.files[0]);
    }
  });

  inputEl.addEventListener("change", () => {
    if (inputEl.files.length) onFile(inputEl.files[0]);
  });

  clearBtn.addEventListener("click", () => {
    inputEl.value = "";
    chipEl.hidden = true;
    dropzoneEl.hidden = false;
    statusEl.textContent = "";
    statusEl.className = "doc-status";
    onClear();
  });

  function showChip(file) {
    nameEl.textContent = file.name;
    chipEl.hidden = false;
    dropzoneEl.hidden = true;
  }

  return { showChip };
}

async function uploadFileToEndpoint(file, endpoint, statusEl) {
  statusEl.textContent = "Extracting text…";
  statusEl.className = "doc-status";
  const formData = new FormData();
  formData.append("file", file);

  const res = await authFetch(`${API_BASE}${endpoint}`, { method: "POST", body: formData });
  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error(err.detail || `Upload failed (${res.status})`);
  }
  const data = await res.json();
  statusEl.textContent = `Extracted ${data.word_count} words`;
  statusEl.className = "doc-status ok";
  return data.text;
}

// ---------- Resume dropzone ----------
const resumeDz = setupDropzone({
  dropzoneEl: document.getElementById("resumeDropzone"),
  inputEl: document.getElementById("resumeFileInput"),
  chipEl: document.getElementById("resumeFileChip"),
  nameEl: document.getElementById("resumeFileName"),
  clearBtn: document.getElementById("resumeFileClear"),
  statusEl: document.getElementById("resumeStatus"),
  onFile: async (file) => {
    const statusEl = document.getElementById("resumeStatus");
    resumeDz.showChip(file);
    try {
      resumeSourceText = await uploadFileToEndpoint(file, "/resume/upload", statusEl);
    } catch (e) {
      statusEl.textContent = e.message;
      statusEl.className = "doc-status error";
      resumeSourceText = "";
    }
  },
  onClear: () => { resumeSourceText = ""; },
});

// ---------- JD dropzone ----------
const jdDz = setupDropzone({
  dropzoneEl: document.getElementById("jdDropzone"),
  inputEl: document.getElementById("jdFileInput"),
  chipEl: document.getElementById("jdFileChip"),
  nameEl: document.getElementById("jdFileName"),
  clearBtn: document.getElementById("jdFileClear"),
  statusEl: document.getElementById("jdStatus"),
  onFile: async (file) => {
    const statusEl = document.getElementById("jdStatus");
    jdDz.showChip(file);
    try {
      jdSourceText = await uploadFileToEndpoint(file, "/jd/upload", statusEl);
    } catch (e) {
      statusEl.textContent = e.message;
      statusEl.className = "doc-status error";
      jdSourceText = "";
    }
  },
  onClear: () => { jdSourceText = ""; },
});

// ---------- Gather current text (from whichever tab is active) ----------
function getResumeText() {
  const pasteActive = document.getElementById("resumePaste").classList.contains("active");
  if (pasteActive) return document.getElementById("resumeTextArea").value.trim();
  return resumeSourceText.trim();
}

function getJdText() {
  const uploadActive = document.getElementById("jdUpload").classList.contains("active");
  if (uploadActive) return jdSourceText.trim();
  return document.getElementById("jdTextArea").value.trim();
}

// ---------- Scan action ----------
const scanBtn = document.getElementById("scanBtn");
const intakeError = document.getElementById("intakeError");

scanBtn.addEventListener("click", async () => {
  const resumeText = getResumeText();
  const jdText = getJdText();

  intakeError.hidden = true;

  if (!resumeText || !jdText) {
    intakeError.textContent = "Add both a resume and a job description before scanning.";
    intakeError.hidden = false;
    return;
  }

  scanBtn.disabled = true;
  scanBtn.classList.add("scanning");
  scanBtn.querySelector(".scan-btn-label").textContent = "Scanning…";

  try {
    const res = await authFetch(`${API_BASE}/match`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ resume_text: resumeText, jd_text: jdText }),
    });
    if (!res.ok) {
      const err = await res.json().catch(() => ({}));
      throw new Error(err.detail || `Scan failed (${res.status})`);
    }
    const data = await res.json();
    renderResults(data, resumeText);
  } catch (e) {
    intakeError.textContent = e.message || "Something went wrong. Check the server is running.";
    intakeError.hidden = false;
  } finally {
    scanBtn.disabled = false;
    scanBtn.classList.remove("scanning");
    scanBtn.querySelector(".scan-btn-label").textContent = "Run compatibility scan";
  }
});

// ---------- Render results ----------
const CATEGORY_LABELS = {
  languages: "Languages",
  backend_frameworks: "Backend Frameworks",
  frontend_frameworks: "Frontend Frameworks",
  databases: "Databases",
  orm_and_data: "ORM & Data",
  devops_cloud: "DevOps & Cloud",
  auth_security: "Auth & Security",
  apis_architecture: "APIs & Architecture",
  testing: "Testing",
  ai_ml: "AI / ML",
  other: "Other",
};

function renderResults(data, resumeText) {
  document.getElementById("intakeStage").hidden = true;
  const resultsStage = document.getElementById("resultsStage");
  resultsStage.hidden = false;

  // Gauge
  const score = Math.round(data.match_score);
  const offset = GAUGE_CIRCUMFERENCE - (GAUGE_CIRCUMFERENCE * data.match_score) / 100;
  const arc = document.getElementById("gaugeArc");
  const gaugeColor = score >= 70 ? "var(--green)" : score >= 40 ? "var(--amber)" : "var(--coral)";
  arc.style.stroke = gaugeColor;

  requestAnimationFrame(() => {
    arc.style.strokeDashoffset = offset;
  });
  animateNumber(document.getElementById("gaugeNumber"), score);

  // Sub scores
  document.getElementById("keywordFill").style.width = `${data.keyword_score}%`;
  document.getElementById("keywordValue").textContent = `${Math.round(data.keyword_score)}%`;
  document.getElementById("semanticFill").style.width = `${data.semantic_score}%`;
  document.getElementById("semanticValue").textContent = `${Math.round(data.semantic_score)}%`;
  document.getElementById("resumeSkillCount").textContent = data.resume_skill_count;
  document.getElementById("jdSkillCount").textContent = data.jd_skill_count;

  // Matched chips
  const matchedChips = document.getElementById("matchedChips");
  matchedChips.innerHTML = "";
  if (data.matched_skills.length === 0) {
    matchedChips.innerHTML = `<p class="empty-note">No overlapping skills found yet.</p>`;
  } else {
    data.matched_skills.forEach((skill) => {
      const chip = document.createElement("span");
      chip.className = "skill-chip";
      chip.textContent = skill;
      matchedChips.appendChild(chip);
    });
  }

  // Missing skills (grouped by category)
  const gapList = document.getElementById("gapList");
  gapList.innerHTML = "";
  if (data.missing_skills.length === 0) {
    gapList.innerHTML = `<p class="empty-note">No gaps detected — great coverage!</p>`;
  } else {
    data.missing_skills.forEach((item) => {
      const el = document.createElement("div");
      el.className = "gap-item";
      el.innerHTML = `
        <div class="gap-item-head">
          <span class="gap-skill">${item.skill}</span>
          <span class="gap-category">${CATEGORY_LABELS[item.category] || item.category}</span>
        </div>
        <p class="gap-recommendation">${item.recommendation}</p>
      `;
      gapList.appendChild(el);
    });
  }

  // Editor pre-filled with resume text so they can edit + rescan
  document.getElementById("editorTextArea").value = resumeText;

  resultsStage.scrollIntoView({ behavior: "smooth", block: "start" });
}

function animateNumber(el, target) {
  const duration = 900;
  const start = performance.now();
  function frame(now) {
    const progress = Math.min((now - start) / duration, 1);
    const eased = 1 - Math.pow(1 - progress, 3);
    el.textContent = Math.round(eased * target);
    if (progress < 1) requestAnimationFrame(frame);
  }
  requestAnimationFrame(frame);
}

// ---------- Rescan from editor ----------
document.getElementById("rescanBtn").addEventListener("click", async () => {
  const editedResume = document.getElementById("editorTextArea").value.trim();
  const jdText = getJdText();
  const btn = document.getElementById("rescanBtn");

  if (!editedResume || !jdText) return;

  btn.disabled = true;
  btn.textContent = "Recalculating…";

  try {
    const res = await authFetch(`${API_BASE}/match`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ resume_text: editedResume, jd_text: jdText }),
    });
    if (!res.ok) throw new Error("Recalculation failed");
    const data = await res.json();
    renderResults(data, editedResume);
  } catch (e) {
    alert(e.message);
  } finally {
    btn.disabled = false;
    btn.textContent = "Recalculate score";
  }
});

// ---------- Start over ----------
document.getElementById("startOverBtn").addEventListener("click", () => {
  document.getElementById("resultsStage").hidden = true;
  document.getElementById("intakeStage").hidden = false;
  window.scrollTo({ top: 0, behavior: "smooth" });
});