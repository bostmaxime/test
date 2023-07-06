import geopandas as gpd
import dash
from dash import dcc
from dash import html
from dash import ctx
from dash.dependencies import Input, Output
import plotly.express as px
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
from PIL import Image
import pandas as pd


# logo_mines = Image.open("data/images/logo_mines_resized.png")
gdf = gpd.read_file("final_bost.geojson")
FUAS = sorted(gdf["fua"].unique())
centroids = gpd.read_file("fuas_centroids.geojson")
centroids = centroids.to_crs("EPSG:4326")
max_Q219 = max(gdf['Q219'])
max_loypredm2 = max(gdf['loypredm2'])
max_TP60IP19 = 0.4
max_T_day = max(gdf['T_day'])
max_T_night = max(gdf['T_night'])

logo_OCDE = Image.open("data/images/lucian-removebg-preview.png")
logo_mines = Image.open("data/images/logo_mines_resized-removebg-preview.png")

mean_values = pd.read_csv("mean_fua.csv")

indicators1=['mean_Q219','mean_loypredm2','mean_TP60IP19']
indicators2=['mean_T_day','mean_T_night']

for indicator in indicators1:
    mean_values['p_'+indicator]=mean_values[indicator]*mean_values['NBPERS19']
for indicator in indicators2:
    mean_values['p_'+indicator]=mean_values[indicator]*mean_values['area']

mean_values=mean_values[['NBPERS19','area','p_mean_Q219','p_mean_loypredm2','p_mean_TP60IP19','p_mean_T_day','p_mean_T_night']]
mean_values=mean_values.sum()
mean_values=pd.DataFrame(mean_values)

dico={}
dico['m_Q219']=mean_values.loc['p_mean_Q219']/mean_values.loc['NBPERS19']
dico['m_loypredm2']=mean_values.loc['p_mean_loypredm2']/mean_values.loc['NBPERS19']
dico['m_TP60IP19']=mean_values.loc['p_mean_TP60IP19']/mean_values.loc['NBPERS19']
dico['m_T_day']=mean_values.loc['p_mean_T_day']/mean_values.loc['area']
dico['m_T_night']=mean_values.loc['p_mean_T_night']/mean_values.loc['area']

# Création du dashboard
app = dash.Dash(external_stylesheets=[dbc.themes.DARKLY])
server=app.server

