import React, { useEffect, useState } from 'react';
import Chart from 'chart.js/auto'; // Importeer Chart.js

const RegenMetingenGrafiek = () => {
  const [dataPerDag, setDataPerDag] = useState({});
  const [selectedDay, setSelectedDay] = useState('');
  const [chart, setChart] = useState(null);

  useEffect(() => {
    // Haal de data op van de Django API
    fetch('http://192.168.0.232:8000/Weerstation/api/regenmetingen/') // Pas deze URL aan naar jouw Django API
      .then(response => response.json())
      .then(data => {
        // Organiseer de data per dag
        const groupedData = groupDataByDay(data);
        setDataPerDag(groupedData);

        // Stel de eerste dag in
        const firstDay = Object.keys(groupedData)[0];
        if (firstDay) {
          setSelectedDay(firstDay);
        }
      })
      .catch(error => console.error('Fout bij het ophalen van data:', error));
  }, []);

  useEffect(() => {
    // Als er een geselecteerde dag is, maak de grafiek
    if (selectedDay && dataPerDag[selectedDay]) {
      const uren = Array.from({ length: 24 }, (_, i) => `${i}:00`);
      const regenData = dataPerDag[selectedDay] || [];

      // Verwijder de oude grafiek als die bestaat
      if (chart) {
        chart.destroy();
      }

      // Maak de nieuwe grafiek
      const ctx = document.getElementById('regenGrafiek').getContext('2d');
      const newChart = new Chart(ctx, {
        type: 'bar', // Staafdiagram
        data: {
          labels: uren, // Urenlabels
          datasets: [
            {
              label: 'Regenval per Uur (mm)',
              data: regenData,
              backgroundColor: 'rgba(75, 192, 192, 0.2)',
              borderColor: 'rgba(75, 192, 192, 1)',
              borderWidth: 1,
            },
          ],
        },
        options: {
          scales: {
            x: {
              title: {
                display: true,
                text: 'Uur',
              },
            },
            y: {
              title: {
                display: true,
                text: 'Regenval (mm)',
              },
              beginAtZero: true,
            },
          },
        },
      });

      setChart(newChart);
    }
  }, [selectedDay, dataPerDag]);

  // Functie om de data te groeperen op basis van de dag
  const groupDataByDay = (data) => {
    const grouped = {};
    data.forEach((item) => {
      const dag = item.tijdstip.split('T')[0]; // Datum zonder tijd
      if (!grouped[dag]) {
        grouped[dag] = new Array(24).fill(0); // Maak een array van 24 uren, ingevuld met nullen
      }
      const uur = new Date(item.tijdstip).getHours(); // Verkrijg het uur van de tijd
      grouped[dag][uur] += item.regenval; // Voeg de regenval toe voor het juiste uur
    });
    return grouped;
  };

  // Functie om de data voor een dag te krijgen
  const handleDayChange = (event) => {
    setSelectedDay(event.target.value);
  };

  return (
    <div>
      <h1>Regenmetingen per Uur</h1>

      {/* Dropdown-menu voor dagen */}
      <label htmlFor="daySelector">Selecteer een dag:</label>
      <select id="daySelector" onChange={handleDayChange} value={selectedDay}>
        {Object.keys(dataPerDag).map((dag) => (
          <option key={dag} value={dag}>
            {dag}
          </option>
        ))}
      </select>

      {/* Grafiek */}
      <canvas id="regenGrafiek" width="400" height="200"></canvas>
    </div>
  );
};

export default RegenMetingenGrafiek;
