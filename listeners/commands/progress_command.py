from slack_bolt import Ack, Say, BoltContext
from logging import Logger
from slack_sdk import WebClient
import os
import requests

"""
Callback for handling the '/debbie-progress' command. This will query the DigitalOcean API for the progress of the last index operation.
"""

def debbie_progress_callback(client: WebClient, ack: Ack, command, say: Say, logger: Logger, context: BoltContext):
    try:
        ack()
        user_id = context["user_id"]
        channel_id = context["channel_id"]
        # Optionally, you can accept arguments from the command text
        data_source_id = command.get("text", "").strip() or os.environ.get("DO_DATA_SOURCE_ID")
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

        # Example DigitalOcean API call (replace with the actual endpoint and payload)
        url = f"https://api.digitalocean.com/v2/ai/index/{data_source_id}/progress"
        headers = {
            "Authorization": f"Bearer {do_api_token}",
            "Content-Type": "application/json"
        }
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            progress = response.json()
            client.chat_postEphemeral(
                channel=channel_id,
                user=user_id,
                text=f"Index progress for `{data_source_id}`: {progress}"
            )
        else:
            client.chat_postEphemeral(
                channel=channel_id,
                user=user_id,
                text=f"Failed to get progress. Status: {response.status_code}, Response: {response.text}"
            )
    except Exception as e:
        logger.error(f"Error in /debbie-progress: {e}")
        client.chat_postEphemeral(
            channel=context["channel_id"],
            user=context["user_id"],
            text=f"An error occurred: {e}"
        )
