Multi-Agent Tourism Planner (LangChain + Streamlit)

Lightweight multi-agent tourism planner using LangChain tools and Streamlit.

Features
- Parent (orchestrator) agent coordinates two child agents: WeatherAgent and PlacesAgent.
- Uses external APIs (no AI memory): Nominatim (geocoding), Open-Meteo (weather), Overpass (places).
- Minimal dependencies: `langchain`, `requests`, `streamlit`.

Folder layout
```
project/
│── app.py
│── agents/
│   ├── parent_agent.py
│   ├── weather_agent.py
│   ├── places_agent.py
│── tools/
│   ├── geocode_tool.py
│   ├── weather_tool.py
│   ├── places_tool.py
│── services/
│   ├── geocode_service.py
│   ├── weather_service.py
│   ├── places_service.py
│── utils/
│   ├── parser.py
│── requirements.txt
```

Setup

1. Create a Python virtual environment and activate it.

Windows (PowerShell):
```
python -m venv .venv; .\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Run locally

```
streamlit run app.py
```

Deploy to Streamlit Cloud

1. Push this repository to GitHub.
2. Add repo to Streamlit Cloud and set Python version to 3.10+.
3. Streamlit Cloud will install `requirements.txt` and run `app.py`.

Notes
- The project uses LangChain tool classes to wrap external API calls. No proprietary LLM/API keys are required to run the tool-based orchestration in this minimal example.
- Error handling is implemented for API failures and when locations cannot be found (responds with: "I don't think this place exists.").

Enjoy!
