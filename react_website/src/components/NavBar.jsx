import { Link } from "react-router-dom";

export default function Navbar() {
  return (
    <>
      <Link to="/">
        <button>Home</button>
      </Link>
      <Link to="/pag1">
        <button>Page 1</button>
      </Link>
    </>
  );
}
