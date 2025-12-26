import os
import sys

# Ensure we can import modules from the current directory
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from docx_handler import extract_text_from_docx, process_resume_updates
from ai_engine import GeminiEngine
from prompts import OPTIMIZER_SYSTEM_PROMPT

def read_text_file(file_path):
    """Helper to read the Job Description text file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read().strip()
    except Exception as e:
        print(f"❌ Error reading file {file_path}: {e}")
        return None

def main():
    print("🚀 Starting Resume Optimizer...")

    # --- 1. CONFIGURATION ---
    # Define paths based on our folder structure
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    INPUT_RESUME = os.path.join(BASE_DIR, "data", "input", "resume.docx")
    INPUT_JD = os.path.join(BASE_DIR, "data", "input", "jd.txt")
    OUTPUT_RESUME = os.path.join(BASE_DIR, "data", "output", "updated_resume.docx")

    # --- 2. VALIDATION ---
    if not os.path.exists(INPUT_RESUME):
        print(f"❌ Error: Resume not found at {INPUT_RESUME}")
        return
    if not os.path.exists(INPUT_JD):
        print(f"❌ Error: Job Description not found at {INPUT_JD}")
        return

    # --- 3. EXTRACTION ---
    print("📂 Reading files...")
    jd_text = read_text_file(INPUT_JD)
    resume_text_list = extract_text_from_docx(INPUT_RESUME)
    
    print(f"   -> Extracted {len(resume_text_list)} text blocks from resume.")

    # --- 4. AI ANALYSIS ---
    print("🧠 Sending data to Gemini (This may take 10-20 seconds)...")
    
    try:
        engine = GeminiEngine()
        changes_list = engine.get_optimization_suggestions(
            resume_text_list=resume_text_list, 
            jd_text=jd_text, 
            system_instruction=OPTIMIZER_SYSTEM_PROMPT
        )
    except Exception as e:
        print(f"❌ Critical AI Error: {e}")
        return

    if not changes_list:
        print("⚠ Gemini suggested no changes (or returned empty data).")
        return

    print(f"💡 Gemini suggested {len(changes_list)} optimizations.")

    # --- 5. EXECUTION (Find & Replace) ---
    print("✍️  Applying changes to Word Document...")
    
    success = process_resume_updates(
        input_path=INPUT_RESUME, 
        output_path=OUTPUT_RESUME, 
        replacements_list=changes_list
    )

    if success:
        print("\n" + "="*40)
        print(f"✅ SUCCESS! Optimized resume saved at:")
        print(f"{OUTPUT_RESUME}")
        print("="*40 + "\n")
    else:
        print("\n❌ Failed to save the document.")

if __name__ == "__main__":
    main()