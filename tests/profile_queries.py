import httpx
import time
import os
from datetime import date

# URL da API (pode ser o localhost se você rodar localmente,
# ou o nome do serviço se rodar via docker compose run)
API_URL = os.environ.get("API_URL", "http://backend-api:8000")
START_DATE = "2025-05-01"
END_DATE = "2025-10-31"

# Lista de todos os endpoints que queremos medir
ENDPOINTS_TO_PROFILE = [
    {
        "name": "Health Check",
        "url": "/api/health",
        "params": {}
    },
    {
        "name": "Metrics Overview",
        "url": "/api/metrics/overview",
        "params": {"start_date": START_DATE, "end_date": END_DATE}
    },
    {
        "name": "Product Ranking",
        "url": "/api/products/ranking",
        "params": {"start_date": START_DATE, "end_date": END_DATE, "limit": 10}
    },
    {
        "name": "Product Customizations",
        "url": "/api/products/customizations",
        "params": {"start_date": START_DATE, "end_date": END_DATE, "limit": 10}
    },
    {
        "name": "Channel Analytics",
        "url": "/api/channels/analytics",
        "params": {"start_date": START_DATE, "end_date": END_DATE}
    },
    {
        "name": "Store Ranking",
        "url": "/api/stores/ranking",
        "params": {"start_date": START_DATE, "end_date": END_DATE}
    },
    {
        "name": "Time Heatmap",
        "url": "/api/time-analysis/heatmap",
        "params": {"start_date": START_DATE, "end_date": END_DATE}
    },
    {
        "name": "Time Timeline (by week)",
        "url": "/api/time-analysis/timeline",
        "params": {"start_date": START_DATE, "end_date": END_DATE, "group_by": "week"}
    },
    {
        "name": "Top Customers",
        "url": "/api/customers/top",
        "params": {"start_date": START_DATE, "end_date": END_DATE, "limit": 10}
    },
    {
        "name": "Customer Segment (At Risk)",
        "url": "/api/customers/segments",
        "params": {"start_date": START_DATE, "end_date": END_DATE, "segment": "at_risk"}
    }
]

def profile_endpoints():
    print(f"--- Iniciando Profiling da API em {API_URL} ---")
    print(f"Intervalo de Datas: {START_DATE} a {END_DATE}\n")
    
    with httpx.Client(timeout=30.0) as client:
        for endpoint in ENDPOINTS_TO_PROFILE:
            url = f"{API_URL}{endpoint['url']}"
            params = endpoint.get("params", {})
            
            try:
                # "Aquecimento" - A primeira query pode ser mais lenta
                client.get(url, params=params)
                
                # Medição real
                start_time = time.time()
                response = client.get(url, params=params)
                end_time = time.time()
                
                duration_ms = (end_time - start_time) * 1000
                
                if response.status_code == 200:
                    status = "SUCESSO"
                else:
                    status = f"FALHA ({response.status_code})"
                    
                print(f"  - {endpoint['name']:<25} | {status:<15} | {duration_ms:>8.2f} ms")
                
            except httpx.RequestError as e:
                print(f"  - {endpoint['name']:<25} | ERRO DE CONEXÃO: {e}")

if __name__ == "__main__":
    # Espera 5s para garantir que a API está pronta
    print("Aguardando 5s pela inicialização da API...")
    time.sleep(5)
    profile_endpoints()
