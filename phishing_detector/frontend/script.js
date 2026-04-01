let currentURL = "";

// ================= SCAN =================
function checkURL() {
  const input = document.getElementById("url");
  const result = document.getElementById("result");
  const btn = document.getElementById("scanButton");
  const continueBtn = document.getElementById("continueBtn");

  let url = input.value.trim();
  
  // Guard against empty input
  if (!url) {
    result.textContent = "Please enter a URL to scan.";
    result.style.color = "#ff7a7a";
    document.getElementById("analysisBox").style.display = "none";
    document.querySelector(".status-box").style.boxShadow = "none";
    continueBtn.style.display = "none";
    return;
  }

  // Basic domain check: must contain a dot
  if (!url.includes(".")) {
    result.textContent = "Please enter a valid URL (e.g., example.com).";
    result.style.color = "#ff7a7a";
    btn.disabled = false;
    return;
  }

  if (!url.startsWith("http")) url = "https://" + url;

  btn.disabled = true;
  result.textContent = "🔍 Scanning...";
  result.style.color = "#edf0ff"; // Reset colour during scan
  continueBtn.style.display = "none";
  document.getElementById("analysisBox").style.display = "none"; // Hide previous analysis during scan
  document.querySelector(".status-box").style.boxShadow = "none"; // Reset glowing shadow

  try {
    currentURL = new URL(url).href;
  } catch {
    result.textContent = "Invalid URL format.";
    result.style.color = "#ff7a7a";
    btn.disabled = false;
    return;
  }

  // Call the Flask backend API
  fetch("http://127.0.0.1:5000/predict", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({ url: url })
  })
  .then(response => {
    if (!response.ok) {
        throw new Error("Server response was not ok");
    }
    return response.json();
  })
  .then(data => {
    const isSafe = data.safe;
    const score = data.trust_score;
    const warning = data.warning;

    const status = isSafe ? "SAFE" : "DANGEROUS";
    result.textContent = status;
    result.style.color = isSafe ? "#8cff99" : "#ff7a7a";

    if (isSafe) continueBtn.style.display = "block";

    addToHistory(url, status);
    updateAnalysis(url, isSafe, score, warning);
    
    btn.disabled = false;
  })
  .catch(error => {
    console.error("Error connecting to backend:", error);
    result.textContent = "Error: Cannot reach server.";
    result.style.color = "orange";
    
    // Provide a fallback UI that shows null values safely
    updateAnalysis(url, null, null);
    
    btn.disabled = false;
  });
}

// ================= ANALYSIS =================
function updateAnalysis(url, isSafe, backendScore, backendWarning) {
  const box = document.getElementById("analysisBox");
  const desc = document.getElementById("siteDescription");
  const features = document.getElementById("featureList");
  const trust = document.getElementById("trustScore");
  const warn = document.getElementById("securityWarning");

  box.style.display = "block";

  const domain = new URL(url).hostname;

  desc.textContent =
    isSafe === null
      ? `${domain}: Unable to fully verify (server offline).`
      : isSafe
        ? `${domain}: This website appears legitimate.`
        : `${domain}: This website may be dangerous.`;
  
  if (backendWarning) {
      desc.textContent = `${domain}: ${backendWarning}`;
  }

  features.innerHTML = `
    <p>🔐 HTTPS: ${url.startsWith("https") ? "Secure" : "Not Secure"}</p>
    <p>📏 URL Length: ${url.length > 50 ? "Long" : "Short"}</p>
    <p>⚠️ Suspicious: ${/[@\-]/.test(url) ? "Yes" : "No"}</p>
  `;

  let score;
  if (isSafe === null) {
    score = "N/A";
  } else if (backendScore !== undefined && backendScore !== null) {
    score = `${backendScore}%`;
  }

  trust.textContent = `Trust Score: ${score}`;
  trust.style.color =
    isSafe === null ? "orange" :
    isSafe ? "#8cff99" : "#ff7a7a";

  warn.textContent =
    isSafe === null
      ? "⚠️ Unable to fully verify"
      : isSafe
        ? "✅ Safe but stay cautious"
        : "⚠️ Do not enter sensitive data";

  document.querySelector(".status-box").style.boxShadow =
    isSafe === null
      ? "0 0 15px orange"
      : isSafe
        ? "0 0 20px green"
        : "0 0 20px red";
}

// ================= HISTORY =================
function addToHistory(url, status) {
  if (!isLoggedIn()) return;

  let history = JSON.parse(localStorage.getItem("history") || "[]");
  history.unshift({ url, status });

  localStorage.setItem("history", JSON.stringify(history));
  loadHistory();
}

function loadHistory() {
  const list = document.getElementById("history");
  if (!list) return;

  list.innerHTML = "";

  let history = JSON.parse(localStorage.getItem("history") || "[]");

  if (history.length === 0) {
    list.innerHTML = "<li>No scans yet</li>";
    return;
  }

  history.forEach((item, index) => {
    const li = document.createElement("li");
    li.className = "history-item";

    const contentDiv = document.createElement("div");
    const strong = document.createElement("strong");
    strong.textContent = item.status;
    contentDiv.appendChild(strong);
    contentDiv.appendChild(document.createTextNode(` - ${item.url}`));

    const deleteBtn = document.createElement("button");
    deleteBtn.className = "delete-item-btn";
    deleteBtn.innerHTML = "×";
    deleteBtn.onclick = () => deleteHistoryItem(index);

    li.appendChild(contentDiv);
    li.appendChild(deleteBtn);
    list.appendChild(li);
  });
}

function clearAllHistory() {
  if (confirm("Are you sure you want to clear all your scan history?")) {
    localStorage.removeItem("history");
    loadHistory();
  }
}

function deleteHistoryItem(index) {
  let history = JSON.parse(localStorage.getItem("history") || "[]");
  history.splice(index, 1);
  localStorage.setItem("history", JSON.stringify(history));
  loadHistory();
}

// ================= AUTH =================
function isLoggedIn() {
  return localStorage.getItem("safeBrowseLoggedIn") === "true";
}

function updateAuthUI() {
  const auth = document.getElementById("authLink");
  const logout = document.getElementById("logoutLink");
  const historyBtn = document.getElementById("historyLink");
  const historySec = document.getElementById("historySection");

  if (isLoggedIn()) {
    const user = localStorage.getItem("safeBrowseUser");

    auth.textContent = `Welcome, ${user}`;
    auth.href = "#";

    logout.style.display = "inline";
    historyBtn.style.display = "inline";
    historySec.style.display = "block";

    loadHistory();
  } else {
    auth.textContent = "Sign In / Register";
    auth.href = "login.html";

    logout.style.display = "none";
    historyBtn.style.display = "none";
    historySec.style.display = "none";
  }
}

document.getElementById("logoutLink").onclick = () => {
  localStorage.removeItem("safeBrowseLoggedIn");
  localStorage.removeItem("safeBrowseUser");
  updateAuthUI();
};

// ================= SCROLL =================
function scrollToHistory() {
  document.getElementById("historySection").scrollIntoView({ behavior: "smooth" });
}

// ================= NAVIGATION =================
function goToSite() {
  if (currentURL) {
    window.location.href = currentURL;
  }
}

window.onload = updateAuthUI;