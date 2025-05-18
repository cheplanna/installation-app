<template>
  <div>
    <h1>Visitor Analytics Dashboard</h1>
    
    <button @click="fetchMetrics">Load Metrics</button>
    <canvas id="metricsChart" width="400" height="200"></canvas>
    
    <button @click="fetchPopularInstallations">Load Popular Installations</button>
    <canvas id="popularChart" width="400" height="200"></canvas>
    
    <button @click="fetchEvents">Load Events</button>
    <div v-if="events.length">
      <h2>Events</h2>
      <ul>
        <li v-for="event in events" :key="event.id">
          ID: {{ event.id }}, Installation: {{ event.installation_id }}, Event: {{ event.event_type }}, Time: {{ event.timestamp }}
        </li>
      </ul>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { Chart, registerables } from 'chart.js';

Chart.register(...registerables);

const metrics = ref([]);
const events = ref([]);
const popularInstallations = ref([]);

let metricsChart = null;
let popularChart = null;

async function fetchMetrics() {
  const res = await fetch('http://127.0.0.1:8000/metrics');
  const data = await res.json();
  metrics.value = data.metrics;
  renderMetricsChart();
}

async function fetchPopularInstallations() {
  const res = await fetch('http://127.0.0.1:8000/popular_installations');
  const data = await res.json();
  popularInstallations.value = data.popular_installations;
  renderPopularChart();
}

async function fetchEvents() {
  const res = await fetch('http://127.0.0.1:8000/events');
  const data = await res.json();
  events.value = data.events;
}

function renderMetricsChart() {
  const ctx = document.getElementById('metricsChart').getContext('2d');
  const labels = metrics.value.map(m => `${m.installation_id} (${m.event_type})`);
  const counts = metrics.value.map(m => m.count);
  
  if (metricsChart) {
    metricsChart.destroy();
  }
  
  metricsChart = new Chart(ctx, {
    type: 'bar',
    data: {
      labels: labels,
      datasets: [{
        label: 'Event Counts',
        data: counts,
        backgroundColor: 'rgba(54, 162, 235, 0.6)',
        borderColor: 'rgba(54, 162, 235, 1)',
        borderWidth: 1
      }]
    },
    options: {
      scales: {
        y: {
          beginAtZero: true
        }
      }
    }
  });
}

function renderPopularChart() {
  const ctx = document.getElementById('popularChart').getContext('2d');
  const labels = popularInstallations.value.map(p => p.installation_id);
  const counts = popularInstallations.value.map(p => p.event_count);
  
  if (popularChart) {
    popularChart.destroy();
  }
  
  popularChart = new Chart(ctx, {
    type: 'pie',
    data: {
      labels: labels,
      datasets: [{
        label: 'Popular Installations',
        data: counts,
        backgroundColor: [
          'rgba(255, 99, 132, 0.6)',
          'rgba(54, 162, 235, 0.6)',
          'rgba(255, 206, 86, 0.6)',
          'rgba(75, 192, 192, 0.6)',
          'rgba(153, 102, 255, 0.6)',
          'rgba(255, 159, 64, 0.6)'
        ],
        borderWidth: 1
      }]
    },
    options: {
      responsive: true,
    }
  });
}
</script>

<style>
body {
  font-family: Arial, sans-serif;
  padding: 20px;
}
h1 {
  color: #333;
}
button {
  margin: 10px 0;
  padding: 10px;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}
button:hover {
  background-color: #0056b3;
}
canvas {
  margin-top: 20px;
}
</style>
