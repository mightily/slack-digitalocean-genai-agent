# Slack AI Chatbot with DigitalOcean GenAI

This Slack chatbot app template provides a customizable solution for integrating AI-powered conversations into your Slack workspace using DigitalOcean's GenAI Platform. Deploy the app on DigitalOcean App Platform for a fully managed experience.

## Features

* **Interact with the bot** by mentioning it in conversations and threads
* **Send direct messages** to the bot for private interactions
* Use the **`/ask-sailor`** command to communicate with the bot in channels where it hasn't been added
* Use the **`/sailor-summary`** command to have Sailor summarize a Slack thread and DM you an AI generated summary
* **Utilize a custom function** for integration with Workflow Builder to summarize messages
* **Select your preferred AI model** from the app home to customize responses
* **Seamless integration** with DigitalOcean GenAI Platform
* **Choice of state storage (optional)**:
  * **File-based state store** creates a file in /data per user to store preferences
  * **Redis state store** for distributed deployments (recommended for App Platform)

## Installation

#### Prerequisites
* A Slack workspace where you have permissions to install apps
* Access to the [DigitalOcean GenAI Platform](https://docs.digitalocean.com/products/genai-platform/)

#### Create a Slack App
1. Open [https://api.slack.com/apps/new](https://api.slack.com/apps/new) and choose "From an app manifest"
2. Choose the workspace you want to install the application to
3. Copy the contents of [manifest.json](./manifest.json) into the text box that says `*Paste your manifest code here*` (within the JSON tab) and click *Next*
4. Review the configuration and click *Create*
5. Click *Install to Workspace* and *Allow* on the screen that follows. You'll be redirected to the App Configuration dashboard.

#### Environment Variables
Before running the app, store these environment variables:

1. From your app's configuration page, go to **OAuth & Permissions** and copy the Bot User OAuth Token (`SLACK_BOT_TOKEN`)
2. From **Basic Information**, create an app-level token with the `connections:write` scope (`SLACK_APP_TOKEN`)
3. Get your DigitalOcean GenAI API key from the DigitalOcean dashboard (`GENAI_API_KEY`)
4. Set your GenAI API URL, append `/api/v1` (`GENAI_API_URL`)

```zsh
# Set environment variables
export SLACK_BOT_TOKEN=<your-bot-token>
export SLACK_APP_TOKEN=<your-app-token>
export GENAI_API_KEY=<your-genai-api-key>
export GENAI_API_URL=<your-genai-api-url>  # https://agent-<id>.ondigitalocean.app/api/v1
```

### Local Development

```zsh
# Clone this project
git clone https://github.com/DO-Solutions/slack-digitalocean-genai-agent

# Navigate to the project directory
cd bolt-python-ai-chatbot

# Setup python virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Start your local server
python3 app.py
```

### Deploy to DigitalOcean App Platform

This application can be easily deployed to DigitalOcean App Platform:

1. Fork or clone this repository to your GitHub account
2. In the DigitalOcean control panel, go to App Platform and create a new app
3. Connect your GitHub repository
4. Configure the environment variables (`SLACK_BOT_TOKEN`, `SLACK_APP_TOKEN`, `GENAI_API_KEY`, `GENAI_API_URL`)
5. Optionally add a Redis database component for state storage
6. Deploy the application

## Project Structure

### `/ai` - AI Integration

The `/ai` directory contains the core AI functionality:

* `ai_constants.py`: Defines constants used throughout the AI module
* `/providers/__init__.py`: Contains utility functions for handling API responses and available providers

The GenAI provider enables communication with DigitalOcean's GenAI Platform through an OpenAI-compatible API.

### `/state_store` - User Data Storage

For App Platform deployments, we recommend using the Redis state storage option:

```zsh
# Set Redis connection string
export REDIS_URL=<your-redis-connection-string>
```

Example with DigitalOcean Managed Redis:
```
export REDIS_URL=rediss://default:password@hostname.db.ondigitalocean.com:25061
```

## Alternative AI Providers

While DigitalOcean GenAI is the primary focus, this template also supports other AI providers:

### OpenAI

To use OpenAI models, add your API key:
```zsh
export OPENAI_API_KEY=<your-api-key>
```

### Anthropic

For Anthropic models, configure your API key:
```zsh
export ANTHROPIC_API_KEY=<your-api-key>
```

## Bring Your Own Language Model

You can create a custom provider by extending the base class in `ai/providers/base_api.py` and updating `ai/providers/__init__.py` to include your implementation.