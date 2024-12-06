from dataclasses import dataclass, fields, is_dataclass, MISSING, asdict
from typing import Dict, List, Optional, Type, Any
import numpy as np
import json
import requests
import pandas as pd
import funcnodes as fn
import plotly.graph_objects as go
from plotly.subplots import make_subplots


@dataclass
class Condition:
    text: str
    icon: str
    code: int


@dataclass
class AirQuality:
    co: float
    no2: float
    o3: float
    so2: float
    pm2_5: float
    pm10: float
    us_epa_index: int
    gb_defra_index: int


@dataclass
class WeatherMetrics:
    wind_mph: float
    wind_kph: float
    wind_degree: int
    wind_dir: str
    pressure_mb: float
    pressure_in: float
    precip_mm: float
    precip_in: float
    humidity: int
    cloud: int
    feelslike_c: float
    feelslike_f: float
    vis_km: float
    vis_miles: float
    uv: float
    gust_mph: float
    gust_kph: float
    air_quality: Optional[AirQuality] = None
    windchill_c: Optional[float] = None
    windchill_f: Optional[float] = None
    heatindex_c: Optional[float] = None
    heatindex_f: Optional[float] = None
    dewpoint_c: Optional[float] = None
    dewpoint_f: Optional[float] = None


@dataclass(kw_only=True)
class CurrentWeather(WeatherMetrics):
    temp_c: float
    temp_f: float
    last_updated_epoch: int
    last_updated: str
    condition: Condition
    is_day: int


@dataclass(kw_only=True)
class DayForecast:
    maxtemp_c: float
    maxtemp_f: float
    mintemp_c: float
    mintemp_f: float
    avgtemp_c: float
    avgtemp_f: float
    maxwind_mph: float
    maxwind_kph: float
    totalprecip_mm: float
    totalprecip_in: float
    totalsnow_cm: float
    avgvis_km: float
    avgvis_miles: float
    avghumidity: int
    daily_will_it_rain: int
    daily_chance_of_rain: int
    daily_will_it_snow: int
    daily_chance_of_snow: int
    condition: Condition
    uv: float
    air_quality: Optional[AirQuality] = None


@dataclass
class Astro:
    sunrise: str
    sunset: str
    moonrise: str
    moonset: str
    moon_phase: str
    moon_illumination: str
    is_moon_up: int
    is_sun_up: int


@dataclass(kw_only=True)
class HourForecast(WeatherMetrics):
    temp_c: float
    temp_f: float
    time_epoch: int
    time: str
    condition: Condition
    is_day: int
    will_it_rain: int
    chance_of_rain: int
    will_it_snow: int
    chance_of_snow: int


@dataclass
class ForecastDay:
    date: str
    date_epoch: int
    day: DayForecast
    astro: Astro
    hour: List[HourForecast]


@dataclass
class Forecast:
    forecastday: List[ForecastDay]


@dataclass
class Location:
    name: str
    region: str
    country: str
    lat: float
    lon: float
    tz_id: str
    localtime_epoch: int
    localtime: str


@dataclass
class WeatherData:
    location: Location
    current: CurrentWeather
    forecast: Forecast


def kebab_to_snake(s: str) -> str:
    """
    Convert kebab-case to snake_case.
    """
    return s.replace("-", "_")


