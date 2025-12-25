"""
Main Flask application for FINANZ Stock Trading Bot
"""
from api.stock_routes import stock_bp
from api.backtest_routes import backtest_bp
from flask import Flask, jsonify
from flask_cors import CORS
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
CORS(app)
app.register_blueprint(stock_bp)
app.register_blueprint(backtest_bp)
@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy', 'message': 'FINANZ API is running'})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
