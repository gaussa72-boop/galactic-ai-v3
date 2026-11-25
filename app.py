from main import app

from agent_bridge import register_agent_bridge
register_agent_bridge(app, agent_id="galactic", display_name="Galactic AI", persona="Du orchestrierst kreative Archetypen, Storytelling, Weltenbau und systemische Projektideen.")

# Render entry point. The application routes are defined in main.py.
