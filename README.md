# WhatsApp ChatBot with Perplexity AI and Flask

A WhatsApp ChatBot powered by Perplexity AI's LLM, built with Python and Flask, and integrated with Twilio's WhatsApp API.

## Features

- 🤖 AI-powered responses using Perplexity AI's LLM
- 💬 WhatsApp message handling via Twilio
- 🔄 Conversation history management
- ✅ Health check endpoint
- 🔒 Secure configuration using environment variables

## Prerequisites

- Python 3.8 or higher
- Twilio Account with WhatsApp Sandbox access
- Perplexity AI API Key
- ngrok (for local testing)

## Setup Instructions

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd chatbotwhatsapp
   ```

2. **Create and activate a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   - Copy `.env.example` to `.env`
   - Update the `.env` file with your actual API keys and configuration:
     - `PERPLEXITY_API_KEY`: Your Perplexity AI API key
     - `TWILIO_ACCOUNT_SID`: Your Twilio Account SID
     - `TWILIO_AUTH_TOKEN`: Your Twilio Auth Token
     - `TWILIO_PHONE_NUMBER`: Your Twilio WhatsApp number (format: +1234567890)
     - `SERVER_URL`: Your server's public URL (ngrok URL for testing)

5. **Run the application**
   ```bash
   python app.py
   ```

6. **Expose your local server** (for testing)
   - Install ngrok if you haven't already: https://ngrok.com/download
   - In a new terminal, run:
     ```bash
     ngrok http 5000
     ```
   - Copy the HTTPS URL provided by ngrok (it will look like `https://abc123.ngrok.io`)

7. **Configure Twilio Webhook**
   - Go to Twilio Console → Messaging → Settings → WhatsApp Sandbox Settings
   - Set the webhook URL to `YOUR_NGROK_URL/webhook`
   - Select "HTTP POST" as the request type
   - Save the configuration

8. **Test your bot**
   - Send a message to your Twilio WhatsApp Sandbox number
   - You should receive an AI-generated response

## Environment Variables

- `PERPLEXITY_API_KEY`: Your Perplexity AI API key
- `TWILIO_ACCOUNT_SID`: Your Twilio Account SID
- `TWILIO_AUTH_TOKEN`: Your Twilio Auth Token
- `TWILIO_PHONE_NUMBER`: Your Twilio WhatsApp number (format: +1234567890)
- `SERVER_URL`: Your server's public URL (ngrok URL for testing)

## Project Structure

- `app.py`: Main Flask application with webhook and AI integration
- `requirements.txt`: Python dependencies
- `.env`: Environment variables (not committed to version control)
- `README.md`: This file

## Deployment

For production deployment, consider using:
- Heroku
- AWS Elastic Beanstalk
- Google Cloud Run
- PythonAnywhere

Make sure to set the appropriate environment variables in your hosting platform.

## License

MIT
