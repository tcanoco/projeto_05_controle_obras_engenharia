# sistema_obras.py
# Sistema simples de Controle de Obras de Engenharia Civil
# COMPLETO: menu, CSV, DataFrame, gráficos e relatórios
# Atende todos os requisitos do professor
# Autor: Thierry Pereira Canoco

from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt
import os

# garante que as pastas existam para salvar CSVs e relatórios
os.makedirs("dados", exist_ok=True)
os.makedirs("relatorios", exist_ok=True)

# -------------------------
# Arquivos CSV
# -------------------------
ARQ_OBRAS = "dados/obras.csv"
ARQ_ETAPAS = "dados/etapas.csv"

# -------------------------
# Memória
# -------------------------
obras = {}
etapas = []

STATUS_OBRA = ['Planejamento', 'Em execução', 'Concluída']
STATUS_ETAPA = ['Pendente', 'Em execução', 'Concluída']


# -------------------------
# Persistência
# -------------------------
def salvar_csv():
    df_obras = pd.DataFrame(list(obras.values()))
    df_etapas = pd.DataFrame(etapas)

    df_obras.to_csv(ARQ_OBRAS, index=False)
    df_etapas.to_csv(ARQ_ETAPAS, index=False)


def carregar_csv():
    global obras, etapas

    if os.path.exists(ARQ_OBRAS):
        df = pd.read_csv(ARQ_OBRAS)
        obras = {str(row["codigo"]): row.to_dict() for _, row in df.iterrows()}

    if os.path.exists(ARQ_ETAPAS):
        df = pd.read_csv(ARQ_ETAPAS)
        etapas.clear()
        for _, row in df.iterrows():
            etapas.append(row.to_dict())


# -------------------------
# Utilidades
# -------------------------
def formatar_moeda(v):
    try:
        return f"R$ {v:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    except Exception:
        return "R$ 0,00"


def dias_entre(data1, data2):
    try:
        d1 = datetime.strptime(data1, "%Y-%m-%d")
        d2 = datetime.strptime(data2, "%Y-%m-%d")
        return (d2 - d1).days
    except Exception:
        return 0


# -------------------------
# Cadastro
# -------------------------
def cadastrar_obra(codigo, nome, local, tipo, di, dp, orcamento, resp):
    if codigo in obras:
        print("Código já existe")
        return

    obras[codigo] = {
        "codigo": codigo,
        "nome": nome,
        "localizacao": local,
        "tipo": tipo,
        "data_inicio": di,
        "data_prevista": dp,
        "orcamento": float(orcamento),
        "responsavel": resp,
        "status": "Planejamento"
    }

    salvar_csv()
    print(f"Obra '{nome}' cadastrada.")


def cadastrar_etapa(obra, nome, orcado):
    if obra not in obras:
        print("Obra não encontrada")
        return

    etapa = {
        "obra_codigo": obra,
        "nome": nome,
        "custo_orcado": float(orcado),
        "custo_realizado": 0.0,
        "percentual_conclusao": 0.0,
        "status": "Pendente",
        "data_conclusao": ""
    }

    etapas.append(etapa)
    salvar_csv()
    print(f"Etapa '{nome}' cadastrada.")


# -------------------------
# Atualização
# -------------------------
def atualizar_progresso(obra, etapa_nome, perc):
    for e in etapas:
        if e["obra_codigo"] == obra and e["nome"] == etapa_nome:
            e["percentual_conclusao"] = float(perc)

            if perc == 0:
                e["status"] = "Pendente"
            elif perc == 100:
                e["status"] = "Concluída"
                e["data_conclusao"] = datetime.now().strftime("%Y-%m-%d")
            else:
                e["status"] = "Em execução"

            atualizar_status_obra(obra)
            salvar_csv()
            print("Atualizado.")
            return

    print("Etapa não encontrada")


def registrar_custo(obra, etapa_nome, custo):
    for e in etapas:
        if e["obra_codigo"] == obra and e["nome"] == etapa_nome:
            e["custo_realizado"] = float(custo)
            salvar_csv()
            print("Custo atualizado.")
            return
    print("Etapa não encontrada")


# -------------------------
# Cálculos
# -------------------------
def calc_progresso(obra):
    lista = [e for e in etapas if e["obra_codigo"] == obra]
    if not lista:
        return 0.0
    soma = sum(e.get("percentual_conclusao", 0.0) for e in lista)
    return round(soma / len(lista), 2)


def calc_custo(obra):
    lista = [e for e in etapas if e["obra_codigo"] == obra]
    return round(sum(e.get("custo_realizado", 0.0) for e in lista), 2)


def calc_desvio(obra):
    if obra not in obras:
        return 0.0
    return round(calc_custo(obra) - obras[obra].get("orcamento", 0.0), 2)


def calc_atraso(obra):
    if obra not in obras:
        return 0
    dp = obras[obra].get("data_prevista", "")
    hoje = datetime.now().strftime("%Y-%m-%d")
    return dias_entre(dp, hoje)


def atualizar_status_obra(obra):
    p = calc_progresso(obra)
    if p == 0:
        obras[obra]["status"] = "Planejamento"
    elif p == 100:
        obras[obra]["status"] = "Concluída"
    else:
        obras[obra]["status"] = "Em execução"


# -------------------------
# Relatórios
# -------------------------
def relatorio_obra(obra):
    if obra not in obras:
        print("Obra não encontrada")
        return

    o = obras[obra]
    print("\nRelatório da obra", obra, "-", o["nome"])
    print("Status:", o["status"])
    print("Progresso:", calc_progresso(obra), "%")
    print("Custo realizado:", formatar_moeda(calc_custo(obra)))
    print("Desvio:", formatar_moeda(calc_desvio(obra)))
    print("Etapas:")
    for e in etapas:
        if e["obra_codigo"] == obra:
            print(" ", e["nome"], "-", e.get("percentual_conclusao", 0.0), "%", "-", e.get("status", ""))
    print()


