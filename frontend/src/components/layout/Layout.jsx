import React from 'react';
import { Outlet } from 'react-router-dom'; // O Outlet é onde as páginas serão renderizadas
import Sidebar from './Sidebar';
import FilterBar from './FilterBar';
import './Layout.css';

function Layout() {
  return (
    <div className="app-container">
      <Sidebar />
      <main className="main-content">
        <FilterBar />
        <div className="page-content">
          {/* O Outlet renderiza a página da rota atual (Dashboard, Products, etc.) */}
          <Outlet /> 
        </div>
      </main>
    </div>
  );
}

export default Layout;