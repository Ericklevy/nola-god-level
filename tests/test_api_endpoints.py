import httpx
import os
import pytest

# URL da API (o test-runner acessa pela rede interna do Docker)
API_URL = os.environ.get("API_URL", "http://backend-api:8000")

# Datas padrão para todos os testes, conforme solicitado
START_DATE = "2025-05-01"
END_DATE = "2025-10-31"

# Criar um cliente HTTP único para todos os testes
# (Para testes mais complexos, usaríamos fixtures, mas
#  para validação de endpoint, isso é eficiente)
client = httpx.Client(base_url=API_URL, timeout=30.0)

# --- Testes Básicos ---

def test_health_check():
    """Testa se o endpoint /api/health está respondendo 200 OK."""
    response = client.get("/api/health")
    assert response.status_code == 200, f"Health check falhou: {response.text}"
    data = response.json()
    assert data["status"] == "ok"
    assert data["database"] == "connected"

# --- Testes de Métricas ---

def test_metrics_overview():
    """Testa o endpoint de overview com o intervalo de datas padrão."""
    params = {"start_date": START_DATE, "end_date": END_DATE}
    response = client.get("/api/metrics/overview", params=params)
    assert response.status_code == 200, f"Metrics Overview falhou: {response.text}"
    data = response.json()
    assert "total_sales" in data
    assert "revenue" in data

# --- Testes de Produtos ---

def test_products_ranking():
    """Testa o endpoint de ranking de produtos."""
    params = {"start_date": START_DATE, "end_date": END_DATE, "limit": 5}
    response = client.get("/api/products/ranking", params=params)
    assert response.status_code == 200, f"Products Ranking falhou: {response.text}"
    data = response.json()
    assert isinstance(data, list)
    if len(data) > 0:
        assert "product_id" in data[0]

def test_products_customizations():
    """Testa o endpoint de ranking de customizações."""
    params = {"start_date": START_DATE, "end_date": END_DATE, "limit": 5}
    response = client.get("/api/products/customizations", params=params)
    assert response.status_code == 200, f"Products Customizations falhou: {response.text}"
    data = response.json()
    assert isinstance(data, list)
    if len(data) > 0:
        assert "item_id" in data[0]

# --- Testes de Canais ---

def test_channels_analytics():
    """Testa o endpoint de análise de canais."""
    params = {"start_date": START_DATE, "end_date": END_DATE}
    response = client.get("/api/channels/analytics", params=params)
    assert response.status_code == 200, f"Channels Analytics falhou: {response.text}"
    data = response.json()
    assert isinstance(data, list)
    if len(data) > 0:
        assert "channel_name" in data[0]

# --- Testes de Lojas ---

def test_stores_ranking():
    """Testa o endpoint de ranking de lojas."""
    params = {"start_date": START_DATE, "end_date": END_DATE}
    response = client.get("/api/stores/ranking", params=params)
    assert response.status_code == 200, f"Stores Ranking falhou: {response.text}"
    data = response.json()
    assert isinstance(data, list)
    if len(data) > 0:
        assert "store_id" in data[0]

# --- Testes de Análise Temporal ---

def test_time_analysis_heatmap():
    """Testa o endpoint do heatmap."""
    params = {"start_date": START_DATE, "end_date": END_DATE}
    response = client.get("/api/time-analysis/heatmap", params=params)
    assert response.status_code == 200, f"Time Heatmap falhou: {response.text}"
    data = response.json()
    assert isinstance(data, list)
    if len(data) > 0:
        assert "day_of_week" in data[0]

def test_time_analysis_timeline():
    """Testa o endpoint de linha do tempo (agrupado por semana)."""
    params = {"start_date": START_DATE, "end_date": END_DATE, "group_by": "week"}
    response = client.get("/api/time-analysis/timeline", params=params)
    assert response.status_code == 200, f"Time Timeline falhou: {response.text}"
    data = response.json()
    assert isinstance(data, list)
    if len(data) > 0:
        assert "timestamp" in data[0]

# --- Testes de Clientes ---

def test_customers_top_ranking():
    """Testa o endpoint de top clientes."""
    params = {"start_date": START_DATE, "end_date": END_DATE, "limit": 5}
    response = client.get("/api/customers/top", params=params)
    assert response.status_code == 200, f"Customers Top falhou: {response.text}"
    data = response.json()
    assert isinstance(data, list)
    if len(data) > 0:
        assert "customer_id" in data[0]

def test_customers_at_risk_segment():
    """Testa o endpoint de segmento 'at_risk'."""
    params = {"start_date": START_DATE, "end_date": END_DATE, "segment": "at_risk"}
    response = client.get("/api/customers/segments", params=params)
    assert response.status_code == 200, f"Customers Segments falhou: {response.text}"
    data = response.json()
    assert data["segment_name"] == "at_risk"
    assert "customer_count" in data

