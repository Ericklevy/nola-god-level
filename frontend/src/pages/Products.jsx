import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './Products.css'; // O CSS que já criamos e atualizamos

const API_URL = import.meta.env.VITE_API_BASE_URL;
// REMOVEMOS O PAGE_LIMIT

// --- Funções de Formatação ---
function formatCurrency(value) {
  const number = parseFloat(value);
  if (isNaN(number)) return "R$ 0,00";
  return number.toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' });
}

function formatNumber(value) {
  const number = parseInt(value, 10);
  if (isNaN(number)) return "0";
  return number.toLocaleString('pt-BR');
}
// ---------------------------------------------------------

function Products() {
  const [rankingData, setRankingData] = useState([]);
  const [customData, setCustomData] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  // REMOVEMOS O ESTADO 'page'

  // Ajuste estas datas para o intervalo real do seu banco!
  const START_DATE = '2025-06-01';
  const END_DATE = '2025-10-31';

  useEffect(() => {
    // Voltamos a ter uma função única para buscar tudo
    const fetchAllData = async () => {
      try {
        setLoading(true);
        
        // URL do ranking AGORA SEM skip/limit
        const rankingUrl = `${API_URL}/products/ranking?start_date=${START_DATE}&end_date=${END_DATE}`;
        const customUrl = `${API_URL}/products/customizations?start_date=${START_DATE}&end_date=${END_DATE}&limit=10`;

        const [rankingResponse, customResponse] = await Promise.all([
          axios.get(rankingUrl),
          axios.get(customUrl)
        ]);
        
        setRankingData(rankingResponse.data);
        setCustomData(customResponse.data);
        setError(null);
      } catch (err) {
        console.error("Erro ao buscar dados de produtos:", err);
        setError("Falha ao carregar dados. Verifique o console.");
      } finally {
        setLoading(false);
      }
    };

    fetchAllData();
  }, []); // REMOVEMOS 'page' da dependência

  // --- Funções de Renderização ---

  const renderRankingTable = () => (
    <div className="data-section">
      <h2 className="data-section-title">Ranking de Produtos (Todos)</h2>
      <div className="table-container">
        <table className="data-table">
          <thead>
            <tr>
              <th>Rank</th>
              <th>Produto</th>
              <th>Categoria</th>
              <th className="align-right">Qtd. Vendida</th>
              <th className="align-right">Faturamento</th>
              <th className="align-right">Ticket Médio</th>
            </tr>
          </thead>
          <tbody>
            {rankingData.map((product, index) => (
              <tr key={product.product_id}>
                <td>{index + 1}</td> {/* O Rank agora é simples */}
                <td>{product.product_name}</td>
                <td>{product.category_name || '-'}</td>
                <td className="align-right">{formatNumber(product.quantity_sold)}</td>
                <td className="align-right">{formatCurrency(product.revenue)}</td>
                <td className="align-right">{formatCurrency(product.revenue / product.quantity_sold)}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
      {/* REMOVEMOS OS CONTROLES DE PAGINAÇÃO DAQUI */}
    </div>
  );

  const renderCustomizationsList = () => (
    <div className="data-section">
      <h2 className="data-section-title">Customizações Populares (Top 10)</h2>
      <ul className="custom-list">
        {customData.map((item) => (
          <li key={item.item_id} className="custom-list-item">
            <span className="custom-list-name">{item.item_name}</span>
            <span className="custom-list-details">
              <div>{formatNumber(item.times_added)} adições</div>
              <div>{formatCurrency(item.revenue_generated)}</div>
            </span>
          </li>
        ))}
      </ul>
    </div>
  );

  // --- Renderização Principal ---

  if (loading) return <p>Carregando análises de produtos...</p>;
  if (error) return <p style={{ color: 'red' }}>{error}</p>;

  return (
    <>
      <h1 style={{ fontSize: '2rem', marginBottom: '1rem', color: '#F9FAFB', textAlign: 'left' }}>Análise de Produtos</h1>
      <div className="page-grid">
        <div className="main-column">
          {renderRankingTable()}
        </div>
        <div className="sidebar-column">
          {renderCustomizationsList()}
        </div>
      </div>
    </>
  );
}

export default Products;