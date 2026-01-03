"""
Price prediction service using CNN-LSTM model
"""
import numpy as np
import pandas as pd
from tensorflow import keras
import joblib

class StockPredictor:
    def __init__(self, model_path=None):
        self.model = None
        self.scaler = None
        self.sequence_length = 60
        
        if model_path:
            self.load_model(model_path)
    
    def load_model(self, model_path):
        """Load trained CNN-LSTM model"""
        try:
            self.model = keras.models.load_model(model_path)
            self.scaler = joblib.load(model_path.replace('.h5', '_scaler.pkl'))
        except Exception as e:
            raise Exception(f"Error loading model: {str(e)}")
    
    def prepare_data(self, df, feature_columns=['Close', 'Volume', 'High', 'Low']):
        """
        Prepare data for prediction
        
        Args:
            df: DataFrame with stock data
            feature_columns: Columns to use as features
        
        Returns:
            Scaled and sequenced data
        """
        # Extract features
        data = df[feature_columns].values
        
        # Scale data
        if self.scaler is None:
            from sklearn.preprocessing import MinMaxScaler
            self.scaler = MinMaxScaler()
            scaled_data = self.scaler.fit_transform(data)
        else:
            scaled_data = self.scaler.transform(data)
        
        # Create sequences
        sequences = []
        for i in range(self.sequence_length, len(scaled_data)):
            sequences.append(scaled_data[i-self.sequence_length:i])
        
        return np.array(sequences)
    
    def predict(self, data):
        """
        Make predictions using the CNN-LSTM model
        
        Args:
            data: Prepared input data
        
        Returns:
            Predictions
        """
        if self.model is None:
            raise Exception("Model not loaded. Call load_model() first.")
        
        predictions = self.model.predict(data)
        
        # Inverse transform predictions
        predictions = self.scaler.inverse_transform(predictions)
        
        return predictions
    
    def predict_next_days(self, df, days=5):
        """
        Predict stock prices for next N days
        
        Args:
            df: DataFrame with historical stock data
            days: Number of days to predict
        
        Returns:
            Array of predictions
        """
        predictions = []
        current_sequence = self.prepare_data(df)[-1:]
        
        for _ in range(days):
            pred = self.model.predict(current_sequence)
            predictions.append(pred[0])
            
            # Update sequence with prediction
            current_sequence = np.append(current_sequence[:, 1:, :], 
                                        pred.reshape(1, 1, -1), axis=1)
        
        return np.array(predictions)