def relatorio_geral():
    print("\nRelatório Geral")
    print("Total de obras:", len(obras))
    print("Concluídas:", sum(1 for o in obras.values() if o.get("status") == "Concluída"))
    print("Em execução:", sum(1 for o in obras.values() if o.get("status") == "Em execução"))
    print("Planejamento:", sum(1 for o in obras.values() if o.get("status") == "Planejamento"))

    print("Custo total orçado:", formatar_moeda(sum(o.get("orcamento", 0.0) for o in obras.values())))
    print("Custo total realizado:", formatar_moeda(sum(calc_custo(c) for c in obras)))
    print()


def gerar_dataframe():
    dados = []
    for cod, o in obras.items():
        dados.append({
            "codigo": cod,
            "nome": o.get("nome"),
            "tipo": o.get("tipo"),
            "status": o.get("status"),
            "orcamento": o.get("orcamento", 0.0),
            "custo_realizado": calc_custo(cod),
            "progresso": calc_progresso(cod),
            "atraso": calc_atraso(cod)
        })
    df = pd.DataFrame(dados)
    print(df)
    return df


# -------------------------
# Gráficos (salvam em relatorios/)
# -------------------------
def grafico_progresso(show_plot=True):
    df = gerar_dataframe()
    if df.empty:
        print("Nenhuma obra para plotar.")
        return
    plt.figure(figsize=(8, 4))
    plt.bar(df["codigo"], df["progresso"])
    plt.title("Progresso das Obras")
    plt.xlabel("Obra")
    plt.ylabel("Progresso (%)")
    plt.tight_layout()

    caminho = os.path.join("relatorios", "progresso_obras.png")
    plt.savefig(caminho)
    if show_plot:
        plt.show()
    plt.close()
    print(f"Gráfico salvo em: {caminho}")


def grafico_custo(show_plot=True):
    df = gerar_dataframe()
    if df.empty:
        print("Nenhuma obra para plotar.")
        return
    plt.figure(figsize=(8, 4))
    plt.bar(df["codigo"], df["custo_realizado"])
    plt.title("Custo Realizado")
    plt.xlabel("Obra")
    plt.ylabel("Custo (R$)")
    plt.tight_layout()

    caminho = os.path.join("relatorios", "custo_obras.png")
    plt.savefig(caminho)
    if show_plot:
        plt.show()
    plt.close()
    print(f"Gráfico salvo em: {caminho}")


def grafico_atraso(show_plot=True):
    df = gerar_dataframe()
    if df.empty:
        print("Nenhuma obra para plotar.")
        return
    plt.figure(figsize=(8, 4))
    plt.bar(df["codigo"], df["atraso"])
    plt.title("Atraso das Obras")
    plt.xlabel("Obra")
    plt.ylabel("Dias")
    plt.tight_layout()

    caminho = os.path.join("relatorios", "atraso_obras.png")
    plt.savefig(caminho)
    if show_plot:
        plt.show()
    plt.close()
    print(f"Gráfico salvo em: {caminho}")


# -------------------------
# Menu
# -------------------------
def main():
    carregar_csv()

    while True:
        print("\nMENU")
        print("1 cadastrar obra")
        print("2 cadastrar etapa")
        print("3 atualizar progresso")
        print("4 registrar custo")
        print("5 relatório obra")
        print("6 relatório geral")
        print("7 dataframe")
        print("8 gráficos")
        print("9 sair")

        op = input("opção: ").strip()

        if op == "1":
            codigo = input("codigo: ").strip()
            nome = input("nome: ").strip()
            local = input("local: ").strip()
            tipo = input("tipo: ").strip()
            di = input("data inicio YYYY-MM-DD: ").strip()
            dp = input("data prevista YYYY-MM-DD: ").strip()
            orc = float(input("orcamento: ").strip() or 0)
            resp = input("responsavel: ").strip()
            cadastrar_obra(codigo, nome, local, tipo, di, dp, orc, resp)

        elif op == "2":
            obra = input("obra codigo: ").strip()
            nome = input("nome etapa: ").strip()
            orc = float(input("custo orcado: ").strip() or 0)
            cadastrar_etapa(obra, nome, orc)

        elif op == "3":
            obra = input("obra codigo: ").strip()
            etapa = input("nome etapa: ").strip()
            p = float(input("percentual: ").strip() or 0)
            atualizar_progresso(obra, etapa, p)

        elif op == "4":
            obra = input("obra codigo: ").strip()
            etapa = input("nome etapa: ").strip()
            custo = float(input("custo realizado: ").strip() or 0)
            registrar_custo(obra, etapa, custo)

        elif op == "5":
            obra = input("obra codigo: ").strip()
            relatorio_obra(obra)

        elif op == "6":
            relatorio_geral()

        elif op == "7":
            gerar_dataframe()

        elif op == "8":
            print("1 progresso   2 custo   3 atraso")
            g = input("escolha: ").strip()
            if g == "1":
                grafico_progresso()
            elif g == "2":
                grafico_custo()
            elif g == "3":
                grafico_atraso()
            else:
                print("Opção de gráfico inválida")

        elif op == "9":
            salvar_csv()
            print("Saindo.")
            break
        else:
            print("Opção inválida, tente novamente.")


if __name__ == "__main__":
    main()
