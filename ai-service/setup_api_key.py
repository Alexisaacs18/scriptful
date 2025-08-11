#!/usr/bin/env python3
"""
Setup script for OpenAI API key configuration
"""

import os
import sys

def setup_api_key():
    print("🔑 OpenAI API Key Setup")
    print("=" * 40)
    
    # Check if .env file exists
    if not os.path.exists('.env'):
        print("❌ .env file not found!")
        print("   Please run this script from the ai-service directory")
        return False
    
    # Read current .env file
    with open('.env', 'r') as f:
        content = f.read()
    
    # Check if API key is already set
    if 'your_openai_api_key_here' not in content:
        print("✅ API key appears to be already configured!")
        return True
    
    print("📝 Current .env file:")
    print("-" * 20)
    print(content)
    print("-" * 20)
    
    print("\n🔧 To configure your API key:")
    print("1. Open the .env file in a text editor")
    print("2. Replace 'your_openai_api_key_here' with your actual API key")
    print("3. Save the file")
    print("4. Restart the app")
    
    print("\n📋 Example:")
    print("   OPENAI_API_KEY=sk-1234567890abcdef...")
    
    print("\n🌐 Get your API key from:")
    print("   https://platform.openai.com/account/api-keys")
    
    return False

if __name__ == "__main__":
    setup_api_key()
