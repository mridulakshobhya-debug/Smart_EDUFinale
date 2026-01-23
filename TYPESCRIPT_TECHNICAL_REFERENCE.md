# TypeScript Course - Technical Reference

## 📚 Data Structure Reference

### 1. TYPESCRIPT_MASTERY_MODULES

**File Location:** `SmartEDU/app/elearning/routes.py` (Lines 175-196)

**Structure:**
```python
TYPESCRIPT_MASTERY_MODULES = {
    'ts-module{n}': {
        'name': 'Step {n}: {Module Title}',
        'lessons': 4
    },
    # ... 21 modules total
}
```

**All Module IDs:**
- ts-module1 through ts-module21

**Properties:**
- `name` (str): Full module title starting with "Step X:"
- `lessons` (int): Always 4 lessons per module

**Example:**
```python
'ts-module1': {
    'name': 'Step 1: TypeScript Setup & Compiler Basics',
    'lessons': 4
}
```

---

### 2. TYPESCRIPT_MASTERY_MODULE_DETAILS

**File Location:** `SmartEDU/app/elearning/routes.py` (Lines 1950-2460)

**Structure:**
```python
TYPESCRIPT_MASTERY_MODULE_DETAILS = {
    'ts-module{n}': {
        'title': str,                    # Module title
        'description': str,              # Brief description
        'video_url': str,                # YouTube embed URL
        'video_duration': str,           # Duration string
        'information': str,              # Rich HTML content
        'learning_objectives': list,     # Array of objectives
        'quiz_questions': list           # Array of question objects
    },
    # ... 21 modules total
}
```

**Detailed Property Descriptions:**

#### title
- Type: `str`
- Example: `'Step 1: TypeScript Setup & Compiler Basics'`
- Used in: Module header display

#### description
- Type: `str`
- Example: `'Install TypeScript, create your first file, and compile to JavaScript'`
- Used in: Course module listings

#### video_url
- Type: `str`
- Format: `'https://www.youtube.com/embed/{VIDEO_ID}?controls=1&modestbranding=0&rel=0&autoplay=0'`
- Example: `'https://www.youtube.com/embed/BCg4ti0gP9E?controls=1&modestbranding=0&rel=0&autoplay=0'`
- URL Parameters:
  - `controls=1`: Show playback controls
  - `modestbranding=0`: Cleaner YouTube interface
  - `rel=0`: Don't show related videos
  - `autoplay=0`: Don't autoplay

#### video_duration
- Type: `str`
- Examples: `'1.5 hours'`, `'1 hour'`, `'2 hours'`, `'3 hours'`, `'4 hours'`
- Used for: Time management display

#### information
- Type: `str` (HTML content)
- Format: Rich HTML with `<h3>`, `<h4>`, `<p>`, `<ul>`, `<pre>` tags
- Structure:
  ```html
  <h3>🧩 STEP {n}: {Title}</h3>
  <h4>Step {n}.1: {Subsection}</h4>
  <pre>Code examples</pre>
  <h4>Step {n}.2: {Subsection}</h4>
  ```
- Contains: Learning material, code examples, instructions

#### learning_objectives
- Type: `list` of `str`
- Count: 4-5 objectives per module
- Format: Action-oriented statements
- Examples:
  - `'Install TypeScript globally'`
  - `'Write typed TypeScript code'`
  - `'Compile TS to JS'`
  - `'Understand transpilation process'`

#### quiz_questions
- Type: `list` of `dict`
- Count: 2-3 questions per module
- Structure:
  ```python
  [
    {
      'question': str,      # Question text
      'options': list[str], # 4 answer options
      'correct': int,       # Index of correct answer (0-3)
      'explanation': str    # Explanation for correct answer
    },
    # ... 2-3 questions per module
  ]
  ```

**Example Quiz Question:**
```python
{
    'question': 'What command installs TypeScript globally?',
    'options': [
        'npm install typescript',
        'npm install -g typescript',
        'npm setup typescript',
        'tsc install'
    ],
    'correct': 1,  # Index of 'npm install -g typescript'
    'explanation': 'npm install -g typescript installs TypeScript globally.'
}
```

