from dash import html, dcc
from dash.dependencies import Input, Output, State
from datetime import date, datetime, timedelta
import dash_bootstrap_components as dbc
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import calendar

from app import app

from dash_bootstrap_templates import template_from_url, ThemeChangerAIO
import dash

card_icon = {
    "color": "white",
    "textAlign": "center",
    "fontSize": "30",
    "margin": "auto",
}

graph_margin = dict(l=25, r=25, t=25, b=0)


# =========  Layout  =========== #
layout = (
    dbc.Col(
        [
            dbc.Row(
                [
                    # Saldo Total -----------------------------
                    dbc.Col(
                        [
                            dbc.CardGroup(
                                [
                                    dbc.Card(
                                        [
                                            html.Legend("Saldo"),
                                            html.H5("R$ 5400", id="p-saldo-dashboards"),
                                        ],
                                        style={
                                            "padding-left": "20px",
                                            "padding-top": "10px",
                                        },
                                    ),
                                    dbc.Card(
                                        [
                                            html.Div(
                                                className="fa fa-university",
                                                style=card_icon,
                                            ),
                                        ],
                                        color="warning",
                                        style={
                                            "maxWidth": "75px",
                                            "height": "100",
                                            "margin-left": "-10px",
                                        },
                                    ),
                                ],
                            )
                        ],
                        width=4,
                    ),
                    # Receita -----------------------------
                    dbc.Col(
                        [
                            dbc.CardGroup(
                                [
                                    dbc.Card(
                                        [
                                            html.Legend("Receita"),
                                            html.H5(
                                                "R$ 10000",
                                                id="p-receita-dashboards",
                                                style={},
                                            ),
                                        ],
                                        style={
                                            "padding-left": "20px",
                                            "padding-top": "10px",
                                        },
                                    ),
                                    dbc.Card(
                                        [
                                            html.Div(
                                                className="fa fa-smile-o",
                                                style=card_icon,
                                            ),
                                        ],
                                        color="success",
                                        style={
                                            "maxWidth": "75px",
                                            "height": "100",
                                            "margin-left": "-10px",
                                        },
                                    ),
                                ],
                            )
                        ],
                        width=4,
                    ),
                    # Despesa -----------------------------
                    dbc.Col(
                        [
                            dbc.CardGroup(
                                [
                                    dbc.Card(
                                        [
                                            html.Legend("Despesa"),
                                            html.H5(
                                                "R$ 4600",
                                                id="p-despesa-dashboards",
                                                style={},
                                            ),
                                        ],
                                        style={
                                            "padding-left": "20px",
                                            "padding-top": "10px",
                                        },
                                    ),
                                    dbc.Card(
                                        [
                                            html.Div(
                                                className="fa fa-meh-o",
                                                style=card_icon,
                                            ),
                                        ],
                                        color="danger",
                                        style={
                                            "maxWidth": "75px",
                                            "height": "100",
                                            "margin-left": "-10px",
                                        },
                                    ),
                                ],
                            )
                        ],
                        width=4,
                    ),
                ],
                style={"margin": "10px"},
            ),
            # Linha -----------------------------
            dbc.Row(
                [
                    dbc.Col(
                        [
                            dbc.Card(
                                [
                                    html.Legend(
                                        "Filtrar lançamentos", className="card-title"
                                    ),
                                    html.Label("Categorias das receitas"),
                                    html.Div(
                                        dcc.Dropdown(
                                            id="dropdown-receita",
                                            clearable=False,
                                            style={"width": "100%"},
                                            persistence=True,
                                            persistence_type="session",
                                            multi=True,
                                        )
                                    ),
                                    html.Label(
                                        "Categorias das despesas",
                                        style={"margin-top": "10px"},
                                    ),
                                    dcc.Dropdown(
                                        id="dropdown-despesa",
                                        clearable=False,
                                        style={"width": "100%"},
                                        persistence=True,
                                        persistence_type="session",
                                        multi=True,
                                    ),
                                    html.Legend(
                                        "Período de análise",
                                        style={"margin-top": "10px"},
                                    ),
                                    dcc.DatePickerRange(
                                        month_format="Do MMM, YY",
                                        end_date_placeholder_text="Data...",
                                        start_date=datetime(2022, 4, 1).date(),
                                        end_date=datetime.today() + timedelta(days=31),
                                        updatemode="singledate",
                                        id="date-picker-config",
                                        style={"z-index": "100"},
                                    ),
                                ],
                                style={"height": "100%", "padding": "20px"},
                            )
                        ],
                        width=4,
                    ),
                    dbc.Col(
                        dbc.Card(
                            dcc.Graph(id="graph1"),
                            style={"height": "100%", "padding": "10px"},
                        ),
                        width=8,
                    ),
                ],
                style={"margin": "10px"},
            ),
            # Linha -----------------------------
            dbc.Row(
                [
                    dbc.Col(
                        dbc.Card(dcc.Graph(id="graph2"), style={"padding": "10px"}),
                        width=6,
                    ),
                    dbc.Col(
                        dbc.Card(dcc.Graph(id="graph3"), style={"padding": "10px"}),
                        width=3,
                    ),
                    dbc.Col(
                        dbc.Card(dcc.Graph(id="graph4"), style={"padding": "10px"}),
                        width=3,
                    ),
                ]
            ),
        ]
    ),
)


