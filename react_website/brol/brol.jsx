import React, { useState, useEffect } from 'react';
import axios from 'axios';
import SensorDataChart from './SensorDataChart';
import DatePicker from 'react-datepicker'; // Importeer react-datepicker
import "react-datepicker/dist/react-datepicker.css"; // Importeer de CSS voor de datepicker
import { getWeek, getMonth, getHours } from 'date-fns'; // Importeer date-fns functies

const SensorDataList = () => {
  const [sensorData, setSensorData] = useState([]);
  const [filteredData, setFilteredData] = useState([]);
  const [selectedDate, setSelectedDate] = useState(null);  // Staat voor de geselecteerde datum
  const [filterOption, setFilterOption] = useState('day');  // Dag, uur, week, maand
  const [selectedHour, setSelectedHour] = useState(null);  // Staat voor het geselecteerde uur

  useEffect(() => {
    // Haal de sensor gegevens op van de Django API
    axios.get('http://192.168.0.232:8000/Weerstation/api/sensordata/')
      .then(response => {
        setSensorData(response.data); // Zet de data in de state
        setFilteredData(response.data); // Zet ook de gefilterde data
        console.log(response.data);
        
      })
      .catch(error => {
        console.error("Er is een fout opgetreden bij het ophalen van de sensor data:", error);
      });
  }, []);

  // Filter de data op basis van de geselecteerde datum en filteroptie
  const handleDateChange = (date) => {
    setSelectedDate(date);  // Bewaar de geselecteerde datum
    filterData(date, selectedHour, filterOption);
  };

  const handleHourChange = (event) => {
    const hour = event.target.value;
    setSelectedHour(hour);  // Bewaar het geselecteerde uur
    filterData(selectedDate, hour, filterOption);
  };

  const handleFilterOptionChange = (event) => {
    const option = event.target.value;
    setFilterOption(option); // Verander de filteroptie (dag, uur, week, maand)
    filterData(selectedDate, selectedHour, option);
  };

  // Functie om de data te filteren op basis van de geselecteerde datum en filteroptie
  const filterData = (date, hour, filterOption) => {
    if (date) {
      let filtered = [];
      switch (filterOption) {
        case 'day':
          // Filter op specifieke datum
          const formattedDate = date.toISOString().split('T')[0];
          filtered = sensorData.filter(item => {
            const itemDate = new Date(item.timestamp).toISOString().split('T')[0];
            return itemDate === formattedDate;
          });
          break;
        case 'hour':
          // Filter op specifiek uur
          filtered = sensorData.filter(item => {
            const itemHour = new Date(item.timestamp).getHours();
            return itemHour === parseInt(hour);
          });
          break;
        case 'week':
          // Filter op specifieke week
          const week = getWeek(date);
          filtered = sensorData.filter(item => {
            const itemWeek = getWeek(new Date(item.timestamp));
            return itemWeek === week;
          });
          break;
        case 'month':
          // Filter op specifieke maand
          const month = getMonth(date);
          filtered = sensorData.filter(item => {
            const itemMonth = new Date(item.timestamp).getMonth();
            return itemMonth === month;
          });
          break;
        default:
          filtered = sensorData;
          break;
      }
      setFilteredData(filtered);  // Update de gefilterde data
    } else {
      setFilteredData(sensorData);  // Toon alles als er geen datum is geselecteerd
    }
  };

  return (
    <div>
      <h1>Sensor Gegevens</h1>

      {/* Voeg de keuze voor de filteroptie toe */}
      <div>
        <h3>Filter op:</h3>
        <select onChange={handleFilterOptionChange} value={filterOption}>
          <option value="day">Dag</option>
          <option value="hour">Uur</option>
          <option value="week">Week</option>
          <option value="month">Maand</option>
        </select>
      </div>

      {/* Voeg de datumkiezer toe */}
      <div>
        <h3>Selecteer een datum:</h3>
        <DatePicker
          selected={selectedDate}
          onChange={handleDateChange}
          dateFormat="yyyy-MM-dd"
          placeholderText="Selecteer een datum"
        />
      </div>
      <SensorDataChart data={filteredData} />

      {/* Voeg de uurkiezer toe als we filteren op uur */}
      {filterOption === 'hour' && (
        <div>
          <h3>Selecteer een uur:</h3>
          <select onChange={handleHourChange} value={selectedHour}>
            {[...Array(24)].map((_, hour) => (
              <option key={hour} value={hour}>
                {hour}:00
              </option>
            ))}
          </select>
        </div>
      )}

      {/* Tabel van sensor gegevens */}
      <table>
        <thead>
          <tr>
            <th>Timestamp</th>
            <th>Temperatuur (°C)</th>
            <th>Vochtigheid (%)</th>
            <th>Druk (hPa)</th>
            <th>Gas (PPM)</th>
            <th>Windsnelheid (km/h)</th>
          </tr>
        </thead>
        <tbody>
          {filteredData.map((data, index) => (
            <tr key={index}>
              <td>{new Date(data.timestamp).toLocaleString()}</td>
              <td>{data.temperature}</td>
              <td>{data.humidity}</td>
              <td>{data.pressure}</td>
              <td>{data.gas}</td>
              <td>{data.wind_speed_kmh}</td>
            </tr>
          ))}
        </tbody>
      </table>

      {/* Grafiek met de gefilterde data */}
    </div>
  );
};

export default SensorDataList;
