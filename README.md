Perfect 👍 since you’ve integrated **LangSmith** for tracing, let’s update the README to highlight that. I’ll also add setup instructions for **LangSmith API key** and mention how runs show up in the LangSmith dashboard.

Here’s the updated **README.md** 👇

---

```markdown
# 📚 Adaptive Storybook Creator  

An AI-powered **storybook generator** that creates **personalized interactive stories** for children.  
It generates:  
- 📝 Custom story text (LLM-based)  
- 🖼️ Illustrations (AI-generated images)  
- 🔊 Narration (AI-generated audio)  
- 🎬 Animated scene (AI-generated video, experimental)  

The app uses **FastAPI** for the backend and **Streamlit** for the frontend.  
It integrates with **LangSmith** for **observability and tracing**.  

---

## 🚀 Features
- Generate child-friendly stories based on:
  - **Age** (1–15 years)  
  - **Reading Level** (Beginner, Intermediate, Advanced)  
  - **Theme** (e.g., Space, Animals, Magic)  
  - **Gender** (to personalize characters)  
  - **Optional description** for extra preferences  
- Markdown formatted storybook with chapters  
- AI-generated illustrations using Stable Diffusion  
- AI narration with fallback to gTTS (Google Text-to-Speech)  
- Experimental AI video generation (Zeroscope)  
- **LangSmith Integration**:
  - All steps (`text`, `image`, `audio`, `video`) are logged as **child traces** under a single **main run**  
  - View execution traces, inputs/outputs, and errors in the [LangSmith dashboard](https://smith.langchain.com/)  

---

## 📂 Project Structure
```bash
.
├── backend_api.py # FastAPI backend with LangSmith tracing
├── frontend.py # Streamlit frontend
├── .env # Environment variables (HF_TOKEN, LANGCHAIN_API_KEY, etc.)
└── README.md # Project documentation
````


## ⚙️ Installation

### 1️⃣ Clone Repository
```bash
git clone https://github.com/<your-username>/storybook-creator.git
cd storybook-creator
````

### 2️⃣ Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate   # Mac/Linux
venv\Scripts\activate      # Windows
```

### 3️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```

## 🔑 Environment Variables

Create a `.env` file in the project root:

```ini
# Hugging Face
HF_TOKEN=your_huggingface_api_token
# LangSmith
LANGCHAIN_API_KEY=your_langsmith_api_key
LANGCHAIN_TRACING_V2=true
LANGCHAIN_ENDPOINT='https://api.smith.langchain.com'
LANGCHAIN_PROJECT=storybook-creator
```

* Get a Hugging Face token: [https://huggingface.co/settings/tokens](https://huggingface.co/settings/tokens)
* Get a LangSmith API key: [https://smith.langchain.com/settings](https://smith.langchain.com/settings)

---

## ▶️ Running the App
### Start Backend (FastAPI)
```bash
uvicorn backend_api:app --reload
```
Backend will run at: `http://127.0.0.1:8000`

### Start Frontend (Streamlit)
```bash
streamlit run frontend.py
```
Frontend will open in your browser: `http://localhost:8501`

---

## 🖥️ Usage
1. Open the Streamlit app in your browser.
2. Enter child’s **age, reading level, theme, gender, and preferences**.
3. Click **Generate Storybook**.
4. Get:
   * AI-generated story (Markdown format)
   * Illustration (displayed inline)
   * Audio narration (downloadable/playable)
   * Video animation (if available)
---

## 📊 LangSmith Tracing
* Each request to `/generate_story/` creates **one main run** in LangSmith.
* Inside it, you’ll see **child traces**:

  * ✍️ `Generate Story Text`
  * 🖼️ `Generate Image`
  * 🔊 `Generate Audio`
  * 🎬 `Generate Video`
* This makes debugging and monitoring easier.

👉 View traces at [smith.langchain.com](https://smith.langchain.com/).
---

## ⚠️ Notes
* Video generation is **experimental** and may fail if Hugging Face credits are insufficient.
* Audio narration uses **gTTS fallback** if Hugging Face model is unavailable(Refresh Audio Page once if you not found play Butoon).
* Ensure you have enough Hugging Face **inference credits** for image/video generation.
---

