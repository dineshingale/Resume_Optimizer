# 📄 Resume Optimizer

An AI-powered tool that automatically tailors your resume to match specific job descriptions. Using Google's Gemini AI, it analyzes your existing resume against a job description (JD) and generates a new, optimized version with improved keywords and phrasing.

## 🚀 Features

-   **Intelligent Analysis**: Uses Gemini AI to understand context and matching requirements.
-   **Docx Support**: Reads and Writes directly to Microsoft Word (`.docx`) files.
-   **Smart Replacement**: Identifies specific text blocks in your resume and replaces them with tailored content while maintaining document structure.
-   **Automated Workflow**: Simple command-line interface to run the entire process.

## 🛠️ Tech Stack

-   **Language**: Python 3
-   **AI Model**: Google Gemini Pro (`google-generativeai`)
-   **Document Processing**: `python-docx`
-   **Environment Management**: `python-dotenv`

## 📦 Installation & Setup

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/dineshingale/Resume_Optimizer.git
    cd Resume_Optimizer
    ```

2.  **Set up a virtual environment (Optional but Recommended):**
    ```bash
    python -m venv venv
    # Windows
    .\venv\Scripts\activate
    # macOS/Linux
    source venv/bin/activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configure API Key:**
    Create a `.env` file in the root directory and add your Google Gemini API key:
    ```env
    GEMINI_API_KEY=your_actual_api_key_here
    ```

## 📖 Usage

1.  **Prepare your Input Files:**
    -   Place your resume file at: `data/input/resume.docx`
    -   Place the job description text at: `data/input/jd.txt`

2.  **Run the Optimizer:**
    ```bash
    python run.py
    ```

3.  **Get Results:**
    -   The script will analyze the documents and apply changes.
    -   Find your optimized resume at: `data/output/updated_resume.docx`

## 📂 Project Structure

```
Resume_Optimizer/
├── data/
│   ├── input/       # Place your resume.docx and jd.txt here
│   └── output/      # Generated resumes will appear here
├── src/
│   ├── ai_engine.py    # Handles interaction with Gemini API
│   ├── docx_handler.py # Reads and modifies Word documents
│   ├── main.py         # Main orchestration logic
│   └── prompts.py      # System prompts for the AI
├── run.py           # Entry point script
├── requirements.txt # Python dependencies
└── .env             # Environment variables (API Key)
```

## ⚠️ Notes

-   Ensure your `.docx` file is not open in Word while running the script, or it may fail to save.
-   The tool works best with text-based resumes. Complex layouts with text boxes may require manual adjustment.

## 🤝 Contributing

1.  Fork the repository.
2.  Create a feature branch (`git checkout -b feat/amazing-feature`).
3.  Commit your changes (`git commit -m 'feat: add amazing feature'`).
4.  Push to the branch (`git push origin feat/amazing-feature`).
5.  Open a Pull Request.
