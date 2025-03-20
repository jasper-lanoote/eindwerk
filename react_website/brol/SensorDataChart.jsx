import React, { useState, useEffect } from 'react';
import { Line } from 'react-chartjs-2';
import { Chart as ChartJS, CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend } from 'chart.js';

ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend);

const SensorDataChart = ({ data }) => {
  const [selectedData, setSelectedData] = useState('temperature');  // Begin met temperatuur als geselecteerde data

  const handleChange = (event) => {
    setSelectedData(event.target.value);  // Verander het geselecteerde data type
  };

  // Verwerk de data in het formaat dat Chart.js verwacht
  const chartData = {
    labels: data.map(item => new Date(item.timestamp).toLocaleString()),  // Gebruik de tijdstempel als labels
    datasets: [
      {
        label: selectedData.charAt(0).toUpperCase() + selectedData.slice(1),  // Maak de eerste letter van de label hoofdletter
        data: data.map(item => item[selectedData]),  // Haal de geselecteerde data op (temperatuur, vochtigheid, etc.)
        borderColor: 'rgba(75, 192, 192, 1)',
        backgroundColor: 'rgba(75, 192, 192, 0.2)',
        fill: false,
      },
    ],
  };

  return (
    <div>
      <h2>Sensor Data Chart</h2>

      {/* Selectie voor het kiezen van de data */}
      <select value={selectedData} onChange={handleChange}>
        <option value="temperature">Temperatuur</option>
        <option value="humidity">Vochtigheid</option>
        <option value="pressure">Druk</option>
        <option value="gas">Gas (PPM)</option>
        <option value="wind_speed_kmh">Windsnelheid (km/h)</option>
      </select>

      {/* Chart.js grafiek */}
      <Line data={chartData} />
    </div>
  );
};

export default SensorDataChart;
