#!/usr/bin/env python3
"""
Stock Market Analyzer - Web Application
Flask-based web interface for comprehensive stock market analysis
"""

from flask import Flask, render_template, request, jsonify
import json
from stock_market_analyzer import StockMarketAnalyzer
import traceback

app = Flask(__name__)
analyzer = StockMarketAnalyzer()

@app.route('/')
def index():
    """Home page with stock analysis form"""
    return render_template('index.html')

@app.route('/api/analyze/<symbol>')
def analyze_stock_api(symbol):
    """API endpoint for stock analysis"""
    try:
        analysis = analyzer.comprehensive_analysis(symbol.upper())
        if analysis:
            # Convert any pandas objects to serializable format
            if 'historical_data' in analysis['basic_data']:
                del analysis['basic_data']['historical_data']  # Remove non-serializable data
            return jsonify(analysis)
        else:
            return jsonify({'error': 'Could not analyze stock symbol'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/compare')
def compare_stocks_api():
    """API endpoint for comparing multiple stocks"""
    symbols = request.args.get('symbols', '').split(',')
    symbols = [s.strip().upper() for s in symbols if s.strip()]
    
    if not symbols:
        return jsonify({'error': 'No symbols provided'}), 400
    
    try:
        analyses = {}
        for symbol in symbols:
            analysis = analyzer.comprehensive_analysis(symbol)
            if analysis:
                # Remove non-serializable data
                if 'historical_data' in analysis['basic_data']:
                    del analysis['basic_data']['historical_data']
                analyses[symbol] = analysis
        
        return jsonify(analyses)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/market-overview')
def market_overview_api():
    """API endpoint for market overview"""
    try:
        indices = ['SPY', 'QQQ', 'DIA', 'IWM']
        overview = {}
        
        for index in indices:
            analysis = analyzer.comprehensive_analysis(index)
            if analysis:
                overview[index] = {
                    'symbol': index,
                    'price': analysis['basic_data']['current_price'],
                    'change': analysis['basic_data']['change'],
                    'change_percent': analysis['basic_data']['change_percent'],
                    'signal': analysis['trading_signals']['overall_signal']
                }
        
        return jsonify(overview)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/analyze')
def analyze_page():
    """Stock analysis page"""
    symbol = request.args.get('symbol', '')
    return render_template('analyze.html', symbol=symbol)

@app.route('/compare')
def compare_page():
    """Stock comparison page"""
    return render_template('compare.html')

@app.route('/market')
def market_page():
    """Market overview page"""
    return render_template('market.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)