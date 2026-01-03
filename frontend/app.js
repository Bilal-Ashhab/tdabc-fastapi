const API = "http://127.0.0.1:8000";

// ==========================
// Utility: inline notify
// ==========================
function notify(id, msg) {
    const el = document.getElementById(id);
    el.innerText = msg;
    setTimeout(() => el.innerText = "", 3000);
}

// ==========================
// Create Case
// ==========================
async function createCase() {
    const res = await fetch(`${API}/cases`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            patient_key: document.getElementById("patientKey").value,
            pathway: document.getElementById("pathway").value
        })
    });

    const data = await res.json();
    notify("caseResult", `Case created with ID: ${data.id}`);
}

// ==========================
// Add Event
// ==========================
async function addEvent() {
    const caseId = document.getElementById("eventCaseId").value;

    await fetch(`${API}/cases/${caseId}/events`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            event_type: document.getElementById("eventType").value
        })
    });

    notify("eventStatus", "Event added ✅");
}

// ==========================
// Add Delay
// ==========================
async function addDelay() {
    const caseId = document.getElementById("delayCaseId").value;

    await fetch(`${API}/cases/${caseId}/delays`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            code: document.getElementById("delayCode").value,
            minutes: parseInt(document.getElementById("delayMinutes").value)
        })
    });

    notify("delayStatus", "Delay added ✅");
}

// ==========================
// Calculate TDABC
// ==========================
async function calculateTDABC() {
    const caseId = document.getElementById("calcCaseId").value;

    const res = await fetch(`${API}/tdabc/calculate/${caseId}`, {
        method: "POST"
    });

    const data = await res.json();

    let html = `<h3>TDABC – Case ${data.case_id}</h3>`;
    html += `<table border="1" style="width:100%; border-collapse:collapse">
        <tr>
            <th>Activity</th>
            <th>Minutes</th>
            <th>Role</th>
            <th>Rate (₪/min)</th>
            <th>Cost (₪)</th>
        </tr>`;

    data.details.forEach(d => {
        html += `<tr>
            <td>${d.activity}</td>
            <td>${d.minutes}</td>
            <td>${d.resource}</td>
            <td>${d.rate}</td>
            <td>${d.cost}</td>
        </tr>`;
    });

    html += `<tr>
        <td><strong>Total</strong></td>
        <td><strong>${data.total_minutes}</strong></td>
        <td>-</td>
        <td>-</td>
        <td><strong>${data.total_cost}</strong></td>
    </tr>`;
    html += `</table>`;

    document.getElementById("tdabcResult").innerHTML = html;
}

// ==========================
// Dashboard
// ==========================
async function loadDashboard() {
    const res = await fetch("http://127.0.0.1:8000/dashboard/metrics");
    const data = await res.json();

    document.getElementById("totalCases").innerText = data.total_cases;
    document.getElementById("avgCaseTime").innerText = data.avg_case_time + " min";
    document.getElementById("csRate").innerText = data.cs_rate + "%";
}

