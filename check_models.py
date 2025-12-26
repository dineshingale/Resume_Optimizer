import google.generativeai as genai
from dotenv import load_dotenv
import os

# 1. Load environment variables from your .env file
load_dotenv()

# 2. Get the API key from the environment
api_key = os.getenv("GEMINI_API_KEY")

# 3. Check if the API key was loaded correctly
if not api_key:
    print("❌ ERROR: Could not find GEMINI_API_KEY in your .env file.")
else:
    print("✅ API Key loaded successfully from .env file.")
    
    try:
        # 4. Configure the SDK with your key
        genai.configure(api_key=api_key)
        
        print("\n🔍 Fetching available models for your API key...")
        
        # 5. List all models and check if they support the method your code uses
        model_found = False
        for m in genai.list_models():
            # The 'generateContent' method is what your ai_engine.py uses
            if 'generateContent' in m.supported_generation_methods:
                print(f"  - Available Model: {m.name}")
                model_found = True
        
        if not model_found:
            print("\n❌ CRITICAL: No models supporting 'generateContent' were found for your API key.")
            print("   This likely means the 'Generative Language API' is not enabled on your Google Cloud project,")
            print("   or your project is in a region that does not yet support these models.")

    except Exception as e:
        print(f"\n❌ An error occurred while communicating with the API: {e}")