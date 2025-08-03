#!/usr/bin/env python3
"""
Setup script for Stock Market Analyzer
Installs dependencies and prepares the environment
"""

import subprocess
import sys
import os

def install_requirements():
    """Install required packages"""
    print("📦 Installing required packages...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "pip"])
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ All packages installed successfully!")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error installing packages: {e}")
        return False
    return True

def test_installation():
    """Test if all required packages are available"""
    print("🧪 Testing installation...")
    required_packages = [
        'yfinance', 'pandas', 'numpy', 'matplotlib', 'seaborn', 
        'requests', 'scipy', 'plotly', 'dash', 'flask'
    ]
    
    missing_packages = []
    for package in required_packages:
        try:
            __import__(package)
            print(f"✅ {package}")
        except ImportError:
            print(f"❌ {package}")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\n❌ Missing packages: {', '.join(missing_packages)}")
        return False
    else:
        print("\n✅ All packages are available!")
        return True

def create_startup_script():
    """Create convenient startup scripts"""
    print("📝 Creating startup scripts...")
    
    # CLI startup script
    cli_script = '''#!/bin/bash
echo "🏦 Starting Stock Market Analyzer (CLI)..."
python3 stock_market_analyzer.py
'''
    
    # Web app startup script  
    web_script = '''#!/bin/bash
echo "🌐 Starting Stock Market Analyzer (Web)..."
echo "Open http://localhost:5000 in your browser"
python3 stock_web_app.py
'''
    
    try:
        with open('start_cli.sh', 'w') as f:
            f.write(cli_script)
        os.chmod('start_cli.sh', 0o755)
        
        with open('start_web.sh', 'w') as f:
            f.write(web_script)
        os.chmod('start_web.sh', 0o755)
        
        print("✅ Created start_cli.sh and start_web.sh")
    except Exception as e:
        print(f"⚠️  Could not create startup scripts: {e}")

def main():
    """Main setup function"""
    print("🚀 Stock Market Analyzer Setup")
    print("=" * 40)
    
    # Check Python version
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        sys.exit(1)
    
    print(f"✅ Python {sys.version.split()[0]} detected")
    
    # Install requirements
    if not install_requirements():
        print("❌ Setup failed during package installation")
        sys.exit(1)
    
    # Test installation
    if not test_installation():
        print("❌ Setup failed during testing")
        sys.exit(1)
    
    # Create startup scripts
    create_startup_script()
    
    print("\n🎉 Setup completed successfully!")
    print("\nTo start the program:")
    print("  CLI Version:  python stock_market_analyzer.py")
    print("  Web Version:  python stock_web_app.py")
    print("  Or use:       ./start_cli.sh or ./start_web.sh")
    
    print("\n📖 See README.md for detailed usage instructions")
    print("🔗 Web interface will be available at http://localhost:5000")

if __name__ == "__main__":
    main()