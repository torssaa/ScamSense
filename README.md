<<<<<<< HEAD
# ScamSense
=======
# 🛡️ ScamSense - AI-Powered Scam Detector

ScamSense is a hybrid security system designed to protect users from phishing and scams on popular communication platforms. It combines a Chrome extension with a Python-based RAG (Retrieval-Augmented Generation) engine and Gemini AI to analyze messages in real-time.

---

## 🚀 Features

- **Multi-Platform Support:** Works seamlessly on **WhatsApp Web**, **Telegram Web** (Version K & A), and **Gmail**.
- **Manual Scanning:** Click "Scan This Message" in the extension popup to analyze the currently open conversation.
- **Background Protection:** Automatically monitors incoming messages and displays a high-visibility UI alert directly on the page if a scam is detected.
- **AI Intelligence:** Powered by **Gemini 3 Flash** for sophisticated intent analysis.
- **Knowledge Base (RAG):** Uses a local database of known scam patterns to provide context-aware results and reduce false positives.

---

## 🛠️ Installation

### 1. Prerequisites
- [Python 3.10+](https://www.python.org/)
- [Google Gemini API Key](https://aistudio.google.com/app/apikey)

### 2. Backend Setup
1. Clone the repository: `git clone https://github.com/torssaa/ScamSense.git`
2. Navigate to the backend directory: `cd ScamSense/backend`
3. Install dependencies: `pip install -r requirements.txt`
4. Create a `.env.local` file in the `backend/` folder and add your key:
   ```env
   GEMINI_API_KEY=your_actual_key_here
   PORT=8000
   ```

### 3. Extension Setup
1. Open Chrome and go to `chrome://extensions/`.
2. Enable **Developer mode** (top right toggle).
3. Click **Load unpacked**.
4. Select the `extension/` folder in the project directory.

---

## 🏁 How to Use

1.  **Start the Server:**
    - Double-click `START_SCAMSENSE.bat` in the main folder.
    - *Alternatively:* Run `python backend/main.py` in your terminal.
2.  **Open Messaging Apps:** Go to WhatsApp Web or Telegram Web.
3.  **Analyze:**
    - **Automatic:** The extension will alert you if it detects a high-risk message.
    - **Manual:** Click the extension icon and hit **Scan This Message**.

---

## 🏗️ Technical Architecture

- **Frontend:** Pure JavaScript Content Scripts and Browser Extension.
- **Backend:** FastAPI (Python) serving an inference endpoint.
- **AI Engine:** Google Generative AI (Gemini 3 Flash).
- **Vector DB:** ChromaDB for local scam pattern storage.
- **Protection Logic:** MutationObservers for real-time DOM monitoring.

---

## 📄 License
This project is for educational purposes as part of cybersecurity research.

---

*Stay safe out there! 🐜🚫*
>>>>>>> 763b53f (Initialize ScamSense: AI-Powered Scam Detector)
