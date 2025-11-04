import React from 'react';
import { NavLink } from 'react-router-dom';
import './Sidebar.css';

// Lista de páginas baseada no PDF
const navItems = [
  { name: 'Dashboard', path: '/' },
  { name: 'Produtos', path: '/produtos' },
  { name: 'Canais', path: '/canais' },
  { name: 'Lojas', path: '/lojas' },
  { name: 'Análise Temporal', path: '/temporal' },
  { name: 'Clientes', path: '/clientes' },
];

function Sidebar() {
  return (
    <nav className="sidebar">
      <h2 className="sidebar-title">Food Commerce</h2>
      <ul className="sidebar-menu">
        {navItems.map((item) => (
          <li key={item.name}>
            <NavLink
              to={item.path}
              className={({ isActive }) =>
                isActive ? 'sidebar-link active' : 'sidebar-link'
              }
            >
              {item.name}
            </NavLink>
          </li>
        ))}
      </ul>
    </nav>
  );
}

export default Sidebar;