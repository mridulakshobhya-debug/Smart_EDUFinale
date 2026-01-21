# SmartEDU Pro - Developer Guide

## 🏗️ Architecture Overview

### Project Structure
```
SmartEDU/
├── app/
│   ├── __init__.py           # App factory and initialization
│   ├── models.py             # Database models (User, Course, Book, etc.)
│   ├── auth/                 # Authentication blueprint
│   │   └── routes.py
│   ├── main/                 # Main routes (home, course editor)
│   │   └── routes.py
│   ├── elearning/            # E-learning courses
│   │   └── routes.py
│   ├── elibrary/             # Digital library
│   │   └── routes.py
│   ├── services/             # Business logic
│   │   └── book_search_service.py
│   └── static/
│       ├── css/
│       │   └── styles_enhanced.css   # Professional UI styling
│       └── js/
│           └── main.js       # JavaScript functionality
├── templates/
│   ├── base_enhanced.html    # Master template
│   ├── index_animated.html   # Home page with slideshow
│   ├── elearning.html        # Course listing
│   ├── course_editor.html    # ⭐ Interactive code editor
│   ├── elibrary.html         # Books and resources
│   ├── login.html            # Authentication
│   ├── signup.html
│   ├── profile.html          # User dashboard
│   └── navbar_enhanced.html  # Navigation component
├── config.py                 # Configuration
├── run.py                    # Application entry point
├── requirements.txt          # Python dependencies
└── smartedu.db              # SQLite database
```

---

## 🎨 Design System

### Typography
```css
/* Headings - Outfit */
h1, h2, h3, h4, h5, h6 {
    font-family: 'Outfit', sans-serif;
    font-weight: 700;
    letter-spacing: -0.5px;
}

/* Body Text - Inter */
body {
    font-family: 'Inter', sans-serif;
    letter-spacing: -0.3px;
}

/* Utility Classes */
.font-outfit { font-family: 'Outfit', sans-serif; }
.font-inter { font-family: 'Inter', sans-serif; }
```

### Color Palette
```css
:root {
    /* Brand Colors */
    --primary: #667eea;      /* Purple-Blue */
    --secondary: #764ba2;    /* Rich Purple */
    --accent: #f093fb;       /* Pink */
    
    /* Semantic Colors */
    --success: #10b981;      /* Green */
    --danger: #ef4444;       /* Red */
    --warning: #f59e0b;      /* Amber */
    --info: #3b82f6;         /* Blue */
    
    /* Neutral Colors */
    --text-primary: #1f2937;
    --text-secondary: #6b7280;
    --text-tertiary: #9ca3af;
    --bg-primary: #ffffff;
    --bg-secondary: #f9fafb;
    --border: #e5e7eb;
}

/* Dark Mode Override */
[data-theme="dark"] {
    --text-primary: #f9fafb;
    --bg-primary: #111827;
    --bg-secondary: #1f2937;
    --border: #374151;
}
```

### Animation Timings
```css
--transition-fast: 0.15s cubic-bezier(0.4, 0, 0.2, 1);
--transition-base: 0.3s cubic-bezier(0.4, 0, 0.2, 1);
--transition-slow: 0.5s cubic-bezier(0.4, 0, 0.2, 1);
```

---

## 🔧 Backend Development

### Flask Application Setup
```python
# app/__init__.py
from flask import Flask
from flask_login import LoginManager
from .models import db, init_db

def create_app():
    app = Flask(__name__)
    app.config.from_object("config.Config")
    
    db.init_app(app)
    login_manager.init_app(app)
    
    # Register blueprints
    app.register_blueprint(main)
    app.register_blueprint(auth)
    app.register_blueprint(elearning)
    app.register_blueprint(elibrary)
    
    return app
```

### Database Models
```python
# app/models.py
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    full_name = db.Column(db.String(120))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    # Relationships
    courses = db.relationship('Course', backref='instructor', lazy=True)
    enrollments = db.relationship('Enrollment', backref='user', lazy=True)

class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    instructor_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    level = db.Column(db.String(20))  # Beginner, Intermediate, Advanced
    category = db.Column(db.String(50))
    # Relationships
    modules = db.relationship('Module', backref='course', lazy=True)
    enrollments = db.relationship('Enrollment', backref='course', lazy=True)
```

