"""
CNN-LSTM model for stock price prediction
"""
import numpy as np
import pandas as pd
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, LSTM, Dropout, Conv1D, MaxPooling1D, Flatten
from tensorflow.keras.optimizers import Adam
from sklearn.preprocessing import MinMaxScaler
import joblib

class CNNLSTMModel:
    def __init__(self, sequence_length=60, n_features=5):
        """
        Initialize CNN-LSTM model
        
        Args:
            sequence_length: Number of time steps to look back
            n_features: Number of features (OHLCV + indicators)
        """
        self.sequence_length = sequence_length
        self.n_features = n_features
        self.model = None
        self.scaler = MinMaxScaler()
        
    def build_model(self):
        """Build CNN-LSTM architecture"""
        model = Sequential()
        
        # CNN layers for feature extraction
        model.add(Conv1D(filters=64, kernel_size=3, activation='relu', 
                        input_shape=(self.sequence_length, self.n_features)))
        model.add(MaxPooling1D(pool_size=2))
        model.add(Dropout(0.2))
        
        model.add(Conv1D(filters=128, kernel_size=3, activation='relu'))
        model.add(MaxPooling1D(pool_size=2))
        model.add(Dropout(0.2))
        
        # LSTM layers for sequence learning
        model.add(LSTM(units=128, return_sequences=True))
        model.add(Dropout(0.3))
        
        model.add(LSTM(units=128, return_sequences=False))
        model.add(Dropout(0.3))
        
        # Dense layers for prediction
        model.add(Dense(units=64, activation='relu'))
        model.add(Dropout(0.2))
        model.add(Dense(units=32, activation='relu'))
        model.add(Dense(units=1))
        
        # Compile model
        model.compile(optimizer=Adam(learning_rate=0.001), 
                     loss='mean_squared_error',
                     metrics=['mae', 'mse'])
        
        self.model = model
        return model
    
    def prepare_data(self, df, target_col='Close'):
        """
        Prepare data for training
        
        Args:
            df: DataFrame with OHLCV data
            target_col: Column to predict
        
        Returns:
            X_train, y_train, X_test, y_test
        """
        # Add technical indicators
        df = self.add_technical_indicators(df)
        
        # Select features
        feature_cols = ['Open', 'High', 'Low', 'Close', 'Volume']
        data = df[feature_cols].values
        
        # Scale data
        scaled_data = self.scaler.fit_transform(data)
        
        # Create sequences
        X, y = [], []
        for i in range(self.sequence_length, len(scaled_data)):
            X.append(scaled_data[i-self.sequence_length:i])
            y.append(scaled_data[i, 3])  # Close price index
        
        X, y = np.array(X), np.array(y)
        
        # Split into train and test
        split_idx = int(len(X) * 0.8)
        X_train, X_test = X[:split_idx], X[split_idx:]
        y_train, y_test = y[:split_idx], y[split_idx:]
        
        return X_train, y_train, X_test, y_test
    
    def add_technical_indicators(self, df):
        """Add technical indicators to dataframe"""
        # Simple Moving Averages
        df['SMA_20'] = df['Close'].rolling(window=20).mean()
        df['SMA_50'] = df['Close'].rolling(window=50).mean()
        
        # Exponential Moving Average
        df['EMA_20'] = df['Close'].ewm(span=20, adjust=False).mean()
        
        # Relative Strength Index (RSI)
        delta = df['Close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / loss
        df['RSI'] = 100 - (100 / (1 + rs))
        
        # Fill NaN values
        df = df.bfill().fillna(0)
        
        return df
    
    def train(self, X_train, y_train, X_val, y_val, epochs=100, batch_size=32):
        """
        Train the model
        
        Args:
            X_train, y_train: Training data
            X_val, y_val: Validation data
            epochs: Number of training epochs
            batch_size: Batch size for training
        
        Returns:
            Training history
        """
        if self.model is None:
            self.build_model()
        
        history = self.model.fit(
            X_train, y_train,
            validation_data=(X_val, y_val),
            epochs=epochs,
            batch_size=batch_size,
            verbose=1
        )
        
        return history
    
    def predict(self, X):
        """Make predictions"""
        if self.model is None:
            raise Exception("Model not trained. Call train() first.")
        
        predictions = self.model.predict(X)
        return predictions
    
    def save_model(self, filepath):
        """Save model and scaler"""
        self.model.save(filepath)
        joblib.dump(self.scaler, filepath.replace('.h5', '_scaler.pkl'))
    
    def load_model(self, filepath):
        """Load model and scaler"""
        from tensorflow.keras.models import load_model
        self.model = load_model(filepath)
        self.scaler = joblib.load(filepath.replace('.h5', '_scaler.pkl'))
