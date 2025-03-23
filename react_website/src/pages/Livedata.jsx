import { Link } from "react-router-dom";
import Livesensor from '../components/Livesensor'
import SensorGrafiek from '../components/SensorGrafiek'
import RegenMetingenGrafiek from '../components/regenmeter'
import './Livedata.css'
export default function Livedata() {
  return (
    <>
    <div className="flexbox">
      <Livesensor/>
      <SensorGrafiek/>
      <RegenMetingenGrafiek/>
    </div>
    </>
  );
}

