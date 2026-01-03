"""
Stock data API routes
"""
from flask import Blueprint, jsonify, request
from services.data_fetcher import DataFetcher

stock_bp = Blueprint('stock', __name__, url_prefix='/api/stock')
data_fetcher = DataFetcher()

@stock_bp.route('/price/<symbol>', methods=['GET'])
def get_stock_price(symbol):
    """Get current stock price"""
    try:
        period = request.args.get('period', '1d')
        data = data_fetcher.fetch_stock_data(symbol, period)
        return jsonify({'success': True, 'data': data})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@stock_bp.route('/predict/<symbol>', methods=['POST'])
def predict_price(symbol):
    """Predict stock price using CNN-LSTM model"""
    try:
        # Implementation will use the trained model
        return jsonify({'success': True, 'prediction': []})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400
