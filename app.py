from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import os

from api.routes import api_bp
from storage.memory_store import ConversationStore

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key')
CORS(app)

# Register blueprints
app.register_blueprint(api_bp, url_prefix='/api')

# Initialize storage
conversation_store = ConversationStore()

@app.route('/')
def index():
    """Main dashboard"""
    return render_template('dashboard.html')

@app.route('/conversation/<conv_id>')
def conversation_view(conv_id):
    """View specific conversation"""
    return render_template('conversation.html', conv_id=conv_id)

@app.route('/analytics')
def analytics():
    """Analytics dashboard"""
    return render_template('analytics.html')

if __name__ == '__main__':
    app.run(
        debug=os.getenv('FLASK_DEBUG', 'True') == 'True',
        host='0.0.0.0',
        port=5000
    )