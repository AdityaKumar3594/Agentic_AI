import os
import requests
from dotenv import load_dotenv
import streamlit as st
from tavily import TavilyClient

load_dotenv()

OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

if TAVILY_API_KEY:
    tavily_client = TavilyClient(api_key=TAVILY_API_KEY)
else:
    tavily_client = None


def get_weather(city: str) -> str:
    if not OPENWEATHER_API_KEY:
        return "Error: OPENWEATHER_API_KEY is not set in .env"

    url = f"http://api.openweathermap.org/data/2.5/weather?q={city},IN&appid={OPENWEATHER_API_KEY}&units=metric"
    response = requests.get(url)

    try:
        data = response.json()
    except ValueError:
        return "Error: Invalid response from weather API"

    if str(data.get("cod")) != "200":
        return f"Error: {data.get('message', 'Could not fetch weather')}"

    temp = data["main"]["temp"]
    desc = data["weather"][0]["description"]
    return f"Weather in {city}: {desc}, {temp}°C"


def get_news(city: str) -> str:
    if not tavily_client:
        return "Error: TAVILY_API_KEY is not set in .env"

    response = tavily_client.search(
        query=f"latest news in {city}",
        search_depth="basic",
        max_results=3,
    )

    results = response.get("results", [])
    if not results:
        return f"No news found for {city}"

    lines = []
    for item in results:
        title = item.get("title", "No title")
        url = item.get("url", "")
        snippet = item.get("content", "")
        lines.append(f"• {title}\n  🔗 {url}\n  📝 {snippet[:120]}...")

    return f"Latest news in {city}:\n\n" + "\n\n".join(lines)


st.set_page_config(page_title="Agentic AI Streamlit", layout="wide")

st.title("Agentic AI Streamlit Interface")
st.write("Use the controls below to fetch weather or news for a city.")

city = st.text_input("City", value="Bangalore")
option = st.radio("Tool", ["Weather", "News"], index=0, horizontal=True)

if st.button("Run"):
    if not city.strip():
        st.warning("Please enter a city name.")
    else:
        with st.spinner(f"Fetching {option.lower()} for {city}..."):
            if option == "Weather":
                output = get_weather(city)
            else:
                output = get_news(city)

        if output.startswith("Error:"):
            st.error(output)
        else:
            st.success(output)

st.markdown("---")
status = []
if OPENWEATHER_API_KEY:
    status.append("✅ Weather key loaded")
else:
    status.append("⚠️ OPENWEATHER_API_KEY missing")
if TAVILY_API_KEY:
    status.append("✅ News key loaded")
else:
    status.append("⚠️ TAVILY_API_KEY missing")

st.caption(" | ".join(status))