---

## 🔧 Route Handlers

### 1. course_detail(course_id)

**File Location:** `SmartEDU/app/elearning/routes.py` (Line 2701)

**Decorator:** `@elearning.route('/elearning/course/<course_id>')`

**Parameters:**
- `course_id` (str): Course identifier (e.g., 'typescript')

**TypeScript Handling (Lines 2743-2750):**
```python
if course_id == 'typescript':
    modules = TYPESCRIPT_MASTERY_MODULES
    return render_template('course_modules.html', 
                         course_name=course_name,
                         course_id=course_id,
                         modules=modules,
                         is_enrolled=is_enrolled)
```

**Return Value:**
- Template: `course_modules.html`
- Context:
  - `course_name`: 'TypeScript for Developers'
  - `course_id`: 'typescript'
  - `modules`: TYPESCRIPT_MASTERY_MODULES dict
  - `is_enrolled`: boolean

**Session Requirements:**
- Requires `'enrolled_courses'` in session (auto-created if missing)

---

### 2. enroll_course(course_id)

**File Location:** `SmartEDU/app/elearning/routes.py` (Line 2756)

**Decorator:** `@elearning.route('/elearning/course/<course_id>/enroll')`

**Parameters:**
- `course_id` (str): Course identifier

**TypeScript Handling (Line 2765):**
```python
if course_id in ['python-basics', 'python-advanced', 'javascript', 'typescript']:
    return redirect(url_for('elearning.course_detail', course_id=course_id))
```

**Actions:**
1. Initialize `session['enrolled_courses']` if missing
2. Add course_id to enrolled_courses list
3. Mark session as modified
4. Redirect to course_detail route

**Return Value:**
- Redirect to `/elearning/course/typescript`

---

### 3. module_detail(course_id, module_id)

**File Location:** `SmartEDU/app/elearning/routes.py` (Line 2773)

**Decorator:** `@elearning.route('/elearning/course/<course_id>/module/<module_id>')`

**Parameters:**
- `course_id` (str): Course identifier (e.g., 'typescript')
- `module_id` (str): Module identifier (e.g., 'ts-module1')

**TypeScript Handling (Lines 2799-2801):**
```python
elif course_id == 'typescript':
    module = TYPESCRIPT_MASTERY_MODULES.get(module_id, {'name': 'Module Not Found'})
    module_info = TYPESCRIPT_MASTERY_MODULE_DETAILS.get(module_id, {})
```

**Return Value:**
- Template: `module_detail.html`
- Context:
  - `course_name`: 'TypeScript for Developers'
  - `course_id`: 'typescript'
  - `module_name`: Module title from TYPESCRIPT_MASTERY_MODULES
  - `module_id`: 'ts-module{n}'
  - `module_info`: Full module details dict
  - `is_enrolled`: boolean

**Module Info Contains:**
- title, description, video_url, video_duration
- information (HTML content)
- learning_objectives (list)
- quiz_questions (list of question dicts)

---

### 4. submit_quiz(course_id, module_id)

**File Location:** `SmartEDU/app/elearning/routes.py` (Line 2835)

**Decorator:** `@elearning.route('/api/course/<course_id>/module/<module_id>/submit-quiz', methods=['POST'])`

**Parameters:**
- `course_id` (str): Course identifier
- `module_id` (str): Module identifier
- Request Body (JSON):
  ```json
  {
    "answers": [0, 1, 2]  // Array of selected option indices
  }
  ```

**TypeScript Handling (Lines 2844-2845):**
```python
elif course_id == 'typescript':
    module_info = TYPESCRIPT_MASTERY_MODULE_DETAILS.get(module_id, {})
```

**Processing:**
1. Extract answers from JSON request
2. Retrieve module_info from TYPESCRIPT_MASTERY_MODULE_DETAILS
3. Get quiz_questions from module_info
4. Compare each answer with correct answer
5. Calculate score percentage
6. Generate explanation for each question

