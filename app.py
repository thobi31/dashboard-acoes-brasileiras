from flask import Flask, render_template
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
import plotly.io as pio
from datetime import date

app = Flask(__name__)

TICKERS = {
    "Petrobras": "PETR4.SA",
    "Itaú": "ITUB4.SA",
    "Vale": "VALE3.SA",
}

CORES = {
    "Petrobras": "#1f77b4",
    "Itaú": "#ff7f0e",
    "Vale": "#2ca02c",
}


def buscar_dados():
    simbolos = list(TICKERS.values())
    df_raw = yf.download(simbolos, start="2026-01-02", end=date.today().isoformat(), progress=False)
    df = df_raw["Close"].copy()
    df.columns = list(TICKERS.keys())
    df = df.dropna(how="all")
    return df


def calcular_performance(df):
    primeiro = df.iloc[0]
    return ((df / primeiro) - 1) * 100


def gerar_grafico_cotacao(df):
    fig = go.Figure()
    for nome in df.columns:
        fig.add_trace(go.Scatter(
            x=df.index,
            y=df[nome],
            name=nome,
            line=dict(color=CORES[nome], width=2),
            hovertemplate="%{x|%d/%m/%Y}<br>R$ %{y:.2f}<extra>" + nome + "</extra>",
        ))
    fig.update_layout(
        title="Cotação em 2026 (R$)",
        xaxis_title="Data",
        yaxis_title="Preço (R$)",
        hovermode="x unified",
        template="plotly_dark",
        legend=dict(orientation="h", y=1.05),
        margin=dict(t=80, b=40),
    )
    return pio.to_html(fig, full_html=False, include_plotlyjs="cdn")


def gerar_grafico_performance(df_perf):
    fig = go.Figure()
    fig.add_hline(y=0, line_dash="dot", line_color="gray", opacity=0.5)
    for nome in df_perf.columns:
        fig.add_trace(go.Scatter(
            x=df_perf.index,
            y=df_perf[nome],
            name=nome,
            line=dict(color=CORES[nome], width=2, dash="solid"),
            hovertemplate="%{x|%d/%m/%Y}<br>%{y:.2f}%<extra>" + nome + "</extra>",
        ))
    fig.update_layout(
        title="Performance Acumulada em 2026 (%)",
        xaxis_title="Data",
        yaxis_title="Variação (%)",
        hovermode="x unified",
        template="plotly_dark",
        legend=dict(orientation="h", y=1.05),
        margin=dict(t=80, b=40),
    )
    return pio.to_html(fig, full_html=False, include_plotlyjs=False)


@app.route("/")
def index():
    df = buscar_dados()
    df_perf = calcular_performance(df)
    grafico_cotacao = gerar_grafico_cotacao(df)
    grafico_performance = gerar_grafico_performance(df_perf)
    ultima_atualizacao = date.today().strftime("%d/%m/%Y")
    return render_template(
        "index.html",
        grafico_cotacao=grafico_cotacao,
        grafico_performance=grafico_performance,
        data=ultima_atualizacao,
    )


if __name__ == "__main__":
    app.run(debug=True)
