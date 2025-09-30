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

        # Try to get index job ID from file (per channel, in index_jobs directory)
        index_job_id = None
        try:
            dir_path = os.path.join(os.path.dirname(__file__), '../../index_jobs')
            dir_path = os.path.abspath(dir_path)
            file_path = os.path.join(dir_path, f"last_index_job_{channel_id}.txt")
            with open(file_path, "r") as f:
                index_job_id = f.read().strip()
            logger.info(f"Read index job ID {index_job_id} from {file_path}")
        except Exception as file_err:
            logger.error(f"Failed to read index job ID file: {file_err}")

        if not index_job_id:
            client.chat_postEphemeral(
                channel=channel_id,
                user=user_id,
                text="No recent index job found for this channel. Please run /update-debbie first."
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

        # New DigitalOcean API call for progress by index job ID
        url = f"https://api.digitalocean.com/v2/gen-ai/indexing_jobs/{index_job_id}"
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
                text=f"Index job progress for job `{index_job_id}`: {progress}"
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
