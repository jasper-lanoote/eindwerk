import React, { useEffect, useState } from 'react';

import './Livesensor.css'

export default function Livesensor() {
  const [sensorData, setSensorData] = useState(null);

  useEffect(() => {
    // Maak de WebSocket-verbinding
    const ws = new WebSocket('ws://192.168.0.232:8000/ws/sensoren/');

    // Wanneer de verbinding is geopend
    ws.onopen = () => {
      console.log('Verbonden met WebSocket-server');
    };

    // Wanneer een bericht ontvangen wordt
    ws.onmessage = (event) => {
      const data = JSON.parse(event.data);
      //console.log('Ontvangen sensor data:', data);

      // Werk de sensorData bij
      setSensorData(data);
    };

    // Fouten afhandelen
    ws.onerror = (event) => {
      console.error('WebSocket-fout:', event);
    };

    // Wanneer de verbinding wordt gesloten
    ws.onclose = () => {
      console.log('WebSocket-verbinding gesloten');
    };

    // Opruimen bij component unmount
    return () => {
      if (ws) {
        ws.close();
      }
    };
  }, []);

  return (
    <div className='flexbox'>
      <h2>Live sensor data</h2>
      {/* Controleer of we data ontvangen hebben */}
      <div>
        {sensorData ? (
          <table>
            <thead>
              <tr>
                <th> Temperatuur °C </th>
                <th> Vochtigheid % </th>
                <th> Druk hPa </th>
                <th> Gas PPM </th>
                <th> Wind Snelheid km/h </th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td>{sensorData.temperature}</td>
                <td>{sensorData.humidity}</td>
                <td>{sensorData.pressure}</td>
                <td>{sensorData.gas}</td>
                <td>{sensorData.wind_speed_kmh}</td>
              </tr>
            </tbody>
          </table>
        ) : (
          <p>Wachten op gegevens...</p>
        )}
      </div>
    </div>
  );
};