### API Endpoints

#### Execute Code
```python
@main.route('/api/execute-code', methods=['POST'])
def execute_code():
    """Execute Python or JavaScript code"""
    data = request.json
    code = data.get('code', '')
    language = data.get('language', 'python')
    
    try:
        import subprocess
        result = subprocess.run(
            ['python', '-c', code],
            capture_output=True,
            text=True,
            timeout=5
        )
        
        return jsonify({
            "success": result.returncode == 0,
            "output": result.stdout or result.stderr
        })
    except subprocess.TimeoutExpired:
        return jsonify({
            "success": False,
            "error": "Code execution timeout (max 5 seconds)"
        })
```

#### Course Routes
```python
@elearning.route('/courses')
def get_courses():
    """Get all courses with optional filtering"""
    level = request.args.get('level')
    category = request.args.get('category')
    
    query = Course.query
    if level:
        query = query.filter_by(level=level)
    if category:
        query = query.filter_by(category=category)
    
    courses = query.all()
    return jsonify([course.to_dict() for course in courses])

@elearning.route('/courses/<int:course_id>')
def get_course(course_id):
    """Get specific course with modules"""
    course = Course.query.get_or_404(course_id)
    return render_template('course_editor.html', course=course)
```

---

## 💻 Frontend Development

### Component Structure

#### Course Editor Component
```html
<!-- Left Sidebar: Lessons -->
<div class="course-sidebar">
    <div class="lesson-item active">
        <span class="icon">1️⃣</span>
        <span>Getting Started</span>
    </div>
</div>

<!-- Center: Editor & Output -->
<div class="course-main">
    <div class="editor-panel">
        <textarea class="code-editor"></textarea>
    </div>
    <div class="output-panel">
        <div id="outputConsole"></div>
    </div>
</div>

<!-- Right Sidebar: Controls -->
<div class="course-controls">
    <button class="run-button" onclick="runCode()">Run Code</button>
</div>
```

### JavaScript Classes

#### SmartThemeManager
```javascript
class SmartThemeManager {
    constructor() {
        this.storageKey = 'smartedu-theme';
        this.init();
    }
    
    init() {
        this.loadTheme();
        this.setupEventListeners();
    }
    
    setTheme(theme) {
        document.documentElement.setAttribute('data-theme', theme);
        localStorage.setItem(this.storageKey, theme);
        this.showNotification(theme);
    }
    
    toggleTheme() {
        const current = document.documentElement.getAttribute('data-theme');
        this.setTheme(current === 'light' ? 'dark' : 'light');
    }
}
```

### Event Handling
```javascript
// Run Code Function
async function runCode() {
    const code = document.getElementById('codeEditor').value;
    
    const response = await fetch('/api/execute-code', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ code, language: 'python' })
    });
    
    const data = await response.json();
    updateOutput(data);
}

// Update Output Display
function updateOutput(data) {
    const output = document.getElementById('outputConsole');
    if (data.success) {
        output.innerHTML = `<div class="output-success">${data.output}</div>`;
    } else {
        output.innerHTML = `<div class="output-error">${data.error}</div>`;
    }
}
```

---

## 🚀 Deployment

### Production Setup
```bash
# Install dependencies
pip install -r requirements.txt

# Set environment variables
export FLASK_ENV=production
export SECRET_KEY=your-secret-key
export DATABASE_URL=postgresql://user:pass@localhost/smartedu

# Run with production server
gunicorn app:app -w 4
```

### Docker Deployment
```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["gunicorn", "app:app", "-w", "4", "-b", "0.0.0.0:5000"]
```

### Nginx Configuration
```nginx
server {
    listen 80;
    server_name smartedu.com;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    location /static/ {
        alias /app/static/;
        expires 1y;
    }
}
```

---

## 📊 Database Schema

