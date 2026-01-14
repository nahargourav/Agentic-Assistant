# Assistant App - Setup and Deployment Guide

## Overview
This is a full-stack AI-powered Assistant application with a React frontend and FastAPI backend. Users can sign up, log in, and interact with an AI assistant using text or voice commands.

## Prerequisites

### Backend
- Python 3.8 or higher
- pip (Python package manager)

### Frontend
- Node.js 16 or higher
- npm or yarn

## Backend Setup

### 1. Navigate to Backend Directory
```bash
cd Backend
```

### 2. Create Virtual Environment (Recommended)
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Environment Variables (Optional)
Create a `.env` file in the Backend directory:
```
OPENAI_API_KEY=your_openai_api_key_here
SECRET_KEY=your_secret_key_for_jwt
```

### 5. Run the Backend Server
```bash
# From Backend directory
python app.py
```

The backend will start on `http://localhost:8000`

#### API Endpoints:
- `GET /` - Welcome message
- `POST /auth/register` - Register new user
- `POST /auth/login` - Login user
- `GET /auth/validate` - Validate JWT token
- `POST /assistant/command` - Send text command
- `POST /assistant/voice` - Send voice command (audio file)
- `POST /tasks` - Create task
- `GET /tasks/{task_id}` - Get task status
- `GET /status/health` - Health check

## Frontend Setup

### 1. Navigate to Frontend Directory
```bash
cd Frontend
```

### 2. Install Dependencies
```bash
npm install
```

### 3. Environment Variables
Create a `.env` file in the Frontend directory:
```
REACT_APP_API_URL=http://localhost:8000
```

### 4. Run the Development Server
```bash
npm start
```

The frontend will start on `http://localhost:3000`

## Using the Application

### 1. Registration
- Navigate to `http://localhost:3000`
- Click "Get Started" or "Sign Up"
- Fill in your name, email, and password
- Click "Sign Up"

### 2. Login
- Click "Sign In"
- Enter your email and password
- Click "Sign In"

### 3. Using the Assistant
Once logged in, you'll see the Dashboard with the Assistant interface:

#### Text Commands:
- Type your command in the text input field
- Click "Send" or press Enter
- The assistant will respond

#### Voice Commands:
- Click the microphone button (🎤 Start)
- Speak your command
- Click "Stop" when finished
- The assistant will process and respond

### 4. Features
- **Theme Switcher**: Toggle between light and dark mode
- **Real-time Conversation**: View your conversation history
- **Voice Recognition**: Use voice commands (Chrome/Edge recommended)
- **Secure Authentication**: JWT-based token authentication

## Production Deployment

### Backend
1. Set proper environment variables
2. Use a production WSGI server like Gunicorn:
   ```bash
   gunicorn -w 4 -k uvicorn.workers.UvicornWorker app:app
   ```
3. Configure CORS to allow only your frontend domain
4. Use a proper database instead of in-memory storage

### Frontend
1. Build the production bundle:
   ```bash
   npm run build
   ```
2. Serve the `build` folder using a web server (Nginx, Apache, etc.)
3. Update `REACT_APP_API_URL` to your production backend URL

## Troubleshooting

### Backend Issues
- **Import Errors**: Make sure all dependencies are installed with `pip install -r requirements.txt`
- **Port Already in Use**: Change the port in `app.py` from 8000 to another port

### Frontend Issues
- **API Connection Failed**: Verify the backend is running on port 8000
- **Voice Recognition Not Working**: Use Chrome or Edge browser
- **Login Issues**: Check browser console for errors and verify backend is running

## Technology Stack

### Backend
- FastAPI - Modern Python web framework
- JWT - Authentication
- Pydantic - Data validation
- Uvicorn - ASGI server

### Frontend
- React - UI library
- React Router - Routing
- Axios - HTTP client
- Lottie - Animations
- Context API - State management

## Security Notes
- Default SECRET_KEY is insecure - change it in production
- User passwords are hashed using bcrypt
- CORS is set to allow all origins - restrict in production
- JWT tokens expire after 24 hours

## Future Enhancements
- Database integration (PostgreSQL, MongoDB)
- Real AI integration (OpenAI GPT-4, Whisper)
- User profile management
- Assistant conversation history
- Voice response (text-to-speech)
- Multi-language support
