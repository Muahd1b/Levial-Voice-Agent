Research Report: Domain Support - Aviation & Hobbies for Levial
Date: November 24, 2025 Topic: Architectural patterns for Aviation Support in a local-first AI agent.

1. Executive Summary
   Data APIs: CheckWX (Free Tier) is the best balance of ease-of-use and data coverage (METAR/TAF). For NOTAMs, the FAA API is authoritative but requires registration; CheckWX has a paid tier for NOTAMs. NOAA is great for raw XML/CSV data.
   Python Libraries: Use python-metar for parsing raw METAR strings if fetching from NOAA. Use avwx-engine or checkwx-python for a higher-level interface.
   RAG for Manuals: Standard RAG fails on POH tables. Use "Table-Specific Processing": Convert performance charts/tables into Markdown or JSON before indexing. Use a Hybrid RAG approach where tables are stored as structured data and text as vectors.
   Simulation Integration: SimConnect (via python-simconnect) is the standard for MSFS. UDP is the standard for X-Plane. Levial can have a "Sim Interface" module that abstracts these differences.
   Training Scenarios: Build an "Instructor Agent" that uses the RAG knowledge base (FAR/AIM) to generate oral exam questions. For practical training, the agent monitors SimConnect telemetry (e.g., "Altitude deviation!") and provides verbal feedback.
2. Foundations & Definitions
   METAR/TAF: Standard aviation weather reports (Observation / Forecast).
   NOTAM: Notice to Airmen (essential safety updates).
   SimConnect: The API used by Microsoft Flight Simulator (MSFS) to allow external apps to read/write simulation variables.
   UDP (User Datagram Protocol): A fast, connectionless network protocol used by X-Plane to broadcast flight data.
3. Conceptual Map / Framework
   The "Co-Pilot" Architecture:

Data Fetcher (MCP Server):
Tools: get_weather(icao), get_notams(icao).
Source: CheckWX API or NOAA.
Manual Reader (RAG Engine):
Index: Vector Store (ChromaDB) containing chunked POH/FAR/AIM.
Special Handling: Performance tables extracted as JSON.
Sim Interface (Telemetry):
Input: Stream of data from MSFS (SimConnect) or X-Plane (UDP).
Action: Monitor for "Events" (e.g., Stall Warning, Altitude Bust).
Instructor Agent:
Mode 1 (Study): Quizzes user on regulations using RAG.
Mode 2 (Flight): Acts as a safety pilot, calling out deviations based on Telemetry. 4. Current State of the Field
ForeFlight/Garmin Pilot: The gold standard for EFB (Electronic Flight Bag). They digest weather/NOTAMs but don't offer "AI Instruction".
AI Co-Pilots: Emerging tools like "Otto" (Gleim) use LLMs for oral exam prep.
Sim Tools: python-simconnect and XPlaneUDP are mature libraries for connecting Python to sims. 5. Approaches, Methods, and Tools
Data API Strategy
Source Best For Pros Cons
CheckWX General Use. JSON format, easy API, free tier. NOTAMs might be paid.
NOAA Raw Data. Free, authoritative, no limits. XML/CSV format, harder to parse.
FAA API US NOTAMs. Official source. Registration required, US-centric.
Simulation Integration
MSFS: Use python-simconnect. It's a wrapper around the C++ SDK. Note: Windows only.
X-Plane: Use XPlaneUDP or raw socket programming. Works on Mac/Linux/Windows. 6. Risks, Limitations, and Failure Modes
Stale Data: Weather changes fast. Mitigation: Always timestamp data and warn if >1 hour old.
Hallucinated Procedures: LLM invents a "V-speed". Mitigation: Strict RAG. If the POH doesn't say it, the Agent shouldn't guess.
Sim Latency: Voice alerts might be delayed. Mitigation: Keep the telemetry loop tight (local UDP). 7. Actionable Recommendations for Levial
Recommended Stack
Weather: CheckWX (Free) for JSON data. Fallback to NOAA if needed.
Sim: Start with X-Plane UDP (easier to implement on Mac/Linux, no DLLs).
RAG: ChromaDB for text. Manually transcribe key POH tables (V-speeds, Weight & Balance) into a poh_data.json file for 100% accuracy.
Implementation Steps
Build mcp-server-aviation:
Tool: get_metar(icao) -> Calls CheckWX -> Returns parsed JSON.
Tool: get_taf(icao).
Build SimMonitor:
A background thread that listens on X-Plane's UDP port (49000).
Parses "DATA" packets for Altitude, Airspeed, Heading.
Create "Instructor" Persona:
System Prompt: "You are a strict but encouraging Flight Instructor. Use the provided POH data to answer questions." 8. Assumptions & Uncertainties
Assumption: The user has a CheckWX API key (free).
Uncertainty: Parsing complex NOTAMs (which are often unstructured text) into a "clean" format for the LLM might be hit-or-miss.
