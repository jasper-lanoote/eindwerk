import React, { useState, useEffect } from 'react';
import axios from "axios";
import dayjs from 'dayjs';
import DatePicker from 'react-datepicker';
import 'react-datepicker/dist/react-datepicker.css';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend } from 'recharts';
import './SensorGrafiek.css'

const apiEndPoint = 'http://192.168.0.232:8000/Weerstation/api/sensordata/';

const SensorGrafiek = () => {
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

  useEffect(() => {
    axios.get(apiEndPoint).then(({ data }) => setData(data));
  }, []);

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
        temperature: item.temperature < -40 || item.temperature > 55 ? null : item.temperature,
        wind_speed_kmh: item.wind_speed_kmh ?? 0, // Fallback voor ontbrekende waarde
        druk: item.druk < 700 || item.druk > 1050 ? null : item.druk,
        luchtvochtigheid: item.luchtvochtigheid < 98 || item.luchtvochtigheid > 3 ? null : item.luchtvochtigheid,
      }))
      .filter((item) => item.temperature !== null);
  
    setFilteredData(filtered);
  };
  
  const toggleMetric = (metric) => {
    setSelectedMetrics((prev) =>
      prev.includes(metric)
        ? prev.filter((m) => m !== metric)
        : [...prev, metric]
    );
  };

  return (
    <div className="sensor-grafiek">
    <h2>Sensoren data</h2>
    
    <div className="sensor-grafiek__controls">
        {/* Datumkiezer */}
        <DatePicker
            selected={selectedDate}
            onChange={(date) => setSelectedDate(date)}
            dateFormat="yyyy-MM-dd"
            placeholderText="Selecteer een datum"
            className="sensor-grafiek__datepicker"
        />
        
        {/* Tijdfilters als dropdown */}
        <select
            className="sensor-grafiek__dropdown"
            value={timeFilter}
            onChange={(e) => setTimeFilter(e.target.value)}
        >
            <option value="day">Dag</option>
            <option value="week">Week</option>
            <option value="month">Maand</option>
            <option value="year">Jaar</option>
        </select>
    </div>

    {/* Checkboxen voor metrics */}
    <div className="sensor-grafiek__checkboxes">
        <div className="sensor-grafiek__checkbox">
            <label>
                <input
                    type="checkbox"
                    checked={selectedMetrics.includes('temperature')}
                    onChange={() => toggleMetric('temperature')}
                />
                Temperatuur
            </label>
        </div>
        <div className="sensor-grafiek__checkbox">
            <label>
                <input
                    type="checkbox"
                    checked={selectedMetrics.includes('humidity')}
                    onChange={() => toggleMetric('humidity')}
                />
                Luchtvochtigheid
            </label>
        </div>
        <div className="sensor-grafiek__checkbox">
            <label>
                <input
                    type="checkbox"
                    checked={selectedMetrics.includes('pressure')}
                    onChange={() => toggleMetric('pressure')}
                />
                Druk
            </label>
        </div>
        <div className="sensor-grafiek__checkbox">
            <label>
                <input
                    type="checkbox"
                    checked={selectedMetrics.includes('wind_speed_kmh')}
                    onChange={() => toggleMetric('wind_speed_kmh')}
                />
                Windsnelheid (km/h)
            </label>
        </div>
        <div className="sensor-grafiek__checkbox">
            <label>
                <input
                    type="checkbox"
                    checked={selectedMetrics.includes('gas')}
                    onChange={() => toggleMetric('gas')}
                />
                Gas
            </label>
        </div>
    </div>

    {/* Grafiek */}
    <div className="recharts-wrapper">
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
</div>

  );
};

export default SensorGrafiek;
