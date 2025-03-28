import React, { useEffect, useState } from 'react';
import axios from 'axios';
import dayjs from 'dayjs';
import DatePicker from 'react-datepicker';
import 'react-datepicker/dist/react-datepicker.css';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend } from 'recharts';
import './Regenmeter.css';

const apiEndPoint = 'http://localhost:8000/Weerstation/api/regenmetingen/';

const RegenMetingenGrafiek = () => {
  const [data, setData] = useState([]);
  const [filteredData, setFilteredData] = useState([]);
  const [selectedDate, setSelectedDate] = useState(new Date());
  const [timeFilter, setTimeFilter] = useState('day');

  useEffect(() => {
    // Data ophalen van API met axios
    axios.get(apiEndPoint)
      .then(response => setData(response.data))
      .catch(error => console.error('Fout bij het ophalen van data:', error));
  }, []);

  useEffect(() => {
    // Data filteren op basis van datum en filter
    filterData();
  }, [data, selectedDate, timeFilter]);

  const filterData = () => {
    const selected = dayjs(selectedDate);

    let filtered = data
      .filter(item => {
        const date = dayjs(item.tijdstip);
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
      });

    if (timeFilter === 'day') {
      // Groeperen per uur als "dag" geselecteerd is
      const hourlyData = Array.from({ length: 24 }, (_, i) => ({
        tijd: `${i}:00`,
        regenval: 0
      }));

      filtered.forEach(item => {
        const uur = dayjs(item.tijdstip).hour();
        hourlyData[uur].regenval += item.regenval ?? 0;
      });

      setFilteredData(hourlyData);
    } else if (timeFilter === 'week') {
      // Groeperen per dag als "week" geselecteerd is
      const dailyData = {};

      filtered.forEach(item => {
        const dag = dayjs(item.tijdstip).format('YYYY-MM-DD');
        if (!dailyData[dag]) {
          dailyData[dag] = 0;
        }
        dailyData[dag] += item.regenval ?? 0;
      });

      const formattedDailyData = Object.keys(dailyData).map(dag => ({
        tijd: dag,
        regenval: dailyData[dag]
      }));

      setFilteredData(formattedDailyData);
    } else if (timeFilter === 'month') {
      // Groeperen per maand als "month" geselecteerd is
      const monthlyData = {};

      filtered.forEach(item => {
        const maand = dayjs(item.tijdstip).format('YYYY-MM');
        if (!monthlyData[maand]) {
          monthlyData[maand] = 0;
        }
        monthlyData[maand] += item.regenval ?? 0;
      });

      const formattedMonthlyData = Object.keys(monthlyData).map(maand => ({
        tijd: maand,
        regenval: monthlyData[maand]
      }));

      setFilteredData(formattedMonthlyData);
    } else if (timeFilter === 'year') {
      // Groeperen per jaar als "year" geselecteerd is
      const yearlyData = {};

      filtered.forEach(item => {
        const jaar = dayjs(item.tijdstip).format('YYYY');
        if (!yearlyData[jaar]) {
          yearlyData[jaar] = 0;
        }
        yearlyData[jaar] += item.regenval ?? 0;
      });

      const formattedYearlyData = Object.keys(yearlyData).map(jaar => ({
        tijd: jaar,
        regenval: yearlyData[jaar]
      }));

      setFilteredData(formattedYearlyData);
    }
  };

  return (
    <div className="regen-grafiek">
      <h2>Regenmetingen</h2>
      
      <div className="regen-grafiek__controls">
        {/*Datumkiezer */}
        <div className="regen-grafiek__datepicker-container">
          <DatePicker
            selected={selectedDate}
            onChange={(date) => setSelectedDate(date)}
            dateFormat="yyyy-MM-dd"
            placeholderText="Selecteer een datum"
            className="regen-grafiek__datepicker"
          />
        </div>

        {/*Tijdfilters */}
        <select 
          className="regen-grafiek__dropdown" 
          value={timeFilter} 
          onChange={(e) => setTimeFilter(e.target.value)}
        >
          <option value="day">Dag</option>
          <option value="week">Week</option>
          <option value="month">Maand</option>
          <option value="year">Jaar</option>
        </select>
      </div>

      {/*Grafiek */}
      <BarChart width={800} height={400} data={filteredData}>
        <CartesianGrid strokeDasharray="3 3" />
        <XAxis dataKey="tijd" />
        <YAxis />
        <Tooltip />
        <Legend />
        <Bar dataKey="regenval" fill="#82ca9d" />
      </BarChart>
    </div>
  );
};

export default RegenMetingenGrafiek;
