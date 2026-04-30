import requests
import pandas as pd
from tabulate import tabulate
from datetime import datetime, timedelta
import os

# ================================================================
# ⚙️ CONFIGURAÇÕES — edite apenas aqui
# ================================================================
APP_ID  = "seu_app_id"
APP_KEY = "seu_app_key"

PAIS        = "br"
RESULTS     = 20
DIAS_FILTRO = 7   # vagas dos últimos N dias

BUSCAS = [
    "<Nome do cargo>",
    "<Nome do cargo>",
   
]
# ================================================================

DATA_LIMITE = datetime.now() - timedelta(days=DIAS_FILTRO)

def extrair_salario(vaga):
    minimo = vaga.get('salary_min')
    maximo = vaga.get('salary_max')
    if minimo and maximo:
        return f"R$ {int(minimo):,} - {int(maximo):,}"
    elif minimo:
        return f"A partir de R$ {int(minimo):,}"
    return "A combinar"

def extrair_local(vaga):
    location = vaga.get('location', {})
    if isinstance(location, dict):
        return location.get('display_name', 'N/A')
    return str(location)

def is_recente(vaga):
    criada = vaga.get('created')
    if not criada:
        return True
    try:
        return datetime.strptime(criada[:10], "%Y-%m-%d") >= DATA_LIMITE
    except:
        return True

def is_local_valido(vaga):
    titulo    = (vaga.get('title') or '').lower()
    descricao = (vaga.get('description') or '').lower()
    local     = extrair_local(vaga).lower()
    texto     = titulo + descricao + local

    eh_remoto   = any(p in texto for p in ['remoto', 'remote', 'home office', 'homeoffice'])
    eh_hibrido  = any(p in texto for p in ['híbrido', 'hibrido', 'hybrid'])
    em_brasilia = any(p in local for p in ['brasília', 'brasilia', 'distrito federal', ' df'])

    if eh_remoto:
        return True, "🌐 Remoto"
    if eh_hibrido and em_brasilia:
        return True, "🔀 Híbrido - Brasília"
    if em_brasilia:
        return True, "📍 Brasília"
    if local in ['n/a', '', 'brasil']:
        return True, "❓ Verificar"
    return False, ""

def is_banco_talentos(vaga):
    texto = ((vaga.get('title') or '') + (vaga.get('description') or '')).lower()
    return any(p in texto for p in ['banco de talentos', 'banco de candidatos', 'talent pool', 'cadastro reserva'])

def is_pcd(vaga):
    texto = ((vaga.get('title') or '') + (vaga.get('description') or '')).lower()
    return any(p in texto for p in ['pcd', 'pne', 'deficiência', 'deficiencia', 'inclusão', 'inclusao', 'afirmativa'])

