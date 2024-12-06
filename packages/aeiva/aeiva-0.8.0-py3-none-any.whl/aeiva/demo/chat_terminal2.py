# agent.py

import os
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
import asyncio
from dotenv import load_dotenv
import logging

from aeiva.cognition.input_interpreter.simple_input_interpreter import SimpleInputInterpreter
from aeiva.cognition.output_orchestrator.simple_output_orchestrator import SimpleOutputOrchestrator
from aeiva.cognition.emotion.simple_emotion import SimpleEmotion
from aeiva.cognition.world_model.simple_world_model import SimpleWorldModel
from aeiva.cognition.brain.llm_brain import LLMBrain
from aeiva.llm.llm_gateway_config import LLMGatewayConfig
from aeiva.agent.agent import Agent
import litellm

from aeiva.cognition.memory.memory_palace import MemoryPalace
from aeiva.cognition.memory.memory_config import MemoryConfig
from aeiva.embedding.embedder_config import EmbedderConfig
from aeiva.storage.database_factory import DatabaseConfigFactory

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# Embedder dimensions configuration
MODEL_EMBEDDING_DIMENSIONS = {
    'text-embedding-ada-002': 1536,
    # Add other models and their embedding dimensions as needed
}


# Main function
def main():
    # Load environment variables (API keys, etc.)
    load_dotenv()
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "your_default_api_key_here")

    # Ensure 'storage' directory exists
    os.makedirs('storage', exist_ok=True)

    # Define Embedder Configuration
    embedder_config = EmbedderConfig(
        provider_name='openai',
        model_name='text-embedding-ada-002',
        api_key=OPENAI_API_KEY,  # Replace with your actual OpenAI API key
    )

    # Vector Database Configuration (Milvus)
    vector_db_config = DatabaseConfigFactory.create(
        provider_name='milvus',
        uri='storage/milvus_demo.db',
        collection_name='test_collection',
        embedding_model_dims=MODEL_EMBEDDING_DIMENSIONS.get(embedder_config.model_name),  # 1536
        metric_type='COSINE',
    )

    # Graph Database Configuration (Neo4j)
    graph_db_config = DatabaseConfigFactory.create(
        provider_name='neo4j',
        uri='bolt://localhost:7687',
        user='neo4j',
        password='cf57bwP9pcdcEK3',  # Replace with your actual password
        database='neo4j',
        encrypted=False,
    )

    # Relational Database Configuration (SQLite)
    relational_db_config = DatabaseConfigFactory.create(
        provider_name='sqlite',
        database='storage/test_database.db'  # Use a file-based database for persistence
    )

    # Memory Configuration
    memory_config = MemoryConfig(
        embedder_config=embedder_config,
        vector_db_provider='milvus',
        vector_db_config=vector_db_config,
        graph_db_provider='neo4j',
        graph_db_config=graph_db_config,
        relational_db_provider='sqlite',
        relational_db_config=relational_db_config,
    )

    # Initialize MemoryPalace
    memory_palace = MemoryPalace(config=memory_config)

    # Load LLMBrain Configuration
    llm_config = LLMGatewayConfig(
        llm_api_key=OPENAI_API_KEY,
        llm_model_name="gpt-4o",
        llm_temperature=0.7,
        llm_max_output_tokens=10000,
        # llm_logging_level="info",
        llm_stream=True
    )

    # Initialize LLMBrain
    llm_brain = LLMBrain(llm_config)

    # Define cognition components with MemoryPalace
    cognition_components = {
        "input_interpreter": SimpleInputInterpreter(),
        "brain": llm_brain,  # Instance of LLMBrain
        "output_orchestrator": SimpleOutputOrchestrator(),
        "memory": memory_palace,  # Use MemoryPalace instead of SimpleMemory
        "emotion": SimpleEmotion(),
        "world_model": SimpleWorldModel(),
        "config": None  # Placeholder for additional configurations if needed
    }

    # Define action configuration with available tools
    action_config = {
        "tools": [
            "get_system_info",
            "get_package_root",
            "get_user_home_path",
            "open_application",
            "close_application",
            "percept_terminal_input",
            "play_music",
            "stop_music",
            "take_screenshot",
            "create_file_or_folder",
            "delete_file",
            "edit_file",
            "find_file",
            "list_files",
            "open_file_or_folder",
            "read_file",
            "rename_file",
            "search_file_or_folder",
            "write_file",
            "analyze_gui",
            "analyze_gui_by_ocr",
            "click_mouse",
            "click_on_element",
            "move_mouse",
            "operate_computer",
            "scroll",
            "type_into_element",
            "type_keyboard",
            "click_webpage_element",
            "crawl",
            "execute_js_script_on_webpage",
            "get_webpage_details",
            "get_webpage_elements",
            "navigate_browser_history",
            "navigate_to_webpage",
            "refresh_webpage",
            "scrape",
            "scroll_webpage",
            "type_text_in_webpage_element",
            "web_search"
        ]
    }

    # Define configurations
    perception_config = {
        "sensors": [
            {
                "sensor_name": "percept_terminal_input",
                "sensor_params": {"prompt_message": "You: "}
            }
        ]
    }

    # Create agent instance
    agent = Agent(perception_config=perception_config,
                  cognition_components=cognition_components,
                  action_config=action_config)
    agent.setup()

    # Run the agent
    try:
        asyncio.run(agent.run())
    except KeyboardInterrupt:
        logger.info("Agent execution interrupted by user.")
    except Exception as e:
        logger.error(f"An error occurred during agent execution: {e}")
    finally:
        # Optional: Perform any cleanup if necessary
        try:
            memory_palace.delete_all()
            logger.info("All memory units deleted during cleanup.")
        except NotImplementedError as nie:
            logger.warning(f"Delete All feature not implemented: {nie}")
        except Exception as e:
            logger.error(f"Error during cleanup: {e}")
            print("Failed to delete all memory units.")


if __name__ == "__main__":
    main()