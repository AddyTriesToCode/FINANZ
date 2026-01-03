"""
Backtesting API routes
"""
from flask import Blueprint, jsonify, request
from services.backtester import Backtester

backtest_bp = Blueprint('backtest', __name__, url_prefix='/api/backtest')

@backtest_bp.route('/run', methods=['POST'])
def run_backtest():
    """Run backtesting on a strategy"""
    try:
        data = request.get_json()
        symbol = data.get('symbol')
        strategy = data.get('strategy')
        start_date = data.get('start_date')
        end_date = data.get('end_date')
        
        backtester = Backtester(symbol, start_date, end_date)
        results = backtester.run_strategy(strategy)
        
        return jsonify({'success': True, 'results': results})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400
