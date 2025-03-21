import { Link } from "react-router-dom";
import Livesensor from '../components/Livesensor'
import SensorGrafiek from '../components/SensorGrafiek'
import RegenMetingenGrafiek from '../components/regenmeter'
export default function Livedata() {
  return (
    <>
      <Livesensor/>
      <SensorGrafiek/>
      <RegenMetingenGrafiek/>
    </>
  );
}

