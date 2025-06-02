import requests
import datetime
import os
import subprocess

# --- Configurações do Serviço ---
SERVICE_URL = "http://localhost:8080/api/envio-propostas"  # URL do endpoint de envio de propostas
LOG_FILE_PATH = "/var/log/minha_aplicacao/app.log"  # Caminho do arquivo de log da aplicação
NUM_LOG_LINES = 100  # Número de linhas de log a serem coletadas em caso de erro

# --- Dados de Exemplo para a Proposta (ajuste conforme a API real) ---
PROPOSAL_DATA = {
    "titulo": "Proposta de Teste Automatizada",
    "descricao": "Esta é uma proposta de teste gerada por script para validação de integridade.",
    "licitacao_id": 12345,
    "valor": 1000.00,
    "anexos": []
}

def validate_proposal_service():
    """
    Valida a integridade do serviço de envio de propostas.
    Tenta enviar uma proposta e, em caso de falha, coleta os logs relevantes.
    """
    print(f"[{datetime.datetime.now()}] Iniciando validação do serviço '{SERVICE_URL}'...")

    try:
        response = requests.post(SERVICE_URL, json=PROPOSAL_DATA, timeout=10) # Timeout de 10 segundos
        response.raise_for_status()  # Levanta uma exceção para códigos de status HTTP 4xx ou 5xx

        print(f"[{datetime.datetime.now()}] Serviço OK. Status HTTP: {response.status_code}")
        # Opcional: Você pode querer validar o corpo da resposta aqui também
        # if "sucesso" not in response.json():
        #     print("Erro: Resposta de sucesso inesperada no corpo da resposta.")
        #     collect_logs("resposta_inesperada")
        #     return False

    except requests.exceptions.HTTPError as e:
        print(f"[{datetime.datetime.now()}] ERRO HTTP! Status: {e.response.status_code}. Razão: {e.response.reason}")
        print(f"Detalhes da resposta: {e.response.text}")
        collect_logs("http_error", e.response.status_code)
        return False
    except requests.exceptions.ConnectionError as e:
        print(f"[{datetime.datetime.now()}] ERRO DE CONEXÃO! Serviço inacessível ou porta incorreta.")
        print(f"Detalhes: {e}")
        collect_logs("connection_error")
        return False
    except requests.exceptions.Timeout as e:
        print(f"[{datetime.datetime.now()}] ERRO DE TIMEOUT! O serviço não respondeu a tempo.")
        print(f"Detalhes: {e}")
        collect_logs("timeout_error")
        return False
    except Exception as e:
        print(f"[{datetime.datetime.now()}] Ocorreu um erro inesperado: {e}")
        collect_logs("unexpected_error")
        return False

    return True

def collect_logs(error_type, status_code=None):
    """
    Coleta as últimas N linhas do arquivo de log da aplicação.
    """
    log_output_filename = f"error_logs_{error_type}_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
    if status_code:
        log_output_filename = f"error_logs_{status_code}_{error_type}_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.log"

    print(f"[{datetime.datetime.now()}] Coletando as últimas {NUM_LOG_LINES} linhas do log '{LOG_FILE_PATH}'...")
    try:
        # Comando para coletar as últimas N linhas do log
        # No Linux/macOS, 'tail -n NUM_LOG_LINES' é comum
        # No Windows, pode ser 'Get-Content -Tail NUM_LOG_LINES' ou adaptar
        if os.name == 'posix': # Linux, macOS
            cmd = ['tail', '-n', str(NUM_LOG_LINES), LOG_FILE_PATH]
        else: # Windows (requer PowerShell)
            cmd = ['powershell', '-Command', f'Get-Content -Tail {NUM_LOG_LINES} {LOG_FILE_PATH}']

        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        with open(log_output_filename, 'w') as f:
            f.write(result.stdout)
        print(f"[{datetime.datetime.now()}] Logs salvos em '{log_output_filename}'")
    except FileNotFoundError:
        print(f"[{datetime.datetime.now()}] ERRO: Arquivo de log '{LOG_FILE_PATH}' não encontrado.")
    except subprocess.CalledProcessError as e:
        print(f"[{datetime.datetime.now()}] ERRO ao coletar logs: {e.stderr}")
    except Exception as e:
        print(f"[{datetime.datetime.now()}] ERRO inesperado ao coletar logs: {e}")

if __name__ == "__main__":
    if validate_proposal_service():
        print(f"[{datetime.datetime.now()}] Validação concluída com sucesso.")
    else:
        print(f"[{datetime.datetime.now()}] Validação falhou. Verifique os logs gerados.")