document.getElementById("checkBtn").addEventListener("click", async () => {

  const [tab] = await chrome.tabs.query({active: true, currentWindow: true});
  const url = tab.url;

  const response = await fetch("http://127.0.0.1:5000/predict", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({ url: url })
  });

  const data = await response.json();

  const outputDiv = document.getElementById("output");

  let riskClass = "";
  if (data.risk_level === "High Risk") riskClass = "high";
  else if (data.risk_level === "Medium Risk") riskClass = "medium";
  else riskClass = "low";

  outputDiv.innerHTML = `
    <p><strong>URL:</strong> ${data.url}</p>
    <p><strong>Prediction:</strong> ${data.prediction}</p>
    <p><strong>Risk Level:</strong> <span class="${riskClass}">${data.risk_level}</span></p>
    <p><strong>Block Recommended:</strong> ${data.block_recommended}</p>
  `;
});