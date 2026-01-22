import os
import json
from google import genai
from google.genai import types
from dotenv import load_dotenv

# Load environment variables (API Key)
load_dotenv()

class GeminiEngine:
    def __init__(self):
        # 1. Setup Configuration
        api_key = os.getenv("GEMINI_API_KEY")
        
        # Check if API key is missing or is just a placeholder
        if not api_key or "AIza" not in api_key:
            raise ValueError("❌ GEMINI_API_KEY not found or invalid in .env file. Please check your configuration.")
        
        # 2. Initialize Client (New SDK Method)
        self.client = genai.Client(api_key=api_key)

    def get_optimization_suggestions(self, resume_text_list, jd_text, system_instruction):
        """
        Sends the resume chunks and JD to Gemini and asks for JSON-formatted changes.
        """
        # 3. Construct the User Prompt
        # We join the list of strings into a formatted block for the AI to read
        resume_content_str = "\n".join([f"- {text}" for text in resume_text_list])
        
        full_prompt = (
            f"JOB DESCRIPTION:\n{jd_text}\n\n"
            f"RESUME CONTENT CHUNK:\n{resume_content_str}\n"
        )

        try:
            # 4. Call the API (New SDK Method)
            # The new SDK allows passing system_instruction directly in the config
            response = self.client.models.generate_content(
                model='gemini-flash-latest', # Using the faster, newer model
                contents=full_prompt,
                config=types.GenerateContentConfig(
                    system_instruction=system_instruction,
                    response_mime_type='application/json',
                    temperature=0.7 
                )
            )

            # 5. Parse the JSON Response
            # The new SDK returns the text directly in .text
            if not response.text:
                print("❌ Error: Received empty response from Gemini.")
                return []

            response_json = json.loads(response.text)
            
            # Extract the list of changes
            if "changes" in response_json:
                return response_json["changes"]
            else:
                # Handle cases where AI returns valid JSON but with wrong key
                print("⚠ Warning: AI returned JSON but 'changes' key was missing.")
                # Fallback: check if it returned a list directly
                if isinstance(response_json, list):
                    return response_json
                return []

        except json.JSONDecodeError:
            print("❌ Error: Gemini did not return valid JSON.")
            print(f"Raw Response: {response.text if 'response' in locals() else 'No Response'}")
            return []
        except Exception as e:
            print(f"❌ API Error: {e}")
            return []

    def get_gemini_response(prompt):
        try:
            # Use 'gemini-1.5-flash' which is the standard identifier
            model = genai.GenerativeModel('gemini-1.5-flash')
            response = model.generate_content(prompt)
            return response
        except Exception as e:
            print(f"❌ Error while getting response from Gemini: {e}")
            return None

# Simple test block to check if file loads correctly
if __name__ == "__main__":
    try:
        engine = GeminiEngine()
        print("✅ GeminiEngine class loaded and Client initialized successfully.")
    except Exception as e:
        print(f"❌ Initialization Failed: {e}")