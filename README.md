# 🛡️ PhreshPhish AI: Next-Gen Phishing Detection

An advanced, AI-driven phishing detection application powered by a custom fine-tuned **Llama-3.2 (3B)** model. PhreshPhish analyzes raw HTML DOM structures, URLs, and webpage features locally to identify sophisticated phishing attempts without relying on static blocklists.

## 🚀 Features
* **Custom Fine-Tuned LLM:** Utilizes a Llama-3.2 3B model fine-tuned specifically on phishing datasets using Unsloth.
* **Local & Secure Inference:** Runs entirely locally via Ollama, ensuring 100% data privacy and zero API costs.
* **Intelligent DOM Extraction:** Parses and sanitizes raw HTML to extract critical threat indicators (hidden forms, suspicious iframes, credential harvesting setups).
* **Strict JSON Output Validation:** Leverages Pydantic to enforce strict JSON schema outputs from the LLM, preventing parsing errors.
* **Interactive UI:** A clean, professional web interface built with Streamlit for real-time analysis.

## 🛠️ Tech Stack
* **Language:** Python 3.10+
* **Frontend:** Streamlit
* **AI Engine:** Ollama, Llama-cpp
* **Fine-tuning:** Unsloth (LoRA/QLoRA), Hugging Face `trl`
* **Data Validation:** Pydantic, BeautifulSoup4

## ⚙️ Local Installation & Setup

Follow these instructions to run the PhreshPhish AI detector on your local machine.

## 1. Clone the Repository

git clone [https://github.com/Avanijain09/PhreshPhish-AI-Detector.git](https://github.com/Avanijain09/PhreshPhish-AI-Detector.git)
cd PhreshPhish-AI-Detector

2. Set Up Virtual Environment
   
python -m venv venv
# On Windows
venv\Scripts\activate
# On Mac/Linux
source venv/bin/activate

pip install -r requirements.txt
3. Load the Custom AI Model
Since the GGUF model file is large (~2GB), it is not hosted directly on GitHub.

Install Ollama on your system.

Place your fine-tuned model file (Llama-3.2-3B-Instruct.Q4_K_M.gguf) in the root directory.

Build the model in Ollama using the provided Modelfile:

ollama create phreshphish_ai -f Modelfile
4. Run the Application

streamlit run app.py
The application will launch in your default web browser at http://localhost:8501
