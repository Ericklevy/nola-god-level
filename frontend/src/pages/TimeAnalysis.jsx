import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './TimeAnalysis.css'; // O CSS que já criamos
import './Products.css'; // Reutiliza o estilo .data-section

const API_URL = import.meta.env.VITE_API_BASE_URL;

// Labels para o nosso gráfico
const DAYS_OF_WEEK = ['Dom', 'Seg', 'Ter', 'Qua', 'Qui', 'Sex', 'Sáb'];
const HOURS_OF_DAY = Array.from({ length: 24 }, (_, i) => `${i}h`);

// --- NOVA PALETA DE 6 CORES (COM OS MEIOS-TERMOS) ---
const COLOR_VERMELHO = [239, 68, 68];     // Baixo
const COLOR_ROXO = [139, 92, 246];       // Meio-baixo (Cor "Info" do PDF)
const COLOR_ROSA = [236, 72, 153];       // Médio (Cor vibrante)
const COLOR_AZUL = [59, 130, 246];       // Médio-Normal (Cor "Primary" do PDF)
const COLOR_AZUL_CLARO = [96, 165, 250]; // Meio-alto (Um tom mais claro de azul)
const COLOR_VERDE = [16, 185, 129];       // Alto (Cor "Secondary" do PDF)

/**
 * Interpola linearmente entre dois valores (Função matemática)
 */
function lerp(a, b, t) {
  return a + (b - a) * t;
}

/**
 * NOVA FUNÇÃO DE GRADIENTE DE 6 PONTOS
 * Calcula a cor no gradiente Vermelho -> Roxo -> Rosa -> Azul -> Azul Claro -> Verde
 */
function getMultiColorGradient(intensity) {
  let r, g, b, color1, color2, t;

  if (intensity <= 0.2) { 
    // 0.0 - 0.2: Vermelho -> Roxo
    color1 = COLOR_VERMELHO;
    color2 = COLOR_ROXO;
    t = intensity / 0.2; // Normaliza (0 -> 1)
  } else if (intensity <= 0.4) {
    // 0.2 - 0.4: Roxo -> Rosa
    color1 = COLOR_ROXO;
    color2 = COLOR_ROSA;
    t = (intensity - 0.2) / 0.2; // Normaliza (0 -> 1)
  } else if (intensity <= 0.6) {
    // 0.4 - 0.6: Rosa -> Azul (Normal)
    color1 = COLOR_ROSA;
    color2 = COLOR_AZUL;
    t = (intensity - 0.4) / 0.2; // Normaliza (0 -> 1)
  } else if (intensity <= 0.8) {
    // 0.6 - 0.8: Azul -> Azul Claro
    color1 = COLOR_AZUL;
    color2 = COLOR_AZUL_CLARO;
    t = (intensity - 0.6) / 0.2; // Normaliza (0 -> 1)
  } else {
    // 0.8 - 1.0: Azul Claro -> Verde
    color1 = COLOR_AZUL_CLARO;
    color2 = COLOR_VERDE;
    t = (intensity - 0.8) / 0.2; // Normaliza (0 -> 1)
  }

  r = Math.round(lerp(color1[0], color2[0], t));
  g = Math.round(lerp(color1[1], color2[1], t));
  b = Math.round(lerp(color1[2], color2[2], t));

  return `rgb(${r}, ${g}, ${b})`;
}
// --- FIM DAS FUNÇÕES DE COR ---


// --- Função de Formatação ---
function formatCurrency(value) {
  const number = parseFloat(value);
  if (isNaN(number)) return "R$ 0,00";
  return number.toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' });
}

function TimeAnalysis() {
  const [heatmapData, setHeatmapData] = useState([]);
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

        // 1. Encontra o valor máximo para normalizar
        const max = Math.max(...data.map(item => parseFloat(item.value)), 0);

        // 2. Cria a matriz 7x24
        const grid = Array(7).fill(0).map(() => 
          Array(24).fill(0).map(() => ({ value: 0, color: 'rgb(31, 41, 55)' })) // Cor --gray-800
        );

        // 3. Preenche a matriz com os dados da API
        data.forEach(item => {
          const day = parseInt(item.day_of_week);
          const hour = parseInt(item.hour_of_day);
          const value = parseFloat(item.value);
          
          if (day >= 0 && day < 7 && hour >= 0 && hour < 24) {
            const intensity = max > 0 ? (value / max) : 0;
            grid[day][hour] = {
              value: value,
              color: getMultiColorGradient(intensity) // <-- USA A NOVA FUNÇÃO DE 6 CORES
            };
          }
        });
        
        setHeatmapData(grid);
        setError(null);
      } catch (err)
 {
        console.error("Erro ao buscar dados do heatmap:", err);
        setError("Falha ao carregar dados. Verifique o console.");
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []); // Roda apenas uma vez

  // --- ATUALIZA A LEGENDA COM SEUS NOVOS TEXTOS ---
  const renderLegend = () => (
    <div className="heatmap-legend">
      <div className="legend-item">
        <div className="legend-square" style={{ backgroundColor: `rgb(${COLOR_VERMELHO.join(',')})` }}></div>
        <span>Baixo Movimentação (Vermelho)</span>
      </div>
       <div className="legend-item">
        <div className="legend-square" style={{ backgroundColor: `rgb(${COLOR_ROXO.join(',')})` }}></div>
        <span>Meio-baixo (Roxo)</span>
      </div>
      <div className="legend-item">
        <div className="legend-square" style={{ backgroundColor: `rgb(${COLOR_ROSA.join(',')})` }}></div>
        <span>Médio (Rosa)</span>
      </div>
      <div className="legend-item">
        <div className="legend-square" style={{ backgroundColor: `rgb(${COLOR_AZUL.join(',')})` }}></div>
        <span>Movimentação normalizada (Azul)</span>
      </div>
       <div className="legend-item">
        <div className="legend-square" style={{ backgroundColor: `rgb(${COLOR_AZUL_CLARO.join(',')})` }}></div>
        <span>Meio-alto (Azul Claro)</span>
      </div>
      <div className="legend-item">
        <div className="legend-square" style={{ backgroundColor: `rgb(${COLOR_VERDE.join(',')})` }}></div>
        <span>Movimentação acima do normal (Verde)</span>
      </div>
    </div>
  );

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
        
        <div className="heatmap-container-wrapper">
          <div className="heatmap-container">
            
            <div className="heatmap-labels-y">
              {DAYS_OF_WEEK.map(day => (
                <div key={day} className="heatmap-label-y">{day}</div>
              ))}
            </div>

            <div className="heatmap-labels-x">
              {HOURS_OF_DAY.map(hour => (
                <div key={hour} className="heatmap-label">{hour}</div>
              ))}
            </div>
            
            <div className="heatmap-grid">
              {heatmapData.flat().map((cell, index) => (
                <div
                  key={index}
                  className="heatmap-cell"
                  // Define a cor calculada (Vermelho -> ... -> Verde)
                  style={{ backgroundColor: cell.color }} 
                  title={`Faturamento: ${formatCurrency(cell.value)}`} 
                >
                </div>
              ))}
            </div>

          </div>
        </div>
        
        {/* ADICIONA A LEGENDA ATUALIZADA */}
        {renderLegend()}
        
      </div>
    </>
  );
}

export default TimeAnalysis;