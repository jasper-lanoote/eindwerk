import React, { useState, useEffect } from 'react';
import axios from "axios";
import dayjs from 'dayjs';
import DatePicker from 'react-datepicker';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend } from 'recharts';
import 'react-datepicker/dist/react-datepicker.css';

const apiEndPoint = 'http://192.168.0.232:8000/Weerstation/api/sensordata/';

const Testen = () => {
  const [data, setData] = useState([]);
  const [filteredData, setFilteredData] = useState([]);
  const [selectedDate, setSelectedDate] = useState(new Date());
  const [timeFilter, setTimeFilter] = useState('day');
  const [selectedMetrics, setSelectedMetrics] = useState([
    "temperature",
    "humidity",
    "pressure",
    "wind_speed_kmh",
    "gas"
  ]);

  // ✅ Data ophalen bij laden van de component
  useEffect(() => {
    axios.get(apiEndPoint).then(({ data }) => setData(data));
  }, []);

  // ✅ Data filteren op basis van de geselecteerde periode
  useEffect(() => {
    filterData();
  }, [data, selectedDate, timeFilter]);

  const filterData = () => {
    const selected = dayjs(selectedDate);
  
    let filtered = data
      .filter((item) => {
        const date = dayjs(item.timestamp);
        switch (timeFilter) {
          case 'day':
            return date.isSame(selected, 'day');
          case 'week':
            return date.isSame(selected, 'week');
          case 'month':
            return date.isSame(selected, 'month');
          case 'year':
            return date.isSame(selected, 'year');
          default:
            return true;
        }
      })
      .map((item) => ({
        ...item,
        // ✅ Filter temperaturen onder -40 eruit
        temperature: item.temperature < -40 || item.temperature > 55 ? null : item.temperature,
        wind_speed_kmh: item.wind_speed_kmh ?? 0, // Fallback voor ontbrekende waarde
        druk: item.druk < 700 || item.druk > 1050 ? null : item.druk,
        luchtvochtigheid: item.luchtvochtigheid < 98 || item.luchtvochtigheid > 3 ? null : item.luchtvochtigheid,

      }))
      // ✅ Outliers eruit filteren door `null` waardes te negeren
      .filter((item) => item.temperature !== null);
  
    setFilteredData(filtered);
  };
  
  // ✅ Metrics toggelen (aan/uit zetten)
  const toggleMetric = (metric) => {
    setSelectedMetrics((prev) =>
      prev.includes(metric)
        ? prev.filter((m) => m !== metric)
        : [...prev, metric]
    );
  };

  return (
    <div style={{ padding: '20px' }}>
      {/* 🔹 Datumkiezer met z-index */}
      <div style={{ marginBottom: '20px', position: 'relative', zIndex: 999 }}>
        <DatePicker
          selected={selectedDate}
          onChange={(date) => setSelectedDate(date)}
          dateFormat="yyyy-MM-dd"
          placeholderText="Selecteer een datum"
          style={{
            padding: '10px',
            border: '1px solid #ccc',
            borderRadius: '4px',
            width: '200px',
          }}
        />
      </div>

      {/* 🔹 Tijdfilters */}
      <div style={{ marginBottom: '20px' }}>
        <button onClick={() => setTimeFilter('day')}>Dag</button>
        <button onClick={() => setTimeFilter('week')}>Week</button>
        <button onClick={() => setTimeFilter('month')}>Maand</button>
        <button onClick={() => setTimeFilter('year')}>Jaar</button>
      </div>

      {/* 🔹 Checkboxes voor metrics */}
      <div style={{ marginBottom: '20px' }}>
        <label>
          <input
            type="checkbox"
            checked={selectedMetrics.includes('temperature')}
            onChange={() => toggleMetric('temperature')}
          />
          Temperatuur
        </label>
        <label>
          <input
            type="checkbox"
            checked={selectedMetrics.includes('humidity')}
            onChange={() => toggleMetric('humidity')}
          />
          Luchtvochtigheid
        </label>
        <label>
          <input
            type="checkbox"
            checked={selectedMetrics.includes('pressure')}
            onChange={() => toggleMetric('pressure')}
          />
          Druk
        </label>
        <label>
          <input
            type="checkbox"
            checked={selectedMetrics.includes('wind_speed_kmh')}
            onChange={() => toggleMetric('wind_speed_kmh')}
          />
          Windsnelheid (km/h)
        </label>
        <label>
          <input
            type="checkbox"
            checked={selectedMetrics.includes('gas')}
            onChange={() => toggleMetric('gas')}
          />
          Gas
        </label>
      </div>

      {/* 🔹 Grafiek */}
      <LineChart width={800} height={400} data={filteredData}>
        <CartesianGrid strokeDasharray="3 3" />
        <XAxis
          dataKey="timestamp"
          tickFormatter={(tick) => dayjs(tick).format('HH:mm')}
        />
        <YAxis domain={['auto', 'auto']} />
        <Tooltip />
        <Legend />
        {selectedMetrics.includes('temperature') && (
          <Line type="monotone" dataKey="temperature" stroke="#8884d8" dot={false} />
        )}
        {selectedMetrics.includes('humidity') && (
          <Line type="monotone" dataKey="humidity" stroke="#82ca9d" dot={false} />
        )}
        {selectedMetrics.includes('pressure') && (
          <Line type="monotone" dataKey="pressure" stroke="#ff7300" dot={false} />
        )}
        {selectedMetrics.includes('wind_speed_kmh') && (
          <Line type="monotone" dataKey="wind_speed_kmh" stroke="#00c0ef" dot={false} />
        )}
        {selectedMetrics.includes('gas') && (
          <Line type="monotone" dataKey="gas" stroke="#ff00ff" dot={false} />
        )}
      </LineChart>
    </div>
  );
};

export default Testen;
