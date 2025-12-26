import os
import json
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables (API Key)
load_dotenv()

class GeminiEngine:
    def __init__(self):
        # 1. Setup Configuration
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("❌ GEMINI_API_KEY not found in .env file. Please check your configuration.")
        
        genai.configure(api_key=api_key)
        
        # 2. Initialize Model
        self.model = genai.GenerativeModel(
            # Use the full, correct Pro model name from your list
            model_name="models/gemini-pro-latest",
            generation_config={"response_mime_type": "application/json"}
        )

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
            # 4. Call the API with the System Instruction (The Rules) and User Data
            response = self.model.generate_content(
                contents=full_prompt,
                # We pass the system instruction (the specific "Do not lie" rules) here
                # Note: System instructions are technically part of model config or prepended to prompt
                # For simplicity in 1.5, we often prepend, but let's use the 'system_instruction' param if supported
                # or prepend it to the prompt.
            )
            
            # Since 'system_instruction' is a specific parameter in newer SDKs:
            # We will use a chat session approach or prepend it for maximum compatibility.
            # Here is the robust 'Chat' approach:
            chat = self.model.start_chat(history=[
                {"role": "user", "parts": system_instruction}
            ])
            
            response = chat.send_message(full_prompt)

            # 5. Parse the JSON Response
            # Gemini returns a string, we need to convert it to a Python Dictionary
            response_json = json.loads(response.text)
            
            # Extract the list of changes
            if "changes" in response_json:
                return response_json["changes"]
            else:
                # Handle cases where AI returns a valid JSON but with wrong key
                print("⚠ Warning: AI returned JSON but 'changes' key was missing.")
                return []

        except json.JSONDecodeError:
            print("❌ Error: Gemini did not return valid JSON.")
            print(f"Raw Response: {response.text}")
            return []
        except Exception as e:
            print(f"❌ API Error: {e}")
            return []

# Simple test block to check if file loads correctly (not for running the app)
if __name__ == "__main__":
    print("GeminiEngine class loaded successfully.")