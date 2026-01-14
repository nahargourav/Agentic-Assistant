# 🚀 QUICK START GUIDE - Assistant App

## Get Running in 5 Minutes!

### Step 1: Start Backend (2 minutes)
```powershell
# Open PowerShell in the Assistant folder
cd Backend

# Create virtual environment
python -m venv venv
.\venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Start server
python app.py
```
✅ Backend running at http://localhost:8000

---

### Step 2: Start Frontend (3 minutes)
```powershell
# Open NEW PowerShell window in the Assistant folder
cd Frontend

# Install dependencies (first time only)
npm install

# Start development server
npm start
```
✅ Frontend running at http://localhost:3000

---

### Step 3: Use the App!

#### Register (First Time):
1. Click "Get Started"
2. Enter: Name, Email, Password
3. Click "Sign Up"

#### Login:
1. Click "Sign In"
2. Enter your email and password
3. Click "Sign In"

#### Chat with Assistant:
- **Type**: Enter text and click "Send"
- **Speak**: Click 🎤, speak, then click "Stop"

#### Toggle Theme:
- Click 🌙/☀️ in header to switch themes

---

## That's It! 🎉

Your AI Assistant is now running and ready to use!

### Need Help?
- See [README.md](README.md) for detailed setup
- See [FIX_REPORT.md](FIX_REPORT.md) for all fixes applied
- Check backend console for API logs
- Check browser console (F12) for frontend errors

### Common Issues:
- **Port already in use**: Close other apps or change port
- **Module not found**: Run `pip install -r requirements.txt`
- **npm errors**: Delete `node_modules`, run `npm install` again
- **Voice not working**: Use Chrome/Edge browser, allow mic access
