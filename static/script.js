function chooseOption(opt) {
  const container = document.getElementById("dynamicContainer");
  const result = document.getElementById("resultBox");
  result.innerHTML = "";

  if (opt === "weather") {
    container.innerHTML = `
      <div class="card p-3 shadow-sm">
        <h5>Weather Fetching</h5>
        <div class="mb-3">
          <button class="btn btn-outline-primary w-100" onclick="chooseWeatherType('date')">By Date</button>
          <button class="btn btn-outline-primary w-100 mt-2" onclick="chooseWeatherType('month')">By Month</button>
        </div>
      </div>`;
  } else {
    container.innerHTML = `
      <div class="card p-3 shadow-sm">
        <h5>Temperature Stats</h5>
        <input id="yearInput" type="number" placeholder="Enter Year" class="form-control mb-2">
        <button class="btn btn-success w-100" onclick="fetchStats()">Show Stats</button>
      </div>`;
  }
}

function chooseWeatherType(type) {
  const container = document.getElementById("dynamicContainer");
  if (type === "date") {
    container.innerHTML = `
      <div class="card p-3 shadow-sm">
        <h5>Weather by Date</h5>
        <input id="dateInput" type="date" class="form-control mb-2">
        <button class="btn btn-primary w-100" onclick="fetchByDate()">Fetch</button>
      </div>`;
  } else {
    container.innerHTML = `
      <div class="card p-3 shadow-sm">
        <h5>Weather by Month</h5>
        <input id="monthInput" type="number" class="form-control mb-2" placeholder="Enter Month (1-12)">
        <button class="btn btn-outline-primary w-100 mt-1" onclick="monthChoice(1)">1️⃣ First Occurrence</button>
        <button class="btn btn-outline-primary w-100 mt-1" onclick="monthChoice(2)">2️⃣ 20-Year Analysis</button>
        <button class="btn btn-outline-primary w-100 mt-1" onclick="monthChoice(3)">3️⃣ Specific Month of Year</button>
      </div>`;
  }
}

function monthChoice(choice) {
  const month = document.getElementById('monthInput').value;
  const box = document.getElementById('resultBox');
  box.innerHTML = '';

  if (!month) {
    box.innerHTML = '<p class="text-danger">⚠️ Please enter a valid month.</p>';
    return;
  }

  if (choice === 1) {
    fetch(`/weather-first-occurrence?month=${month}`)
      .then(r => r.json())
      .then(d => {
        box.textContent = JSON.stringify(d, null, 2);
      });
  } 
  else if (choice === 2) {
    fetch(`/weather-month-analysis?month=${month}`)
      .then(r => r.json())
      .then(d => {
        if (!Object.keys(d).length) {
          box.innerHTML = '<p class="text-warning">⚠️ No data available for that month.</p>';
          return;
        }
        const condRows = Object.entries(d.condition_counts)
          .map(([cond, count]) => `<tr><td>${cond}</td><td>${count}</td></tr>`)
          .join('');

        box.innerHTML = `
          <h5 class="text-primary">20-Year Month Analysis</h5>
          <table class="table table-bordered table-sm mt-3">
            <thead><tr><th>Condition</th><th>Occurrences</th></tr></thead>
            <tbody>${condRows}</tbody>
          </table>
          <p><strong>Min Temp:</strong> ${d.temp_min}°C</p>
          <p><strong>Median Temp:</strong> ${d.temp_median}°C</p>
          <p><strong>Max Temp:</strong> ${d.temp_max}°C</p>
        `;
      });
  } 
  else {
    const year = prompt("Enter Year:");
    if (!year) return;
    fetch(`/weather-month-year?month=${month}&year=${year}`)
      .then(r => r.json())
      .then(d => box.textContent = JSON.stringify(d, null, 2));
  }
}

function fetchByDate() {
  const date = document.getElementById("dateInput").value;
  const box = document.getElementById("resultBox");
  fetch(`/weather-date?date=${date}`)
    .then(r => r.json())
    .then(d => {
      if (!d.length) box.innerHTML = '<p class="text-warning">⚠️ No data found for this date.</p>';
      else box.textContent = JSON.stringify(d, null, 2);
    });
}

async function fetchStats() {
  const year = document.getElementById("yearInput").value;
  const res = await fetch(`/temperature-stats?year=${year}`);
  const data = await res.json();
  const box = document.getElementById("resultBox");
  if (!data.length) {
    box.innerHTML = '<p class="text-warning">⚠️ No data found for this year.</p>';
  } else {
    box.textContent = JSON.stringify(data, null, 2);
  }
}
