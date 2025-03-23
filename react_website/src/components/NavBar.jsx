import { Link } from "react-router-dom";
import './NavBar.css'


export default function Navbar() {
  return (
    <>
      <div className="flexbox">
        <Link to="/">
          <button>Home</button>
        </Link>
        <Link to="/pag1">
          <button>Page 1</button>
        </Link> 
      </div>
    </>
   
  );
}
