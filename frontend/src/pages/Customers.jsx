import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './Products.css'; // Reutiliza o CSS da tabela de Produtos
import './Customers.css'; // O CSS que acabamos de criar

const API_URL = import.meta.env.VITE_API_BASE_URL;

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

function formatDate(dateTimeStr) {
  if (!dateTimeStr) return 'N/A';
  const date = new Date(dateTimeStr);
  return date.toLocaleDateString('pt-BR');
}
// ---------------------------------------------------------

function Customers() {
  const [segmentsData, setSegmentsData] = useState(null);
  const [topCustomersData, setTopCustomersData] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Ajuste estas datas para o intervalo real do seu banco!
  const START_DATE = '2025-06-01';
  const END_DATE = '2025-10-31';

  useEffect(() => {
    const fetchAllData = async () => {
      try {
        setLoading(true);
        
        // 1. Define as URLs dos endpoints
        const segmentsUrl = `${API_URL}/customers/segments?start_date=${START_DATE}&end_date=${END_DATE}&segment=at_risk`;
        const topCustomersUrl = `${API_URL}/customers/top?start_date=${START_DATE}&end_date=${END_DATE}&limit=20`;

        // 2. Faz as duas requisições em paralelo
        const [segmentsResponse, topCustomersResponse] = await Promise.all([
          axios.get(segmentsUrl),
          axios.get(topCustomersUrl)
        ]);
        
        setSegmentsData(segmentsResponse.data);
        setTopCustomersData(topCustomersResponse.data);
        setError(null);
      } catch (err) {
        console.error("Erro ao buscar dados de clientes:", err);
        setError("Falha ao carregar dados. Verifique o console.");
      } finally {
        setLoading(false);
      }
    };

    fetchAllData();
  }, []); // Roda apenas uma vez

  // --- Renderização dos Segmentos ---
  const renderSegments = () => (
    <div className="segments-grid">
      {/* Card 1: Clientes em Risco (o que a API retorna) */}
      {segmentsData && (
        <div className={`segment-card ${segmentsData.segment_name}`}>
          <h3 className="segment-card-title">Clientes em Risco</h3>
          <p className="segment-card-count">{formatNumber(segmentsData.customer_count)}</p>
          <p className="segment-card-description">Não compram há 30+ dias</p>
        </div>
      )}
      {/* Cards "placeholder" (apenas para visual) */}
      <div className="segment-card vips">
        <h3 className="segment-card-title">Clientes VIPs</h3>
        <p className="segment-card-count">--</p>
        <p className="segment-card-description">Compram com alta frequência e valor</p>
      </div>
      <div className="segment-card loyal">
        <h3 className="segment-card-title">Clientes Fiéis</h3>
        <p className="segment-card-count">--</p>
        <p className="segment-card-description">Compram com frequência</p>
      </div>
    </div>
  );

  // --- Renderização da Tabela de Top Clientes ---
  const renderTopCustomersTable = () => (
    <div className="data-section">
      <h2 className="data-section-title">Top 20 Clientes por Faturamento</h2>
      <div className="table-container">
        <table className="data-table">
          <thead>
            <tr>
              <th>Cliente</th>
              <th>Email</th>
              <th className="align-right">Total Gasto</th>
              <th className="align-right">Nº Pedidos</th>
              <th className="align-right">Ticket Médio</th>
              <th className="align-right">Última Compra</th>
            </tr>
          </thead>
          <tbody>
            {topCustomersData.map((customer) => (
              <tr key={customer.customer_id}>
                <td>{customer.customer_name || 'N/A'}</td>
                <td>{customer.email || 'N/A'}</td>
                <td className="align-right">{formatCurrency(customer.total_spent)}</td>
                <td className="align-right">{formatNumber(customer.total_orders)}</td>
                <td className="align-right">{formatCurrency(customer.avg_ticket)}</td>
                <td className="align-right">{formatDate(customer.last_order_date)}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );

  // --- Renderização Principal ---

  if (loading) return <p>Carregando análises de clientes...</p>;
  if (error) return <p style={{ color: 'red' }}>{error}</p>;

  return (
    <>
      <h1 style={{ fontSize: '2rem', marginBottom: '1rem', color: '#F9FAFB', textAlign: 'left' }}>
        Análise de Clientes
      </h1>
      
      {/* 1. Grid de Segmentos */}
      {renderSegments()}
      
      {/* 2. Tabela de Top Clientes */}
      {renderTopCustomersTable()}
    </>
  );
}

export default Customers;