### Key Tables
```sql
-- Users
CREATE TABLE user (
    id INTEGER PRIMARY KEY,
    username VARCHAR(80) UNIQUE,
    email VARCHAR(120) UNIQUE,
    password VARCHAR(200),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Courses
CREATE TABLE course (
    id INTEGER PRIMARY KEY,
    name VARCHAR(200),
    description TEXT,
    category VARCHAR(50),
    level VARCHAR(20),
    instructor_id INTEGER FOREIGN KEY REFERENCES user(id)
);

-- Modules/Lessons
CREATE TABLE module (
    id INTEGER PRIMARY KEY,
    course_id INTEGER FOREIGN KEY,
    title VARCHAR(200),
    description TEXT,
    content TEXT,
    order_index INTEGER
);

-- Enrollments
CREATE TABLE enrollment (
    id INTEGER PRIMARY KEY,
    user_id INTEGER FOREIGN KEY,
    course_id INTEGER FOREIGN KEY,
    enrolled_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    completed_at DATETIME
);
```

---

## 🔐 Security Best Practices

### Code Execution Safety
```python
# Sandboxed execution
def safe_execute_code(code, timeout=5):
    try:
        # Run in subprocess to isolate execution
        result = subprocess.run(
            ['python', '-c', code],
            capture_output=True,
            timeout=timeout,
            cwd='/tmp'  # Isolated directory
        )
        return result
    except subprocess.TimeoutExpired:
        return "Error: Execution timeout"
```

### Input Validation
```python
def validate_code_input(code):
    # Check code length
    if len(code) > 10000:
        raise ValueError("Code too long")
    
    # Block dangerous imports
    dangerous = ['os', 'sys', 'subprocess', '__import__']
    for item in dangerous:
        if item in code:
            raise ValueError("Dangerous code detected")
    
    return code
```

### CSRF Protection
```python
from flask_wtf.csrf import CSRFProtect

csrf = CSRFProtect(app)

# In forms
<form method="POST">
    {{ csrf_token() }}
    ...
</form>
```

---

## 🧪 Testing

### Unit Tests
```python
import unittest

class TestCourseEditor(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()
    
    def test_course_editor_loads(self):
        response = self.client.get('/course-editor')
        self.assertEqual(response.status_code, 200)
    
    def test_execute_code_success(self):
        response = self.client.post('/api/execute-code', json={
            'code': 'print("Hello")',
            'language': 'python'
        })
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertTrue(data['success'])
```

### Running Tests
```bash
python -m pytest tests/
python -m unittest discover
```

---

## 📈 Performance Optimization

### Frontend Optimization
```javascript
// Lazy Loading
const images = document.querySelectorAll('[data-src]');
const imageObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.src = entry.target.dataset.src;
        }
    });
});
images.forEach(img => imageObserver.observe(img));

// Code Splitting
const courseEditor = dynamic(() => import('./course-editor'));
```

### Backend Optimization
```python
# Database Query Optimization
courses = Course.query.join(User).filter(
    User.id == current_user.id
).options(
    joinedload(Course.modules)
).all()

# Caching
@app.cache.cached(timeout=3600)
def get_popular_courses():
    return Course.query.order_by(Course.rating.desc()).limit(10).all()
```

---

## 🔄 Continuous Integration

### GitHub Actions
```yaml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.9'
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install pytest
      - name: Run tests
        run: pytest tests/
```

---

## 📚 Contributing Guidelines

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/amazing-feature`)
3. **Commit** changes (`git commit -m 'Add amazing feature'`)
4. **Push** to branch (`git push origin feature/amazing-feature`)
5. **Open** a Pull Request

### Code Style
- PEP 8 for Python
- ESLint for JavaScript
- 4-space indentation
- Meaningful variable names

---

## 🐛 Debugging

### Browser DevTools
```javascript
// Check theme
console.log(document.documentElement.getAttribute('data-theme'));

// Test API
fetch('/api/execute-code', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ code: 'print("test")', language: 'python' })
}).then(r => r.json()).then(console.log);
```

### Server Debugging
```python
# Enable debug mode
app.debug = True
app.config['DEBUG'] = True

# Add logging
import logging
logging.basicConfig(level=logging.DEBUG)
```

---

## 📖 Additional Resources

- [Flask Documentation](https://flask.palletsprojects.com/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [Bootstrap 5](https://getbootstrap.com/)
- [MDN Web Docs](https://developer.mozilla.org/)

---

**Happy Coding! 🚀**

Version 2.0 - Updated 2024
