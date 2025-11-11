# 🚀 Quick Start Guide - Neil deGrasse Tyson Chatbot

Get your chatbot running in 2 minutes!

## Step 1: Start the Backend (Terminal 1)

```bash
# Navigate to project directory
cd "c:\Users\Antho\OneDrive\Desktop\Neil deGrasse Tyson ChatBot"

# Start the server
uvicorn backend.app:app --port 8000
```

You should see:
```
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Application startup complete.
```

## Step 2: Open the Frontend

**Easiest Option - Standalone HTML:**

Simply double-click `chatbot.html` in your file explorer, or run:

```bash
# Windows
start chatbot.html

# Or open in your default browser
explorer chatbot.html
```

**Alternative - React App:**

```bash
# In a new terminal
cd frontend
npm install
npm run dev
```

Then open the URL shown (usually http://localhost:5173)

## Step 3: Start Chatting! 💬

Try these questions:
- Why are we made of stardust?
- What happens inside a black hole?
- Should humans colonize Mars?
- What is the cosmic perspective?

## Visual Preview

Your chatbot features:
- ✅ Neil deGrasse Tyson's photo in the header
- ✅ NDT's avatar in bot message bubbles
- ✅ Cosmic space-themed design
- ✅ Source citations for every response
- ✅ 543 knowledge chunks from real NDT content
- ✅ 180-word limit with inline citations

## Troubleshooting

**Backend won't start:**
```bash
# Make sure you're in the project directory and virtual environment is activated
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Mac/Linux

# Try again
uvicorn backend.app:app --port 8000
```

**Frontend shows "Failed to fetch":**
- Check that backend is running at http://localhost:8000
- Visit http://localhost:8000/docs to verify backend is accessible

**NDT's photo doesn't load:**
- The app will automatically use a fallback avatar
- Check your internet connection

## What's Running

🔹 **Backend:** http://localhost:8000
   - RAG pipeline with FAISS vector store
   - 543 knowledge chunks from NDT interviews
   - GPT-4 with citation-first responses

🔹 **Frontend:** chatbot.html or http://localhost:5173
   - Modern chat interface
   - NDT's photo and cosmic theme
   - Real-time messaging

## Next Steps

1. **Test different questions** - Try astronomy, physics, space exploration topics
2. **Check citations** - Click the source links to see where answers come from
3. **Add more training data** - Run `train_from_urls.py` with new URLs
4. **Customize the design** - Edit colors in chatbot.html or App.css

---

**Need Help?**
- Check FRONTEND_README.md for detailed instructions
- Visit http://localhost:8000/docs for API documentation
- Review backend logs for error messages

**Enjoy chatting with Neil deGrasse Tyson! 🌌**
