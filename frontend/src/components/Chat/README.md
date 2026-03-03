# Chat Component

AI-powered chatbot component for the Physical AI & Humanoid Robotics textbook.

## Features

- 💬 Real-time chat with AI teaching assistant
- 📚 RAG-powered responses from textbook content
- 🎨 Modern, responsive UI with smooth animations
- 📱 Mobile-friendly design
- 🔄 Auto-scrolling message history
- ⌨️ Enter key to send messages
- 📖 Source citations for responses
- ⚡ Typing indicator
- 🗂️ Collapsible chat window

## Installation

The chat component is already integrated into the Docusaurus site. No additional installation required.

## Configuration

### API URL

Edit the `apiUrl` prop in `frontend/src/theme/Layout.tsx`:

```tsx
<Chat 
  apiUrl="http://localhost:8000"  // Change to your backend URL
  userId={1} 
/>
```

### User ID

For production, implement proper authentication and replace the hardcoded `userId`:

```tsx
<Chat 
  apiUrl="https://your-backend.com" 
  userId={currentUser.id} 
/>
```

## Customization

### Styling

Edit `Chat.module.css` to customize:
- Colors (uses Docusaurus theme variables by default)
- Size and position
- Animations
- Responsive breakpoints

### Position

By default, the chat is positioned at bottom-right. To change position, modify `.chat-container` in `Chat.module.css`:

```css
.chat-container {
  bottom: 20px;
  right: 20px;
  /* Or use left: 20px for bottom-left */
}
```

## Component Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `apiUrl` | `string` | `'http://localhost:8000'` | Backend API URL |
| `userId` | `number` | `1` | User identifier |

## File Structure

```
src/components/Chat/
├── Chat.tsx              # Main chat component
├── Chat.module.css       # Component styles
└── index.ts              # Export file

src/theme/
└── Layout.tsx            # Layout wrapper with chat integration
```

## Usage Examples

### Basic Usage

The chat is automatically available on all pages after integration.

### Manual Usage (Specific Pages)

```tsx
import Chat from '@site/src/components/Chat';

function MyPage() {
  return (
    <div>
      <h1>My Page</h1>
      <Chat apiUrl="http://localhost:8000" userId={1} />
    </div>
  );
}
```

## Backend Requirements

The chat component expects a FastAPI backend with the following endpoint:

### POST /chat/

**Request:**
```
POST /chat/?user_id=1&message=Hello&session_id=optional
```

**Response:**
```json
{
  "response": "AI response text",
  "context_used": true,
  "context_count": 3,
  "sources": [
    {
      "chapter": "Chapter Title",
      "module": "module-name",
      "score": 0.89
    }
  ],
  "user_id": 1
}
```

## Development

### Testing Locally

1. Start the backend:
   ```bash
   cd backend
   python main.py
   ```

2. Start the frontend:
   ```bash
   cd frontend
   npm start
   ```

3. Open http://localhost:3000 and look for the chat widget in the bottom-right corner

### Troubleshooting

**Chat not appearing:**
- Check that `Layout.tsx` is in `src/theme/`
- Verify the backend is running
- Check browser console for errors

**CORS errors:**
- Ensure backend CORS is configured correctly
- Check `apiUrl` matches the backend origin

**No responses:**
- Verify backend `/chat/` endpoint is working
- Check network tab for failed requests
- Ensure database and Qdrant are connected

## Future Enhancements

- [ ] User authentication integration
- [ ] Session management
- [ ] Chat history persistence
- [ ] Markdown rendering in messages
- [ ] Code syntax highlighting
- [ ] Export chat conversations
- [ ] Feedback mechanism (thumbs up/down)
- [ ] Multi-language support