**JSON Response:**
```json
{
  "score": 100,
  "correct_count": 2,
  "total_questions": 2,
  "passed": true,
  "results": [
    {
      "question_index": 0,
      "is_correct": true,
      "explanation": "Explanation text"
    },
    {
      "question_index": 1,
      "is_correct": true,
      "explanation": "Explanation text"
    }
  ]
}
```

**Response Properties:**
- `score` (int): Percentage score (0-100)
- `correct_count` (int): Number of correct answers
- `total_questions` (int): Total questions in quiz
- `passed` (bool): True if score >= 70
- `results` (list): Array of result objects
  - `question_index` (int): Question number (0-indexed)
  - `is_correct` (bool): Whether answer correct
  - `explanation` (str): Correct answer explanation

---

## 📊 Integration Points

### Template Integration

**Template:** `module_detail.html`

**Context Variables Used:**
```python
{
    'course_name': 'TypeScript for Developers',
    'course_id': 'typescript',
    'module_name': 'Step 1: TypeScript Setup & Compiler Basics',
    'module_id': 'ts-module1',
    'module_info': {
        'title': '...',
        'description': '...',
        'video_url': '...',
        'video_duration': '...',
        'information': '...',
        'learning_objectives': [...],
        'quiz_questions': [...]
    },
    'is_enrolled': True
}
```

**JavaScript Integration:**
```javascript
// Quiz submission via AJAX
fetch('/api/course/typescript/module/ts-module1/submit-quiz', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({answers: [0, 1]})
})
.then(response => response.json())
.then(data => {
    // Display score: data.score
    // Display passed: data.passed
    // Display results: data.results
})
```

---

## 🔌 URL Routing Map

### Course Routes
```
GET  /elearning/course/typescript
     ↓
course_detail('typescript')
     ↓
course_modules.html
```

### Enrollment Route
```
GET  /elearning/course/typescript/enroll
     ↓
enroll_course('typescript')
     ↓
Redirect: /elearning/course/typescript
```

### Module Routes (for each of 21 modules)
```
GET  /elearning/course/typescript/module/ts-module{n}
     ↓
module_detail('typescript', 'ts-module{n}')
     ↓
module_detail.html
```

### Quiz API Routes (for each of 21 modules)
```
POST /api/course/typescript/module/ts-module{n}/submit-quiz
     ↓
submit_quiz('typescript', 'ts-module{n}')
     ↓
JSON Response {score, correct_count, total_questions, passed, results}
```

---

## 🎯 Configuration Details

### Course Configuration

**In COURSES dict (Line 14):**
```python
'typescript': {
    'name': 'TypeScript for Developers',
    'instructor': 'Sarah Johnson',
    'level': 'Intermediate'
}
```

### Video Embedding Parameters

**All YouTube URLs use:**
```
https://www.youtube.com/embed/{VIDEO_ID}?controls=1&modestbranding=0&rel=0&autoplay=0
```

**Parameters Explanation:**
- `controls=1`: Show standard player controls (play, volume, etc.)
- `modestbranding=0`: Cleaner interface without YouTube branding
- `rel=0`: Don't show suggested videos at the end
- `autoplay=0`: Don't start playing automatically

### Quiz Scoring Logic

**Passing Score:** 70%

```python
score = int((correct_count / total_questions) * 100)
passed = score >= 70
```

**Example:**
- 2/2 correct = 100% = PASSED ✓
- 2/3 correct = 67% = FAILED ✗
- 3/4 correct = 75% = PASSED ✓

---

## 🔍 Data Retrieval Examples

### Getting Module from Course
```python
course_id = 'typescript'
module_id = 'ts-module1'

# Get module metadata
module = TYPESCRIPT_MASTERY_MODULES.get(module_id)
# Returns: {'name': 'Step 1: TypeScript Setup & Compiler Basics', 'lessons': 4}

# Get full module details
module_info = TYPESCRIPT_MASTERY_MODULE_DETAILS.get(module_id)
# Returns: {'title': '...', 'description': '...', 'video_url': '...', ...}

# Get quiz questions
quiz_questions = module_info.get('quiz_questions', [])
# Returns: [{'question': '...', 'options': [...], 'correct': 1, 'explanation': '...'}, ...]
```

