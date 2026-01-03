"""
Model evaluation and testing script
"""
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from models.cnn_lstm_model import CNNLSTMModel
from backend.services.data_fetcher import DataFetcher
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

def evaluate_model(symbol='RELIANCE.NS', model_path='./saved_models/cnn_lstm_model.h5'):
    """
    Evaluate trained CNN-LSTM model
    
    Args:
        symbol: Stock symbol to evaluate
        model_path: Path to saved model
    """
    print(f"Evaluating model for {symbol}...")
    
    # Load model
    model = CNNLSTMModel(sequence_length=60, n_features=5)
    model.load_model(model_path)
    print("Model loaded successfully")
    
    # Fetch recent data
    data_fetcher = DataFetcher()
    stock_data = data_fetcher.fetch_stock_data(symbol, period='1y')
    df = pd.DataFrame(stock_data)
    
    # Prepare data
    X_train, y_train, X_test, y_test = model.prepare_data(df)
    
    # Make predictions
    predictions = model.predict(X_test)
    
    # Calculate metrics
    mae = mean_absolute_error(y_test, predictions)
    mse = mean_squared_error(y_test, predictions)
    rmse = np.sqrt(mse)
    r2 = r2_score(y_test, predictions)
    
    print("\n" + "="*50)
    print("Model Performance Metrics")
    print("="*50)
    print(f"Mean Absolute Error (MAE): {mae:.4f}")
    print(f"Mean Squared Error (MSE): {mse:.4f}")
    print(f"Root Mean Squared Error (RMSE): {rmse:.4f}")
    print(f"R² Score: {r2:.4f}")
    print("="*50)
    
    # Calculate directional accuracy
    actual_direction = np.diff(y_test.flatten()) > 0
    pred_direction = np.diff(predictions.flatten()) > 0
    directional_accuracy = np.mean(actual_direction == pred_direction) * 100
    print(f"Directional Accuracy: {directional_accuracy:.2f}%")
    
    # Plot results
    plt.figure(figsize=(15, 8))
    
    # Plot 1: Predictions vs Actual
    plt.subplot(2, 2, 1)
    plt.plot(y_test[:200], label='Actual', alpha=0.7)
    plt.plot(predictions[:200], label='Predicted', alpha=0.7)
    plt.title('Stock Price Predictions vs Actual')
    plt.xlabel('Time Step')
    plt.ylabel('Normalized Price')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    # Plot 2: Scatter plot
    plt.subplot(2, 2, 2)
    plt.scatter(y_test, predictions, alpha=0.5)
    plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'r--', lw=2)
    plt.title('Predicted vs Actual (Scatter)')
    plt.xlabel('Actual Price')
    plt.ylabel('Predicted Price')
    plt.grid(True, alpha=0.3)
    
    # Plot 3: Prediction errors
    plt.subplot(2, 2, 3)
    errors = predictions.flatten() - y_test.flatten()
    plt.hist(errors, bins=50, edgecolor='black')
    plt.title('Prediction Error Distribution')
    plt.xlabel('Prediction Error')
    plt.ylabel('Frequency')
    plt.grid(True, alpha=0.3)
    
    # Plot 4: Cumulative error
    plt.subplot(2, 2, 4)
    cumulative_error = np.cumsum(np.abs(errors))
    plt.plot(cumulative_error)
    plt.title('Cumulative Absolute Error')
    plt.xlabel('Time Step')
    plt.ylabel('Cumulative Error')
    plt.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('../data/evaluation_results.png', dpi=300)
    print("\nEvaluation results saved to data/evaluation_results.png")
    
    return {
        'mae': mae,
        'mse': mse,
        'rmse': rmse,
        'r2': r2,
        'directional_accuracy': directional_accuracy
    }

if __name__ == '__main__':
    symbol = 'RELIANCE.NS'
    results = evaluate_model(symbol)