# On définit le layout
app.layout = html.Div(
    [
        html.Div(
            [
                html.Img(
                    src=logo_mines,
                    style={
                        "height": "130px",
                        "width": "90 px",
                        "grid-column": "1",
                        "grid-row": "1",
                        "padding-right": "150 px",
                        "padding-top": "50 px",
                    },
                ),
                html.Img(
                    src=logo_OCDE,
                    style={
                        "height": "100px",
                        "width": "60 px",
                        "grid-column": "3",
                        "grid-row": "1",
                        "padding-top": "45px",
                        "padding-left": "250px",
                    },
                ),
                html.H1(
                    "INTRACITY INEQUALITIES",
                    style={
                        "color": "#878787",
                        "font-size": 42,
                        "src": "font/San Francisco.ttf",
                        "grid-column": "2",
                        "grid-row": "1",
                        "padding-left": "250px",
                        "padding-top": "47px",
                        "text-align": "center",
                    },
                ),
            ],
            style={
                "backgroundColor": "#E4E4E4",
                "font-size": 20,
                "font-weight": "bold",
                "font-family": "Arial",
                "height": "80 px",
                "display": "grid",
                "grid-template-column": "1fr 5fr",
                "grid-template-row": "1fr",
                "text-align": "center",
            },
        ),
        html.Div(
            [
                html.Div(
                    [
                        html.H3(
                            "Choisissez la FUA à étudier",
                            style={
                                "font-size": 20,
                                "textAlign": "center",
                                "padding": "15px",
                                "color": "#555555",
                            },
                        ),
                        dcc.Dropdown(
                            options=[
                                {
                                    "label": html.Span(
                                        [fua_name],
                                        style={
                                            "color": "#555555",
                                            "font-size": 20,
                                            "textAlign": "center",
                                        },
                                    ),
                                    "value": fua_name,
                                }
                                for fua_name in FUAS
                            ],
                            value="Paris",
                            searchable=True,
                            optionHeight=50,
                            style={
                                "width": "95%",
                                "backgroundColor": "white",
                                "color": "white",
                                "margin-left": "5px",
                                "border-color": "#555555",
                            },
                            id="selected_FUA",
                        ),
                        html.H3(
                            "Choisissez l'indicateur à afficher",
                            style={
                                "font-size": 20,
                                "textAlign": "center",
                                "padding": "15px",
                                "color": "#555555",
                            },
                        ),
                        dcc.Dropdown(
                            options=[
                                {
                                    "label": html.Span(
                                        ["💸 Revenus"],
                                        style={"color": "#555555", "font-size": "15"},
                                    ),
                                    "value": "Q219",
                                },
                                {
                                    "label": html.Span(
                                        ["💰 Indice de pauvreté TP60IP19"],
                                        style={"color": "#555555", "font-size": 15},
                                    ),
                                    "value": "TP60IP19",
                                },
                                {
                                    "label": html.Span(
                                        ["🏠 Prix loyer/m^2"],
                                        style={"color": "#555555", "font-size": 15},
                                    ),
                                    "value": "loypredm2",
                                },
                                {
                                    "label": html.Span(
                                        ["☀️ Température moyenne au sol le jour"],
                                        style={"color": "#555555", "font-size": 15},
                                    ),
                                    "value": "T_day",
                                },
                                {
                                    "label": html.Span(
                                        ["🌙 Température moyenne au sol la nuit"],
                                        style={"color": "#555555", "font-size": 15},
                                    ),
                                    "value": "T_night",
                                },
                            ],
                            value="Q219",
                            searchable=True,
                            optionHeight=50,
                            style={
                                "width": "95%",
                                "backgroundColor": "white",
                                "color": "#555555",
                                "margin-bottom": "25px",
                                "margin-left": "5px",
                                "border-color": "#555555",
                            },
                            id="selected_indicator",
                        ),
    
                    
                    dcc.Graph(id='radar-graph')
                    ],
                    style={
                        "grid-column": "1",
                        "align-self": "center",
                        "grid-row": "1",
                        "background-color": "white",
                        "height": "100%",
                    },
               
                ),
                html.Div(
                    [
                        dcc.Graph(
                            id="map-graph",
                            style={
                                "width": "80vw",
                                "height": "80vh",
                                "border-radius": "15 px",
                                "background-color": "white",
                                "grid-row": "2",
                                "display": "inline-block",
                                "displayModeBar": "False",
                            },
                        )
                    ],
                    style={"grid-column ": "2"},
                ),
            ],
            style={
                "display": "grid",
                "grid-template-columns": "1fr 2fr",
                "grid-gap": "50 px",
                "background-color": "white",
            },
        ),
    ],
    style={"background-color": "white"},
)

initial_center_lat = 48.864716
initial_center_lon = 2.349014
initial_zoom = 7


