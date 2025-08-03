#!/usr/bin/env python3
"""
Test script for Stock Market Analyzer
Quick verification that the system works
"""

import sys
from stock_market_analyzer import StockMarketAnalyzer

def test_analyzer():
    """Test the stock analyzer with a known stock"""
    print("🧪 Testing Stock Market Analyzer...")
    print("=" * 40)
    
    try:
        # Initialize analyzer
        analyzer = StockMarketAnalyzer()
        print("✅ Analyzer initialized successfully")
        
        # Test with Apple stock
        print("\n📊 Testing with AAPL (Apple Inc.)...")
        analysis = analyzer.comprehensive_analysis('AAPL')
        
        if analysis:
            print("✅ Analysis completed successfully!")
            
            # Check basic data
            basic = analysis['basic_data']
            print(f"✅ Current Price: ${basic['current_price']}")
            print(f"✅ Daily Change: {basic['change_percent']:.2f}%")
            
            # Check technical analysis
            technical = analysis['technical_analysis']
            if technical.get('rsi'):
                print(f"✅ RSI: {technical['rsi']:.2f}")
            
            # Check trading signal
            signal = analysis['trading_signals']['overall_signal']
            print(f"✅ Trading Signal: {signal}")
            
            print("\n🎉 All tests passed! The analyzer is working correctly.")
            return True
            
        else:
            print("❌ Analysis returned no data")
            return False
            
    except Exception as e:
        print(f"❌ Test failed with error: {str(e)}")
        print("\nTroubleshooting tips:")
        print("1. Check internet connection")
        print("2. Verify all packages are installed: python setup.py")
        print("3. Try again in a few minutes (API limits)")
        return False

def test_web_imports():
    """Test if web application dependencies are available"""
    print("\n🌐 Testing web application imports...")
    
    try:
        from flask import Flask
        print("✅ Flask imported successfully")
        
        import json
        print("✅ JSON module available")
        
        return True
        
    except ImportError as e:
        print(f"❌ Web import failed: {e}")
        print("Run: pip install flask")
        return False

def main():
    """Main test function"""
    print("🚀 Stock Market Analyzer - Test Suite")
    print("=" * 50)
    
    # Test core analyzer
    analyzer_ok = test_analyzer()
    
    # Test web dependencies
    web_ok = test_web_imports()
    
    print("\n" + "=" * 50)
    if analyzer_ok and web_ok:
        print("🎉 ALL TESTS PASSED!")
        print("\nYou can now use:")
        print("• CLI: python stock_market_analyzer.py")
        print("• Web: python stock_web_app.py")
    else:
        print("⚠️  SOME TESTS FAILED")
        print("See error messages above for troubleshooting")
        sys.exit(1)

if __name__ == "__main__":
    main()