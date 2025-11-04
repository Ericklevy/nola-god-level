import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './Products.css'; // <--- REUTILIZANDO O CSS da página de Produtos

const API_URL = import.meta.env.VITE_API_BASE_URL;

// --- Funções de Formatação (copiadas do Dashboard) ---
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

function Stores() {
  const [storeData, setStoreData] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Ajuste estas datas para o intervalo real do seu banco!
  const START_DATE = '2025-06-01';
  const END_DATE = '2025-10-31';

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true);
        // 1. Busca no endpoint correto de Lojas
        const url = `${API_URL}/stores/ranking?start_date=${START_DATE}&end_date=${END_DATE}`;
        
        const response = await axios.get(url);
        
        setStoreData(response.data);
        setError(null);
      } catch (err) {
        console.error("Erro ao buscar dados de lojas:", err);
        setError("Falha ao carregar dados. Verifique o console.");
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []); // Roda apenas uma vez

  // --- Renderização Principal ---

  if (loading) return <p>Carregando análises de lojas...</p>;
  if (error) return <p style={{ color: 'red' }}>{error}</p>;

  return (
    <>
      <h1 style={{ fontSize: '2rem', marginBottom: '1rem', color: '#F9FAFB', textAlign: 'left' }}>
        Análise de Lojas
      </h1>
      
      {/* Usamos as mesmas classes CSS da página de produtos */}
      <div className="data-section">
        <h2 className="data-section-title">Ranking de Lojas por Faturamento</h2>
        <div className="table-container">
          <table className="data-table">
            <thead>
              <tr>
                <th>Rank</th>
                <th>Loja</th>
                <th>Cidade/Estado</th>
                <th className="align-right">Total de Vendas</th>
                <th className="align-right">Faturamento</th>
                <th className="align-right">Ticket Médio</th>
              </tr>
            </thead>
            <tbody>
              {storeData.map((store, index) => (
                <tr key={store.store_id}>
                  <td>{index + 1}</td>
                  <td>{store.store_name}</td>
                  <td>{store.city || 'N/A'} - {store.state || 'N/A'}</td>
                  <td className="align-right">{formatNumber(store.total_sales)}</td>
                  <td className="align-right">{formatCurrency(store.revenue)}</td>
                  <td className="align-right">{formatCurrency(store.avg_ticket)}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </>
  );
}

export default Stores;