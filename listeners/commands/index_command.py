from slack_bolt import Ack, Say, BoltContext
from logging import Logger
from slack_sdk import WebClient
import os
import requests

"""
Callback for handling the '/update-debbie' command. This will trigger the DigitalOcean API to start indexing a data source.
"""

def do_index_callback(client: WebClient, ack: Ack, command, say: Say, logger: Logger, context: BoltContext):
    try:
        ack()
        user_id = context["user_id"]
        channel_id = context["channel_id"]
        # Optionally, you can accept arguments from the command text
        data_source_id = command.get("text", "").strip() or os.environ.get("DO_DATA_SOURCE_ID")
        knowledge_base_id = os.environ.get("DO_KB_ID")
        if not knowledge_base_id:
            client.chat_postEphemeral(
                channel=channel_id,
                user=user_id,
                text="Knowledge base ID is not set. Please set DO_KB_ID in the environment."
            )
            return

        if not data_source_id:
            client.chat_postEphemeral(
                channel=channel_id,
                user=user_id,
                text="Please provide a data source ID as an argument or set DO_DATA_SOURCE_ID in the environment."
            )
            return

        # DigitalOcean API endpoint and token
        do_api_token = os.environ.get("DO_API_TOKEN")
        if not do_api_token:
            client.chat_postEphemeral(
                channel=channel_id,
                user=user_id,
                text="DigitalOcean API token is not set. Please set DO_API_TOKEN in the environment."
            )
            return

        # New DigitalOcean API call for indexing job
        url = "https://api.digitalocean.com/v2/gen-ai/indexing_jobs"
        headers = {
            "Authorization": f"Bearer {do_api_token}",
            "Content-Type": "application/json"
        }
        payload = {
            "knowledge_base_uuid": knowledge_base_id,
            "data_source_uuids": [data_source_id]
        }
        response = requests.post(url, headers=headers, json=payload)
        if response.status_code == 200:
            client.chat_postEphemeral(
                channel=channel_id,
                user=user_id,
                text=f"Indexing job started for data source `{data_source_id}` in knowledge base `{knowledge_base_id}`."
            )
        else:
            client.chat_postEphemeral(
                channel=channel_id,
                user=user_id,
                text=f"Failed to start indexing job. Status: {response.status_code}, Response: {response.text}"
            )
    except Exception as e:
        logger.error(f"Error in /update-debbie: {e}")
        client.chat_postEphemeral(
            channel=context["channel_id"],
            user=context["user_id"],
            text=f"An error occurred: {e}"
        )
