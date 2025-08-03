#!/usr/bin/env python3
"""
Stock Market Analyzer - Comprehensive Tool for Cash Market Decisions
This program provides all essential information needed for stock market trading decisions.
"""

import yfinance as yf
import pandas as pd
import numpy as np
import requests
import json
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import seaborn as sns
from typing import Dict, List, Tuple, Optional
import warnings
warnings.filterwarnings('ignore')

class StockMarketAnalyzer:
    def __init__(self):
        self.api_keys = {
            'alpha_vantage': 'YOUR_ALPHA_VANTAGE_KEY',  # Free at https://www.alphavantage.co/
            'fmp': 'YOUR_FMP_KEY'  # Free at https://financialmodelingprep.com/
        }
        
    def get_stock_data(self, symbol: str, period: str = "1y") -> Dict:
        """
        Get comprehensive stock data including price, volume, and basic metrics
        """
        try:
            stock = yf.Ticker(symbol)
            
            # Get historical data
            hist = stock.history(period=period)
            
            # Get stock info
            info = stock.info
            
            # Calculate basic metrics
            current_price = hist['Close'].iloc[-1]
            prev_close = hist['Close'].iloc[-2] if len(hist) > 1 else current_price
            change = current_price - prev_close
            change_percent = (change / prev_close) * 100
            
            # Volume analysis
            avg_volume = hist['Volume'].mean()
            current_volume = hist['Volume'].iloc[-1]
            volume_ratio = current_volume / avg_volume
            
            return {
                'symbol': symbol,
                'current_price': round(current_price, 2),
                'change': round(change, 2),
                'change_percent': round(change_percent, 2),
                'volume': int(current_volume),
                'avg_volume': int(avg_volume),
                'volume_ratio': round(volume_ratio, 2),
                'market_cap': info.get('marketCap', 'N/A'),
                'pe_ratio': info.get('trailingPE', 'N/A'),
                'dividend_yield': info.get('dividendYield', 'N/A'),
                'beta': info.get('beta', 'N/A'),
                'historical_data': hist
            }
        except Exception as e:
            print(f"Error fetching data for {symbol}: {str(e)}")
            return None

    def technical_analysis(self, hist_data: pd.DataFrame) -> Dict:
        """
        Calculate technical indicators for trading decisions
        """
        try:
            # Moving Averages
            hist_data['SMA_20'] = hist_data['Close'].rolling(window=20).mean()
            hist_data['SMA_50'] = hist_data['Close'].rolling(window=50).mean()
            hist_data['SMA_200'] = hist_data['Close'].rolling(window=200).mean()
            hist_data['EMA_12'] = hist_data['Close'].ewm(span=12).mean()
            hist_data['EMA_26'] = hist_data['Close'].ewm(span=26).mean()
            
            # MACD
            hist_data['MACD'] = hist_data['EMA_12'] - hist_data['EMA_26']
            hist_data['MACD_Signal'] = hist_data['MACD'].ewm(span=9).mean()
            
            # RSI
            delta = hist_data['Close'].diff()
            gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
            rs = gain / loss
            hist_data['RSI'] = 100 - (100 / (1 + rs))
            
            # Bollinger Bands
            hist_data['BB_Middle'] = hist_data['Close'].rolling(window=20).mean()
            bb_std = hist_data['Close'].rolling(window=20).std()
            hist_data['BB_Upper'] = hist_data['BB_Middle'] + (bb_std * 2)
            hist_data['BB_Lower'] = hist_data['BB_Middle'] - (bb_std * 2)
            
            # Support and Resistance levels
            recent_high = hist_data['High'].tail(50).max()
            recent_low = hist_data['Low'].tail(50).min()
            
            current_price = hist_data['Close'].iloc[-1]
            latest_indicators = {
                'current_price': round(current_price, 2),
                'sma_20': round(hist_data['SMA_20'].iloc[-1], 2) if not pd.isna(hist_data['SMA_20'].iloc[-1]) else None,
                'sma_50': round(hist_data['SMA_50'].iloc[-1], 2) if not pd.isna(hist_data['SMA_50'].iloc[-1]) else None,
                'sma_200': round(hist_data['SMA_200'].iloc[-1], 2) if not pd.isna(hist_data['SMA_200'].iloc[-1]) else None,
                'rsi': round(hist_data['RSI'].iloc[-1], 2) if not pd.isna(hist_data['RSI'].iloc[-1]) else None,
                'macd': round(hist_data['MACD'].iloc[-1], 4) if not pd.isna(hist_data['MACD'].iloc[-1]) else None,
                'macd_signal': round(hist_data['MACD_Signal'].iloc[-1], 4) if not pd.isna(hist_data['MACD_Signal'].iloc[-1]) else None,
                'bb_upper': round(hist_data['BB_Upper'].iloc[-1], 2) if not pd.isna(hist_data['BB_Upper'].iloc[-1]) else None,
                'bb_lower': round(hist_data['BB_Lower'].iloc[-1], 2) if not pd.isna(hist_data['BB_Lower'].iloc[-1]) else None,
                'resistance': round(recent_high, 2),
                'support': round(recent_low, 2)
            }
            
            return latest_indicators
            
        except Exception as e:
            print(f"Error in technical analysis: {str(e)}")
            return {}

    def fundamental_analysis(self, symbol: str) -> Dict:
        """
        Get fundamental analysis data
        """
        try:
            stock = yf.Ticker(symbol)
            info = stock.info
            
            # Financial ratios and metrics
            fundamentals = {
                'pe_ratio': info.get('trailingPE'),
                'forward_pe': info.get('forwardPE'),
                'peg_ratio': info.get('pegRatio'),
                'price_to_book': info.get('priceToBook'),
                'price_to_sales': info.get('priceToSalesTrailing12Months'),
                'debt_to_equity': info.get('debtToEquity'),
                'return_on_equity': info.get('returnOnEquity'),
                'return_on_assets': info.get('returnOnAssets'),
                'profit_margin': info.get('profitMargins'),
                'operating_margin': info.get('operatingMargins'),
                'revenue_growth': info.get('revenueGrowth'),
                'earnings_growth': info.get('earningsGrowth'),
                'current_ratio': info.get('currentRatio'),
                'quick_ratio': info.get('quickRatio'),
                'dividend_yield': info.get('dividendYield'),
                'payout_ratio': info.get('payoutRatio')
            }
            
            # Clean up None values and convert to percentages where appropriate
            for key, value in fundamentals.items():
                if value is not None:
                    if key in ['return_on_equity', 'return_on_assets', 'profit_margin', 'operating_margin', 
                              'revenue_growth', 'earnings_growth', 'dividend_yield', 'payout_ratio']:
                        fundamentals[key] = round(value * 100, 2) if value != 'N/A' else None
                    else:
                        fundamentals[key] = round(value, 2) if isinstance(value, (int, float)) else value
            
            return fundamentals
            
        except Exception as e:
            print(f"Error in fundamental analysis for {symbol}: {str(e)}")
            return {}

    def market_sentiment(self, symbol: str) -> Dict:
        """
        Analyze market sentiment and news
        """
        try:
            stock = yf.Ticker(symbol)
            
            # Get recent news
            news = stock.news[:5] if hasattr(stock, 'news') and stock.news else []
            
            # Analyst recommendations
            recommendations = stock.recommendations
            latest_rec = None
            if recommendations is not None and not recommendations.empty:
                latest_rec = recommendations.tail(1).iloc[0].to_dict()
            
            # Institutional ownership
            institutional_holders = stock.institutional_holders
            major_holders = stock.major_holders
            
            sentiment_data = {
                'recent_news': [{'title': item.get('title', ''), 'link': item.get('link', '')} for item in news],
                'analyst_recommendation': latest_rec,
                'institutional_ownership': institutional_holders.to_dict('records') if institutional_holders is not None else [],
                'major_holders': major_holders.to_dict('records') if major_holders is not None else []
            }
            
            return sentiment_data
            
        except Exception as e:
            print(f"Error getting market sentiment for {symbol}: {str(e)}")
            return {}

    def risk_analysis(self, hist_data: pd.DataFrame, symbol: str) -> Dict:
        """
        Calculate risk metrics
        """
        try:
            # Calculate returns
            returns = hist_data['Close'].pct_change().dropna()
            
            # Risk metrics
            volatility = returns.std() * np.sqrt(252)  # Annualized volatility
            sharpe_ratio = (returns.mean() * 252) / (returns.std() * np.sqrt(252))
            
            # Value at Risk (95% confidence)
            var_95 = np.percentile(returns, 5)
            
            # Maximum drawdown
            cumulative = (1 + returns).cumprod()
            rolling_max = cumulative.expanding().max()
            drawdown = (cumulative - rolling_max) / rolling_max
            max_drawdown = drawdown.min()
            
            # Beta calculation (vs SPY)
            try:
                spy = yf.Ticker("SPY")
                spy_hist = spy.history(period="1y")
                spy_returns = spy_hist['Close'].pct_change().dropna()
                
                # Align dates
                common_dates = returns.index.intersection(spy_returns.index)
                stock_aligned = returns.loc[common_dates]
                spy_aligned = spy_returns.loc[common_dates]
                
                beta = np.cov(stock_aligned, spy_aligned)[0][1] / np.var(spy_aligned)
            except:
                beta = None
            
            risk_metrics = {
                'volatility': round(volatility * 100, 2),
                'sharpe_ratio': round(sharpe_ratio, 2),
                'var_95': round(var_95 * 100, 2),
                'max_drawdown': round(max_drawdown * 100, 2),
                'beta': round(beta, 2) if beta else None
            }
            
            return risk_metrics
            
        except Exception as e:
            print(f"Error in risk analysis: {str(e)}")
            return {}

    def trading_signals(self, technical_data: Dict, fundamentals: Dict) -> Dict:
        """
        Generate trading signals based on technical and fundamental analysis
        """
        signals = {
            'overall_signal': 'NEUTRAL',
            'technical_signals': [],
            'fundamental_signals': [],
            'risk_signals': []
        }
        
        technical_score = 0
        fundamental_score = 0
        
        # Technical signals
        if technical_data.get('rsi'):
            if technical_data['rsi'] < 30:
                signals['technical_signals'].append("RSI oversold - potential buy signal")
                technical_score += 1
            elif technical_data['rsi'] > 70:
                signals['technical_signals'].append("RSI overbought - potential sell signal")
                technical_score -= 1
                
        if technical_data.get('macd') and technical_data.get('macd_signal'):
            if technical_data['macd'] > technical_data['macd_signal']:
                signals['technical_signals'].append("MACD bullish crossover")
                technical_score += 1
            else:
                signals['technical_signals'].append("MACD bearish crossover")
                technical_score -= 1
                
        # Moving average signals
        if all(technical_data.get(key) for key in ['current_price', 'sma_20', 'sma_50']):
            if technical_data['current_price'] > technical_data['sma_20'] > technical_data['sma_50']:
                signals['technical_signals'].append("Price above short-term moving averages - bullish trend")
                technical_score += 1
            elif technical_data['current_price'] < technical_data['sma_20'] < technical_data['sma_50']:
                signals['technical_signals'].append("Price below short-term moving averages - bearish trend")
                technical_score -= 1
                
        # Fundamental signals
        if fundamentals.get('pe_ratio'):
            if fundamentals['pe_ratio'] < 15:
                signals['fundamental_signals'].append("Low P/E ratio - potentially undervalued")
                fundamental_score += 1
            elif fundamentals['pe_ratio'] > 25:
                signals['fundamental_signals'].append("High P/E ratio - potentially overvalued")
                fundamental_score -= 1
                
        if fundamentals.get('debt_to_equity'):
            if fundamentals['debt_to_equity'] < 0.3:
                signals['fundamental_signals'].append("Low debt-to-equity - strong balance sheet")
                fundamental_score += 1
            elif fundamentals['debt_to_equity'] > 1.0:
                signals['fundamental_signals'].append("High debt-to-equity - potential risk")
                fundamental_score -= 1
        
        # Overall signal
        total_score = technical_score + fundamental_score
        if total_score >= 2:
            signals['overall_signal'] = 'BUY'
        elif total_score <= -2:
            signals['overall_signal'] = 'SELL'
        else:
            signals['overall_signal'] = 'HOLD'
            
        return signals

    def comprehensive_analysis(self, symbol: str) -> Dict:
        """
        Perform comprehensive analysis of a stock
        """
        print(f"Analyzing {symbol}...")
        
        # Get basic stock data
        stock_data = self.get_stock_data(symbol)
        if not stock_data:
            return None
            
        # Technical analysis
        technical_data = self.technical_analysis(stock_data['historical_data'])
        
        # Fundamental analysis
        fundamental_data = self.fundamental_analysis(symbol)
        
        # Market sentiment
        sentiment_data = self.market_sentiment(symbol)
        
        # Risk analysis
        risk_data = self.risk_analysis(stock_data['historical_data'], symbol)
        
        # Trading signals
        signals = self.trading_signals(technical_data, fundamental_data)
        
        return {
            'symbol': symbol,
            'basic_data': stock_data,
            'technical_analysis': technical_data,
            'fundamental_analysis': fundamental_data,
            'market_sentiment': sentiment_data,
            'risk_analysis': risk_data,
            'trading_signals': signals,
            'analysis_timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

    def print_analysis_report(self, analysis: Dict):
        """
        Print a comprehensive analysis report
        """
        if not analysis:
            print("No analysis data available")
            return
            
        symbol = analysis['symbol']
        basic = analysis['basic_data']
        technical = analysis['technical_analysis']
        fundamental = analysis['fundamental_analysis']
        risk = analysis['risk_analysis']
        signals = analysis['trading_signals']
        
        print(f"\n{'='*60}")
        print(f"COMPREHENSIVE STOCK ANALYSIS: {symbol}")
        print(f"Analysis Date: {analysis['analysis_timestamp']}")
        print(f"{'='*60}")
        
        # Basic Information
        print(f"\n📊 BASIC STOCK INFORMATION")
        print(f"Current Price: ${basic['current_price']}")
        print(f"Daily Change: ${basic['change']} ({basic['change_percent']:.2f}%)")
        print(f"Volume: {basic['volume']:,} (Avg: {basic['avg_volume']:,})")
        print(f"Volume Ratio: {basic['volume_ratio']:.2f}x")
        if basic['market_cap'] != 'N/A':
            market_cap_b = basic['market_cap'] / 1e9
            print(f"Market Cap: ${market_cap_b:.2f}B")
        
        # Technical Analysis
        print(f"\n📈 TECHNICAL ANALYSIS")
        if technical.get('sma_20'):
            print(f"SMA 20: ${technical['sma_20']}")
        if technical.get('sma_50'):
            print(f"SMA 50: ${technical['sma_50']}")
        if technical.get('rsi'):
            print(f"RSI: {technical['rsi']}")
        if technical.get('macd'):
            print(f"MACD: {technical['macd']:.4f}")
        print(f"Support Level: ${technical.get('support', 'N/A')}")
        print(f"Resistance Level: ${technical.get('resistance', 'N/A')}")
        
        # Fundamental Analysis
        print(f"\n💰 FUNDAMENTAL ANALYSIS")
        if fundamental.get('pe_ratio'):
            print(f"P/E Ratio: {fundamental['pe_ratio']:.2f}")
        if fundamental.get('price_to_book'):
            print(f"P/B Ratio: {fundamental['price_to_book']:.2f}")
        if fundamental.get('debt_to_equity'):
            print(f"Debt/Equity: {fundamental['debt_to_equity']:.2f}")
        if fundamental.get('return_on_equity'):
            print(f"ROE: {fundamental['return_on_equity']:.2f}%")
        if fundamental.get('profit_margin'):
            print(f"Profit Margin: {fundamental['profit_margin']:.2f}%")
        
        # Risk Analysis
        print(f"\n⚠️  RISK ANALYSIS")
        print(f"Volatility: {risk.get('volatility', 'N/A')}%")
        print(f"Sharpe Ratio: {risk.get('sharpe_ratio', 'N/A')}")
        print(f"Max Drawdown: {risk.get('max_drawdown', 'N/A')}%")
        print(f"Beta: {risk.get('beta', 'N/A')}")
        
        # Trading Signals
        print(f"\n🎯 TRADING SIGNALS")
        print(f"Overall Signal: {signals['overall_signal']}")
        print("\nTechnical Signals:")
        for signal in signals['technical_signals']:
            print(f"  • {signal}")
        print("\nFundamental Signals:")
        for signal in signals['fundamental_signals']:
            print(f"  • {signal}")
            
        print(f"\n{'='*60}")

def main():
    """
    Main function to run the stock market analyzer
    """
    analyzer = StockMarketAnalyzer()
    
    print("🏦 Stock Market Analyzer - Comprehensive Trading Tool")
    print("This tool provides all essential information for cash market decisions\n")
    
    while True:
        print("\nOptions:")
        print("1. Analyze a single stock")
        print("2. Compare multiple stocks")
        print("3. Portfolio analysis")
        print("4. Market overview")
        print("5. Exit")
        
        choice = input("\nSelect an option (1-5): ").strip()
        
        if choice == '1':
            symbol = input("Enter stock symbol (e.g., AAPL): ").strip().upper()
            analysis = analyzer.comprehensive_analysis(symbol)
            if analysis:
                analyzer.print_analysis_report(analysis)
        
        elif choice == '2':
            symbols_input = input("Enter stock symbols separated by commas (e.g., AAPL,GOOGL,MSFT): ")
            symbols = [s.strip().upper() for s in symbols_input.split(',')]
            
            print(f"\nComparing {len(symbols)} stocks...")
            analyses = {}
            for symbol in symbols:
                analyses[symbol] = analyzer.comprehensive_analysis(symbol)
            
            # Print comparison
            print(f"\n{'='*80}")
            print("STOCK COMPARISON SUMMARY")
            print(f"{'='*80}")
            print(f"{'Symbol':<8} {'Price':<10} {'Change%':<10} {'P/E':<8} {'RSI':<8} {'Signal':<8}")
            print("-" * 80)
            
            for symbol, analysis in analyses.items():
                if analysis:
                    basic = analysis['basic_data']
                    tech = analysis['technical_analysis']
                    fund = analysis['fundamental_analysis']
                    signal = analysis['trading_signals']['overall_signal']
                    
                    pe = fund.get('pe_ratio', 'N/A')
                    pe_str = f"{pe:.1f}" if pe != 'N/A' and pe else 'N/A'
                    rsi_str = f"{tech.get('rsi', 0):.1f}" if tech.get('rsi') else 'N/A'
                    
                    print(f"{symbol:<8} ${basic['current_price']:<9.2f} {basic['change_percent']:<9.2f}% {pe_str:<8} {rsi_str:<8} {signal:<8}")
        
        elif choice == '3':
            print("Portfolio analysis feature - coming soon!")
            print("This will allow you to analyze multiple positions and calculate portfolio metrics.")
        
        elif choice == '4':
            # Market overview with major indices
            indices = ['SPY', 'QQQ', 'DIA', 'IWM']  # S&P 500, NASDAQ, Dow, Russell 2000
            print("\n📊 MARKET OVERVIEW")
            print("-" * 50)
            
            for index in indices:
                analysis = analyzer.comprehensive_analysis(index)
                if analysis:
                    basic = analysis['basic_data']
                    print(f"{index}: ${basic['current_price']:.2f} ({basic['change_percent']:+.2f}%)")
        
        elif choice == '5':
            print("Thank you for using Stock Market Analyzer!")
            break
        
        else:
            print("Invalid choice. Please select 1-5.")

if __name__ == "__main__":
    main()