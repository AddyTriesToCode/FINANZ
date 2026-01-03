# Saved Models Directory

This directory stores trained CNN-LSTM models for stock price prediction.

## Model Files

- `cnn_lstm_model.h5` - Main CNN-LSTM model
- `cnn_lstm_model_scaler.pkl` - Data scaler for preprocessing

## Model Architecture

### CNN Layers (Feature Extraction)
- Conv1D: 64 filters, kernel_size=3
- MaxPooling1D: pool_size=2
- Dropout: 0.2
- Conv1D: 128 filters, kernel_size=3
- MaxPooling1D: pool_size=2
- Dropout: 0.2

### LSTM Layers (Sequence Learning)
- LSTM: 128 units, return_sequences=True
- Dropout: 0.3
- LSTM: 128 units
- Dropout: 0.3

### Dense Layers (Prediction)
- Dense: 64 units, ReLU
- Dropout: 0.2
- Dense: 32 units, ReLU
- Dense: 1 unit (output)

## Training Details

- **Input Features**: OHLCV (Open, High, Low, Close, Volume)
- **Sequence Length**: 60 days
- **Optimizer**: Adam (lr=0.001)
- **Loss Function**: Mean Squared Error
- **Metrics**: MAE, MSE
- **Training Data**: 5 years NSE/BSE historical data

## Performance Targets

- RMSE: < 0.025
- MAE: < 0.020
- R² Score: > 0.95
- Directional Accuracy: > 85%