### Getting All Modules for Course
```python
course_id = 'typescript'

# Get all modules for listing
modules = TYPESCRIPT_MASTERY_MODULES
# Returns: {'ts-module1': {...}, 'ts-module2': {...}, ..., 'ts-module21': {...}}

# Iterate through modules
for module_id, module_info in modules.items():
    print(f"{module_id}: {module_info['name']}")
```

### Checking Enrollment Status
```python
course_id = 'typescript'

# Check if user enrolled
is_enrolled = course_id in session.get('enrolled_courses', [])

# Add to enrollment
if course_id not in session['enrolled_courses']:
    session['enrolled_courses'].append(course_id)
    session.modified = True
```

---

## 🛠 Maintenance & Updates

### Adding New Module

To add a 22nd module:

1. **Add to TYPESCRIPT_MASTERY_MODULES:**
```python
'ts-module22': {'name': 'Step 22: Advanced Topic', 'lessons': 4},
```

2. **Add to TYPESCRIPT_MASTERY_MODULE_DETAILS:**
```python
'ts-module22': {
    'title': 'Step 22: Advanced Topic',
    'description': '...',
    'video_url': '...',
    'video_duration': '...',
    'information': '...',
    'learning_objectives': [...],
    'quiz_questions': [...]
}
```

3. No route changes needed (routes are dynamic)

### Updating Quiz for Module

```python
'ts-module1': {
    ...
    'quiz_questions': [
        {
            'question': 'Updated question?',
            'options': ['option1', 'option2', 'option3', 'option4'],
            'correct': 0,  # Index of correct answer
            'explanation': 'Explanation text'
        }
    ]
}
```

### Updating Video URL

```python
'ts-module1': {
    ...
    'video_url': 'https://www.youtube.com/embed/NEW_VIDEO_ID?controls=1&modestbranding=0&rel=0&autoplay=0',
    ...
}
```

---

## 📈 Performance Optimization

### Current Performance
- **Module Load:** O(1) - Direct dict lookup
- **Module Details:** O(1) - Direct dict lookup
- **Quiz Processing:** O(n) where n = number of questions
- **Response Time:** < 500ms for quiz submission

### Optimization Opportunities
- Cache frequently accessed modules
- Pre-compile HTML content
- Implement database storage for quiz results
- Add pagination for large course listings

---

## 🔐 Security Considerations

### Current Security Features
- ✅ Session-based enrollment tracking
- ✅ Input validation on quiz submission
- ✅ JSON response validation
- ✅ Error handling for missing modules

### Future Security Enhancements
- [ ] User authentication required for enrollment
- [ ] Quiz submission verification
- [ ] Database storage for audit trail
- [ ] Rate limiting on API endpoints
- [ ] CSRF protection on quiz submission

---

## 📝 Debugging Tips

### Check Module Loading
```python
# In Python shell
module = TYPESCRIPT_MASTERY_MODULES.get('ts-module1')
print(module['name'])  # Should print: "Step 1: TypeScript Setup & Compiler Basics"
```

### Check Module Details
```python
details = TYPESCRIPT_MASTERY_MODULE_DETAILS.get('ts-module1')
print(details.keys())  # Should show: dict_keys(['title', 'description', 'video_url', ...])
```

### Debug Quiz Submission
```python
# Check browser console for AJAX errors
# Check Flask logs for server-side errors
# Verify JSON request format matches expected schema
```

### Verify Enrollment
```python
# Check session in browser DevTools
# Application → Cookies → Check session cookie
# Or add print statements in enroll_course()
```

---

*TypeScript Course - Technical Reference v1.0*
*For implementation details, see: TYPESCRIPT_IMPLEMENTATION_SUMMARY.md*
*For user guides, see: TYPESCRIPT_USER_ACCESS_GUIDE.md*