def buscar_por_termo(termo):
    url = f"https://api.adzuna.com/v1/api/jobs/{PAIS}/search/1"
    params = {
        "app_id"           : APP_ID,
        "app_key"          : APP_KEY,
        "results_per_page" : RESULTS,
        "what"             : termo,
        "content-type"     : "application/json",
        "sort_by"          : "date",
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json().get('results', [])

def salvar_excel(df, df_pcd, df_banco, df_norm):
    os.makedirs("output", exist_ok=True)
    data_hoje = datetime.now().strftime("%Y-%m-%d")
    arquivo   = f"output/vagas_dados_{data_hoje}.xlsx"

    with pd.ExcelWriter(arquivo, engine='openpyxl') as writer:
        df.drop(columns=['_link']).to_excel(writer, sheet_name='Todas as Vagas', index=False)
        if not df_norm.empty:
            df_norm.drop(columns=['_link']).to_excel(writer, sheet_name='Vagas Abertas', index=False)
        if not df_pcd.empty:
            df_pcd.drop(columns=['_link']).to_excel(writer, sheet_name='PCD', index=False)
        if not df_banco.empty:
            df_banco.drop(columns=['_link']).to_excel(writer, sheet_name='Banco de Talentos', index=False)

    print(f"\n💾 Excel salvo em: '{arquivo}'")
    print(f"   📋 Todas as Vagas | 💼 Vagas Abertas | ♿ PCD | 🗂️ Banco de Talentos")
    return arquivo

def buscar_vagas():
    print("\n" + "=" * 70)
    print("AUTOMAÇÃO DE BUSCA DE VAGAS")
    print("=" * 70)
    print(f"Filtro: vagas dos últimos {DIAS_FILTRO} dias")
    print(f"Filtro: Remoto (Brasil todo) ou Híbrido apenas em Brasília-DF")
    print(f"Termos: {', '.join(BUSCAS)}")
    print("=" * 70 + "\n")

    todas_vagas = []
    ids_vistos  = set()

    for termo in BUSCAS:
        print(f"🔎 Buscando: '{termo}'...")
        try:
            vagas = buscar_por_termo(termo)
        except Exception as e:
            print(f"   ⚠️ Erro ao buscar '{termo}': {e}")
            continue

        for vaga in vagas:
            vid = vaga.get('id')
            if vid in ids_vistos:
                continue
            ids_vistos.add(vid)

            if not is_recente(vaga):
                continue

            valido, tipo_local = is_local_valido(vaga)
            if not valido:
                continue

            tags = []
            if is_banco_talentos(vaga):
                tags.append("🗂️ Banco Talentos")
            if is_pcd(vaga):
                tags.append("♿ PCD")

            criada = vaga.get('created', '')
            try:
                data_fmt = datetime.strptime(criada[:10], "%Y-%m-%d").strftime("%d/%m/%Y")
            except:
                data_fmt = "N/A"

            todas_vagas.append({
                "Vaga"     : vaga.get('title', 'N/A')[:45],
                "Empresa"  : vaga.get('company', {}).get('display_name', 'N/A'),
                "Salário"  : extrair_salario(vaga),
                "Modelo"   : tipo_local,
                "Aberta em": data_fmt,
                "Tags"     : " | ".join(tags) if tags else "—",
                "_link"    : vaga.get('redirect_url', '')
            })

    if not todas_vagas:
        print("\n⚠️ Nenhuma vaga encontrada com esses filtros.")
        print("💡 Dica: aumente DIAS_FILTRO no topo do script.")
        return

    df       = pd.DataFrame(todas_vagas)
    df_pcd   = df[df['Tags'].str.contains('PCD',   na=False)]
    df_banco = df[df['Tags'].str.contains('Banco', na=False)]
    df_norm  = df[~df['Tags'].str.contains('PCD|Banco', na=False)]

    print(f"\n✅ {len(df)} vagas encontradas no total!\n")

    if not df_pcd.empty:
        print(f"♿ VAGAS PCD ({len(df_pcd)}):")
        print(tabulate(df_pcd.drop(columns=['_link']), headers='keys', tablefmt='grid', showindex=False))

    if not df_banco.empty:
        print(f"\n🗂️ BANCO DE TALENTOS ({len(df_banco)}):")
        print(tabulate(df_banco.drop(columns=['_link']), headers='keys', tablefmt='grid', showindex=False))

    if not df_norm.empty:
        print(f"\n💼 VAGAS ABERTAS ({len(df_norm)}):")
        print(tabulate(df_norm.drop(columns=['_link']), headers='keys', tablefmt='grid', showindex=False))

    print("\n🔗 LINKS PARA CANDIDATURA:")
    print("-" * 70)
    for i, row in df.iterrows():
        print(f"{i+1:>2}. {row['Vaga'][:42]:<44} → {row['_link']}")

    salvar_excel(df, df_pcd, df_banco, df_norm)
    print("\n✅ Busca finalizada com sucesso!\n")

if __name__ == "__main__":
    buscar_vagas()
