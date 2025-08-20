from flask import Flask, request, jsonify, Response
from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client
import os
import requests
from dotenv import load_dotenv
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()
logger.debug(f"PERPLEXITY_API_KEY: {'*' * 8}{os.getenv('PERPLEXITY_API_KEY')[-4:] if os.getenv('PERPLEXITY_API_KEY') else 'Not found'}")

app = Flask(__name__)

# Initialize Twilio client
twilio_client = Client(os.getenv('TWILIO_ACCOUNT_SID'), os.getenv('TWILIO_AUTH_TOKEN'))

# Store conversation history (in production, use a database)
conversation_history = {}

def get_ai_response(message, sender_id):
    """Get response from Perplexity AI"""
    try:
        logger.debug(f"Getting AI response for message: {message}")
        # Initialize conversation history if it doesn't exist
        if sender_id not in conversation_history:
            conversation_history[sender_id] = [
                {"role": "system", "content": "You are a helpful WhatsApp assistant."}
            ]
        
        # Add user message to history
        conversation_history[sender_id].append({"role": "user", "content": message})
        
        # Prepare messages for Perplexity API
        messages = conversation_history[sender_id]
        
        # Call Perplexity API
        url = "https://api.perplexity.ai/chat/completions"
        headers = {
            "Authorization": f"Bearer {os.getenv('PERPLEXITY_API_KEY')}",
            "Content-Type": "application/json",
            "accept": "application/json"
        }
        
        data = {
            "model": "sonar",
            "messages": [
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": message}
            ],
            "max_tokens": 500,
            "temperature": 0.7
        }
        
        logger.debug(f"Sending request to Perplexity API: {data}")
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        result = response.json()
        logger.debug(f"Received response from Perplexity API: {result}")
        
        # Get the assistant's reply
        assistant_reply = result['choices'][0]['message']['content']
        
        # Add assistant's reply to history
        conversation_history[sender_id].append({"role": "assistant", "content": assistant_reply})
        
        # Keep conversation history manageable (last 10 messages)
        if len(conversation_history[sender_id]) > 10:
            conversation_history[sender_id] = conversation_history[sender_id][-10:]
        
        return assistant_reply
    except Exception as e:
        logger.error(f"Error in get_ai_response: {str(e)}", exc_info=True)
        return f"I'm sorry, I encountered an error processing your request. Error: {str(e)}"

@app.route("/webhook", methods=['GET', 'POST'])
def webhook():
    """Webhook to handle incoming WhatsApp messages"""
    if request.method == 'GET':
        # Handle verification request
        return jsonify({"status": "ok"}), 200
        
    try:
        logger.debug(f"Received webhook request: {request.form}")
        # Get the incoming message
        incoming_msg = request.values.get('Body', '').strip()
        sender = request.values.get('From', '')
        
        if not incoming_msg:
            logger.warning("Empty message received")
            return jsonify({"status": "error", "message": "Empty message"}), 400
            
        logger.debug(f"Processing message from {sender}: {incoming_msg}")
        # Get response from AI
        response = get_ai_response(incoming_msg, sender)
        
        # Create TwiML response
        resp = MessagingResponse()
        resp.message(str(response))
        
        logger.debug(f"Sending response: {str(resp)}")
        #return str(resp)
        return Response(str(resp), mimetype="application/xml")
    except Exception as e:
        logger.error(f"Error in webhook: {str(e)}", exc_info=True)
        resp = MessagingResponse()
        resp.message(f"I'm sorry, I encountered an error: {str(e)}")
        return str(resp)

@app.route('/')
def home():
    print("WhatsApp Bot is running! Use the /webhook endpoint for Twilio integration.")
    return "WhatsApp Bot is running! Use the /webhook endpoint for Twilio integration."

@app.route("/health")
def health_check():
    """Health check endpoint"""
    print("Health check")
    return jsonify({"status": "ok"}), 200

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))  # Use Railway's PORT or default 8000
    app.run(host="0.0.0.0", port=port, debug=True)
