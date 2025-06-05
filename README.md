# 🔆 Solar Rooftop AI Assistant

This project is an AI-powered assistant that helps assess the solar installation potential of rooftops using image captioning, solar panel estimation logic, and large language models.

It was built as part of an AI internship assessment and demonstrates skills in:

- LangChain (LLM pipelines)
- FastAPI (modular backend logic)
- Streamlit (frontend UI)
- Pydantic (data validation)
- Image captioning (via Gemini/GPT or placeholder)
- Solar panel cost & ROI estimation

---

## 🚀 Features

- Upload or link a rooftop image
- Extracts a descriptive caption using an AI vision model
- Takes additional user input like roof area, orientation, material, etc.
- Calculates:
  - Estimated panel size
  - Cost and ROI
  - Feasibility
- Generates a natural language recommendation using a Large Language Model (LLM)
- Deployable via Streamlit Cloud

---

## 📦 Tech Stack

- Python 3.10+
- Streamlit
- FastAPI (used modularly for backend logic)
- LangChain + Gemini / OpenAI
- Pydantic (for validation)
- Torch + Transformers (for vision models)
- ImageCaptionLoader (LangChain Community tools)

---

## 📦 Project Structure

**app.py**: Streamlit UI
**backend.py**: Core backend logic + validation
**utils.py**: solar estimation function
**requirements.txt**: python dependencies


## 🧑‍💻 Getting Started (Local)

### 1. Clone the Repo

```bash
git clone https://github.com/harshita/solar-ai-assistant.git
cd solar-ai-assistant
```

### 2. Create virtual environment (optional but recommended)
```bash
python -m venv venv
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Set your API keys
Create a ```.env``` file in root directory.

### 5. Run the app
```bash
streamlit run app.py
```
This will start a local streamlut app in your browser.