# On définit le callback, on écrit l'update de la map
@app.callback(
    Output("map-graph", "figure"),
    Input("selected_FUA", "value"),
    Input("selected_indicator", "value"),
    Input("map-graph", "relayoutData"),
)
def update_map(FUA, indicator, relayout_data):
    gdf_partiel = gdf[gdf["fua"] == FUA]
    if indicator == "Q219":
        scale = (10000, 45000)
        colors = "hot"
    elif indicator == "TP60IP19":
        scale = (0.1, 0.4)
        colors = "hot"
    elif indicator == "T_day":
        scale = (25, 40)
        colors = "icefire"
    elif indicator == "T_night":
        scale = (10, 22)
        colors = "icefire"
    else:
        colors = "hot"
        if FUA == "Paris":
            scale = (8, 35)
        else:
            scale = (5, 20)
    # On plot les données
    point = centroids[centroids["fuaname"] == FUA].geometry
    if ctx.triggered_id == "selected_FUA":
        lat = point.y.iloc[0]
        long = point.x.iloc[0]
        if FUA == "Paris":
            zo = 7
        else:
            zo = 8.5
    else:
        try:
            center = relayout_data.get("mapbox.center", None)
        except:
            center = None
        long = center["lon"] if center else point.x.iloc[0]
        lat = center["lat"] if center else point.y.iloc[0]
        try:
            zo = relayout_data.get("mapbox.zoom", 7)
        except:
            zo = 7
    fig = px.choropleth_mapbox(
        # Set the labels orientation horizontal
        data_frame=gdf_partiel,
        geojson=gdf_partiel[["CODGEO", "geometry"]].__geo_interface__,
        featureidkey="properties.CODGEO",
        locations="CODGEO",
        color=indicator,
        range_color=scale,
        mapbox_style="open-street-map",
        hover_name="NOM_COM",
        hover_data={indicator: True, "CODGEO": False},
        labels={
            "Q219": "Revenus (€)",
            "TP60IP19": "Indice de pauvreté",
            "T_day": "Température moy. au sol le jour (°C)",
            "T_night": "Température moy. au sol la nuit (°C)",
            "loypredm2": "Prix loyer au m^2 (€)",
        },
        zoom=zo,
        center={"lat": lat, "lon": long},
        opacity=0.6,
        color_continuous_scale=colors,
    )
    fig.update_layout(
        plot_bgcolor="white",
        paper_bgcolor="white",
        margin={"r": 0, "t": 0, "l": 0, "b": 0},
        font=dict(color="black"),
        hoverlabel=dict(bgcolor="white", font_size=16, font_family="sans-serif"),
        xaxis=dict(tickangle=-90),
    )

    return fig

categories = ['Revenus','Prix loyer',
              'T jour', 'T nuit', 'Taux pauvreté']

@app.callback(
    Output("radar-graph", "figure"),
    Input("map-graph", "clickData"),
)
def display_city_name(click_data):
    fig = go.Figure()
    if click_data is not None:
        city_code = click_data['points'][0]['location']
        part_gdf = gdf[gdf['CODGEO'] == city_code]
        city_name = part_gdf['NOM_COM'].values[0]
        info = [part_gdf['Q219'].values[0]/max_Q219, part_gdf['loypredm2'].values[0]/max_loypredm2, part_gdf['T_day'].values[0]/max_T_day, part_gdf['T_night'].values[0]/max_T_night, part_gdf['TP60IP19'].values[0]/max_TP60IP19]
        fig.add_trace(go.Scatterpolar(
        r=info,
        theta=categories,
        fill='toself',
        name=city_name,
        opacity = 0.6,
        fillcolor = 'red'
        ))
    else:
        city_code = "nothing"
        info = "nothing"
        city_name = ""
    fig.add_trace(go.Scatterpolar(
        r=[float(dico['m_Q219']/max_Q219), float(dico['m_loypredm2']/max_loypredm2), float(dico['m_T_day']/max_T_day), float(dico['m_T_night']/max_T_night), float(dico['m_TP60IP19']/max_TP60IP19)],
        theta=categories,
        fill='toself',
        name="Moyenne française",
        opacity = 0.6,
        fillcolor = 'blue'
    ))

    fig.update_layout(
    polar=dict(
        radialaxis=dict(
        visible=False,
        range=[0, 1]
        )),
    showlegend=False,
    margin=dict(t=50, b=50),
    height = 300,
    hovermode = False
    )
    fig.update_layout(title = dict(text = "Comparaison moyenne française <br>"  + city_name, font = {'size': 15}))
    return fig

if __name__ == "__main__":
    app.run_server(debug=True)
