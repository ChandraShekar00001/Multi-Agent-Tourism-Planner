"""Streamlit front-end for the Multi-Agent Tourism Planner."""
from typing import Any, Dict
import streamlit as st

from agents.parent_agent import ParentAgent

st.set_page_config(page_title="Multi-Agent Tourism Planner", layout="centered")

def render_weather_card(weather_data: Dict[str, Any]) -> None:
    with st.container():
        st.markdown(
            """
            <div style='background: #e3f2fd; border-radius: 10px; padding: 18px 16px 10px 16px; margin-bottom: 10px;'>
            <h4 style='color:#1976d2; margin-top:0;'>Weather</h4>
            """,
            unsafe_allow_html=True,
        )
        if not weather_data:
            st.info("No weather information available.")
        elif weather_data.get("error"):
            st.error(weather_data.get("error"))
        else:
            loc = weather_data.get("location", {})
            weather = weather_data.get("weather", {})
            st.markdown(f"**Location:** {loc.get('display_name', 'Unknown')}")
            st.markdown(f"**Temperature:** {weather.get('temperature')} °C")
            st.markdown(f"**Wind:** {weather.get('windspeed')} m/s, direction {weather.get('winddirection')}°")
            st.markdown(f"**Observed at:** {weather.get('time')}")
        st.markdown("</div>", unsafe_allow_html=True)

def render_places_card(places_data: Dict[str, Any]) -> None:
    with st.container():
        st.markdown(
            """
            <div style='background: #fff3e0; border-radius: 10px; padding: 18px 16px 10px 16px; margin-bottom: 10px;'>
            <h4 style='color:#ef6c00; margin-top:0;'>Places / Attractions</h4>
            """,
            unsafe_allow_html=True,
        )
        if not places_data:
            st.info("No places information available.")
        elif places_data.get("error"):
            st.error(places_data.get("error"))
        else:
            loc = places_data.get("location", {})
            places = places_data.get("places", [])
            st.markdown(f"**Location:** {loc.get('display_name', 'Unknown')}")
            if not places:
                st.markdown("No attractions found nearby.")
            else:
                for p in places[:10]:
                    name = p.get("name")
                    tags = p.get("tags", {})
                    dist = p.get("distance_m")
                    st.markdown(f"- **{name}** — {tags.get('tourism') or tags.get('amenity') or tags.get('operator','')} ({int(dist)} m)")
        st.markdown("</div>", unsafe_allow_html=True)

def main() -> None:
    # Custom CSS for background and buttons
    st.markdown(
        """
        <style>
        body {
            background-color: #f5f7fa;
        }
        .stButton>button {
            color: white;
            background: linear-gradient(90deg, #1976d2 60%, #ef6c00 100%);
            border: none;
            border-radius: 8px;
            padding: 0.5em 1.5em;
            font-weight: 600;
            font-size: 1.1em;
            margin-right: 0.5em;
        }
        .stButton>button:hover {
            background: linear-gradient(90deg, #1565c0 60%, #f57c00 100%);
        }
        .stTextInput>div>div>input {
            border-radius: 8px;
            border: 1.5px solid #1976d2;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div style='background: linear-gradient(90deg, #1976d2 60%, #ef6c00 100%); padding: 1.5em 1em; border-radius: 12px; margin-bottom: 1.5em;'>
            <h2 style='color: white; margin-bottom: 0;'>Multi-Agent Tourism Planner</h2>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.write("Enter a place or ask a travel question (e.g., 'Weather in Paris' or 'Attractions near Tokyo').")

    col1, col2 = st.columns([3, 1])
    with col1:
        user_input = st.text_input("Enter a place or ask a travel question", value="Paris", key="input")
    with col2:
        radius = st.slider("Search radius (meters)", min_value=500, max_value=10000, value=3000, step=500, key="radius")

    # Button row
    col_search, col_clear = st.columns([1, 1])
    search_clicked = col_search.button("Search", use_container_width=True)
    clear_clicked = col_clear.button("Clear", use_container_width=True)

    # Session state for results
    if "result" not in st.session_state:
        st.session_state.result = None
    if "input_value" not in st.session_state:
        st.session_state.input_value = user_input

    if search_clicked:
        agent = ParentAgent()
        with st.spinner("Planning... talking to agents..."):
            try:
                result = agent.handle(user_input)
                st.session_state.result = result
                st.session_state.input_value = user_input
            except Exception as e:
                st.error(f"Agent error: {e}")
                st.session_state.result = None

    if clear_clicked:
        st.session_state.result = None
        st.session_state.input_value = ""
        st.experimental_rerun()

    # Show results if available
    if st.session_state.result:
        cols = st.columns(2)
        with cols[0]:
            render_weather_card(st.session_state.result.get("weather"))
        with cols[1]:
            places_resp = st.session_state.result.get("places")
            if places_resp and places_resp.get("location"):
                render_places_card(places_resp)
            else:
                from agents.places_agent import PlacesAgent
                pa = PlacesAgent()
                places_resp = pa.handle(st.session_state.result.get("place"), radius=radius)
                render_places_card(places_resp)

if __name__ == "__main__":
    main()
