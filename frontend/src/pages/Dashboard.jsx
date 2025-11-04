import { useState, useEffect } from 'react'
import axios from 'axios'
import './Dashboard.css';

const API_URL = import.meta.env.VITE_API_BASE_URL;

// --- Funções para formatar os números ---
function formatCurrency(value) {
  // Converte string para número
  const number = parseFloat(value);
  return number.toLocaleString('pt-BR', {
    style: 'currency',
    currency: 'BRL',
  });
}

function formatNumber(value) {
  // Converte string para número
  const number = parseInt(value, 10);
  return number.toLocaleString('pt-BR');
}

function formatPercent(value) {
  // Converte string para número
  const number = parseFloat(value);
  return `${number.toFixed(1).replace('.', ',')}%`;
}
// ----------------------------------------


function Dashboard() {
  const [overviewData, setOverviewData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Ajuste estas datas para o intervalo real do seu banco!
  const START_DATE = '2025-06-01';
  const END_DATE = '2025-10-31';

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true);
        const url = `${API_URL}/metrics/overview?start_date=${START_DATE}&end_date=${END_DATE}`;
        console.log("Buscando dados de:", url);
        const response = await axios.get(url);
        setOverviewData(response.data);
        setError(null);
      } catch (err) {
        console.error("Erro ao buscar dados:", err);
        setError("Falha ao carregar dados. Verifique o console.");
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  return (
    <>
      <h1 style={{ fontSize: '2rem' }}>Dashboard Nola Analytics</h1>
      <h2 style={{ fontSize: '1.25rem', color: '#E5E7EB' }}>Visão Geral do Período</h2>
      
      {loading && <p>Carregando métricas...</p>}
      {error && <p style={{ color: 'red' }}>{error}</p>}
      
      {overviewData && (
        <div className="kpi-grid">
          
          {/* Card 1: Faturamento */}
          <div className="kpi-card">
            <h3 className="kpi-card-title">Faturamento</h3>
            <p className="kpi-card-value">
              {overviewData ? formatCurrency(overviewData.revenue) : 'R$ 0,00'}
            </p>
          </div>
          
          {/* Card 2: Total de Vendas */}
          <div className="kpi-card">
            <h3 className="kpi-card-title">Total de Vendas</h3>
            <p className="kpi-card-value">
              {overviewData ? formatNumber(overviewData.total_sales) : '0'}
            </p>
          </div>
          
          {/* Card 3: Ticket Médio */}
          <div className="kpi-card">
            <h3 className="kpi-card-title">Ticket Médio</h3>
            <p className="kpi-card-value">
              {overviewData ? formatCurrency(overviewData.avg_ticket) : 'R$ 0,00'}
            </p>
          </div>
          
          {/* Card 4: Taxa de Conversão */}
          <div className="kpi-card">
            <h3 className="kpi-card-title">Taxa de Conversão</h3>
            <p className="kpi-card-value">
              {overviewData ? formatPercent(overviewData.conversion_rate) : '0,0%'}
            </p>
          </div>
          
        </div>
      )}
    </>
  )
}

export default Dashboard