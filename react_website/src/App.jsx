import './App.css'
// import Livesensor from './components/Livesensor'
// import SensorGrafiek from './components/SensorGrafiek'
// import RegenMetingenGrafiek from './components/regenmeter'
import { HashRouter as Router, Routes, Route } from "react-router-dom";
import Home from "./pages/Home";
import Livedata from "./pages/Livedata";
import Layout from "./Layout";

export default function App() {
  
  return (
    <>
    <div className='flexbox'>
    <Router>
        <Routes>
          <Route element={<Layout />}>
            <Route path="/" element={<Home />} />
            <Route path="/pag1" element={<Livedata />} />
          </Route>
        </Routes>
      </Router>
      </div>
    </>
  )
}

