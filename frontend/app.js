const API = "";  // Same origin

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
    document.getElementById("caseResult").innerText = `Case created with ID ${data.id}`;
}

async function addEvent() {
    const id = document.getElementById("eventCaseId").value;
    await fetch(`${API}/cases/${id}/events`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            event_type: document.getElementById("eventType").value
        })
    });
    document.getElementById("eventStatus").innerText = "Event added ✓";
}

async function addDelay() {
    const id = document.getElementById("delayCaseId").value;
    await fetch(`${API}/cases/${id}/delays`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            code: document.getElementById("delayCode").value,
            minutes: Number(document.getElementById("delayMinutes").value)
        })
    });
    document.getElementById("delayStatus").innerText = "Delay added ✓";
}

async function calculateTDABC() {
    const id = document.getElementById("calcCaseId").value;
    const res = await fetch(`${API}/tdabc/calculate/${id}`, { method: "POST" });
    const data = await res.json();

    let html = `<table>
        <tr>
            <th>Activity</th>
            <th>Minutes</th>
            <th>Role</th>
            <th>Rate</th>
            <th>Cost</th>
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
        <td>${data.total_minutes}</td>
        <td>-</td>
        <td>-</td>
        <td>${data.total_cost}</td>
    </tr></table>`;

    document.getElementById("tdabcResult").innerHTML = html;
}

async function loadDashboard() {
    const res = await fetch(`${API}/dashboards/metrics`);
    const data = await res.json();

    document.getElementById("totalCases").innerText = data.total_cases;
    document.getElementById("avgCaseTime").innerText = `${data.avg_case_time} min`;
    document.getElementById("csRate").innerText = `${data.cs_rate}%`;
}
