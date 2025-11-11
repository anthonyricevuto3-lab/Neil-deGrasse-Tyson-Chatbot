# Neil deGrasse Tyson AI Chatbot - Frontend

Beautiful, modern chat interface featuring Neil deGrasse Tyson's photo and cosmic-themed design.

## Quick Start Options

### Option 1: Standalone HTML (Easiest - No Build Required)

Simply open `chatbot.html` in your browser:

1. **Start the backend server:**
   ```bash
   uvicorn backend.app:app --port 8000
   ```

2. **Open the chatbot:**
   - Double-click `chatbot.html` or
   - Right-click → Open with → Your browser

That's it! The chatbot is ready to use.

### Option 2: React App (Full Development Setup)

For the full React/TypeScript development experience:

1. **Navigate to frontend directory:**
   ```bash
   cd frontend
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

3. **Start development server:**
   ```bash
   npm run dev
   ```

4. **In a separate terminal, start the backend:**
   ```bash
   cd ..
   uvicorn backend.app:app --port 8000
   ```

5. **Open browser:**
   - Navigate to the URL shown in the terminal (usually http://localhost:5173)

## Features

✨ **Beautiful Design:**
- Neil deGrasse Tyson's photo prominently featured
- Cosmic space theme with gradient backgrounds
- Smooth animations and transitions
- Responsive design for mobile and desktop

🚀 **Interactive Chat:**
- Real-time messaging with NDT AI
- Message avatars (NDT's photo for bot responses)
- Source citations displayed as clickable links
- Character counter and auto-resizing input

💫 **Suggested Questions:**
- "Why are we made of stardust?"
- "What happens inside a black hole?"
- "Should humans colonize Mars?"
- "What is the cosmic perspective?"

## Configuration

### Backend API URL

Both frontends default to `http://localhost:8000/api/chat`

**To change the API URL:**

**For chatbot.html:**
- Edit line 457: `const API_URL = 'http://localhost:8000/api/chat';`

**For React app:**
- Edit `frontend/src/hooks/useChat.tsx`
- Change the API_URL constant

## Troubleshooting

### "Failed to fetch" Error

**Problem:** Frontend can't connect to backend

**Solution:**
1. Verify backend is running: `http://localhost:8000/docs`
2. Check that port 8000 is not blocked
3. Ensure API_URL matches backend address

### Avatar Images Not Loading

**Problem:** NDT's photo doesn't display

**Solution:**
- The app will automatically fallback to a generated avatar
- Check your internet connection (images are hosted externally)
- Alternatively, download the image and host it locally

### React App Won't Start

**Problem:** npm install or npm run dev fails

**Solution:**
```bash
# Delete node_modules and package-lock.json
rm -rf node_modules package-lock.json

# Reinstall
npm install

# Try again
npm run dev
```

## Customization

### Change Color Theme

Edit CSS variables at the top of `chatbot.html` or `frontend/src/styles/App.css`:

```css
:root {
    --primary-color: #1a1a2e;      /* Dark blue background */
    --secondary-color: #16213e;    /* Card backgrounds */
    --accent-color: #0f3460;       /* User message bubbles */
    --highlight-color: #e94560;    /* Buttons and accents */
    --text-color: #eaeaea;         /* Text color */
}
```

### Add Custom Welcome Questions

Edit the suggested questions in:
- `chatbot.html` (lines 475-488)
- `frontend/src/components/Chat.tsx` (lines 57-70)

### Change NDT Quote

Edit the header subtitle:
- `chatbot.html` (line 456)
- `frontend/src/App.tsx` (line 20)

## Tech Stack

### Standalone HTML Version
- Pure HTML5/CSS3/JavaScript
- No dependencies or build tools
- Works in any modern browser

### React Version
- React 18 with TypeScript
- Vite build tool
- CSS Modules
- React Markdown for message formatting

## Performance

- **Standalone HTML:** Instant load, <100KB total
- **React App:** ~500KB bundle size after build
- **API Response:** Typically 2-5 seconds for chatbot responses

## Browser Support

- Chrome/Edge 90+
- Firefox 88+
- Safari 14+
- Opera 76+

## License

This chatbot interface is part of the Neil deGrasse Tyson AI project.

---

**Enjoy exploring the cosmos with Neil deGrasse Tyson! 🌌✨**
