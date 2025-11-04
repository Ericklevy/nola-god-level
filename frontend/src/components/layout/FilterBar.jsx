import React from 'react';
import './FilterBar.css';

// Este é o Header com Filtros Globais do PDF
function FilterBar() {
  return (
    <header className="filter-bar">
      <div className="filter-group">
        <label htmlFor="date-range">Período</label>
        {/* Futuramente, trocaremos por um Date Picker real */}
        <input type="text" id="date-range" placeholder="Últimos 30 dias" />
      </div>
      <div className="filter-group">
        <label htmlFor="stores">Lojas</label>
        <select id="stores">
          <option value="all">Todas as Lojas</option>
        </select>
      </div>
      <div className="filter-group">
        <label htmlFor="channels">Canais</label>
        <select id="channels">
          <option value="all">Todos os Canais</option>
        </select>
      </div>
      <div className="filter-actions">
        <button className="btn-secondary">Atualizar</button>
        <button className="btn-primary">Exportar</button>
      </div>
    </header>
  );
}

export default FilterBar;