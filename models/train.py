"""
Training script for CNN-LSTM model
"""
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from models.cnn_lstm_model import CNNLSTMModel
from backend.services.data_fetcher import DataFetcher
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

def train_model(symbol='RELIANCE.NS', period='5y'):
    """
    Train CNN-LSTM model for stock prediction
    
    Args:
        symbol: Stock symbol to train on
        period: Historical data period
    """
    print(f"Training CNN-LSTM model for {symbol}...")
    
    # Fetch data
    print("Fetching historical data...")
    data_fetcher = DataFetcher()
    stock_data = data_fetcher.fetch_stock_data(symbol, period=period)
    df = pd.DataFrame(stock_data)
    
    print(f"Data shape: {df.shape}")
    
    # Initialize model
    model = CNNLSTMModel(sequence_length=60, n_features=5)
    
    # Prepare data
    print("Preparing data...")
    X_train, y_train, X_test, y_test = model.prepare_data(df)
    
    print(f"Training data shape: {X_train.shape}")
    print(f"Test data shape: {X_test.shape}")
    
    # Build and train model
    print("Building model...")
    model.build_model()
    print(model.model.summary())
    
    print("Training model...")
    history = model.train(X_train, y_train, X_test, y_test, epochs=50, batch_size=32)
    
    # Evaluate model
    print("\nEvaluating model...")
    test_loss, test_mae, test_mse = model.model.evaluate(X_test, y_test)
    print(f"Test Loss: {test_loss:.4f}")
    print(f"Test MAE: {test_mae:.4f}")
    print(f"Test MSE: {test_mse:.4f}")
    
    # Make predictions
    predictions = model.predict(X_test)
    
    # Calculate metrics
    rmse = np.sqrt(test_mse)
    print(f"RMSE: {rmse:.4f}")
    
    # Plot training history
    plt.figure(figsize=(12, 4))
    
    plt.subplot(1, 2, 1)
    plt.plot(history.history['loss'], label='Training Loss')
    plt.plot(history.history['val_loss'], label='Validation Loss')
    plt.title('Model Loss')
    plt.xlabel('Epoch')
    plt.ylabel('Loss')
    plt.legend()
    
    plt.subplot(1, 2, 2)
    plt.plot(y_test[:100], label='Actual')
    plt.plot(predictions[:100], label='Predicted')
    plt.title('Predictions vs Actual')
    plt.xlabel('Time Step')
    plt.ylabel('Normalized Price')
    plt.legend()
    
    plt.tight_layout()
    plt.savefig('../data/training_results.png')
    print("Training results saved to data/training_results.png")
    
    # Save model
    model_path = './saved_models/cnn_lstm_model.h5'
    os.makedirs('./saved_models', exist_ok=True)
    model.save_model(model_path)
    print(f"Model saved to {model_path}")
    
    return model, history

if __name__ == '__main__':
    # Train model for multiple NSE stocks
    stocks = ['RELIANCE.NS', 'TCS.NS', 'INFY.NS', 'HDFCBANK.NS']
    
    for stock in stocks:
        print(f"\n{'='*50}")
        print(f"Training model for {stock}")
        print(f"{'='*50}\n")
        
        try:
            model, history = train_model(stock, period='5y')
        except Exception as e:
            print(f"Error training {stock}: {str(e)}")
            continue
