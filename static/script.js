async function fetchWeather() {
  const date = document.getElementById('dateInput').value;
  const month = document.getElementById('monthInput').value;
  let url = `/weather?`;
  if (date) url += `date=${date}`;
  else if (month) url += `month=${month}`;
  const res = await fetch(url);
  const data = await res.json();
  document.getElementById('weatherResult').textContent = JSON.stringify(data, null, 2);
}

async function fetchStats() {
  const year = document.getElementById('yearInput').value;
  const res = await fetch(`/temperature-stats?year=${year}`);
  const data = await res.json();
  const table = document.getElementById('statsTable');
  table.innerHTML = '';
  data.forEach(r => {
    table.innerHTML += `<tr><td>${r.Month}</td><td>${r.max.toFixed(1)}</td><td>${r.median.toFixed(1)}</td><td>${r.min.toFixed(1)}</td></tr>`;
  });
}
