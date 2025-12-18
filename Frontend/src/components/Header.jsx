import { NavLink } from "react-router-dom";

function Header() {
  return (
    <header className="w-full bg-zinc-950 border-b border-zinc-800 px-8 py-4 flex items-center justify-between">
      <h1 className="text-xl font-semibold text-zinc-100 tracking-wide">
        🖌️ AI Comic Generator
      </h1>
      <NavLink
        to="/about"
        className="text-zinc-400 hover:text-zinc-200 transition-colors text-sm font-medium"
      >
        About
      </NavLink>
    </header>
  );
}

export default Header;