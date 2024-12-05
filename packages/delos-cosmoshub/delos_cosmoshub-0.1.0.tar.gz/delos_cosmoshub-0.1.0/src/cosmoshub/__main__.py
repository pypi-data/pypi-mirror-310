"""Main module for the CosmosHub API client."""

import logging

from .client import CosmosHubClient

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

if __name__ == "__main__":
    client = CosmosHubClient("my-api-key", "https://platform.cosmos-suite.ai", debug_mode=True)
    response = client.status_health_request()

    if response:
        logger.info(f"Response: {response}")
