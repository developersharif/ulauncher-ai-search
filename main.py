import json
import logging
from urllib.parse import quote_plus

from ulauncher.api.client.Extension import Extension
from ulauncher.api.client.EventListener import EventListener
from ulauncher.api.shared.event import KeywordQueryEvent
from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem
from ulauncher.api.shared.action.RenderResultListAction import RenderResultListAction
from ulauncher.api.shared.action.OpenUrlAction import OpenUrlAction

logger = logging.getLogger(__name__)


class AiSearchExtension(Extension):
    def __init__(self):
        super().__init__()
        self.subscribe(KeywordQueryEvent, KeywordQueryEventListener())


class KeywordQueryEventListener(EventListener):
    def on_event(self, event, extension):
        query = event.get_argument() or ""
        
        default_engine_id = extension.preferences.get("default_engine_id", "googleai")
        engines_config_json = extension.preferences.get("engines_config", "[]")
        
        try:
            engines = json.loads(engines_config_json)
            
            if default_engine_id == "gemini":
                default_engine_id = "googleai"
            
            engine_ids = [e.get("id") for e in engines]
            if "googleai" not in engine_ids:
                engines.insert(0, {
                    "id": "googleai", 
                    "name": "Google AI Mode", 
                    "url_template": "https://www.google.com/search?udm=50&q=%s",
                    "icon": "fa-brain"
                })
            
            engines = [e for e in engines if e.get("id") != "gemini"]
            
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse engines_config JSON: {e}")
            return RenderResultListAction([
                ExtensionResultItem(
                    icon="images/icon.png",
                    name="Error: Invalid Engines Configuration",
                    description="Please check your engines_config JSON in preferences",
                    on_enter=None
                )
            ])
        
        # Create engine lookup dictionary
        engines_dict = {engine["id"]: engine for engine in engines}
        
        # Determine search mode and extract components
        # Get query and strip leading/trailing whitespace
        query = (event.get_argument() or "").strip()
        
        engine_id = None
        search_query = None
        
        # Logic 1: Check for ":engine" syntax (e.g. ":chatgpt query")
        if query.startswith(":"):
            # Remove colon and strip leading whitespace (e.g. ": chatgpt" -> "chatgpt")
            content = query[1:].strip()
            
            # Split by space to get engine_id
            if " " in content:
                engine_id, search_query = content.split(" ", 1)
            else:
                engine_id = content
                search_query = ""
            
        # Logic 2: Check for "engine:" syntax (e.g. "chatgpt: query")
        elif ":" in query:
            parts = query.split(":", 1)
            potential_id = parts[0].strip()
            if potential_id in engines_dict:
                engine_id = potential_id
                search_query = parts[1].strip() if len(parts) > 1 else ""

        if engine_id:
            engine_id = engine_id.strip()
        
        if search_query:
            search_query = search_query.strip()

        if engine_id:
            if engine_id not in engines_dict:
                return RenderResultListAction([
                    ExtensionResultItem(
                        icon="images/icon.png",
                        name=f"Error: Engine '{engine_id}' not found",
                        description="Available engines: " + ", ".join(engines_dict.keys()),
                        on_enter=None
                    )
                ])
            
            engine = engines_dict[engine_id]
            
            if not search_query:
                return RenderResultListAction([
                    ExtensionResultItem(
                        icon="images/icon.png",
                        name=f"Search {engine['name']}",
                        description="Enter your query to search",
                        on_enter=None
                    )
                ])
            
            url_template = engine["url_template"]
            if "%s" in url_template:
                url = url_template.replace("%s", quote_plus(search_query))
                description = f"Opens query in browser: {search_query}"
            else:
                url = url_template
                description = f"Opens {engine['name']} (paste your query: {search_query})"
            
            return RenderResultListAction([
                ExtensionResultItem(
                    icon="images/icon.png",
                    name=f"Search {engine['name']}",
                    description=description,
                    on_enter=OpenUrlAction(url)
                )
            ])
        
        else:
            # Default Search Mode: ai query text
            if not query:
                # Show available engines when no query is provided
                items = []
                for engine in engines:
                    items.append(
                        ExtensionResultItem(
                            icon="images/icon.png",
                            name=engine["name"],
                            description=f"Use {engine['id']}: to search this engine directly",
                            on_enter=None
                        )
                    )
                return RenderResultListAction(items[:8])
            
            if default_engine_id not in engines_dict:
                if "googleai" in engines_dict:
                    default_engine_id = "googleai"
                elif engines_dict:
                    default_engine_id = list(engines_dict.keys())[0]
            
            if default_engine_id not in engines_dict:
                return RenderResultListAction([
                    ExtensionResultItem(
                        icon="images/icon.png",
                        name=f"Error: Default engine '{default_engine_id}' not found",
                        description="Please configure a valid default_engine_id in preferences",
                        on_enter=None
                    )
                ])
            
            engine = engines_dict[default_engine_id]
            url_template = engine["url_template"]
            if "%s" in url_template:
                url = url_template.replace("%s", quote_plus(query))
                description = f"Opens query in browser: {query}"
            else:
                url = url_template
                description = f"Opens {engine['name']} (paste your query: {query})"
            
            return RenderResultListAction([
                ExtensionResultItem(
                    icon="images/icon.png",
                    name=f"Search {engine['name']}",
                    description=description,
                    on_enter=OpenUrlAction(url)
                )
            ])


if __name__ == "__main__":
    AiSearchExtension().run()

