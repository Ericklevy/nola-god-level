import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './TimeAnalysis.css'; // Importa o CSS que acabamos de criar

const API_URL = import.meta.env.VITE_API_BASE_URL;

// Labels para o nosso gráfico
const DAYS_OF_WEEK = ['Dom', 'Seg', 'Ter', 'Qua', 'Qui', 'Sex', 'Sáb'];
const HOURS_OF_DAY = Array.from({ length: 24 }, (_, i) => `${i}h`);

// --- Função de Formatação ---
function formatCurrency(value) {
  const number = parseFloat(value);
  if (isNaN(number)) return "R$ 0,00";
  return number.toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' });
}

function TimeAnalysis() {
  const [heatmapData, setHeatmapData] = useState([]);
  const [maxValue, setMaxValue] = useState(0);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Ajuste estas datas para o intervalo real do seu banco!
  const START_DATE = '2025-06-01';
  const END_DATE = '2025-10-31';

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true);
        const url = `${API_URL}/time-analysis/heatmap?start_date=${START_DATE}&end_date=${END_DATE}`;
        
        const response = await axios.get(url);
        const data = response.data;

        // 1. Encontra o valor máximo para normalizar (calcular intensidade)
        const max = Math.max(...data.map(item => parseFloat(item.value)), 0);
        setMaxValue(max);

        // 2. Cria a matriz 7x24
        // (Preenchemos com valores padrão primeiro)
        const grid = Array(7).fill(0).map(() => 
          Array(24).fill(0).map(() => ({ value: 0, intensity: 0 }))
        );

        // 3. Preenche a matriz com os dados da API
        data.forEach(item => {
          const day = parseInt(item.day_of_week);
          const hour = parseInt(item.hour_of_day);
          const value = parseFloat(item.value);
          
          if (day >= 0 && day < 7 && hour >= 0 && hour < 24) {
            grid[day][hour] = {
              value: value,
              intensity: max > 0 ? (value / max) : 0 // Intensidade de 0.0 a 1.0
            };
          }
        });
        
        setHeatmapData(grid);
        setError(null);
      } catch (err) {
        console.error("Erro ao buscar dados do heatmap:", err);
        setError("Falha ao carregar dados. Verifique o console.");
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []); // Roda apenas uma vez

  // --- Renderização Principal ---

  if (loading) return <p>Carregando análise temporal...</p>;
  if (error) return <p style={{ color: 'red' }}>{error}</p>;

  return (
    <>
      <h1 style={{ fontSize: '2rem', marginBottom: '1rem', color: '#F9FAFB', textAlign: 'left' }}>
        Análise Temporal
      </h1>
      
      <div className="data-section">
        <h2 className="data-section-title">Heatmap de Horários de Pico (por Faturamento)</h2>
        
        <div className="heatmap-container">
          
          {/* Labels do Eixo Y (Dias) */}
          <div className="heatmap-labels-y">
            {DAYS_OF_WEEK.map(day => (
              <div key={day} className="heatmap-label-y">{day}</div>
            ))}
          </div>

          {/* Labels do Eixo X (Horas) */}
          <div className="heatmap-labels-x">
            {HOURS_OF_DAY.map(hour => (
              <div key={hour} className="heatmap-label">{hour}</div>
            ))}
          </div>
          
          {/* O Grid do Heatmap */}
          <div className="heatmap-grid">
            {heatmapData.flat().map((cell, index) => (
              <div
                key={index}
                className="heatmap-cell"
                // Passa a intensidade para o CSS
                style={{ '--intensity': cell.intensity }}
                // Tooltip que o PDF pedia
                title={`Faturamento: ${formatCurrency(cell.value)}`} 
              >
              </div>
            ))}
          </div>

        </div>
      </div>
    </>
  );
}

export default TimeAnalysis;