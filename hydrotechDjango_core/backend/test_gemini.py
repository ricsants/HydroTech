import os
import requests
import sys

# Tentar carregar dotenv manualmente ou via django se python-dotenv não estiver disponível
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

api_key = os.getenv('GEMINI_API_KEY')

print("=" * 50)
print("TESTE DE CONECTIVIDADE DA API DO GEMINI")
print("=" * 50)

if not api_key:
    # Se não carregou do os.environ, tentar ler o arquivo .env manualmente
    env_path = os.path.join(os.path.dirname(__file__), '.env')
    if os.path.exists(env_path):
        with open(env_path, 'r', encoding='utf-8') as f:
            for line in f:
                if line.strip() and not line.startswith('#') and '=' in line:
                    k, v = line.strip().split('=', 1)
                    if k.strip() == 'GEMINI_API_KEY':
                        api_key = v.strip().strip("'").strip('"')
                        break

if not api_key:
    print("[ERRO] Nenhuma chave 'GEMINI_API_KEY' foi encontrada no arquivo .env!")
    sys.exit(1)

# Ocultar maior parte da chave para segurança
obscured_key = api_key[:6] + "..." + api_key[-4:] if len(api_key) > 10 else "chave muito curta"
print(f"Chave encontrada: {obscured_key}")
print("Enviando requisicao de teste para o Google Gemini API...")

url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={api_key}"
prompt = "Diga exatamente e apenas: 'O token do Gemini esta ativo e respondendo perfeitamente!'"

payload = {
    "contents": [{
        "parts": [{
            "text": prompt
        }]
    }]
}

try:
    response = requests.post(url, json=payload, timeout=12)
    print(f"Codigo de status HTTP: {response.status_code}")
    
    if response.status_code == 200:
        res_json = response.json()
        try:
            texto = res_json['candidates'][0]['content']['parts'][0]['text'].strip()
            print(f"Resposta do Gemini: \"{texto}\"")
            print("=" * 50)
            print("STATUS: A API DO GEMINI ESTA FUNCIONANDO PERFEITAMENTE! OK")
            print("=" * 50)
        except (KeyError, IndexError) as e:
            print("[ERRO] A requisicao retornou 200 OK, mas o formato do JSON de resposta foi inesperado:")
            print(res_json)
    else:
        print("[ERRO] O Google retornou um erro ao processar a requisicao.")
        print(f"Resposta de erro: {response.text}")
        print("=" * 50)
        print("STATUS: A CHAVE ESTA INVALIDA, EXPIRADA OU SEM LIMITE (QUOTA) DISPONIVEL.")
        print("=" * 50)
except Exception as e:
    print(f"[ERRO DE CONEXAO] Nao foi possivel alcancar a API do Google. Detalhes: {str(e)}")