# =========  Callbacks  =========== #
# Receitas
@app.callback(
    [
        Output("dropdown-receita", "options"),
        Output("dropdown-receita", "value"),
        Output("p-receita-dashboards", "children"),
    ],
    [
        Input("store-receitas", "data"),
    ],
)
def populate_dropdownvalues_receita(data):
    df = pd.DataFrame(data)
    valor = df["Valor"].sum()
    val = df.Categoria.unique().tolist()

    return ([{"label": i, "value": i} for i in val], val, f"R$ {valor}")


# Despesas
@app.callback(
    [
        Output("dropdown-despesa", "options"),
        Output("dropdown-despesa", "value"),
        Output("p-despesa-dashboards", "children"),
    ],
    [
        Input("store-despesas", "data"),
    ],
)
def populate_dropdownvalues_despesa(data):
    df = pd.DataFrame(data)
    valor = df["Valor"].sum()
    val = df.Categoria.unique().tolist()

    return ([{"label": i, "value": i} for i in val], val, f"R$ {valor}")


# Saldo
@app.callback(
    Output("p-saldo-dashboards", "children"),
    [
        Input("store-receitas", "data"),
        Input("store-despesas", "data"),
    ],
)
def saldo_total(receitas, despesas):
    df_receitas = pd.DataFrame(receitas)
    df_despesas = pd.DataFrame(despesas)

    saldo = df_receitas["Valor"].sum() - df_despesas["Valor"].sum()

    return f"R$ {saldo}"


# grafico 1
@app.callback(
    Output("graph1", "figure"),
    [
        Input("store-receitas", "data"),
        Input("store-despesas", "data"),
        Input("dropdown-receita", "value"),
        Input("dropdown-despesa", "value"),
        Input(ThemeChangerAIO.ids.radio("theme"), "value"),
    ],
)
def update_graph1(receitas, despesas, cat_receita, cat_despesa, theme):
    df_despesas = pd.DataFrame(despesas).set_index("Data")[["Valor"]]
    df_despesas = df_despesas.groupby("Data").sum().rename(columns={"Valor": "Despesa"})

    df_receitas = pd.DataFrame(receitas).set_index("Data")[["Valor"]]
    df_receitas = df_receitas.groupby("Data").sum().rename(columns={"Valor": "Receita"})

    df_acumulado = df_despesas.join(df_receitas, how="outer").fillna(0)
    df_acumulado["Saldo Acumulado"] = df_acumulado["Receita"] - df_acumulado["Despesa"]
    df_acumulado["Saldo Acumulado"] = df_acumulado["Saldo Acumulado"].cumsum()

    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            
            x=df_acumulado.index,
            y=df_acumulado["Saldo Acumulado"],
            mode="lines+markers",
            name="Fluxo de Caixa",
        )
    )
    fig.update_layout(
        title="Evolução do saldo",
        margin=graph_margin,
        template=template_from_url(theme),
        height=400,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
    )

    return fig


# grafico 2
@app.callback(
    Output("graph2", "figure"),
    [
        Input("store-receitas", "data"),
        Input("store-despesas", "data"),
        Input("dropdown-receita", "value"),
        Input("dropdown-despesa", "value"),
        Input("date-picker-config", "start_date"),
        Input("date-picker-config", "end_date"),
        Input(ThemeChangerAIO.ids.radio("theme"), "value"),
    ],
)
def update_graph2(
    receitas, despesas, cat_receita, cat_despesa, start_date, end_date, theme
):
    df_despesas = pd.DataFrame(despesas)
    df_receitas = pd.DataFrame(receitas)

    df_despesas["Output"] = "Despesas"
    df_receitas["Output"] = "Receitas"

    df_final = pd.concat([df_despesas, df_receitas])
    df_final["Data"] = pd.to_datetime(df_final["Data"])

    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)
    df_final = df_final[
        (df_final["Data"] >= start_date) & (df_final["Data"] <= end_date)
    ]
    df_final = df_final[
        (df_final["Categoria"].isin(cat_receita))
        | (df_final["Categoria"].isin(cat_despesa))
    ]

    fig = px.bar(
        df_final,
        x="Data",
        y="Valor",
        color="Output",
        barmode="group",
        color_discrete_sequence=["red", "blue"],
        title="Receitas e Despesas",
    )
    fig.update_layout(
        margin=graph_margin,
        template=template_from_url(theme),
        height=350,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
    )

    return fig


# grafico 3
@app.callback(
    Output("graph3", "figure"),
    [
        Input("store-receitas", "data"),
        Input("dropdown-receita", "value"),
        Input(ThemeChangerAIO.ids.radio("theme"), "value"),
    ],
)
def update_graph3(data_receita, receita, theme):
    df = pd.DataFrame(data_receita)
    df = df[df["Categoria"].isin(receita)]

    fig = px.pie(df, values="Valor", names="Categoria", hole=0.2)
    fig.update_layout(title={"text": "Receitas"})
    fig.update_layout(
        margin=graph_margin, template=template_from_url(theme), height=350
    )
    fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")

    return fig


# grafico 4
@app.callback(
    Output("graph4", "figure"),
    [
        Input("store-despesas", "data"),
        Input("dropdown-despesa", "value"),
        Input(ThemeChangerAIO.ids.radio("theme"), "value"),
    ],
)
def update_graph4(data_despesa, despesa, theme):
    if data_despesa is None or despesa is None or theme is None:
        raise dash.exceptions.PreventUpdate

    df = pd.DataFrame(data_despesa)
    df = df[df["Categoria"].isin(despesa)]

    fig = px.pie(df, values="Valor", names="Categoria", hole=0.2)
    fig.update_layout(title={"text": "Despesas"})
    fig.update_layout(
        margin=graph_margin, template=template_from_url(theme), height=350
    )
    fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")

    return fig
