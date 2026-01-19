# Quick Setup Guide - Internet Book Search

## ⚡ Quick Start (5 minutes)

### Step 1: Get Groq API Key (2 min)
```
1. Go to https://console.groq.com/keys
2. Sign up (free)
3. Click "Create New Secret Key"
4. Copy the key
```

### Step 2: Configure .env (1 min)
```bash
# In SmartEdu/ directory, create or edit .env file:

GROQ_API_KEY=paste_your_key_here
SECRET_KEY=dev-secret-key-change-in-production
```

### Step 3: Install Requirements (1 min - already done!)
```bash
# If not already done:
pip install -r requirements.txt
```

### Step 4: Run Application (1 min)
```bash
python run.py
```

### Step 5: Test It! (0 min)
1. Go to http://localhost:5000/elibrary
2. Click "🌐 Search All Internet Books"
3. Search for any book (e.g., "Pride and Prejudice")
4. Click "📖 Read Now" and it opens the book!

---

## 🎯 What You Can Do Now

| Feature | Where | What It Does |
|---------|-------|--------------|
| **Search Internet Books** | E-Library page | Access millions of free books |
| **Find Online Button** | Any book detail | Search internet for that specific book |
| **Browse Classics** | Internet Library | See popular free books |
| **Quick Search** | Search results | Find books from multiple sources |

---

## 📚 Popular Books to Try

- "Pride and Prejudice" by Jane Austen
- "1984" by George Orwell  
- "To Kill a Mockingbird" by Harper Lee
- "The Great Gatsby" by F. Scott Fitzgerald
- "Jane Eyre" by Charlotte Brontë
- "Moby Dick" by Herman Melville

---

## ✅ Verification Checklist

Make sure everything is working:

```bash
# Check Groq is installed
pip list | grep groq
# Output: groq 0.9.0

# Check Flask runs
python run.py
# Visit http://localhost:5000

# Test E-Library
# Visit http://localhost:5000/elibrary

# Try a search
# Click "Search All Internet Books" → Search "Pride and Prejudice"
```

---

## 🚨 Troubleshooting

| Problem | Solution |
|---------|----------|
| "No GROQ_API_KEY found" | Add `GROQ_API_KEY=your_key` to `.env` file |
| "Connection timeout" | Check internet connection, verify API key |
| "No results found" | Try different book title or author name |
| "Search is slow" | Normal! Internet search takes 2-10 seconds for best results |

---

## 📖 Documentation

For detailed information:
- See `ELIBRARY_INTERNET_SEARCH.md` for complete documentation
- Check `requirements.txt` for all dependencies
- View source code in `app/services/book_search_service.py`

---

## 🎉 You're All Set!

Your E-Library now has access to **millions of books from across the internet**!

Happy reading! 📚✨

---

**Need Help?**
1. Check the detailed guide: `ELIBRARY_INTERNET_SEARCH.md`
2. Verify `.env` file has your Groq API key
3. Ensure all requirements are installed: `pip install -r requirements.txt`
4. Check that Flask app runs: `python run.py`
