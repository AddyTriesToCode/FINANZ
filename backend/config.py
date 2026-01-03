"""
Configuration settings for the backend
"""
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    DEBUG = os.getenv('DEBUG', 'True') == 'True'
    
    # Database
    DATABASE_URI = os.getenv('DATABASE_URI', 'sqlite:///finanz.db')
    
    # API Keys
    YAHOO_FINANCE_API_KEY = os.getenv('YAHOO_FINANCE_API_KEY', '')
    
    # Model settings
    MODEL_PATH = os.getenv('MODEL_PATH', '../models/saved_models/')
    DATA_PATH = os.getenv('DATA_PATH', '../data/')
    
    # Trading settings
    INITIAL_CAPITAL = float(os.getenv('INITIAL_CAPITAL', '100000'))
    RISK_PER_TRADE = float(os.getenv('RISK_PER_TRADE', '0.02'))
