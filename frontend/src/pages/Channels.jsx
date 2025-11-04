import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './Channels.css'; // Importa o CSS que acabamos de criar

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
// ---------------------------------------------------------

// Mapeia nomes de canais (como vêm do banco) para as classes CSS
const channelStyleMap = {
  'ifood': 'ifood',
  'rappi': 'rappi',
  'presencial': 'presencial',
  'whatsapp': 'whatsapp',
  'app próprio': 'app',
  'uber eats': 'uber'
};

// Mapeia comissões (do PDF)
const channelCommissionMap = {
  'iFood': 0.27,
  'Rappi': 0.25,
  'Uber Eats': 0.30,
  'Presencial': 0,
  'WhatsApp': 0,
  'App Próprio': 0
};

function getChannelStyle(channelName) {
  const lowerName = channelName.toLowerCase();
  // Encontra a chave no map (ex: 'ifood')
  const key = Object.keys(channelStyleMap).find(k => lowerName.includes(k));
  return key ? channelStyleMap[key] : 'default';
}

function Channels() {
  const [channelData, setChannelData] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Ajuste estas datas para o intervalo real do seu banco!
  const START_DATE = '2025-06-01';
  const END_DATE = '2025-10-31';

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true);
        const url = `${API_URL}/channels/analytics?start_date=${START_DATE}&end_date=${END_DATE}`;
        
        // 1. Busca os dados da API
        const response = await axios.get(url);
        
        // 2. Processa os dados para adicionar comissão e líquido (como no PDF)
        const processedData = response.data.map(channel => {
          const revenue = parseFloat(channel.revenue);
          const commissionRate = channelCommissionMap[channel.channel_name] || 0;
          const commissionValue = revenue * commissionRate;
          const netRevenue = revenue - commissionValue;
          
          return {
            ...channel,
            revenue: revenue, // Garante que é um número
            commissionRate: commissionRate,
            commissionValue: commissionValue,
            netRevenue: netRevenue,
            styleClass: getChannelStyle(channel.channel_name)
          };
        });
        
        setChannelData(processedData);
        setError(null);
      } catch (err) {
        console.error("Erro ao buscar dados de canais:", err);
        setError("Falha ao carregar dados. Verifique o console.");
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  if (loading) return <p>Carregando análises de canais...</p>;
  if (error) return <p style={{ color: 'red' }}>{error}</p>;

  return (
    <>
      <h1 style={{ fontSize: '2rem', marginBottom: '1rem', color: '#F9FAFB', textAlign: 'left' }}>Análise de Canais</h1>
      
      <div className="channels-grid">
        {channelData.map(channel => (
          <div key={channel.channel_id} className="channel-card">
            {/* Borda colorida */}
            <div className={`channel-card-header ${channel.styleClass}`}></div>
            
            <div className="channel-card-body">
              <h2 className="channel-card-title">{channel.channel_name}</h2>
              
              <ul className="channel-card-metrics">
                <li className="channel-card-metric">
                  <span>Faturamento Bruto</span>
                  <span>{formatCurrency(channel.revenue)}</span>
                </li>
                <li className="channel-card-metric">
                  <span>Total de Vendas</span>
                  <span>{formatNumber(channel.total_sales)}</span>
                </li>
                <li className="channel-card-metric">
                  <span>Ticket Médio</span>
                  <span>{formatCurrency(channel.avg_ticket)}</span>
                </li>
                <li className="channel-card-metric">
                  <span>Comissão ({channel.commissionRate * 100}%)</span>
                  <span>- {formatCurrency(channel.commissionValue)}</span>
                </li>
                {/* Métrica de Líquido */}
                <li className="channel-card-metric net">
                  <span>Faturamento Líquido</span>
                  <span>{formatCurrency(channel.netRevenue)}</span>
                </li>
              </ul>
            </div>
          </div>
        ))}
      </div>
    </>
  );
}

export default Channels;