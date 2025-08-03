# Stock Market Analyzer 📈

A comprehensive Python-based tool for making informed cash market trading decisions. This program provides all essential information needed for stock analysis including technical indicators, fundamental analysis, risk metrics, and trading signals.

## Features 🚀

### 📊 Technical Analysis
- **Moving Averages**: SMA 20, 50, 200 and EMA 12, 26
- **Momentum Indicators**: RSI (14), MACD with signal line
- **Volatility Indicators**: Bollinger Bands
- **Support & Resistance**: Dynamic levels based on recent price action

### 💰 Fundamental Analysis
- **Valuation Ratios**: P/E, P/B, P/S, PEG ratios
- **Profitability Metrics**: ROE, ROA, Profit Margin, Operating Margin
- **Financial Health**: Debt-to-Equity, Current Ratio, Quick Ratio
- **Growth Metrics**: Revenue Growth, Earnings Growth
- **Dividend Information**: Yield and Payout Ratio

### ⚠️ Risk Analysis
- **Volatility**: Annualized price volatility
- **Sharpe Ratio**: Risk-adjusted returns
- **Beta**: Market correlation coefficient
- **Value at Risk (VaR)**: 95% confidence level
- **Maximum Drawdown**: Largest peak-to-trough decline

### 🎯 Trading Signals
- **Combined Analysis**: Technical + Fundamental scoring
- **Signal Generation**: BUY, SELL, HOLD recommendations
- **Detailed Reasoning**: Specific signals for each indicator
- **Market Sentiment**: News and analyst recommendations

### 🌐 Multiple Interfaces
1. **Command Line**: Interactive terminal interface
2. **Web Application**: Modern web interface with real-time data
3. **API**: RESTful endpoints for integration

## Installation 🔧

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Quick Setup

1. **Clone or Download** the files to your directory

2. **Install Dependencies**:
```bash
pip install -r requirements.txt
```

3. **Run the Program**:

   **Command Line Interface**:
   ```bash
   python stock_market_analyzer.py
   ```

   **Web Application**:
   ```bash
   python stock_web_app.py
   ```
   Then open http://localhost:5000 in your browser

## Usage Guide 📖

### Command Line Interface

The CLI provides 5 main options:

1. **Single Stock Analysis**: Enter any stock symbol (e.g., AAPL, GOOGL, TSLA)
2. **Compare Multiple Stocks**: Enter comma-separated symbols
3. **Portfolio Analysis**: (Coming soon)
4. **Market Overview**: Analysis of major indices (SPY, QQQ, DIA, IWM)
5. **Exit**: Close the program

### Web Interface

- **Home Page**: Quick analysis with search functionality
- **Deep Analysis**: Comprehensive stock evaluation
- **Compare Stocks**: Side-by-side comparison of multiple stocks
- **Market Overview**: Real-time market indices data

### API Endpoints

- `GET /api/analyze/<symbol>`: Get comprehensive analysis for a stock
- `GET /api/compare?symbols=AAPL,GOOGL,MSFT`: Compare multiple stocks
- `GET /api/market-overview`: Get major market indices data

## Sample Analysis Output 📋

```
============================================================
COMPREHENSIVE STOCK ANALYSIS: AAPL
Analysis Date: 2024-01-15 10:30:25
============================================================

📊 BASIC STOCK INFORMATION
Current Price: $185.50
Daily Change: $2.30 (1.26%)
Volume: 45,123,456 (Avg: 48,567,890)
Volume Ratio: 0.93x
Market Cap: $2.85T

📈 TECHNICAL ANALYSIS
SMA 20: $182.45
SMA 50: $178.20
RSI: 58.32
MACD: 0.0245
Support Level: $175.30
Resistance Level: $190.80

💰 FUNDAMENTAL ANALYSIS
P/E Ratio: 28.45
P/B Ratio: 15.20
Debt/Equity: 1.78
ROE: 147.25%
Profit Margin: 23.45%

⚠️ RISK ANALYSIS
Volatility: 28.5%
Sharpe Ratio: 1.45
Max Drawdown: -15.2%
Beta: 1.23

🎯 TRADING SIGNALS
Overall Signal: HOLD

Technical Signals:
  • RSI in neutral zone - no strong signal
  • Price above short-term moving averages - bullish trend

Fundamental Signals:
  • High P/E ratio - potentially overvalued
============================================================
```

## Key Metrics Explained 📚

### Technical Indicators
- **RSI < 30**: Oversold (potential buy)
- **RSI > 70**: Overbought (potential sell)
- **MACD > Signal**: Bullish momentum
- **Price > SMA**: Uptrend

### Fundamental Ratios
- **P/E Ratio**: Price-to-earnings (lower may indicate value)
- **ROE**: Return on equity (higher is better)
- **Debt/Equity**: Financial leverage (lower is safer)

### Risk Metrics
- **Volatility**: Price fluctuation (lower is less risky)
- **Beta > 1**: More volatile than market
- **Sharpe Ratio**: Risk-adjusted returns (higher is better)

## Data Sources 📡

- **Yahoo Finance**: Primary data source via yfinance library
- **Real-time Data**: Live market prices and volumes
- **Historical Data**: Up to 1 year of price history for calculations
- **Fundamental Data**: Company financials and ratios

## Trading Signal Logic 🧠

The program generates trading signals using a scoring system:

**Technical Score (+/-)**:
- RSI oversold/overbought conditions
- MACD crossover signals
- Moving average trends

**Fundamental Score (+/-)**:
- P/E ratio valuation
- Debt-to-equity health
- Profitability metrics

**Overall Signal**:
- **BUY**: Total score ≥ +2
- **SELL**: Total score ≤ -2
- **HOLD**: Score between -1 and +1

## Customization 🛠️

### Adding New Indicators
Modify the `technical_analysis()` method in `stock_market_analyzer.py`:

```python
# Add your custom indicator
hist_data['Custom_Indicator'] = your_calculation_here
```

### Adjusting Signal Logic
Update the `trading_signals()` method to modify scoring criteria.

### API Integration
The program supports additional API keys for enhanced data:
- Alpha Vantage (free tier available)
- Financial Modeling Prep (free tier available)

## Limitations & Disclaimers ⚠️

1. **Not Financial Advice**: This tool is for educational and analysis purposes only
2. **Data Delays**: Some data may have minor delays
3. **Market Risk**: All investments carry risk of loss
4. **Backtesting**: Past performance doesn't guarantee future results
5. **API Limits**: Free APIs have request limitations

## Troubleshooting 🔧

### Common Issues

**"Module not found" errors**:
```bash
pip install --upgrade -r requirements.txt
```

**Web app won't start**:
- Check if port 5000 is available
- Try: `python stock_web_app.py`

**No data for stock symbol**:
- Verify the symbol is correct
- Check if market is open
- Try a different symbol

**Slow performance**:
- Reduce the number of stocks being analyzed
- Check internet connection
- Consider using API keys for faster access

## Contributing 🤝

Feel free to contribute by:
1. Adding new technical indicators
2. Improving the web interface
3. Adding new data sources
4. Enhancing the analysis algorithms
5. Reporting bugs or suggesting features

## License 📜

This project is open source and available for educational and personal use.

## Support 💬

For questions or issues:
1. Check the troubleshooting section
2. Review the code comments for implementation details
3. Test with known stock symbols like AAPL, GOOGL, MSFT

---

**Happy Trading! 📈💰**

*Remember: This tool provides analysis and signals, but all trading decisions and their consequences are your responsibility. Always do your own research and consider consulting with financial professionals.*