def convert_keys(data: Any) -> Any:
    """
    Recursively convert all dictionary keys from kebab-case to snake_case.
    """
    if isinstance(data, dict):
        return {kebab_to_snake(k): convert_keys(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [convert_keys(item) for item in data]
    return data


def parse_dataclass(data_class: Type, data: Dict) -> Any:
    """
    Parse a dictionary into a dataclass, handling nested dataclasses and lists of dataclasses.
    """
    init_values = {}
    for field in fields(data_class):
        if field.name in data:
            value = data[field.name]
            field_type = field.type

            if hasattr(field_type, "__origin__"):
                # Handle List[x] fields
                if field_type.__origin__ == list:
                    element_type = field_type.__args__[0]
                    if is_dataclass(element_type):
                        init_values[field.name] = [
                            parse_dataclass(element_type, item) for item in value
                        ]
                    else:
                        init_values[field.name] = value
            elif is_dataclass(field_type):
                # Recursively parse dataclasses
                init_values[field.name] = parse_dataclass(field_type, value)
            else:
                # Simple field
                init_values[field.name] = value
        elif field.default is not MISSING:
            init_values[field.name] = field.default
        elif field.default_factory is not MISSING:
            init_values[field.name] = field.default_factory()
        else:
            raise ValueError(
                f"Missing required field {field.name} for {data_class.__name__}"
            )

    return data_class(**init_values)


def parse_weather_data(json_data: dict) -> WeatherData:
    """
    Parse JSON string into the WeatherData dataclass after converting key names.
    """
    if isinstance(json_data, str):
        json_data = json.loads(json_data)
    converted_data = convert_keys(json_data)
    return parse_dataclass(WeatherData, converted_data)


# Load your JSON data as a Python dictionary
def get_weather_data(location: str, api_key: str) -> WeatherData:
    url = f"https://api.weatherapi.com/v1/forecast.json?key={api_key}&q={location}&days=1&aqi=yes&alerts=no"
    resp = requests.get(url)
    data = resp.json()
    return parse_weather_data(data)


def hour_forecast_to_dataframe(wdata: WeatherData) -> pd.DataFrame:
    # Convert each HourForecast instance into a dictionary and handle nested dataclasses
    data = []
    for day in wdata.forecast.forecastday:
        data.extend([asdict(hour) for hour in day.hour])

    # Flatten nested dictionaries if necessary (e.g., condition fields)
    for entry in data:
        for key, value in list(entry.items()):
            if isinstance(value, dict):
                for subkey, subvalue in value.items():
                    entry[f"{key}_{subkey}"] = subvalue
                del entry[key]

    return pd.DataFrame(data)


def plot_wind(dataframe: pd.DataFrame) -> go.Figure:
    # Convert 'time' to datetime if it isn't already
    if not pd.api.types.is_datetime64_any_dtype(dataframe["time"]):
        dataframe["time"] = pd.to_datetime(dataframe["time"])

    fig = go.Figure()

    arrows = {
        "N": "↑",
        "NNE": "↗",
        "NE": "↗",
        "ENE": "↗",
        "E": "→",
        "ESE": "↘",
        "SE": "↘",
        "SSE": "↘",
        "S": "↓",
        "SSW": "↙",
        "SW": "↙",
        "WSW": "↙",
        "W": "←",
        "WNW": "↖",
        "NW": "↖",
        "NNW": "↖",
    }

    fig.add_trace(
        go.Scatter(
            x=dataframe["time"],
            y=dataframe["wind_kph"],
            mode="lines+markers+text",
            name="Wind Speed (kph)",
            text=[arrows[k] for k in dataframe["wind_dir"]],
            textposition="top center",
            line=dict(shape="linear"),
            marker=dict(size=8, color="blue"),
            textfont=dict(size=16),
        ),
    )

    # Convert timestamps back to readable dates for x-axis
    fig.update_xaxes(
        type="date",
        tickformat="%H:%M\n%d-%b",  # Customize date format as you like
    )

    # Set titles and labels
    fig.update_layout(
        title="Wind Speed and Direction",
        xaxis_title="Time",
        yaxis_title="Wind Speed (kph)",
        showlegend=True,
    )

    return fig


def plot_precipitation(dataframe: pd.DataFrame) -> go.Figure:
    # Convert 'time' to datetime if it isn't already
    if not pd.api.types.is_datetime64_any_dtype(dataframe["time"]):
        dataframe["time"] = pd.to_datetime(dataframe["time"])

    # Create figure with secondary y-axis
    fig = make_subplots(specs=[[{"secondary_y": True}]])

    # Add precipitation amount as a bar plot
    fig.add_trace(
        go.Bar(
            x=dataframe["time"],
            y=dataframe["precip_mm"],
            name="Precipitation (mm)",
            marker_color="royalblue",
        ),
        secondary_y=False,
    )

    # Add chance of rain as a line plot
    fig.add_trace(
        go.Scatter(
            x=dataframe["time"],
            y=dataframe["chance_of_rain"],
            name="Chance of Rain (%)",
            mode="lines+markers",
            line=dict(color="green"),
        ),
        secondary_y=True,
    )

    # Add figure titles and labels
    fig.update_layout(
        title_text="Precipitation and Chance of Rain",
        xaxis_title="Time",
        showlegend=True,
    )

    # Set x-axis to date format
    fig.update_xaxes(
        type="date",
        tickformat="%H:%M\n%d-%b",  # Customize date format as you like
    )

    # Set y-axes titles
    fig.update_yaxes(title_text="<b>Precipitation (mm)</b>", secondary_y=False)
    fig.update_yaxes(title_text="<b>Chance of Rain (%)</b>", secondary_y=True)

    return fig


def plot_temperature_humidity(dataframe: pd.DataFrame) -> go.Figure:
    # Convert 'time' to datetime if it isn't already
    if not pd.api.types.is_datetime64_any_dtype(dataframe["time"]):
        dataframe["time"] = pd.to_datetime(dataframe["time"])

    # Create figure with secondary y-axis
    fig = make_subplots(specs=[[{"secondary_y": True}]])

    # Add temperature as a line plot
    fig.add_trace(
        go.Scatter(
            x=dataframe["time"],
            y=dataframe["temp_c"],
            name="Temperature (°C)",
            mode="lines+markers",
            line=dict(color="red"),
        ),
        secondary_y=False,
    )

    # Add humidity as a line plot
    fig.add_trace(
        go.Scatter(
            x=dataframe["time"],
            y=dataframe["humidity"],
            name="Humidity (%)",
            mode="lines+markers",
            line=dict(color="blue"),
        ),
        secondary_y=True,
    )

    # Add figure titles and labels
    fig.update_layout(
        title_text="Temperature and Humidity", xaxis_title="Time", showlegend=True
    )

    # Set x-axis to date format
    fig.update_xaxes(
        type="date",
        tickformat="%H:%M\n%d-%b",  # Customize date format as you like
    )

    # Set y-axes titles
    fig.update_yaxes(title_text="<b>Temperature (°C)</b>", secondary_y=False)
    fig.update_yaxes(title_text="<b>Humidity (%)</b>", secondary_y=True)

    return fig


def current_weather_series(wdata: WeatherData) -> dict:
    data = asdict(wdata.current)

    def flatten(d):
        for key, value in list(d.items()):
            if isinstance(value, dict):
                value = flatten(value)
                for subkey, subvalue in value.items():
                    d[f"{key}_{subkey}"] = subvalue
                del d[key]
        return d

    data = flatten(data)
    return data


get_weather_data_node = fn.NodeDecorator(node_id="weather.wapi.get", name="Get Data")(
    get_weather_data
)

hour_forecast_to_dataframe_node = fn.NodeDecorator(
    node_id="weather.wapi.hdf", name="to hourly Dataframe"
)(hour_forecast_to_dataframe)

plot_wind_node = fn.NodeDecorator(
    node_id="weather.wapi.plot_wind",
    name="Plot Wind",
    default_render_options={"data": {"src": "out"}},
)(plot_wind)

plot_precipitation_node = fn.NodeDecorator(
    node_id="weather.wapi.plot_prec",
    name="Plot Precipitation",
    default_render_options={"data": {"src": "out"}},
)(plot_precipitation)

plot_temperature_humidity_node = fn.NodeDecorator(
    node_id="weather.wapi.plot_temphum",
    name="Plot Temperature/Humidity",
    default_render_options={"data": {"src": "out"}},
)(plot_temperature_humidity)

current_weather_series_node = fn.NodeDecorator(
    node_id="weather.wapi.current_ser",
    name="Current Weather",
    default_render_options={"data": {"src": "out"}},
)(current_weather_series)
NODE_SHELF = fn.Shelf(
    name="Weather API",
    description="Nodes for weatherapi.com",
    subshelves=[],
    nodes=[
        get_weather_data_node,
        hour_forecast_to_dataframe_node,
        plot_wind_node,
        plot_precipitation_node,
        plot_temperature_humidity_node,
        current_weather_series_node,
    ],
)
