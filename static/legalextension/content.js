// Step 1: Detect possible legal text
function findTerms() {
  const text = document.body.innerText.toLowerCase();

  if (
    text.includes("terms") ||
    text.includes("privacy") ||
    text.includes("cookies")
  ) {
    return document.body.innerText.slice(0, 1000);
  }
  return null;
}

// Step 2: Create floating UI box
function createBox(content) {
  // Prevent duplicate box
  if (document.getElementById("legal-box")) return;

  const box = document.createElement("div");
  box.id = "legal-box";

  box.innerHTML = `
    <h3>⚖️ Legal Simplifier</h3>
    <p>${content}</p>
  `;

  document.body.appendChild(box);
}

// Step 3: Run logic
const termsText = findTerms();

if (termsText) {
  createBox("Analyzing terms...");

  fetch("http://127.0.0.1:5000/analyze", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({
      text: termsText
    })
  })
  .then(res => res.json())
  .then(data => {
    document.getElementById("legal-box").innerHTML = `
      <h3>⚖️ Legal Simplifier</h3>
      <pre>${data.result}</pre>
    `;
  })
  .catch(err => {
    document.getElementById("legal-box").innerText = "Error connecting to server";
    console.error(err);
  }); 
}