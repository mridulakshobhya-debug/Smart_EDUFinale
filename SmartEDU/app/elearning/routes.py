# E-Learning Routes
from flask import Blueprint, render_template, session, jsonify, request, redirect, url_for
from flask_login import login_required, current_user
from ..models import db, Module, Quiz, UserProgress

elearning = Blueprint('elearning', __name__)

# Enhanced course data - 50+ comprehensive courses
COURSES = {
    # Programming Languages (15 courses)
    'python-basics': {'name': 'Python Basics', 'instructor': 'John Smith', 'level': 'Beginner'},
    'python-advanced': {'name': 'Advanced Python Programming', 'instructor': 'John Smith', 'level': 'Advanced'},
    'javascript': {'name': 'JavaScript Mastery', 'instructor': 'Sarah Johnson', 'level': 'Intermediate'},
    'typescript': {'name': 'TypeScript for Developers', 'instructor': 'Sarah Johnson', 'level': 'Intermediate'},
    'java-basics': {'name': 'Java Programming Basics', 'instructor': 'Alex Kumar', 'level': 'Beginner'},
    'java-advanced': {'name': 'Advanced Java Programming', 'instructor': 'Alex Kumar', 'level': 'Advanced'},
    'cpp': {'name': 'C++ Programming', 'instructor': 'Prof. Andrei Alekseyev', 'level': 'Intermediate'},
    'csharp': {'name': 'C# and .NET Development', 'instructor': 'Marcus Johnson', 'level': 'Intermediate'},
    'rust': {'name': 'Rust Programming', 'instructor': 'Emma Wilson', 'level': 'Intermediate'},
    'golang': {'name': 'Go (Golang) Programming', 'instructor': 'David Zhang', 'level': 'Intermediate'},
    'swift': {'name': 'Swift for iOS Development', 'instructor': 'Lisa Park', 'level': 'Intermediate'},
    'kotlin': {'name': 'Kotlin Programming', 'instructor': 'Daniel Lee', 'level': 'Beginner'},
    'php': {'name': 'PHP Web Development', 'instructor': 'Robert Brown', 'level': 'Beginner'},
    'ruby': {'name': 'Ruby on Rails Development', 'instructor': 'Jennifer White', 'level': 'Intermediate'},
    'scala': {'name': 'Scala Functional Programming', 'instructor': 'Victor Chen', 'level': 'Advanced'},
    
    # Web Development (10 courses)
    'web-dev': {'name': 'Full Stack Web Development', 'instructor': 'Mike Chen', 'level': 'Advanced'},
    'html-css': {'name': 'HTML & CSS Fundamentals', 'instructor': 'Nina Patel', 'level': 'Beginner'},
    'responsive-design': {'name': 'Responsive Web Design', 'instructor': 'Nina Patel', 'level': 'Intermediate'},
    'react': {'name': 'React.js Mastery', 'instructor': 'Tom Brady', 'level': 'Intermediate'},
    'angular': {'name': 'Angular Framework', 'instructor': 'Kevin Smith', 'level': 'Intermediate'},
    'vue': {'name': 'Vue.js Development', 'instructor': 'Grace Liu', 'level': 'Beginner'},
    'node-js': {'name': 'Node.js Backend Development', 'instructor': 'Michael Zhang', 'level': 'Intermediate'},
    'express': {'name': 'Express.js & REST APIs', 'instructor': 'Michael Zhang', 'level': 'Intermediate'},
    'webpack': {'name': 'Webpack & Build Tools', 'instructor': 'Alex Rivera', 'level': 'Advanced'},
    'nextjs': {'name': 'Next.js Full Stack', 'instructor': 'Chris Martin', 'level': 'Advanced'},
    
    # Mobile Development (8 courses)
    'mobile-dev': {'name': 'Mobile App Development', 'instructor': 'Lisa Garcia', 'level': 'Advanced'},
    'react-native': {'name': 'React Native Development', 'instructor': 'Amanda Foster', 'level': 'Intermediate'},
    'flutter': {'name': 'Flutter App Development', 'instructor': 'Raj Patel', 'level': 'Intermediate'},
    'android': {'name': 'Android Development', 'instructor': 'James Wilson', 'level': 'Intermediate'},
    'ios-dev': {'name': 'iOS App Development', 'instructor': 'Rachel Green', 'level': 'Intermediate'},
    'xamarin': {'name': 'Xamarin Cross-Platform', 'instructor': 'David Miller', 'level': 'Advanced'},
    'progressive-web': {'name': 'Progressive Web Apps (PWA)', 'instructor': 'Sarah Chen', 'level': 'Intermediate'},
    'mobile-testing': {'name': 'Mobile App Testing', 'instructor': 'Omar Hassan', 'level': 'Intermediate'},
    
    # Data Science & Analytics (10 courses)
    'data-science': {'name': 'Data Science Fundamentals', 'instructor': 'Dr. Patricia Moore', 'level': 'Intermediate'},
    'ml-basics': {'name': 'Machine Learning Fundamentals', 'instructor': 'Dr. Anna Martinez', 'level': 'Beginner'},
    'deep-learning': {'name': 'Deep Learning & Neural Networks', 'instructor': 'Prof. James Wilson', 'level': 'Advanced'},
    'nlp': {'name': 'Natural Language Processing', 'instructor': 'Dr. Lisa Brown', 'level': 'Intermediate'},
    'computer-vision': {'name': 'Computer Vision Basics', 'instructor': 'Dr. Hassan Ahmed', 'level': 'Intermediate'},
    'data-analytics': {'name': 'Data Analytics with Python', 'instructor': 'Sarah Williams', 'level': 'Beginner'},
    'pandas': {'name': 'Pandas for Data Analysis', 'instructor': 'Marcus Thompson', 'level': 'Beginner'},
    'tensorflow': {'name': 'TensorFlow & Keras', 'instructor': 'Dr. Yuki Tanaka', 'level': 'Advanced'},
    'pytorch': {'name': 'PyTorch Deep Learning', 'instructor': 'Dr. Arjun Singh', 'level': 'Advanced'},
    'sklearn': {'name': 'Scikit-Learn for ML', 'instructor': 'Elena Rossi', 'level': 'Intermediate'},
    
    # Computer Science Fundamentals (7 courses)
    'data-structures': {'name': 'Data Structures & Algorithms', 'instructor': 'Dr. Emily White', 'level': 'Intermediate'},
    'algorithms': {'name': 'Algorithm Design & Analysis', 'instructor': 'Prof. Steven Brown', 'level': 'Advanced'},
    'operating-systems': {'name': 'Operating Systems Concepts', 'instructor': 'Dr. Frank Schmidt', 'level': 'Advanced'},
    'databases': {'name': 'Database Systems', 'instructor': 'Prof. David Lee', 'level': 'Intermediate'},
    'sql': {'name': 'SQL Mastery', 'instructor': 'Jennifer Lopez', 'level': 'Beginner'},
    'nosql': {'name': 'NoSQL Databases', 'instructor': "Kevin O'Brien", 'level': 'Intermediate'},
    'system-design': {'name': 'System Design & Architecture', 'instructor': 'Dr. Raj Reddy', 'level': 'Advanced'},
    
    # Cloud & DevOps (7 courses)
    'aws': {'name': 'Amazon Web Services (AWS)', 'instructor': 'Tom Hardy', 'level': 'Intermediate'},
    'azure': {'name': 'Microsoft Azure Cloud', 'instructor': 'Chris Wilson', 'level': 'Intermediate'},
    'gcp': {'name': 'Google Cloud Platform', 'instructor': 'Priya Sharma', 'level': 'Intermediate'},
    'docker': {'name': 'Docker Containerization', 'instructor': 'Marcus Lee', 'level': 'Intermediate'},
    'kubernetes': {'name': 'Kubernetes Orchestration', 'instructor': 'Dmitri Volkov', 'level': 'Advanced'},
    'ci-cd': {'name': 'CI/CD Pipeline Automation', 'instructor': 'Sandra Kim', 'level': 'Intermediate'},
    'devops': {'name': 'DevOps Engineering', 'instructor': 'Ricardo Fernandez', 'level': 'Advanced'},
    
    # Networking & Security (5 courses)
    'networking': {'name': 'Computer Networks', 'instructor': 'Dr. Robert Kim', 'level': 'Advanced'},
    'cybersecurity': {'name': 'Cybersecurity Fundamentals', 'instructor': 'Dr. Eric Johnson', 'level': 'Intermediate'},
    'ethical-hacking': {'name': 'Ethical Hacking & Penetration Testing', 'instructor': 'Marcus Black', 'level': 'Advanced'},
    'cryptography': {'name': 'Cryptography & Encryption', 'instructor': 'Dr. Sophia Turner', 'level': 'Advanced'},
    'web-security': {'name': 'Web Security Essentials', 'instructor': 'Nathan Gray', 'level': 'Intermediate'},
    
    # Academic Subjects (15+ courses)
    'math-basics': {'name': 'Mathematics Fundamentals', 'instructor': 'Prof. Michael Johnson', 'level': 'Beginner'},
    'algebra': {'name': 'Algebra Mastery', 'instructor': 'Prof. Michael Johnson', 'level': 'Beginner'},
    'geometry': {'name': 'Geometry Essentials', 'instructor': 'Dr. Patricia Lewis', 'level': 'Beginner'},
    'calculus': {'name': 'Calculus I & II', 'instructor': 'Prof. Robert Taylor', 'level': 'Intermediate'},
    'statistics': {'name': 'Statistics & Probability', 'instructor': 'Dr. Elena Garcia', 'level': 'Intermediate'},
    'trigonometry': {'name': 'Trigonometry Mastery', 'instructor': 'Prof. David Chen', 'level': 'Beginner'},
    
    'science-basics': {'name': 'Science Fundamentals', 'instructor': 'Dr. Sarah Wilson', 'level': 'Beginner'},
    'physics': {'name': 'Physics: Mechanics & Motion', 'instructor': 'Prof. James Anderson', 'level': 'Intermediate'},
    'chemistry': {'name': 'Chemistry Essentials', 'instructor': 'Dr. Linda Martinez', 'level': 'Beginner'},
    'biology': {'name': 'Biology: Life Sciences', 'instructor': 'Prof. Emma Brown', 'level': 'Beginner'},
    'environmental-science': {'name': 'Environmental Science', 'instructor': 'Dr. Mark Phillips', 'level': 'Intermediate'},
    
    'social-studies': {'name': 'Social Studies Fundamentals', 'instructor': 'Prof. William Harris', 'level': 'Beginner'},
    'history': {'name': 'World History Overview', 'instructor': 'Dr. Thomas White', 'level': 'Beginner'},
    'geography': {'name': 'Geography & Cultures', 'instructor': 'Prof. Christopher Lee', 'level': 'Beginner'},
    'civics': {'name': 'Civics & Government', 'instructor': 'Dr. Nancy Davis', 'level': 'Beginner'},
    'economics': {'name': 'Economics Basics', 'instructor': 'Prof. Richard Miller', 'level': 'Intermediate'},
    
    'english-basics': {'name': 'English Language Fundamentals', 'instructor': 'Dr. Victoria Turner', 'level': 'Beginner'},
    'literature': {'name': 'World Literature & Classics', 'instructor': 'Prof. Caroline King', 'level': 'Intermediate'},
    'writing-skills': {'name': 'Professional Writing Skills', 'instructor': 'Dr. Benjamin Scott', 'level': 'Intermediate'},
    'grammar': {'name': 'Grammar & Composition', 'instructor': 'Prof. Amanda Green', 'level': 'Beginner'},
    'public-speaking': {'name': 'Public Speaking Mastery', 'instructor': 'Dr. Jonathan Blake', 'level': 'Intermediate'},
}

# Enhanced module data with information, videos, and quizzes
MODULES = {
    'module1': {'name': 'Module 1: Fundamentals & Getting Started', 'lessons': 4},
    'module2': {'name': 'Module 2: Intermediate Techniques & Best Practices', 'lessons': 4},
    'module3': {'name': 'Module 3: Advanced Concepts & Optimization', 'lessons': 4},
    'module4': {'name': 'Module 4: Frameworks & Tools', 'lessons': 4},
    'module5': {'name': 'Module 5: Case Studies & Real-World Applications', 'lessons': 4},
    'module6': {'name': 'Module 6: Mastery & Capstone Project', 'lessons': 4},
}

# Python-specific course modules
PYTHON_BASICS_MODULES = {
    'python-module1': {'name': 'Module 1: Python Syntax & Basics (Day 1-2)', 'lessons': 4},
    'python-module2': {'name': 'Module 2: Variables & Data Types (Day 2)', 'lessons': 4},
    'python-module3': {'name': 'Module 3: Input & Output (Day 3)', 'lessons': 4},
    'python-module4': {'name': 'Module 4: Conditions & Logic (Day 3-4)', 'lessons': 4},
    'python-module5': {'name': 'Module 5: Loops (Day 4-5)', 'lessons': 4},
    'python-module6': {'name': 'Module 6: Functions (Day 5-6)', 'lessons': 4},
    'python-module7': {'name': 'Module 7: Lists & Dictionaries (Day 6-7)', 'lessons': 4},
    'python-module8': {'name': 'Module 8: File Handling (Day 7)', 'lessons': 4},
    'python-module9': {'name': 'Module 9: Mini Projects (Day 7+)', 'lessons': 3},
}

# Advanced Python modules
PYTHON_ADVANCED_MODULES = {
    'python-adv-module1': {'name': 'Step 1: Python Internals & Memory Management', 'lessons': 4},
    'python-adv-module2': {'name': 'Step 2: Advanced Data Structures (Collections)', 'lessons': 4},
    'python-adv-module3': {'name': 'Step 3: Functions – Advanced Level', 'lessons': 4},
    'python-adv-module4': {'name': 'Step 4: Decorators (VERY IMPORTANT)', 'lessons': 4},
    'python-adv-module5': {'name': 'Step 5: Context Managers', 'lessons': 4},
    'python-adv-module6': {'name': 'Step 6: Object-Oriented Python (Deep)', 'lessons': 4},
    'python-adv-module7': {'name': 'Step 7: Iterators & Generators', 'lessons': 4},
    'python-adv-module8': {'name': 'Step 8: Error Handling & Debugging', 'lessons': 4},
    'python-adv-module9': {'name': 'Step 9: File Handling & Serialization', 'lessons': 4},
    'python-adv-module10': {'name': 'Step 10: Concurrency (Threads, Processes, Async)', 'lessons': 4},
    'python-adv-module11': {'name': 'Step 11: Performance Optimization', 'lessons': 4},
    'python-adv-module12': {'name': 'Step 12: Testing & Quality', 'lessons': 4},
    'python-adv-module13': {'name': 'Step 13: Packaging & Deployment', 'lessons': 4},
}

# JavaScript Mastery modules
JAVASCRIPT_MASTERY_MODULES = {
    'js-module1': {'name': 'Step 1: How JavaScript Works Internally', 'lessons': 4},
    'js-module2': {'name': 'Step 2: Variables, Scope & Hoisting', 'lessons': 4},
    'js-module3': {'name': 'Step 3: Data Types & Type System', 'lessons': 4},
    'js-module4': {'name': 'Step 4: Control Flow & Conditions', 'lessons': 4},
    'js-module5': {'name': 'Step 5: Loops & Iteration', 'lessons': 4},
    'js-module6': {'name': 'Step 6: Functions (Core)', 'lessons': 4},
    'js-module7': {'name': 'Step 7: Arrays & Objects', 'lessons': 4},
    'js-module8': {'name': 'Step 8: Advanced Array & Object Methods', 'lessons': 4},
    'js-module9': {'name': 'Step 9: Closures & Advanced Functions', 'lessons': 4},
    'js-module10': {'name': 'Step 10: Asynchronous JavaScript', 'lessons': 4},
    'js-module11': {'name': 'Step 11: Event Loop & Concurrency', 'lessons': 4},
    'js-module12': {'name': 'Step 12: DOM Manipulation', 'lessons': 4},
    'js-module13': {'name': 'Step 13: Browser APIs & Storage', 'lessons': 4},
    'js-module14': {'name': 'Step 14: Error Handling & Debugging', 'lessons': 4},
    'js-module15': {'name': 'Step 15: Modern JavaScript (ES6+)', 'lessons': 4},
    'js-module16': {'name': 'Step 16: Object-Oriented JavaScript', 'lessons': 4},
    'js-module17': {'name': 'Step 17: Performance & Best Practices', 'lessons': 4},
    'js-module18': {'name': 'Step 18: Mini Projects', 'lessons': 4},
    'js-module19': {'name': 'Step 19: Capstone Project', 'lessons': 4},
}

TYPESCRIPT_MASTERY_MODULES = {
    'ts-module1': {'name': 'Step 1: TypeScript Setup & Compiler Basics', 'lessons': 4},
    'ts-module2': {'name': 'Step 2: Basic Types', 'lessons': 4},
    'ts-module3': {'name': 'Step 3: Type Inference & Annotations', 'lessons': 4},
    'ts-module4': {'name': 'Step 4: Functions & Typing', 'lessons': 4},
    'ts-module5': {'name': 'Step 5: Objects & Type Aliases', 'lessons': 4},
    'ts-module6': {'name': 'Step 6: Interfaces (Core)', 'lessons': 4},
    'ts-module7': {'name': 'Step 7: Advanced Interfaces', 'lessons': 4},
    'ts-module8': {'name': 'Step 8: Union & Intersection Types', 'lessons': 4},
    'ts-module9': {'name': 'Step 9: Enums & Literal Types', 'lessons': 4},
    'ts-module10': {'name': 'Step 10: Generics (VERY IMPORTANT)', 'lessons': 4},
    'ts-module11': {'name': 'Step 11: Classes & OOP in TypeScript', 'lessons': 4},
    'ts-module12': {'name': 'Step 12: Inheritance & Abstract Classes', 'lessons': 4},
    'ts-module13': {'name': 'Step 13: Type Guards & Advanced Narrowing', 'lessons': 4},
    'ts-module14': {'name': 'Step 14: Utility Types', 'lessons': 4},
    'ts-module15': {'name': 'Step 15: Modules & Namespaces', 'lessons': 4},
    'ts-module16': {'name': 'Step 16: Compiler Configuration (tsconfig)', 'lessons': 4},
    'ts-module17': {'name': 'Step 17: TypeScript with JavaScript', 'lessons': 4},
    'ts-module18': {'name': 'Step 18: Error Handling & Debugging', 'lessons': 4},
    'ts-module19': {'name': 'Step 19: Performance & Best Practices', 'lessons': 4},
    'ts-module20': {'name': 'Step 20: Mini Projects', 'lessons': 4},
    'ts-module21': {'name': 'Step 21: Capstone Project', 'lessons': 4},
}

# Module details with information, videos, and quiz questions
PYTHON_BASICS_MODULE_DETAILS = {
    'python-module1': {
        'title': 'Python Syntax & Basics',
        'description': 'Learn how Python runs code line by line, print function, and comments',
        'video_url': 'https://www.youtube.com/embed/N4mEzFDjqtA?controls=1&modestbranding=0&rel=0&autoplay=0',
        'video_duration': '4 hours',
        'information': '''<h3>🐍 Getting Started with Python</h3>
<p><strong>📺 What's in This Video:</strong></p>
<p>This comprehensive tutorial covers: installing Python, writing your first program, understanding Python syntax, and using comments.</p>
<p style="margin-top: 15px; padding: 10px; background: var(--bg-secondary); border-left: 4px solid var(--primary); border-radius: 4px;"><strong>▶️ Play the video above to get started!</strong> It has all the controls you need (play, pause, fullscreen, etc.).</p>
<p><strong>STEP 1: Set Up Python (Day 1)</strong></p>
<ul>
<li>Install Python (latest version) from python.org</li>
<li>Install VS Code</li>
<li>Open VS Code → Install Python extension</li>
<li>Create a folder named: <code>python-basics</code></li>
<li>Create a file: <code>main.py</code></li>
</ul>
<h3>💡 What You'll Learn</h3>
<ul>
<li>✅ How Python runs code line by line</li>
<li>✅ The print() function</li>
<li>✅ Comments (#)</li>
<li>✅ Understanding output</li>
</ul>
<h3>🎯 Practice Code</h3>
<pre>print("Hello, Python")
print(5 + 3)</pre>
<p>👉 Run the file and understand output.</p>''',
        'learning_objectives': [
            'Understand how Python executes code',
            'Master the print() function',
            'Learn to use comments',
            'Practice basic output'
        ],
        'quiz_questions': [
            {
                'question': 'What is the correct file extension for a Python file?',
                'options': ['.pt', '.py', '.python', '.exe'],
                'correct': 1,
                'explanation': 'Python files use the .py extension.'
            },
            {
                'question': 'Which function is used to display output in Python?',
                'options': ['show()', 'output()', 'print()', 'display()'],
                'correct': 2,
                'explanation': 'The print() function displays output in Python.'
            },
            {
                'question': 'What symbol is used for comments in Python?',
                'options': ['//', '<!-- -->', '#', '/* */'],
                'correct': 2,
                'explanation': 'The hash symbol (#) is used for comments in Python.'
            }
        ]
    },
    'python-module2': {
        'title': 'Variables & Data Types',
        'description': 'Explore variables, int, float, string, and boolean data types',
        'video_url': 'https://www.youtube.com/embed/khKv-8q7YmY?controls=1&modestbranding=0&rel=0&autoplay=0',
        'video_duration': '1.5 hours',
        'information': '''<h3>📦 Variables & Data Types (Day 2)</h3>
<p><strong>📺 What's in This Video:</strong></p>
<p>Learn all about variables, integers, floating-point numbers, strings, booleans, and type conversion. Perfect for understanding Python's fundamental data types.</p>
<p style="margin-top: 15px; padding: 10px; background: var(--bg-secondary); border-left: 4px solid var(--primary); border-radius: 4px;"><strong>▶️ Play the video above!</strong> It includes practical examples and exercises.</p>
<p><strong>What to Learn:</strong></p>
<ul>
<li>Variables (storing data)</li>
<li>int (integers)</li>
<li>float (decimals)</li>
<li>string (text)</li>
<li>boolean (True/False)</li>
</ul>
<h3>🎯 Practice Code</h3>
<pre>name = "Alex"
age = 15
height = 5.6
is_student = True

print(name)
print(age)
print(height)
print(is_student)</pre>
<p>👉 Print each variable and see different data types in action.</p>''',
        'learning_objectives': [
            'Create and use variables',
            'Understand int, float, string, boolean types',
            'Practice assigning values',
            'Work with different data types'
        ],
        'quiz_questions': [
            {
                'question': 'Which of the following is a string?',
                'options': ['25', 'True', '"Python"', '3.14'],
                'correct': 2,
                'explanation': 'A string is text enclosed in quotes. "Python" is a string.'
            },
            {
                'question': 'What is the output?\nx = 10\ny = 5\nprint(x + y)',
                'options': ['105', '15', 'x + y', 'Error'],
                'correct': 1,
                'explanation': '10 + 5 = 15. Variables hold numeric values.'
            },
            {
                'question': 'What does type(10) return?',
                'options': ['string', 'float', 'int', 'number'],
                'correct': 2,
                'explanation': 'type(10) returns int because 10 is an integer.'
            }
        ]
    },
    'python-module3': {
        'title': 'Input & Output',
        'description': 'Learn input() function and type conversion',
        'video_url': 'https://www.youtube.com/embed/H2EJuAcrZYU?controls=1&modestbranding=0&rel=0&autoplay=0',
        'video_duration': '1 hour',
        'information': '''<h3>⌨️ Input & Output (Day 3)</h3>
<p><strong>📺 What's in This Video:</strong></p>
<p>Master the input() function to get user data, learn type conversion with int(), str(), and float(), and combine input with output to build interactive programs.</p>
<p style="margin-top: 15px; padding: 10px; background: var(--bg-secondary); border-left: 4px solid var(--primary); border-radius: 4px;"><strong>▶️ Play the video above!</strong> Watch step-by-step demonstrations of user interaction.</p>
<p><strong>What to Learn:</strong></p>
<ul>
<li>input() function (getting user data)</li>
<li>Type conversion (int(), str(), float())</li>
<li>Combining input and output</li>
</ul>
<h3>🎯 Practice Code</h3>
<pre>name = input("Enter your name: ")
age = int(input("Enter your age: "))

print("Hello", name)
print("You are", age, "years old")</pre>
<p>👉 Run it and enter your information.</p>''',
        'learning_objectives': [
            'Use input() to get user data',
            'Convert data types with int(), str(), float()',
            'Combine input and output',
            'Build interactive programs'
        ],
        'quiz_questions': [
            {
                'question': 'What does input() return?',
                'options': ['Integer', 'Float', 'String', 'Boolean'],
                'correct': 2,
                'explanation': 'input() always returns a string, even if you type a number.'
            }
        ]
    },
    'python-module4': {
        'title': 'Conditions & Logic',
        'description': 'Master if, elif, else statements and comparison operators',
        'video_url': 'https://www.youtube.com/embed/Zp5MuPOtsSY?controls=1&modestbranding=0&rel=0&autoplay=0',
        'video_duration': '45 minutes',
        'information': '''<h3>🔀 Conditions & Logic (Day 3-4)</h3>
<p><strong>📺 What's in This Video:</strong></p>
<p>Learn if, elif, and else statements. Master comparison operators (==, !=, >, <, >=, <=) and logical operators (and, or, not) for building decision logic.</p>
<p style="margin-top: 15px; padding: 10px; background: var(--bg-secondary); border-left: 4px solid var(--primary); border-radius: 4px;"><strong>▶️ Play the video above!</strong> Includes real-world examples of conditional statements.</p>
<p><strong>What to Learn:</strong></p>
<ul>
<li>if, elif, else statements</li>
<li>Comparison operators (==, !=, >, <, >=, <=)</li>
<li>Logical operators (and, or, not)</li>
</ul>
<h3>🎯 Practice Code</h3>
<pre>marks = int(input("Enter marks: "))

if marks >= 90:
    print("Grade A")
elif marks >= 60:
    print("Grade B")
else:
    print("Fail")</pre>
<p>👉 Run and test different mark values.</p>''',
        'learning_objectives': [
            'Use if, elif, else statements',
            'Apply comparison operators',
            'Build decision logic',
            'Solve conditional problems'
        ],
        'quiz_questions': [
            {
                'question': 'What is the output?\nage = 18\nif age >= 18:\n    print("Adult")\nelse:\n    print("Minor")',
                'options': ['Minor', 'Adult', 'Error', 'Nothing'],
                'correct': 1,
                'explanation': 'Since age (18) >= 18 is True, it prints "Adult".'
            },
            {
                'question': 'Which operator checks equality?',
                'options': ['=', '!=', '==', '>='],
                'correct': 2,
                'explanation': '== is the equality operator (= is for assignment).'
            }
        ]
    },
    'python-module5': {
        'title': 'Loops',
        'description': 'Learn for loops and while loops',
        'video_url': 'https://www.youtube.com/embed/6iF8Xb7Z3wQ?controls=1&modestbranding=0&rel=0&autoplay=0',
        'video_duration': '1 hour',
        'information': '''<h3>🔄 Loops (Day 4-5)</h3>
<p><strong>📺 What's in This Video:</strong></p>
<p>Understand for loops with range(), while loops, and loop control statements like break and continue. Learn how to automate repetitive tasks.</p>
<p style="margin-top: 15px; padding: 10px; background: var(--bg-secondary); border-left: 4px solid var(--primary); border-radius: 4px;"><strong>▶️ Play the video above!</strong> Contains practical loop examples and common patterns.</p>
<p><strong>What to Learn:</strong></p>
<ul>
<li>for loop (iterate a set number of times)</li>
<li>while loop (iterate while condition is true)</li>
<li>range() function</li>
<li>break and continue keywords</li>
</ul>
<h3>🎯 Practice Code - For Loop</h3>
<pre>for i in range(1, 6):
    print(i)</pre>
<h3>🎯 Practice Code - While Loop</h3>
<pre>count = 1
while count <= 5:
    print(count)
    count += 1</pre>
<p>👉 Both will print 1 through 5.</p>''',
        'learning_objectives': [
            'Create for loops with range()',
            'Create while loops',
            'Understand loop control (break, continue)',
            'Solve repetitive tasks'
        ],
        'quiz_questions': [
            {
                'question': 'How many times will this loop run?\nfor i in range(1, 5):\n    print(i)',
                'options': ['5', '4', '3', 'Infinite'],
                'correct': 1,
                'explanation': 'range(1, 5) produces 1, 2, 3, 4 - that\'s 4 iterations.'
            },
            {
                'question': 'What keyword is used to stop a loop?',
                'options': ['stop', 'exit', 'break', 'end'],
                'correct': 2,
                'explanation': 'The break keyword stops a loop immediately.'
            }
        ]
    },
    'python-module6': {
        'title': 'Functions',
        'description': 'Create functions with parameters and return values',
        'video_url': 'https://www.youtube.com/embed/9Os0o3wzS_I?controls=1&modestbranding=0&rel=0&autoplay=0',
        'video_duration': '50 minutes',
        'information': '''<h3>⚙️ Functions (Day 5-6)</h3>
<p><strong>📺 What's in This Video:</strong></p>
<p>Learn how to define functions with the def keyword, use parameters as inputs, and return values as outputs. Discover how to reuse code effectively.</p>
<p style="margin-top: 15px; padding: 10px; background: var(--bg-secondary); border-left: 4px solid var(--primary); border-radius: 4px;"><strong>▶️ Play the video above!</strong> Complete tutorial with function examples and best practices.</p>
<p><strong>What to Learn:</strong></p>
<ul>
<li>Creating functions with def</li>
<li>Parameters (inputs)</li>
<li>Return values (outputs)</li>
<li>Function calls</li>
</ul>
<h3>🎯 Practice Code</h3>
<pre>def add(a, b):
    return a + b

result = add(5, 3)
print(result)  # Output: 8</pre>
<p>👉 Create your own functions to reuse code.</p>''',
        'learning_objectives': [
            'Define functions with def',
            'Use parameters and arguments',
            'Return values from functions',
            'Call functions multiple times'
        ],
        'quiz_questions': [
            {
                'question': 'What is the output?\ndef add(a, b):\n    return a + b\nprint(add(2, 3))',
                'options': ['23', '5', 'None', 'Error'],
                'correct': 1,
                'explanation': '2 + 3 = 5. The function returns and prints the result.'
            }
        ]
    },
    'python-module7': {
        'title': 'Lists & Dictionaries',
        'description': 'Work with lists and dictionaries for storing multiple values',
        'video_url': 'https://www.youtube.com/embed/daefaLgNkw0?controls=1&modestbranding=0&rel=0&autoplay=0',
        'video_duration': '1.5 hours',
        'information': '''<h3>📋 Lists & Dictionaries (Day 6-7)</h3>
<p><strong>📺 What's in This Video:</strong></p>
<p>Master working with lists using square brackets [], learn list methods like append() and remove(), and understand dictionaries with curly braces {} for key-value storage.</p>
<p style="margin-top: 15px; padding: 10px; background: var(--bg-secondary); border-left: 4px solid var(--primary); border-radius: 4px;"><strong>▶️ Play the video above!</strong> Comprehensive guide to Python's most important data structures.</p>
<p><strong>What to Learn:</strong></p>
<ul>
<li>Lists [ ] (ordered collections)</li>
<li>Accessing list items</li>
<li>Modifying lists (append, insert, remove)</li>
<li>Dictionaries { } (key-value pairs)</li>
<li>Accessing dictionary values</li>
</ul>
<h3>🎯 Practice Code - Lists</h3>
<pre>numbers = [1, 2, 3, 4]
numbers.append(5)
print(numbers)  # [1, 2, 3, 4, 5]</pre>
<h3>🎯 Practice Code - Dictionaries</h3>
<pre>student = {
    "name": "Alex",
    "age": 15
}
print(student["name"])  # Alex</pre>''',
        'learning_objectives': [
            'Create and manipulate lists',
            'Use list methods (append, remove, sort)',
            'Create dictionaries',
            'Access and modify dictionary values'
        ],
        'quiz_questions': [
            {
                'question': 'Which is a list?',
                'options': ['(1, 2, 3)', '{1, 2, 3}', '[1, 2, 3]', '"1,2,3"'],
                'correct': 2,
                'explanation': '[1, 2, 3] is a list (square brackets).'
            },
            {
                'question': 'How do you add an item to a list called nums?',
                'options': ['nums.add(5)', 'nums.append(5)', 'nums.insert(5)', 'nums.push(5)'],
                'correct': 1,
                'explanation': 'The append() method adds an item to the end of a list.'
            }
        ]
    },
    'python-module8': {
        'title': 'File Handling',
        'description': 'Read and write files in Python',
        'video_url': 'https://www.youtube.com/embed/Uh2ebFW8OYM?controls=1&modestbranding=0&rel=0&autoplay=0',
        'video_duration': '30 minutes',
        'information': '''<h3>📁 File Handling (Day 7)</h3>
<p><strong>📺 What's in This Video:</strong></p>
<p>Learn how to open files with open(), use different file modes (r for read, w for write, a for append), read and write file contents, and properly close files.</p>
<p style="margin-top: 15px; padding: 10px; background: var(--bg-secondary); border-left: 4px solid var(--primary); border-radius: 4px;"><strong>▶️ Play the video above!</strong> Step-by-step file I/O operations with practical examples.</p>
<p><strong>What to Learn:</strong></p>
<ul>
<li>Opening files (open())</li>
<li>File modes: "r" (read), "w" (write), "a" (append)</li>
<li>Reading files</li>
<li>Writing to files</li>
<li>Closing files</li>
</ul>
<h3>🎯 Practice Code - Write</h3>
<pre>file = open("data.txt", "w")
file.write("Hello File")
file.close()</pre>
<h3>🎯 Practice Code - Read</h3>
<pre>file = open("data.txt", "r")
content = file.read()
print(content)
file.close()</pre>''',
        'learning_objectives': [
            'Open files in different modes',
            'Read file contents',
            'Write data to files',
            'Close files properly'
        ],
        'quiz_questions': [
            {
                'question': 'Which mode is used to write to a file?',
                'options': ['"r"', '"a"', '"w"', '"x"'],
                'correct': 2,
                'explanation': '"w" mode opens a file for writing. It overwrites if file exists.'
            }
        ]
    },
    'python-module9': {
        'title': 'Mini Projects & Practice',
        'description': 'Build real projects: Number Guessing Game, Calculator, Student Marks System',
        'video_url': 'https://www.youtube.com/embed/DLn3jOsNRVE?controls=1&modestbranding=0&rel=0&autoplay=0',
        'video_duration': '8 hours',
        'information': '''<h3>🎮 Mini Practice Projects (Very Important)</h3>
<p><strong>📺 What's in This Video:</strong></p>
<p>This video showcases real projects you can build: Number Guessing Game, Simple Calculator, and Student Marks System. See how to integrate all Python basics concepts into complete working programs.</p>
<p style="margin-top: 15px; padding: 10px; background: var(--bg-secondary); border-left: 4px solid var(--primary); border-radius: 4px;"><strong>▶️ Play the video above!</strong> Watch professional project demonstrations and best practices.</p>
<p><strong>Build these WITHOUT copying:</strong></p>
<h4>Project 1: Number Guessing Game</h4>
<ul>
<li>Generate a random number</li>
<li>User guesses the number</li>
<li>Give hints (too high/too low)</li>
<li>Count attempts</li>
</ul>
<h4>Project 2: Simple Calculator</h4>
<ul>
<li>Take two numbers as input</li>
<li>Choose operation (+, -, *, /)</li>
<li>Display result</li>
</ul>
<h4>Project 3: Student Marks System</h4>
<ul>
<li>Store student names and marks</li>
<li>Calculate average</li>
<li>Find highest/lowest marks</li>
<li>Assign grades</li>
</ul>
<h3>🟢 Daily Rules (IMPORTANT)</h3>
<ul>
<li>✅ Code every day (minimum 30 minutes)</li>
<li>✅ Don't just read — type the code</li>
<li>✅ Break code → fix it</li>
<li>✅ Use Google only after trying</li>
</ul>
<h3>🎯 When Are You "Done" With Python Basics?</h3>
<p>You are done when you can:</p>
<ul>
<li>✅ Write programs without copying</li>
<li>✅ Understand errors</li>
<li>✅ Explain your code in words</li>
</ul>''',
        'video_url': 'https://www.youtube.com/embed/dQw4w9WgXcQ',
        'video_duration': '60 minutes',
        'learning_objectives': [
            'Integrate all Python basics concepts',
            'Build complete working programs',
            'Debug and fix errors',
            'Understand your own code'
        ],
        'quiz_questions': [
            {
                'question': 'When are you "done" with Python basics?',
                'options': [
                    'When you finish all modules',
                    'When you can write programs without copying and explain your code',
                    'When you memorize all syntax',
                    'When you complete one project'
                ],
                'correct': 1,
                'explanation': 'True mastery comes when you can write and understand your own code.'
            }
        ]
    }
}

# Advanced Python module details with quiz
PYTHON_ADVANCED_MODULE_DETAILS = {
    'python-adv-module1': {
        'title': 'Step 1: Python Internals & Memory Management',
        'description': 'Understand Python code execution, bytecode, and memory management',
        'video_url': 'https://www.youtube.com/embed/arxWaw-E8QQ?controls=1&modestbranding=0&rel=0&autoplay=0',
        'video_duration': '2 hours',
        'information': '''<h3>🐍 Python Internals & Memory Management</h3>
<p><strong>What Happens When You Run Python Code:</strong></p>
<ul>
<li>Python reads your .py file</li>
<li>Converts it into bytecode</li>
<li>Bytecode runs inside Python Virtual Machine (PVM)</li>
<li>Objects are stored in heap</li>
<li>References are stored in stack</li>
</ul>
<h3>Step 1.1: Simple Program</h3>
<pre>x = 10
y = 20
print(x + y)</pre>
<h3>Step 1.2: Tools to Learn</h3>
<ul>
<li><strong>id()</strong> - Get memory address of an object</li>
<li><strong>type()</strong> - Get type of an object</li>
<li><strong>sys.getsizeof()</strong> - Get memory size of an object</li>
<li><strong>dis</strong> - Disassemble bytecode to see what Python does internally</li>
</ul>
<h3>Step 1.3: Practice</h3>
<ul>
<li>Check memory of list vs tuple</li>
<li>Compare is vs == operators</li>
<li>Understand object references</li>
</ul>''',
        'learning_objectives': [
            'Understand Python code execution flow',
            'Learn bytecode and PVM',
            'Use id(), type(), sys.getsizeof()',
            'Compare memory usage'
        ],
        'quiz_questions': [
            {
                'question': 'What is the correct order of Python code execution?',
                'options': ['Source Code → Machine Code → Output', 'Source Code → Bytecode → Python Virtual Machine', 'Bytecode → Source Code → Output', 'Source Code → Interpreter → Machine Code'],
                'correct': 1,
                'explanation': 'Python compiles to bytecode which runs in the Python Virtual Machine.'
            },
            {
                'question': 'Which function gives the memory address of an object?',
                'options': ['type()', 'memory()', 'id()', 'sizeof()'],
                'correct': 2,
                'explanation': 'The id() function returns the memory address of an object.'
            },
            {
                'question': 'Where are Python objects stored?',
                'options': ['Stack', 'CPU registers', 'Heap', 'Cache'],
                'correct': 2,
                'explanation': 'Python objects are stored in the heap memory.'
            },
            {
                'question': 'Which tool is used to inspect Python bytecode?',
                'options': ['sys', 'inspect', 'dis', 'gc'],
                'correct': 2,
                'explanation': 'The dis module disassembles bytecode for inspection.'
            }
        ]
    },
    'python-adv-module2': {
        'title': 'Step 2: Advanced Data Structures (Collections)',
        'description': 'Master deque, Counter, and defaultdict from collections module',
        'video_url': 'https://www.youtube.com/embed/R-HLU9Fl5ug?controls=1&modestbranding=0&rel=0&autoplay=0',
        'video_duration': '1.5 hours',
        'information': '''<h3>📚 Advanced Data Structures from Collections</h3>
<p><strong>Why Collections Exist:</strong></p>
<ul>
<li>✅ Faster than standard data structures</li>
<li>✅ Cleaner, more readable code</li>
<li>✅ Less code to write</li>
</ul>
<h3>Step 2.1: Import Collections</h3>
<pre>from collections import deque, Counter, defaultdict</pre>
<h3>Step 2.2: Three Main Collections</h3>
<ul>
<li><strong>deque</strong> - Double-ended queue with fast append/pop from both ends</li>
<li><strong>Counter</strong> - Count frequency of elements</li>
<li><strong>defaultdict</strong> - Dictionary with auto values for missing keys</li>
</ul>
<h3>Step 2.3: Practice</h3>
<ul>
<li>Build a word frequency counter with Counter</li>
<li>Build a queue system with deque</li>
<li>Use defaultdict for grouping data</li>
</ul>''',
        'learning_objectives': [
            'Master deque for fast append/pop',
            'Use Counter for frequency counting',
            'Use defaultdict for auto values',
            'Build real-world projects'
        ],
        'quiz_questions': [
            {
                'question': 'Which collection is optimized for fast append and pop from both ends?',
                'options': ['list', 'tuple', 'deque', 'set'],
                'correct': 2,
                'explanation': 'deque (double-ended queue) provides fast operations at both ends.'
            },
            {
                'question': 'Which module provides Counter and defaultdict?',
                'options': ['itertools', 'collections', 'functools', 'math'],
                'correct': 1,
                'explanation': 'The collections module provides Counter, deque, and defaultdict.'
            },
            {
                'question': 'What happens if a key is missing in defaultdict?',
                'options': ['Error occurs', 'Program stops', 'Key is auto-created', 'Value becomes None'],
                'correct': 2,
                'explanation': 'defaultdict automatically creates keys with default values.'
            },
            {
                'question': 'Which data structure does NOT allow duplicate values?',
                'options': ['list', 'tuple', 'set', 'dictionary'],
                'correct': 2,
                'explanation': 'Sets do not allow duplicate values.'
            }
        ]
    },
    'python-adv-module3': {
        'title': 'Step 3: Functions – Advanced Level',
        'description': 'Learn *args, **kwargs, function annotations, and closures',
        'video_url': 'https://www.youtube.com/embed/9Os0o3wzS_I?controls=1&modestbranding=0&rel=0&autoplay=0',
        'video_duration': '1.5 hours',
        'information': '''<h3>⚙️ Advanced Functions</h3>
<h3>Step 3.1: Functions as Objects</h3>
<pre>def add(a, b):
    return a + b

x = add  # Functions are objects
print(x(2, 3))  # 5</pre>
<h3>Step 3.2: *args and **kwargs</h3>
<ul>
<li><strong>*args</strong> - Accept variable number of positional arguments (tuple)</li>
<li><strong>**kwargs</strong> - Accept variable number of keyword arguments (dictionary)</li>
</ul>
<h3>Step 3.3: Closures</h3>
<ul>
<li>Function inside function</li>
<li>Inner function remembers outer variables</li>
<li>Useful for creating specialized functions</li>
</ul>
<h3>Step 3.4: Practice</h3>
<ul>
<li>Build a calculator using closures</li>
<li>Create validation functions</li>
<li>Use function annotations for documentation</li>
</ul>''',
        'learning_objectives': [
            'Understand functions as objects',
            'Master *args and **kwargs',
            'Create and use closures',
            'Apply function annotations'
        ],
        'quiz_questions': [
            {
                'question': 'Functions in Python are:',
                'options': ['Keywords', 'Objects', 'Data types', 'Modules'],
                'correct': 1,
                'explanation': 'Functions are first-class objects in Python.'
            },
            {
                'question': 'What does *args collect?',
                'options': ['Keyword arguments', 'Dictionary', 'Tuple', 'List'],
                'correct': 2,
                'explanation': '*args collects positional arguments into a tuple.'
            },
            {
                'question': 'What is a closure?',
                'options': ['Function without return', 'Function inside class', 'Function remembering outer variables', 'Recursive function'],
                'correct': 2,
                'explanation': 'A closure is a function that remembers variables from its enclosing scope.'
            },
            {
                'question': 'Which keyword is used for anonymous functions?',
                'options': ['def', 'lambda', 'anon', 'func'],
                'correct': 1,
                'explanation': 'The lambda keyword creates anonymous functions.'
            }
        ]
    },
    'python-adv-module4': {
        'title': 'Step 4: Decorators (VERY IMPORTANT)',
        'description': 'Master decorators for modifying function behavior',
        'video_url': 'https://www.youtube.com/embed/FsAPt_9Bf3U?controls=1&modestbranding=0&rel=0&autoplay=0',
        'video_duration': '2 hours',
        'information': '''<h3>✨ Decorators (VERY IMPORTANT)</h3>
<p><strong>What is a Decorator?</strong></p>
<p>A decorator is a function that modifies another function without changing its code.</p>
<h3>Step 4.1: Simple Decorator</h3>
<pre>def my_decorator(func):
    def wrapper():
        print("Before")
        func()
        print("After")
    return wrapper

@my_decorator
def greet():
    print("Hello!")

greet()  # Prints: Before, Hello!, After</pre>
<h3>Step 4.2: Decorators with Arguments</h3>
<h3>Step 4.3: Multiple Decorators</h3>
<h3>Step 4.4: Class-based Decorators</h3>
<h3>Step 4.5: Real-World Uses</h3>
<ul>
<li>Login check decorator</li>
<li>Time measurement decorator</li>
<li>Caching decorator</li>
<li>Logging decorator</li>
</ul>''',
        'learning_objectives': [
            'Understand decorators concept',
            'Create simple decorators',
            'Use decorators with arguments',
            'Apply multiple decorators'
        ],
        'quiz_questions': [
            {
                'question': 'A decorator is mainly used to:',
                'options': ['Create loops', 'Modify function behavior', 'Handle errors', 'Create classes'],
                'correct': 1,
                'explanation': 'Decorators modify function behavior without changing the original code.'
            },
            {
                'question': 'Which symbol is used to apply a decorator?',
                'options': ['#', '@', '$', '%'],
                'correct': 1,
                'explanation': 'The @ symbol is used to apply decorators.'
            },
            {
                'question': 'The inner function inside a decorator is commonly called:',
                'options': ['helper', 'modifier', 'wrapper', 'inner_func'],
                'correct': 2,
                'explanation': 'The inner function is called the wrapper.'
            },
            {
                'question': 'Decorators execute:',
                'options': ['After function call', 'Before function definition', 'At function definition time', 'Only during runtime errors'],
                'correct': 2,
                'explanation': 'Decorators are applied at function definition time.'
            }
        ]
    },
    'python-adv-module5': {
        'title': 'Step 5: Context Managers',
        'description': 'Master with statement and context managers',
        'video_url': 'https://www.youtube.com/embed/-aKFBoZpiqA?controls=1&modestbranding=0&rel=0&autoplay=0',
        'video_duration': '1 hour',
        'information': '''<h3>🔐 Context Managers</h3>
<h3>Step 5.1: Understanding with Statement</h3>
<pre>with open("file.txt") as f:
    data = f.read()
    # File is automatically closed</pre>
<h3>Step 5.2: Create Your Own Context Manager</h3>
<ul>
<li>Using class (implement __enter__ and __exit__)</li>
<li>Using contextlib decorator</li>
</ul>
<h3>Step 5.3: Real-World Use Cases</h3>
<ul>
<li>File manager - Ensure files close properly</li>
<li>Database connection manager - Handle connections safely</li>
<li>Timer context - Measure execution time</li>
<li>Lock manager - Handle concurrent access</li>
</ul>''',
        'learning_objectives': [
            'Understand with statement',
            'Create context manager classes',
            'Use contextlib decorators',
            'Build resource managers'
        ],
        'quiz_questions': [
            {
                'question': 'Which keyword is used for context managers?',
                'options': ['try', 'open', 'with', 'using'],
                'correct': 2,
                'explanation': 'The with keyword is used for context managers.'
            },
            {
                'question': 'Which methods define a context manager class?',
                'options': ['__start__, __end__', '__enter__, __exit__', '__open__, __close__', '__init__, __del__'],
                'correct': 1,
                'explanation': 'Context managers use __enter__ and __exit__ methods.'
            },
            {
                'question': 'Context managers are mainly used to:',
                'options': ['Speed up code', 'Manage resources safely', 'Create threads', 'Handle decorators'],
                'correct': 1,
                'explanation': 'Context managers ensure resources are properly managed and cleaned up.'
            }
        ]
    },
    'python-adv-module6': {
        'title': 'Step 6: Object-Oriented Python (Deep)',
        'description': 'Master magic methods, inheritance, dataclass, and __slots__',
        'video_url': 'https://www.youtube.com/embed/JeznW_7DlB0?controls=1&modestbranding=0&rel=0&autoplay=0',
        'video_duration': '2 hours',
        'information': '''<h3>🎯 Object-Oriented Python (Deep Dive)</h3>
<h3>Step 6.1: Magic Methods (Dunder Methods)</h3>
<ul>
<li><strong>__init__</strong> - Constructor</li>
<li><strong>__str__</strong> - String representation</li>
<li><strong>__len__</strong> - len() function</li>
<li><strong>__add__</strong> - + operator</li>
<li><strong>__repr__</strong> - Official representation</li>
</ul>
<h3>Step 6.2: Inheritance</h3>
<ul>
<li>Single inheritance</li>
<li>Multiple inheritance</li>
<li>MRO (Method Resolution Order)</li>
</ul>
<h3>Step 6.3: Advanced Features</h3>
<ul>
<li><strong>@dataclass</strong> - Simplify class creation</li>
<li><strong>__slots__</strong> - Reduce memory usage</li>
</ul>
<h3>Step 6.4: Practice</h3>
<ul>
<li>Build custom data class</li>
<li>Build plugin system with inheritance</li>
<li>Implement magic methods</li>
</ul>''',
        'learning_objectives': [
            'Master magic methods',
            'Implement inheritance',
            'Use dataclass decorator',
            'Optimize with __slots__'
        ],
        'quiz_questions': [
            {
                'question': 'Which method is called automatically when an object is created?',
                'options': ['__new__', '__start__', '__init__', '__create__'],
                'correct': 2,
                'explanation': '__init__ is the constructor called when an object is created.'
            },
            {
                'question': 'What does MRO stand for?',
                'options': ['Method Runtime Order', 'Module Resolution Order', 'Method Resolution Order', 'Memory Resolution Order'],
                'correct': 2,
                'explanation': 'MRO stands for Method Resolution Order.'
            },
            {
                'question': 'Which decorator simplifies class boilerplate code?',
                'options': ['@class', '@dataclass', '@object', '@auto'],
                'correct': 1,
                'explanation': '@dataclass simplifies class creation by auto-generating methods.'
            },
            {
                'question': '__slots__ is used to:',
                'options': ['Increase inheritance', 'Reduce memory usage', 'Add methods', 'Create decorators'],
                'correct': 1,
                'explanation': '__slots__ reduces memory usage by limiting instance attributes.'
            }
        ]
    },
    'python-adv-module7': {
        'title': 'Step 7: Iterators & Generators',
        'description': 'Master iterators, the yield keyword, and lazy evaluation',
        'video_url': 'https://www.youtube.com/embed/bD05uGo_sVI?controls=1&modestbranding=0&rel=0&autoplay=0',
        'video_duration': '1.5 hours',
        'information': '''<h3>🔄 Iterators & Generators</h3>
<h3>Step 7.1: Iterator Protocol</h3>
<ul>
<li>__iter__() method - Return iterator</li>
<li>__next__() method - Return next value</li>
</ul>
<h3>Step 7.2: Create Custom Iterator</h3>
<h3>Step 7.3: Generators with yield</h3>
<pre>def count_up_to(n):
    i = 1
    while i <= n:
        yield i
        i += 1

for num in count_up_to(5):
    print(num)</pre>
<h3>Step 7.4: Real-World Examples</h3>
<ul>
<li>Infinite number generator</li>
<li>Log file reader (line by line)</li>
<li>Data stream processor</li>
<li>Fibonacci sequence</li>
</ul>''',
        'learning_objectives': [
            'Understand iterator protocol',
            'Create custom iterators',
            'Master generators with yield',
            'Apply lazy evaluation'
        ],
        'quiz_questions': [
            {
                'question': 'Which keyword creates a generator?',
                'options': ['return', 'yield', 'generate', 'next'],
                'correct': 1,
                'explanation': 'The yield keyword creates generators.'
            },
            {
                'question': 'Generators are:',
                'options': ['Memory heavy', 'Eager loaded', 'Lazy evaluated', 'Slower than lists'],
                'correct': 2,
                'explanation': 'Generators use lazy evaluation, processing one item at a time.'
            },
            {
                'question': 'Which method moves an iterator to the next value?',
                'options': ['move()', 'next()', 'advance()', 'iterate()'],
                'correct': 1,
                'explanation': 'The next() method gets the next value from an iterator.'
            }
        ]
    },
    'python-adv-module8': {
        'title': 'Step 8: Error Handling & Debugging',
        'description': 'Master try-except-finally, custom exceptions, and pdb debugging',
        'video_url': 'https://www.youtube.com/embed/NIWwJbo-9_8?controls=1&modestbranding=0&rel=0&autoplay=0',
        'video_duration': '1 hour',
        'information': '''<h3>🐛 Error Handling & Debugging</h3>
<h3>Step 8.1: Exception Hierarchy</h3>
<pre>try:
    result = 10 / 0
except ZeroDivisionError:
    print("Cannot divide by zero")
except Exception:
    print("Some error occurred")
finally:
    print("Always runs")</pre>
<h3>Step 8.2: Custom Exceptions</h3>
<ul>
<li>Create your own exception classes</li>
<li>Inherit from Exception base class</li>
</ul>
<h3>Step 8.3: Debug with pdb</h3>
<pre>import pdb
pdb.set_trace()  # Debugger stops here</pre>
<h3>Step 8.4: Error Handling Best Practices</h3>
<ul>
<li>Catch specific exceptions</li>
<li>Use finally for cleanup</li>
<li>Log errors for debugging</li>
</ul>''',
        'learning_objectives': [
            'Understand exception hierarchy',
            'Create custom exceptions',
            'Use try-except-finally',
            'Debug with pdb'
        ],
        'quiz_questions': [
            {
                'question': 'Which block always executes?',
                'options': ['try', 'except', 'else', 'finally'],
                'correct': 3,
                'explanation': 'The finally block always executes, regardless of exceptions.'
            },
            {
                'question': 'Custom exceptions should inherit from:',
                'options': ['BaseObject', 'Error', 'Exception', 'Warning'],
                'correct': 2,
                'explanation': 'Custom exceptions should inherit from the Exception class.'
            },
            {
                'question': 'Which module is used for step-by-step debugging?',
                'options': ['debug', 'trace', 'pdb', 'log'],
                'correct': 2,
                'explanation': 'The pdb module provides Python Debugger for step-by-step debugging.'
            }
        ]
    },
    'python-adv-module9': {
        'title': 'Step 9: File Handling & Serialization',
        'description': 'Master JSON, Pickle, CSV, and backup systems',
        'video_url': 'https://www.youtube.com/embed/Uh2ebFW8OYM?controls=1&modestbranding=0&rel=0&autoplay=0',
        'video_duration': '1.5 hours',
        'information': '''<h3>📁 File Handling & Serialization</h3>
<h3>Step 9.1: Serialization Formats</h3>
<ul>
<li><strong>JSON</strong> - Human-readable text format</li>
<li><strong>Pickle</strong> - Python object serialization</li>
<li><strong>CSV</strong> - Comma-separated values for data</li>
</ul>
<h3>Step 9.2: Advanced File Modes</h3>
<pre>"r"  - Read
"w"  - Write (overwrites)
"a"  - Append
"x"  - Exclusive creation
"b"  - Binary mode
"t"  - Text mode (default)</pre>
<h3>Step 9.3: Practice Projects</h3>
<ul>
<li>Backup system using JSON or Pickle</li>
<li>Log storage tool with CSV</li>
<li>Data export functionality</li>
</ul>''',
        'learning_objectives': [
            'Serialize with JSON, Pickle, CSV',
            'Handle files in different modes',
            'Build backup systems',
            'Work with structured data'
        ],
        'quiz_questions': [
            {
                'question': 'Which format is human-readable?',
                'options': ['Pickle', 'Binary', 'JSON', 'Bytecode'],
                'correct': 2,
                'explanation': 'JSON is human-readable text format.'
            },
            {
                'question': 'Which module is used for CSV files?',
                'options': ['csv', 'table', 'sheet', 'excel'],
                'correct': 0,
                'explanation': 'The csv module handles CSV file operations.'
            },
            {
                'question': 'Pickle is mainly used for:',
                'options': ['Encryption', 'Compression', 'Object serialization', 'File reading'],
                'correct': 2,
                'explanation': 'Pickle serializes Python objects for storage.'
            }
        ]
    },
    'python-adv-module10': {
        'title': 'Step 10: Concurrency (Threads, Processes, Async)',
        'description': 'Master threading, multiprocessing, and AsyncIO',
        'video_url': 'https://www.youtube.com/embed/IEEhzQoKtQU?controls=1&modestbranding=0&rel=0&autoplay=0',
        'video_duration': '2 hours',
        'information': '''<h3>⚡ Concurrency</h3>
<h3>Step 10.1: Global Interpreter Lock (GIL)</h3>
<p>Python has a GIL that prevents true parallel execution in threads.</p>
<h3>Step 10.2: Threading</h3>
<p>Best for I/O-bound tasks (network, disk).</p>
<h3>Step 10.3: Multiprocessing</h3>
<p>Best for CPU-bound tasks (calculations). Bypasses GIL.</p>
<h3>Step 10.4: AsyncIO (Async/Await)</h3>
<pre>async def fetch_data():
    await some_io_operation()
    return data

asyncio.run(fetch_data())</pre>
<h3>Step 10.5: Practice Projects</h3>
<ul>
<li>Async web scraper</li>
<li>Parallel task runner</li>
<li>Concurrent network requests</li>
</ul>''',
        'learning_objectives': [
            'Understand GIL and its impact',
            'Create threads for I/O tasks',
            'Use multiprocessing for CPU tasks',
            'Master async/await'
        ],
        'quiz_questions': [
            {
                'question': 'GIL stands for:',
                'options': ['Global Interpreter Lock', 'General Instruction Loop', 'Global Internet Layer', 'Graphical Interface Logic'],
                'correct': 0,
                'explanation': 'GIL is Global Interpreter Lock in Python.'
            },
            {
                'question': 'Threads are best for:',
                'options': ['CPU-bound tasks', 'I/O-bound tasks', 'GPU tasks', 'Memory tasks'],
                'correct': 1,
                'explanation': 'Threads excel at I/O-bound tasks like network and disk operations.'
            },
            {
                'question': 'Which keyword defines an async function?',
                'options': ['await', 'async', 'coroutine', 'future'],
                'correct': 1,
                'explanation': 'The async keyword defines asynchronous functions.'
            }
        ]
    },
    'python-adv-module11': {
        'title': 'Step 11: Performance Optimization',
        'description': 'Measure performance and optimize algorithms',
        'video_url': 'https://www.youtube.com/embed/yrRM4KzO9wA?controls=1&modestbranding=0&rel=0&autoplay=0',
        'video_duration': '1.5 hours',
        'information': '''<h3>⚡ Performance Optimization</h3>
<h3>Step 11.1: Measure Performance</h3>
<ul>
<li><strong>cProfile</strong> - Profile execution time</li>
<li><strong>timeit</strong> - Time code snippets</li>
<li><strong>memory_profiler</strong> - Track memory usage</li>
</ul>
<h3>Step 11.2: Optimize Algorithms</h3>
<ul>
<li>Choose better algorithms</li>
<li>Reduce time complexity</li>
<li>Minimize operations</li>
</ul>
<h3>Step 11.3: Caching with lru_cache</h3>
<pre>from functools import lru_cache

@lru_cache(maxsize=128)
def fibonacci(n):
    if n < 2:
        return n
    return fibonacci(n-1) + fibonacci(n-2)</pre>''',
        'learning_objectives': [
            'Measure code performance',
            'Use profiling tools',
            'Implement caching',
            'Optimize algorithms'
        ],
        'quiz_questions': [
            {
                'question': 'Which tool profiles execution time?',
                'options': ['profiler', 'cProfile', 'speedtest', 'timer'],
                'correct': 1,
                'explanation': 'cProfile is the standard Python profiler.'
            },
            {
                'question': 'lru_cache is used for:',
                'options': ['Logging', 'Caching results', 'Memory cleanup', 'File compression'],
                'correct': 1,
                'explanation': 'lru_cache caches function results to improve performance.'
            }
        ]
    },
    'python-adv-module12': {
        'title': 'Step 12: Testing & Quality',
        'description': 'Write unit tests with pytest and mock objects',
        'video_url': 'https://www.youtube.com/embed/etosV2IWBF0?controls=1&modestbranding=0&rel=0&autoplay=0',
        'video_duration': '1.5 hours',
        'information': '''<h3>🧪 Testing & Quality Assurance</h3>
<h3>Step 12.1: Write Unit Tests</h3>
<pre>import pytest

def test_addition():
    assert 2 + 2 == 4

def test_subtraction():
    assert 5 - 3 == 2</pre>
<h3>Step 12.2: Use pytest</h3>
<ul>
<li>Most popular testing framework</li>
<li>Easy syntax with assertions</li>
<li>Great plugins and extensions</li>
</ul>
<h3>Step 12.3: Mocking</h3>
<p>Replace real objects with mocks for testing.</p>
<h3>Step 12.4: Best Practices</h3>
<ul>
<li>Test-driven development (TDD)</li>
<li>Write tests first, then code</li>
<li>Aim for high coverage</li>
</ul>''',
        'learning_objectives': [
            'Write unit tests',
            'Use pytest framework',
            'Mock external dependencies',
            'Achieve good test coverage'
        ],
        'quiz_questions': [
            {
                'question': 'Which framework is most popular for testing in Python?',
                'options': ['testpy', 'unittest', 'pytest', 'doctest'],
                'correct': 2,
                'explanation': 'pytest is the most popular modern testing framework.'
            },
            {
                'question': 'Mocking is used to:',
                'options': ['Speed execution', 'Replace real objects', 'Create fake errors', 'Debug loops'],
                'correct': 1,
                'explanation': 'Mocking replaces real objects with test doubles.'
            }
        ]
    },
    'python-adv-module13': {
        'title': 'Step 13: Packaging & Deployment',
        'description': 'Create packages and deploy Python applications',
        'video_url': 'https://www.youtube.com/embed/J2zquypYpk4?controls=1&modestbranding=0&rel=0&autoplay=0',
        'video_duration': '1.5 hours',
        'information': '''<h3>📦 Packaging & Deployment</h3>
<h3>Step 13.1: Virtual Environments</h3>
<pre>python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\\Scripts\\activate  # Windows</pre>
<h3>Step 13.2: Project Structure</h3>
<pre>my_project/
├── my_package/
│   ├── __init__.py
│   ├── module1.py
│   └── module2.py
├── tests/
│   └── test_module1.py
├── pyproject.toml
├── setup.py
└── README.md</pre>
<h3>Step 13.3: Modern Packaging</h3>
<ul>
<li><strong>pyproject.toml</strong> - Modern Python packaging (PEP 517/518)</li>
<li><strong>setup.py</strong> - Legacy packaging configuration</li>
<li><strong>requirements.txt</strong> - Dependency list</li>
</ul>
<h3>Step 13.4: Deployment</h3>
<ul>
<li>Package for PyPI</li>
<li>Deploy to cloud platforms</li>
<li>Docker containerization</li>
</ul>''',
        'learning_objectives': [
            'Create virtual environments',
            'Organize project structure',
            'Create pyproject.toml',
            'Deploy packages'
        ],
        'quiz_questions': [
            {
                'question': 'Which file defines modern Python packaging?',
                'options': ['setup.cfg', 'requirements.txt', 'pyproject.toml', 'package.json'],
                'correct': 2,
                'explanation': 'pyproject.toml is the modern Python packaging standard (PEP 517/518).'
            }
        ]
    }
}

# JavaScript Mastery module details with structured content
JAVASCRIPT_MASTERY_MODULE_DETAILS = {
    'js-module1': {
        'title': 'Step 1: How JavaScript Works Internally',
        'description': 'Understand JavaScript engine, execution context, and memory',
        'video_url': 'https://www.youtube.com/embed/8zKuNo4ay8E?controls=1&modestbranding=0&rel=0&autoplay=0',
        'video_duration': '1.5 hours',
        'information': '''<h3>🧩 STEP 1: How JavaScript Works Internally</h3>

<h4>Step 1.1: Write a Simple JavaScript File</h4>
<pre>let a = 10;
let b = 20;
console.log(a + b);</pre>

<h4>Step 1.2: Understand What Happens Internally</h4>
<ul>
<li>JS engine reads the file</li>
<li>Global Execution Context is created</li>
<li>Memory is allocated</li>
<li>Code is executed line by line</li>
</ul>

<h4>Step 1.3: Learn Core Internals</h4>
<ul>
<li>JavaScript Engine (V8)</li>
<li>Call Stack</li>
<li>Memory Heap</li>
</ul>

<h4>Step 1.4: Practice</h4>
<ul>
<li>Predict output of simple scripts</li>
<li>Observe call stack in browser dev tools</li>
</ul>''',
        'learning_objectives': [
            'Understand how JS engine works',
            'Learn Global Execution Context',
            'Understand Call Stack concept',
            'Observe memory allocation'
        ],
        'quiz_questions': [
            {'question': 'Which component executes JavaScript code?', 'options': ['Browser', 'JavaScript Engine', 'DOM', 'API'], 'correct': 1, 'explanation': 'The JavaScript Engine is responsible for executing JavaScript code.'},
            {'question': 'What is created first when a JS file runs?', 'options': ['Call stack', 'Memory heap', 'Global Execution Context', 'Event loop'], 'correct': 2, 'explanation': 'The Global Execution Context is created first when a JS file runs.'},
            {'question': 'Where are function calls stored during execution?', 'options': ['Heap', 'Stack', 'Queue', 'Cache'], 'correct': 1, 'explanation': 'Function calls are stored in the Call Stack during execution.'},
            {'question': 'Which engine is used by Chrome?', 'options': ['SpiderMonkey', 'Chakra', 'V8', 'Nitro'], 'correct': 2, 'explanation': 'Chrome uses the V8 JavaScript Engine.'}
        ]
    },
    'js-module2': {
        'title': 'Step 2: Variables, Scope & Hoisting',
        'description': 'Master var, let, const, scope, and hoisting behavior',
        'video_url': 'https://www.youtube.com/embed/lil4XcqVRwc?controls=1&modestbranding=0&rel=0&autoplay=0',
        'video_duration': '2 hours',
        'information': '''<h3>🧩 STEP 2: Variables, Scope & Hoisting</h3>

<h4>Step 2.1: Create Variables Using</h4>
<pre>var x = 10;
let y = 20;
const z = 30;</pre>

<h4>Step 2.2: Understand Scope</h4>
<ul>
<li>Global scope</li>
<li>Function scope</li>
<li>Block scope</li>
</ul>

<h4>Step 2.3: Learn Hoisting Behavior</h4>
<ul>
<li>var hoisting</li>
<li>let & const hoisting</li>
<li>Temporal Dead Zone</li>
</ul>

<h4>Step 2.4: Practice</h4>
<ul>
<li>Scope prediction problems</li>
<li>Hoisting output questions</li>
</ul>''',
        'learning_objectives': [
            'Understand var, let, const differences',
            'Master scope levels',
            'Learn hoisting behavior',
            'Understand Temporal Dead Zone'
        ],
        'quiz_questions': [
            {'question': 'Which keyword is block scoped?', 'options': ['var', 'let', 'function', 'global'], 'correct': 1, 'explanation': 'The let keyword is block scoped.'},
            {'question': 'Accessing a let variable before declaration results in:', 'options': ['undefined', 'null', 'ReferenceError', 'NaN'], 'correct': 2, 'explanation': 'Accessing a let variable before declaration results in a ReferenceError due to the Temporal Dead Zone.'},
            {'question': 'Hoisting applies to:', 'options': ['let only', 'const only', 'var and function declarations', 'Arrow functions only'], 'correct': 2, 'explanation': 'Hoisting applies to var and function declarations.'}
        ]
    },
    'js-module3': {
        'title': 'Step 3: Data Types & Type System',
        'description': 'Learn primitives, non-primitives, type coercion, and conversions',
        'video_url': 'https://www.youtube.com/embed/sZ5Y82aWw6c?controls=1&modestbranding=0&rel=0&autoplay=0',
        'video_duration': '1.5 hours',
        'information': '''<h3>🧩 STEP 3: Data Types & Type System</h3>

<h4>Step 3.1: Learn Primitive Types</h4>
<ul>
<li>number</li>
<li>string</li>
<li>boolean</li>
<li>undefined</li>
<li>null</li>
<li>symbol</li>
</ul>

<h4>Step 3.2: Learn Non-Primitive Types</h4>
<ul>
<li>object</li>
<li>array</li>
<li>function</li>
</ul>

<h4>Step 3.3: Understand</h4>
<ul>
<li>Type coercion</li>
<li>Type conversion</li>
</ul>

<h4>Step 3.4: Practice</h4>
<ul>
<li>== vs === comparisons</li>
<li>typeof experiments</li>
</ul>''',
        'learning_objectives': [
            'Master all primitive types',
            'Understand non-primitive types',
            'Learn type coercion rules',
            'Practice type conversions'
        ],
        'quiz_questions': [
            {'question': 'Which is NOT a primitive type?', 'options': ['number', 'string', 'object', 'boolean'], 'correct': 2, 'explanation': 'object is NOT a primitive type; it is a non-primitive type.'},
            {'question': 'What does typeof null return?', 'options': ['null', 'object', 'undefined', 'number'], 'correct': 1, 'explanation': 'typeof null returns "object" (this is a known quirk in JavaScript).'},
            {'question': 'Which operator checks both value and type?', 'options': ['==', '!=', '===', '='], 'correct': 2, 'explanation': 'The === operator checks both value and type.'}
        ]
    },
    'js-module4': {
        'title': 'Step 4: Control Flow & Conditions',
        'description': 'Master if, else, switch, and logical operators',
        'video_url': 'https://www.youtube.com/embed/IsG4Xd6LlsM?controls=1&modestbranding=0&rel=0&autoplay=0',
        'video_duration': '1 hour',
        'information': '''<h3>🧩 STEP 4: Control Flow & Conditions</h3>

<h4>Step 4.1: Write Conditions Using</h4>
<ul>
<li>if</li>
<li>else</li>
<li>else if</li>
</ul>

<h4>Step 4.2: Use Logical Operators</h4>
<ul>
<li>&&</li>
<li>||</li>
<li>!</li>
</ul>

<h4>Step 4.3: Learn Switch Statement</h4>

<h4>Step 4.4: Practice</h4>
<ul>
<li>Grade calculator</li>
<li>Login logic</li>
</ul>''',
        'learning_objectives': [
            'Write if-else statements',
            'Use logical operators correctly',
            'Implement switch statements',
            'Build decision logic'
        ],
        'quiz_questions': [
            {'question': 'Which statement handles multiple conditions cleanly?', 'options': ['if', 'for', 'switch', 'while'], 'correct': 2, 'explanation': 'The switch statement handles multiple conditions cleanly.'},
            {'question': 'Which operator returns the first truthy value?', 'options': ['&&', '||', '!', '??'], 'correct': 1, 'explanation': 'The || operator returns the first truthy value.'}
        ]
    },
    'js-module5': {
        'title': 'Step 5: Loops & Iteration',
        'description': 'Master for, while, do-while, break, and continue',
        'video_url': 'https://www.youtube.com/embed/x23SxjFsE3o?controls=1&modestbranding=0&rel=0&autoplay=0',
        'video_duration': '1.5 hours',
        'information': '''<h3>🧩 STEP 5: Loops & Iteration</h3>

<h4>Step 5.1: Learn Loops</h4>
<ul>
<li>for</li>
<li>while</li>
<li>do…while</li>
</ul>

<h4>Step 5.2: Control Loops Using</h4>
<ul>
<li>break</li>
<li>continue</li>
</ul>

<h4>Step 5.3: Nested Loops</h4>

<h4>Step 5.4: Practice</h4>
<ul>
<li>Number patterns</li>
<li>Array traversal</li>
</ul>''',
        'learning_objectives': [
            'Master for, while, do-while loops',
            'Use break and continue',
            'Create nested loops',
            'Build patterns and traverse arrays'
        ],
        'quiz_questions': [
            {'question': 'Which loop runs at least once?', 'options': ['for', 'while', 'do…while', 'forEach'], 'correct': 2, 'explanation': 'The do…while loop runs at least once because the condition is checked after execution.'},
            {'question': 'Which keyword skips the current iteration?', 'options': ['stop', 'break', 'skip', 'continue'], 'correct': 3, 'explanation': 'The continue keyword skips the current iteration.'}
        ]
    },
    'js-module6': {
        'title': 'Step 6: Functions (Core)',
        'description': 'Master function declarations, expressions, and arrow functions',
        'video_url': 'https://www.youtube.com/embed/FOD408a0EzU?controls=1&modestbranding=0&rel=0&autoplay=0',
        'video_duration': '1.5 hours',
        'information': '''<h3>🧩 STEP 6: Functions (Core)</h3>

<h4>Step 6.1: Write Normal Functions</h4>
<pre>function add(a, b) {
  return a + b;
}</pre>

<h4>Step 6.2: Function Expressions</h4>

<h4>Step 6.3: Arrow Functions</h4>

<h4>Step 6.4: Practice</h4>
<ul>
<li>Calculator functions</li>
<li>Reusable utilities</li>
</ul>''',
        'learning_objectives': [
            'Write function declarations',
            'Use function expressions',
            'Master arrow functions',
            'Return values and parameters'
        ],
        'quiz_questions': [
            {'question': 'Arrow functions differ because they:', 'options': ['Have their own this', 'Do not return values', 'Do not have their own this', 'Cannot take parameters'], 'correct': 2, 'explanation': 'Arrow functions do not have their own this context.'},
            {'question': 'A function stored in a variable is called:', 'options': ['Method', 'Expression', 'Declaration', 'Callback'], 'correct': 1, 'explanation': 'A function stored in a variable is called a function expression.'}
        ]
    },
    'js-module7': {
        'title': 'Step 7: Arrays & Objects',
        'description': 'Master array creation, array methods, and object manipulation',
        'video_url': 'https://www.youtube.com/embed/prIGbK0rB1Q?controls=1&modestbranding=0&rel=0&autoplay=0',
        'video_duration': '2 hours',
        'information': '''<h3>🧩 STEP 7: Arrays & Objects</h3>

<h4>Step 7.1: Create and Access Arrays</h4>

<h4>Step 7.2: Array Methods</h4>
<ul>
<li>push</li>
<li>pop</li>
<li>slice</li>
<li>splice</li>
</ul>

<h4>Step 7.3: Objects and Property Access</h4>

<h4>Step 7.4: Practice</h4>
<ul>
<li>Student data object</li>
<li>Product list array</li>
</ul>''',
        'learning_objectives': [
            'Create and access arrays',
            'Use array methods',
            'Create and manipulate objects',
            'Access object properties'
        ],
        'quiz_questions': [
            {'question': 'Which method adds an element to the end of an array?', 'options': ['pop', 'shift', 'push', 'unshift'], 'correct': 2, 'explanation': 'The push method adds an element to the end of an array.'},
            {'question': 'Object properties can be accessed using:', 'options': ['Dot only', 'Bracket only', 'Both dot and bracket', 'Neither'], 'correct': 2, 'explanation': 'Object properties can be accessed using both dot notation and bracket notation.'}
        ]
    },
    'js-module8': {
        'title': 'Step 8: Advanced Array & Object Methods',
        'description': 'Master map(), filter(), reduce(), and object operations',
        'video_url': 'https://www.youtube.com/embed/R9SmjzY-DwE?controls=1&modestbranding=0&rel=0&autoplay=0',
        'video_duration': '2 hours',
        'information': '''<h3>🧩 STEP 8: Advanced Array & Object Methods</h3>

<h4>Step 8.1: Use map()</h4>

<h4>Step 8.2: Use filter()</h4>

<h4>Step 8.3: Use reduce()</h4>

<h4>Step 8.4: Practice</h4>
<ul>
<li>Data transformation</li>
<li>Aggregation logic</li>
</ul>''',
        'learning_objectives': [
            'Use map() for transformation',
            'Use filter() for selection',
            'Use reduce() for aggregation',
            'Manipulate objects with Object methods'
        ],
        'quiz_questions': [
            {'question': 'Which method transforms each element?', 'options': ['filter', 'map', 'reduce', 'find'], 'correct': 1, 'explanation': 'The map method transforms each element in an array.'},
            {'question': 'Which method returns a single value?', 'options': ['map', 'filter', 'reduce', 'forEach'], 'correct': 2, 'explanation': 'The reduce method returns a single value based on the accumulator.'}
        ]
    },
    'js-module9': {
        'title': 'Step 9: Closures & Advanced Functions',
        'description': 'Master closures, higher-order functions, and function composition',
        'video_url': 'https://www.youtube.com/embed/t9r0Hudyl8E?controls=1&modestbranding=0&rel=0&autoplay=0',
        'video_duration': '1.5 hours',
        'information': '''<h3>🧩 STEP 9: Closures & Advanced Functions</h3>

<h4>Step 9.1: Function Inside Function</h4>

<h4>Step 9.2: Understand Closure Memory Behavior</h4>

<h4>Step 9.3: Higher-Order Functions</h4>

<h4>Step 9.4: Practice</h4>
<ul>
<li>Counter using closure</li>
<li>Custom HOF</li>
</ul>''',
        'learning_objectives': [
            'Understand closures concept',
            'Learn closure memory behavior',
            'Create higher-order functions',
            'Use function composition'
        ],
        'quiz_questions': [
            {'question': 'A closure is created when:', 'options': ['Function returns another function', 'Function accesses outer scope variables', 'Function is async', 'Function is recursive'], 'correct': 1, 'explanation': 'A closure is created when a function accesses variables from its outer scope.'}
        ]
    },
    'js-module10': {
        'title': 'Step 10: Asynchronous JavaScript',
        'description': 'Master callbacks, promises, and async/await',
        'video_url': 'https://www.youtube.com/embed/W6MIjkaI_p0?controls=1&modestbranding=0&rel=0&autoplay=0',
        'video_duration': '2 hours',
        'information': '''<h3>🧩 STEP 10: Asynchronous JavaScript</h3>

<h4>Step 10.1: Understand Synchronous vs Asynchronous</h4>

<h4>Step 10.2: Callbacks</h4>

<h4>Step 10.3: Promises</h4>

<h4>Step 10.4: async / await</h4>''',
        'learning_objectives': [
            'Understand synchronous vs asynchronous',
            'Master callback functions',
            'Use promises (.then/.catch)',
            'Master async/await syntax'
        ],
        'quiz_questions': [
            {'question': 'Which runs asynchronously?', 'options': ['for loop', 'console.log', 'setTimeout', 'return'], 'correct': 2, 'explanation': 'setTimeout runs asynchronously after a specified delay.'},
            {'question': 'Which keyword pauses async execution?', 'options': ['stop', 'wait', 'await', 'delay'], 'correct': 2, 'explanation': 'The await keyword pauses async execution until the promise is resolved.'}
        ]
    },
    'js-module11': {
        'title': 'Step 11: Event Loop & Concurrency',
        'description': 'Master call stack, web APIs, callback queue, and microtasks',
        'video_url': 'https://www.youtube.com/embed/8aGhZQkoFbQ?controls=1&modestbranding=0&rel=0&autoplay=0',
        'video_duration': '2 hours',
        'information': '''<h3>🧩 STEP 11: Event Loop & Concurrency</h3>

<h4>Step 11.1: Call Stack</h4>

<h4>Step 11.2: Web APIs</h4>

<h4>Step 11.3: Callback Queue</h4>

<h4>Step 11.4: Microtasks vs Macrotasks</h4>''',
        'learning_objectives': [
            'Understand Call Stack concept',
            'Know Web APIs role',
            'Learn callback queue mechanics',
            'Master microtasks vs macrotasks'
        ],
        'quiz_questions': [
            {'question': 'Which queue has higher priority?', 'options': ['Callback queue', 'Task queue', 'Microtask queue', 'Stack'], 'correct': 2, 'explanation': 'The Microtask queue has higher priority than the callback queue.'}
        ]
    },
    'js-module12': {
        'title': 'Step 12: DOM Manipulation',
        'description': 'Master selecting elements, modifying DOM, and event listeners',
        'video_url': 'https://www.youtube.com/embed/y17RuWkWdn0?controls=1&modestbranding=0&rel=0&autoplay=0',
        'video_duration': '1.5 hours',
        'information': '''<h3>🧩 STEP 12: DOM Manipulation</h3>

<h4>Step 12.1: Select Elements</h4>

<h4>Step 12.2: Modify DOM Content</h4>

<h4>Step 12.3: Event Listeners</h4>

<h4>Step 12.4: Practice</h4>
<ul>
<li>Button click app</li>
<li>Form validation</li>
</ul>''',
        'learning_objectives': [
            'Select DOM elements',
            'Modify DOM content and classes',
            'Add event listeners',
            'Build interactive features'
        ],
        'quiz_questions': [
            {'question': 'Which method selects the first matching element?', 'options': ['getElementsByClassName', 'querySelector', 'querySelectorAll', 'getElementById'], 'correct': 1, 'explanation': 'The querySelector method selects the first matching element.'},
            {'question': 'Which method attaches events?', 'options': ['onclick', 'addEventListener', 'attach', 'bind'], 'correct': 1, 'explanation': 'The addEventListener method attaches event listeners to elements.'}
        ]
    },
    'js-module13': {
        'title': 'Step 13: Browser APIs & Storage',
        'description': 'Master localStorage, sessionStorage, timers, and browser features',
        'video_url': 'https://www.youtube.com/embed/Lyx2V2CXpLY?controls=1&modestbranding=0&rel=0&autoplay=0',
        'video_duration': '1.5 hours',
        'information': '''<h3>🧩 STEP 13: Browser APIs & Storage</h3>

<h4>Step 13.1: localStorage</h4>

<h4>Step 13.2: sessionStorage</h4>

<h4>Step 13.3: Timers</h4>

<h4>Step 13.4: Practice</h4>
<ul>
<li>Todo app storage</li>
</ul>''',
        'learning_objectives': [
            'Use localStorage for persistent storage',
            'Use sessionStorage for temporary storage',
            'Master setTimeout and setInterval',
            'Build storage-based applications'
        ],
        'quiz_questions': [
            {'question': 'Which storage persists after browser close?', 'options': ['sessionStorage', 'cookies only', 'localStorage', 'cache'], 'correct': 2, 'explanation': 'localStorage persists data even after the browser is closed.'}
        ]
    },
    'js-module14': {
        'title': 'Step 14: Error Handling & Debugging',
        'description': 'Master try-catch-finally, custom errors, and debugging',
        'video_url': 'https://www.youtube.com/embed/e-5obm1G_FY?controls=1&modestbranding=0&rel=0&autoplay=0',
        'video_duration': '1.5 hours',
        'information': '''<h3>🧩 STEP 14: Error Handling & Debugging</h3>

<h4>Step 14.1: try / catch / finally</h4>

<h4>Step 14.2: Custom Errors</h4>

<h4>Step 14.3: Common JS Errors</h4>

<h4>Step 14.4: Debugging in Browser</h4>''',
        'learning_objectives': [
            'Use try-catch-finally blocks',
            'Throw custom errors',
            'Understand error types',
            'Debug using browser tools'
        ],
        'quiz_questions': [
            {'question': 'Which block always executes?', 'options': ['try', 'catch', 'else', 'finally'], 'correct': 3, 'explanation': 'The finally block always executes, whether an error occurred or not.'}
        ]
    },
    'js-module15': {
        'title': 'Step 15: Modern JavaScript (ES6+)',
        'description': 'Master destructuring, spread operator, template literals, and modules',
        'video_url': 'https://www.youtube.com/embed/Up0rCqrV53o?controls=1&modestbranding=0&rel=0&autoplay=0',
        'video_duration': '2 hours',
        'information': '''<h3>🧩 STEP 15: Modern JavaScript (ES6+)</h3>

<h4>Step 15.1: Destructuring</h4>

<h4>Step 15.2: Spread & Rest Operators</h4>

<h4>Step 15.3: Template Literals</h4>

<h4>Step 15.4: Modules (import/export)</h4>''',
        'learning_objectives': [
            'Use destructuring for objects and arrays',
            'Master spread operator',
            'Use template literals',
            'Import/export modules'
        ],
        'quiz_questions': [
            {'question': 'Which feature allows unpacking values?', 'options': ['Spread', 'Destructuring', 'Hoisting', 'Binding'], 'correct': 1, 'explanation': 'Destructuring allows unpacking values from arrays or properties from objects.'}
        ]
    },
    'js-module16': {
        'title': 'Step 16: Object-Oriented JavaScript',
        'description': 'Master constructors, prototypes, classes, and inheritance',
        'video_url': 'https://www.youtube.com/embed/GfBvVwjeVAY?controls=1&modestbranding=0&rel=0&autoplay=0',
        'video_duration': '2 hours',
        'information': '''<h3>🧩 STEP 16: Object-Oriented JavaScript</h3>

<h4>Step 16.1: Constructor Functions</h4>

<h4>Step 16.2: Prototypes</h4>

<h4>Step 16.3: Classes</h4>

<h4>Step 16.4: Inheritance</h4>''',
        'learning_objectives': [
            'Use constructor functions',
            'Understand prototypes',
            'Create classes',
            'Implement inheritance'
        ],
        'quiz_questions': [
            {'question': 'Classes in JS are based on:', 'options': ['Classical inheritance', 'Functional inheritance', 'Prototype-based inheritance', 'Interface-based inheritance'], 'correct': 2, 'explanation': 'JavaScript classes are based on prototype-based inheritance.'}
        ]
    },
    'js-module17': {
        'title': 'Step 17: Performance & Best Practices',
        'description': 'Optimize code, avoid memory leaks, clean structure, and security basics',
        'video_url': 'https://www.youtube.com/embed/0UtJr3sJ6kc?controls=1&modestbranding=0&rel=0&autoplay=0',
        'video_duration': '1.5 hours',
        'information': '''<h3>🧩 STEP 17: Performance & Best Practices</h3>

<h4>Step 17.1: Optimize Loops & Logic</h4>

<h4>Step 17.2: Avoid Memory Leaks</h4>

<h4>Step 17.3: Clean Code Structure</h4>

<h4>Step 17.4: Security Basics</h4>''',
        'learning_objectives': [
            'Optimize JavaScript performance',
            'Prevent memory leaks',
            'Write clean code',
            'Follow security best practices'
        ],
        'quiz_questions': [
            {'question': 'Which causes memory leaks?', 'options': ['Closures', 'Unremoved event listeners', 'Arrow functions', 'const variables'], 'correct': 1, 'explanation': 'Unremoved event listeners can cause memory leaks.'}
        ]
    },
    'js-module18': {
        'title': 'Step 18: Mini Projects',
        'description': 'Build calculator, todo app, quiz app, and API-based applications',
        'video_url': 'https://www.youtube.com/embed/f6qkqYgPlG4?controls=1&modestbranding=0&rel=0&autoplay=0',
        'video_duration': '3 hours',
        'information': '''<h3>🧩 STEP 18: Mini Projects</h3>

<h4>Step 18.1: Calculator App</h4>

<h4>Step 18.2: Todo App</h4>

<h4>Step 18.3: Quiz App</h4>

<h4>Step 18.4: API-Based App</h4>''',
        'learning_objectives': [
            'Build working JavaScript projects',
            'Integrate all learned concepts',
            'Handle user interactions',
            'Use external APIs'
        ],
        'quiz_questions': [
            {'question': 'Which feature is required for a Todo app?', 'options': ['Compiler', 'DOM manipulation', 'Encryption', 'Web sockets'], 'correct': 1, 'explanation': 'DOM manipulation is essential for building a Todo app to interact with the user interface.'}
        ]
    },
    'js-module19': {
        'title': 'Step 19: Capstone Project',
        'description': 'Plan, design, implement, and optimize a full JavaScript application',
        'video_url': 'https://www.youtube.com/embed/3PHXvlpOkKI?controls=1&modestbranding=0&rel=0&autoplay=0',
        'video_duration': '4 hours',
        'information': '''<h3>🧩 STEP 19: Capstone Project</h3>

<h4>Step 19.1: Plan Project</h4>

<h4>Step 19.2: Design Structure</h4>

<h4>Step 19.3: Implement Full App</h4>

<h4>Step 19.4: Optimize & Finalize</h4>''',
        'learning_objectives': [
            'Plan complex application',
            'Design scalable architecture',
            'Implement full-featured app',
            'Deploy and optimize'
        ],
        'quiz_questions': [
            {'question': 'What is the first step of a capstone project?', 'options': ['Coding', 'Deployment', 'Planning', 'Optimization'], 'correct': 2, 'explanation': 'Planning is the first crucial step of any capstone project.'}
        ]
    }
}

# TypeScript Mastery Course - 21 comprehensive modules
TYPESCRIPT_MASTERY_MODULE_DETAILS = {
    'ts-module1': {
        'title': 'Step 1: TypeScript Setup & Compiler Basics',
        'description': 'Install TypeScript, create your first file, and compile to JavaScript',
        'video_url': 'https://www.youtube.com/embed/BwuLxPH8IDs?controls=1&modestbranding=0&rel=0&autoplay=0',
        'video_duration': '1.5 hours',
        'information': '''<h3>🧩 STEP 1: TypeScript Setup & Compiler Basics</h3>

<h4>Step 1.1: Install TypeScript</h4>
<pre>npm install -g typescript</pre>

<h4>Step 1.2: Create a TypeScript File</h4>
<pre>let x: number = 10;
console.log(x);</pre>

<h4>Step 1.3: Compile TypeScript to JavaScript</h4>
<pre>tsc index.ts</pre>

<h4>Step 1.4: Practice</h4>
<ul>
<li>Compile multiple files</li>
<li>Observe generated JavaScript</li>
</ul>''',
        'learning_objectives': ['Install TypeScript globally', 'Write typed TypeScript code', 'Compile TS to JS', 'Understand transpilation process'],
        'quiz_questions': [
            {'question': 'What command installs TypeScript globally?', 'options': ['npm install typescript', 'npm install -g typescript', 'npm setup typescript', 'tsc install'], 'correct': 1, 'explanation': 'npm install -g typescript installs TypeScript globally.'},
            {'question': 'How do you compile a TypeScript file?', 'options': ['run file.ts', 'tsc file.ts', 'node file.ts', 'compile file.ts'], 'correct': 1, 'explanation': 'tsc file.ts compiles TypeScript to JavaScript.'}
        ]
    },
    'ts-module2': {
        'title': 'Step 2: Basic Types',
        'description': 'Master primitive types, arrays, tuples, and type declarations',
        'video_url': 'https://www.youtube.com/embed/ahCwqrYpIuM?controls=1&modestbranding=0&rel=0&autoplay=0',
        'video_duration': '1.5 hours',
        'information': '''<h3>🧩 STEP 2: Basic Types</h3>

<h4>Step 2.1: Use Primitive Types</h4>
<pre>number, string, boolean</pre>

<h4>Step 2.2: Use Arrays and Tuples</h4>
<pre>let nums: number[] = [1, 2, 3];
let user: [string, number] = ["Alex", 20];</pre>

<h4>Step 2.3: Use any, unknown, void, never</h4>

<h4>Step 2.4: Practice</h4>
<ul>
<li>Replace any with proper types</li>
</ul>''',
        'learning_objectives': ['Declare primitive types', 'Create typed arrays and tuples', 'Understand special types', 'Avoid using any'],
        'quiz_questions': [
            {'question': 'How do you declare a number array?', 'options': ['let arr: []number', 'let arr: number[]', 'let arr: [number]', 'let arr = number[]'], 'correct': 1, 'explanation': 'number[] declares an array of numbers.'},
            {'question': 'What is a tuple?', 'options': ['Variable length array', 'Fixed length array with specific types', 'Object literal', 'String array'], 'correct': 1, 'explanation': 'A tuple is a fixed-length array with specific types for each position.'}
        ]
    },
    'ts-module3': {
        'title': 'Step 3: Type Inference & Type Annotations',
        'description': 'Understand implicit typing and explicit annotations',
        'video_url': 'https://www.youtube.com/embed/Z5iWr6Srsj8?controls=1&modestbranding=0&rel=0&autoplay=0',
        'video_duration': '1 hour',
        'information': '''<h3>🧩 STEP 3: Type Inference & Type Annotations</h3>

<h4>Step 3.1: Let TypeScript Infer Types Automatically</h4>

<h4>Step 3.2: Add Explicit Type Annotations</h4>

<h4>Step 3.3: Understand Implicit vs Explicit Typing</h4>

<h4>Step 3.4: Practice</h4>
<ul>
<li>Fix type errors</li>
</ul>''',
        'learning_objectives': ['Use type inference', 'Write explicit annotations', 'Know when to annotate', 'Fix type mismatches'],
        'quiz_questions': [
            {'question': 'When TypeScript infers type, it is called:', 'options': ['Type annotation', 'Type inference', 'Type casting', 'Type narrowing'], 'correct': 1, 'explanation': 'Type inference is when TypeScript automatically determines the type.'},
            {'question': 'Which is an explicit annotation?', 'options': ['let x = 5', 'let x: number = 5', 'const x = 5', 'var x = 5'], 'correct': 1, 'explanation': 'let x: number = 5 explicitly annotates the type.'}
        ]
    },
    'ts-module4': {
        'title': 'Step 4: Functions & Typing',
        'description': 'Type function parameters, return values, and optional parameters',
        'video_url': 'https://www.youtube.com/embed/9j1dZwFEJ-c?controls=1&modestbranding=0&rel=0&autoplay=0',
        'video_duration': '1.5 hours',
        'information': '''<h3>🧩 STEP 4: Functions & Typing</h3>

<h4>Step 4.1: Type Function Parameters</h4>
<pre>function add(a: number, b: number): number {
  return a + b;
}</pre>

<h4>Step 4.2: Optional & Default Parameters</h4>

<h4>Step 4.3: Function Types</h4>

<h4>Step 4.4: Practice</h4>
<ul>
<li>Strongly typed utility functions</li>
</ul>''',
        'learning_objectives': ['Type function parameters', 'Type return values', 'Use optional parameters', 'Create function types'],
        'quiz_questions': [
            {'question': 'How do you type function return value?', 'options': ['function f(): number', 'function f() -> number', 'function f(: number)', 'function f(): : number'], 'correct': 0, 'explanation': 'function f(): number specifies the return type.'},
            {'question': 'How do you make a parameter optional?', 'options': ['param: type', 'param?: type', '[param]: type', 'param!: type'], 'correct': 1, 'explanation': 'param?: type makes a parameter optional.'}
        ]
    },
    'ts-module5': {
        'title': 'Step 5: Objects & Type Aliases',
        'description': 'Type object literals and create reusable type aliases',
        'video_url': 'https://www.youtube.com/embed/EJm1x5QG2tY?controls=1&modestbranding=0&rel=0&autoplay=0',
        'video_duration': '1 hour',
        'information': '''<h3>🧩 STEP 5: Objects & Type Aliases</h3>

<h4>Step 5.1: Type Object Literals</h4>

<h4>Step 5.2: Create Type Aliases</h4>

<h4>Step 5.3: Readonly Properties</h4>

<h4>Step 5.4: Practice</h4>
<ul>
<li>User profile object</li>
</ul>''',
        'learning_objectives': ['Type object shapes', 'Create type aliases', 'Use readonly modifier', 'Build complex types'],
        'quiz_questions': [
            {'question': 'How do you create a type alias?', 'options': ['interface User', 'type User', 'class User', 'const User'], 'correct': 1, 'explanation': 'type keyword creates a type alias.'},
            {'question': 'What does readonly do?', 'options': ['Makes property visible', 'Prevents property modification', 'Makes property optional', 'Hides property'], 'correct': 1, 'explanation': 'readonly prevents a property from being modified.'}
        ]
    },
    'ts-module6': {
        'title': 'Step 6: Interfaces (Core)',
        'description': 'Create and use interfaces for object contracts',
        'video_url': 'https://www.youtube.com/embed/VbW6vWTaHOY?controls=1&modestbranding=0&rel=0&autoplay=0',
        'video_duration': '1.5 hours',
        'information': '''<h3>🧩 STEP 6: Interfaces (Core)</h3>

<h4>Step 6.1: Create Interfaces</h4>

<h4>Step 6.2: Interface vs Type</h4>

<h4>Step 6.3: Optional Properties</h4>

<h4>Step 6.4: Practice</h4>
<ul>
<li>Interface-based objects</li>
</ul>''',
        'learning_objectives': ['Create interfaces', 'Understand interface contracts', 'Use optional properties', 'Implement interfaces'],
        'quiz_questions': [
            {'question': 'How do you declare an interface?', 'options': ['class IUser', 'interface IUser', 'type IUser', 'struct IUser'], 'correct': 1, 'explanation': 'interface keyword declares an interface.'},
            {'question': 'How do you make an interface property optional?', 'options': ['prop: type;', 'prop?: type;', '[prop]: type;', 'prop!: type;'], 'correct': 1, 'explanation': 'prop?: type makes an interface property optional.'}
        ]
    },
    'ts-module7': {
        'title': 'Step 7: Advanced Interfaces',
        'description': 'Interface extension, function interfaces, and index signatures',
        'video_url': 'https://www.youtube.com/embed/R8rmfD9Y5-c?controls=1&modestbranding=0&rel=0&autoplay=0',
        'video_duration': '1.5 hours',
        'information': '''<h3>🧩 STEP 7: Advanced Interfaces</h3>

<h4>Step 7.1: Interface Extension</h4>

<h4>Step 7.2: Function Interfaces</h4>

<h4>Step 7.3: Index Signatures</h4>

<h4>Step 7.4: Practice</h4>
<ul>
<li>Config system</li>
</ul>''',
        'learning_objectives': ['Extend interfaces', 'Create function interfaces', 'Use index signatures', 'Build flexible contracts'],
        'quiz_questions': [
            {'question': 'How do you extend an interface?', 'options': ['interface B implements A', 'interface B extends A', 'interface B : A', 'interface B -> A'], 'correct': 1, 'explanation': 'extends keyword is used to extend an interface.'},
            {'question': 'What are index signatures used for?', 'options': ['Defining numeric keys', 'Allowing dynamic property names', 'Creating arrays', 'Setting default values'], 'correct': 1, 'explanation': 'Index signatures allow objects to have dynamic property names.'}
        ]
    },
    'ts-module8': {
        'title': 'Step 8: Union & Intersection Types',
        'description': 'Combine types using union and intersection operators',
        'video_url': 'https://www.youtube.com/embed/Gi2wzZz9m-k?controls=1&modestbranding=0&rel=0&autoplay=0',
        'video_duration': '1.5 hours',
        'information': '''<h3>🧩 STEP 8: Union & Intersection Types</h3>

<h4>Step 8.1: Union Types</h4>
<pre>number | string</pre>

<h4>Step 8.2: Type Narrowing</h4>

<h4>Step 8.3: Intersection Types</h4>

<h4>Step 8.4: Practice</h4>
<ul>
<li>Flexible API response types</li>
</ul>''',
        'learning_objectives': ['Create union types', 'Narrow union types', 'Use intersection types', 'Handle multiple type options'],
        'quiz_questions': [
            {'question': 'What does number | string mean?', 'options': ['number AND string', 'number OR string', 'number to string', 'number modulo string'], 'correct': 1, 'explanation': '| represents union type (OR).'},
            {'question': 'What does & operator do?', 'options': ['Creates union', 'Creates intersection', 'Bitwise AND', 'Combines arrays'], 'correct': 1, 'explanation': '& creates an intersection type combining all properties.'}
        ]
    },
    'ts-module9': {
        'title': 'Step 9: Enums & Literal Types',
        'description': 'Use enums and literal types for restricted values',
        'video_url': 'https://www.youtube.com/embed/4nmoZkY0r2s?controls=1&modestbranding=0&rel=0&autoplay=0',
        'video_duration': '1 hour',
        'information': '''<h3>🧩 STEP 9: Enums & Literal Types</h3>

<h4>Step 9.1: Numeric Enums</h4>

<h4>Step 9.2: String Enums</h4>

<h4>Step 9.3: Literal Types</h4>

<h4>Step 9.4: Practice</h4>
<ul>
<li>Role-based logic</li>
</ul>''',
        'learning_objectives': ['Create numeric enums', 'Create string enums', 'Use literal types', 'Restrict allowed values'],
        'quiz_questions': [
            {'question': 'What are enums used for?', 'options': ['Temporary variables', 'Restricted set of values', 'Memory allocation', 'Type conversion'], 'correct': 1, 'explanation': 'Enums define a restricted set of named constant values.'},
            {'question': 'What is a literal type?', 'options': ['Any string', 'Specific string value like "admin"', 'String union', 'String interface'], 'correct': 1, 'explanation': 'Literal types restrict to specific values like "admin" | "user".'}
        ]
    },
    'ts-module10': {
        'title': 'Step 10: Generics (VERY IMPORTANT)',
        'description': 'Master generics for reusable, type-safe code',
        'video_url': 'https://www.youtube.com/embed/nViEqpgwxHE?controls=1&modestbranding=0&rel=0&autoplay=0',
        'video_duration': '2 hours',
        'information': '''<h3>🧩 STEP 10: Generics (VERY IMPORTANT)</h3>

<h4>Step 10.1: Generic Functions</h4>

<h4>Step 10.2: Generic Interfaces</h4>

<h4>Step 10.3: Generic Constraints</h4>

<h4>Step 10.4: Practice</h4>
<ul>
<li>Reusable typed utilities</li>
</ul>''',
        'learning_objectives': ['Create generic functions', 'Use generic interfaces', 'Apply constraints', 'Build reusable components'],
        'quiz_questions': [
            {'question': 'How do you declare a generic function?', 'options': ['function<T>', 'function(T)', 'function<T>(param: T)', 'function[T]'], 'correct': 2, 'explanation': 'function<T>(param: T) declares a generic function.'},
            {'question': 'What is a generic constraint?', 'options': ['Limiting function calls', 'Restricting type parameter', 'Type validation', 'Memory limit'], 'correct': 1, 'explanation': 'Constraints restrict what types can be used as type parameters.'}
        ]
    },
    'ts-module11': {
        'title': 'Step 11: Classes & OOP in TypeScript',
        'description': 'Use classes with access modifiers and strong typing',
        'video_url': 'https://www.youtube.com/embed/IYF1zj0dM3E?controls=1&modestbranding=0&rel=0&autoplay=0',
        'video_duration': '1.5 hours',
        'information': '''<h3>🧩 STEP 11: Classes & OOP in TypeScript</h3>

<h4>Step 11.1: Class Properties & Constructor</h4>

<h4>Step 11.2: Access Modifiers</h4>
<pre>public, private, protected</pre>

<h4>Step 11.3: Readonly & Parameter Properties</h4>

<h4>Step 11.4: Practice</h4>
<ul>
<li>Class-based service</li>
</ul>''',
        'learning_objectives': ['Create classes with types', 'Use access modifiers', 'Apply readonly', 'Build class services'],
        'quiz_questions': [
            {'question': 'What is the default access modifier?', 'options': ['private', 'protected', 'public', 'readonly'], 'correct': 2, 'explanation': 'public is the default access modifier.'},
            {'question': 'What does private do?', 'options': ['Hides from outside', 'Limits to class', 'Prevents modification', 'Restricts methods'], 'correct': 0, 'explanation': 'private restricts access to only within the class.'}
        ]
    },
    'ts-module12': {
        'title': 'Step 12: Inheritance & Abstract Classes',
        'description': 'Extend classes and use abstract classes',
        'video_url': 'https://www.youtube.com/embed/H0XScE08hy8?controls=1&modestbranding=0&rel=0&autoplay=0',
        'video_duration': '1.5 hours',
        'information': '''<h3>🧩 STEP 12: Inheritance & Abstract Classes</h3>

<h4>Step 12.1: Extend Classes</h4>

<h4>Step 12.2: Method Overriding</h4>

<h4>Step 12.3: Abstract Classes</h4>

<h4>Step 12.4: Practice</h4>
<ul>
<li>Plugin system</li>
</ul>''',
        'learning_objectives': ['Extend classes', 'Override methods', 'Create abstract classes', 'Build inheritance hierarchies'],
        'quiz_questions': [
            {'question': 'How do you extend a class?', 'options': ['class B implements A', 'class B extends A', 'class B : A', 'class B -> A'], 'correct': 1, 'explanation': 'extends keyword is used to extend a class.'},
            {'question': 'Can you instantiate an abstract class?', 'options': ['Yes', 'No', 'Sometimes', 'Only with new'], 'correct': 1, 'explanation': 'Abstract classes cannot be instantiated directly.'}
        ]
    },
    'ts-module13': {
        'title': 'Step 13: Type Guards & Advanced Narrowing',
        'description': 'Safe type narrowing with guards and predicates',
        'video_url': 'https://www.youtube.com/embed/2jXnmdYpJcs?controls=1&modestbranding=0&rel=0&autoplay=0',
        'video_duration': '1.5 hours',
        'information': '''<h3>🧩 STEP 13: Type Guards & Advanced Narrowing</h3>

<h4>Step 13.1: typeof Guards</h4>

<h4>Step 13.2: in Operator</h4>

<h4>Step 13.3: Custom Type Guards</h4>

<h4>Step 13.4: Practice</h4>
<ul>
<li>Safe runtime checks</li>
</ul>''',
        'learning_objectives': ['Use typeof guards', 'Use in operator', 'Create custom guards', 'Narrow types safely'],
        'quiz_questions': [
            {'question': 'What does typeof guard check?', 'options': ['Object type', 'Runtime type', 'Interface', 'Class name'], 'correct': 1, 'explanation': 'typeof checks the runtime type.'},
            {'question': 'What is a custom type guard?', 'options': ['Predicate function returning true/false', 'Builtin type check', 'Interface definition', 'Class method'], 'correct': 0, 'explanation': 'Custom type guards are predicate functions that return type predicates.'}
        ]
    },
    'ts-module14': {
        'title': 'Step 14: Utility Types',
        'description': 'Use built-in utility types for type manipulation',
        'video_url': 'https://www.youtube.com/embed/8pDqJVdNa44?controls=1&modestbranding=0&rel=0&autoplay=0',
        'video_duration': '1.5 hours',
        'information': '''<h3>🧩 STEP 14: Utility Types</h3>

<h4>Step 14.1: Partial</h4>

<h4>Step 14.2: Pick & Omit</h4>

<h4>Step 14.3: Readonly & Record</h4>

<h4>Step 14.4: Practice</h4>
<ul>
<li>Data transformation types</li>
</ul>''',
        'learning_objectives': ['Use Partial type', 'Use Pick and Omit', 'Use Readonly and Record', 'Transform types dynamically'],
        'quiz_questions': [
            {'question': 'What does Partial do?', 'options': ['Makes all properties required', 'Makes all properties optional', 'Removes properties', 'Adds methods'], 'correct': 1, 'explanation': 'Partial makes all properties optional.'},
            {'question': 'What does Record do?', 'options': ['Creates tuple', 'Creates object with specific keys', 'Creates array', 'Creates union'], 'correct': 1, 'explanation': 'Record creates an object type with specific key-value types.'}
        ]
    },
    'ts-module15': {
        'title': 'Step 15: Modules & Namespaces',
        'description': 'Organize code with modules and namespaces',
        'video_url': 'https://www.youtube.com/embed/KDrWZrR4o1U?controls=1&modestbranding=0&rel=0&autoplay=0',
        'video_duration': '1.5 hours',
        'information': '''<h3>🧩 STEP 15: Modules & Namespaces</h3>

<h4>Step 15.1: ES Modules in TypeScript</h4>

<h4>Step 15.2: Import / Export Syntax</h4>

<h4>Step 15.3: Namespaces</h4>

<h4>Step 15.4: Practice</h4>
<ul>
<li>Modular app structure</li>
</ul>''',
        'learning_objectives': ['Use ES6 modules', 'Export types and values', 'Use namespaces', 'Organize large projects'],
        'quiz_questions': [
            {'question': 'How do you export a type?', 'options': ['export type T', 'type export T', 'public type T', 'type: export T'], 'correct': 0, 'explanation': 'export type keyword exports a type.'},
            {'question': 'What is a namespace?', 'options': ['Module system', 'Named scope for organization', 'Function container', 'Class collection'], 'correct': 1, 'explanation': 'Namespaces create named scopes for organizing code.'}
        ]
    },
    'ts-module16': {
        'title': 'Step 16: Compiler Configuration (tsconfig)',
        'description': 'Configure TypeScript compiler with tsconfig.json',
        'video_url': 'https://www.youtube.com/embed/Z5WJZ5f4B2s?controls=1&modestbranding=0&rel=0&autoplay=0',
        'video_duration': '1 hour',
        'information': '''<h3>🧩 STEP 16: Compiler Configuration (tsconfig)</h3>

<h4>Step 16.1: Create tsconfig.json</h4>

<h4>Step 16.2: Strict Mode</h4>

<h4>Step 16.3: Target & Module Options</h4>

<h4>Step 16.4: Practice</h4>
<ul>
<li>Optimize compile output</li>
</ul>''',
        'learning_objectives': ['Create tsconfig.json', 'Enable strict mode', 'Configure target', 'Optimize compilation'],
        'quiz_questions': [
            {'question': 'What does strict mode do?', 'options': ['Disables types', 'Enables all type checking', 'Compiles faster', 'Reduces file size'], 'correct': 1, 'explanation': 'Strict mode enables all type checking options.'},
            {'question': 'What is target in tsconfig?', 'options': ['Output file', 'JavaScript version target', 'Compiler location', 'Module name'], 'correct': 1, 'explanation': 'target specifies which JavaScript version to compile to.'}
        ]
    },
    'ts-module17': {
        'title': 'Step 17: TypeScript with JavaScript',
        'description': 'Migrate JavaScript to TypeScript gradually',
        'video_url': 'https://www.youtube.com/embed/gmUpkIFdE9M?controls=1&modestbranding=0&rel=0&autoplay=0',
        'video_duration': '1.5 hours',
        'information': '''<h3>🧩 STEP 17: TypeScript with JavaScript</h3>

<h4>Step 17.1: Migrating JS to TS</h4>

<h4>Step 17.2: JSDoc Types</h4>

<h4>Step 17.3: Handling Third-Party Libraries</h4>

<h4>Step 17.4: Practice</h4>
<ul>
<li>Convert JS file to TS</li>
</ul>''',
        'learning_objectives': ['Migrate JavaScript to TypeScript', 'Use JSDoc types', 'Handle untyped libraries', 'Gradual adoption'],
        'quiz_questions': [
            {'question': 'How do you use types in JavaScript files?', 'options': ['Not possible', 'JSDoc comments', 'type files only', 'Inline types'], 'correct': 1, 'explanation': 'JSDoc comments can add types to JavaScript files.'},
            {'question': 'What are type definitions?', 'options': ['.d.ts files with type info', 'Configuration files', 'Source code', 'Module exports'], 'correct': 0, 'explanation': '.d.ts files contain type definitions for untyped libraries.'}
        ]
    },
    'ts-module18': {
        'title': 'Step 18: Error Handling & Debugging',
        'description': 'Handle errors and debug TypeScript code effectively',
        'video_url': 'https://www.youtube.com/embed/6kE2lZx0B5M?controls=1&modestbranding=0&rel=0&autoplay=0',
        'video_duration': '1.5 hours',
        'information': '''<h3>🧩 STEP 18: Error Handling & Debugging</h3>

<h4>Step 18.1: Compile-time vs Runtime Errors</h4>

<h4>Step 18.2: Handling Unknown</h4>

<h4>Step 18.3: Debugging TS Code</h4>

<h4>Step 18.4: Practice</h4>
<ul>
<li>Fix broken types</li>
</ul>''',
        'learning_objectives': ['Understand compile-time errors', 'Handle unknown type', 'Debug TypeScript', 'Catch type errors early'],
        'quiz_questions': [
            {'question': 'When are TypeScript errors caught?', 'options': ['At runtime', 'At compile time', 'During deployment', 'Never'], 'correct': 1, 'explanation': 'TypeScript errors are caught at compile time.'},
            {'question': 'What is the unknown type?', 'options': ['Same as any', 'Type-safe any', 'Optional type', 'Union type'], 'correct': 1, 'explanation': 'unknown is a type-safe alternative to any.'}
        ]
    },
    'ts-module19': {
        'title': 'Step 19: Performance & Best Practices',
        'description': 'Write efficient and maintainable TypeScript',
        'video_url': 'https://www.youtube.com/embed/7R9D5ZgM1yU?controls=1&modestbranding=0&rel=0&autoplay=0',
        'video_duration': '1 hour',
        'information': '''<h3>🧩 STEP 19: Performance & Best Practices</h3>

<h4>Step 19.1: Avoid Over-typing</h4>

<h4>Step 19.2: Type Reusability</h4>

<h4>Step 19.3: Clean Type Architecture</h4>

<h4>Step 19.4: Large-Scale Project Patterns</h4>''',
        'learning_objectives': ['Avoid unnecessary types', 'Reuse type definitions', 'Design clean types', 'Scale TypeScript projects'],
        'quiz_questions': [
            {'question': 'When should you use any?', 'options': ['Always', 'Never', 'Only when necessary', 'For all parameters'], 'correct': 2, 'explanation': 'Avoid any unless absolutely necessary - use unknown or specific types.'},
            {'question': 'Why reuse types?', 'options': ['Save space', 'Maintainability and consistency', 'Faster compilation', 'Fewer errors'], 'correct': 1, 'explanation': 'Reusing types improves maintainability and ensures consistency.'}
        ]
    },
    'ts-module20': {
        'title': 'Step 20: Mini Projects',
        'description': 'Build real applications with TypeScript',
        'video_url': 'https://www.youtube.com/embed/1jz8rQm2f3Y?controls=1&modestbranding=0&rel=0&autoplay=0',
        'video_duration': '3 hours',
        'information': '''<h3>🧩 STEP 20: Mini Projects</h3>

<h4>Step 20.1: Typed Todo App</h4>

<h4>Step 20.2: API Client with Generics</h4>

<h4>Step 20.3: Form Validation System</h4>

<h4>Step 20.4: State Management Logic</h4>''',
        'learning_objectives': ['Build typed applications', 'Use generics practically', 'Create reusable components', 'Implement type-safe patterns'],
        'quiz_questions': [
            {'question': 'What is a typed Todo App?', 'options': ['Array of strings', 'Interface/type-based structure', 'Random data', 'String literals'], 'correct': 1, 'explanation': 'A typed Todo App uses interfaces/types to define Todo structure.'},
            {'question': 'Why use generics in API client?', 'options': ['Required', 'For type-safe responses', 'To reduce code', 'For performance'], 'correct': 1, 'explanation': 'Generics make API clients type-safe for different response types.'}
        ]
    },
    'ts-module21': {
        'title': 'Step 21: Capstone Project',
        'description': 'Design and build a complete TypeScript application',
        'video_url': 'https://www.youtube.com/embed/0qF6Y6E9Z0M?controls=1&modestbranding=0&rel=0&autoplay=0',
        'video_duration': '4 hours',
        'information': '''<h3>🧩 STEP 21: Capstone Project</h3>

<h4>Step 21.1: Plan Project Types</h4>

<h4>Step 21.2: Design Type Architecture</h4>

<h4>Step 21.3: Build Full App</h4>

<h4>Step 21.4: Refactor & Finalize</h4>''',
        'learning_objectives': ['Plan type architecture', 'Design scalable types', 'Build full application', 'Refactor and optimize'],
        'quiz_questions': [
            {'question': 'First step of capstone project?', 'options': ['Code immediately', 'Plan types and architecture', 'Setup server', 'Deploy app'], 'correct': 1, 'explanation': 'Planning types and architecture is the first critical step.'},
            {'question': 'Why design type architecture?', 'options': ['Mandatory', 'Scalability and maintainability', 'For fun', 'No reason'], 'correct': 1, 'explanation': 'Good type architecture ensures scalability and maintainability.'}
        ]
    }
}

# Module details with information, videos, and quiz questions
MODULE_DETAILS = {
    'module1': {
        'title': 'Fundamentals & Getting Started',
        'description': 'Learn the core concepts and fundamentals',
        'information': '''<h3>Module Overview</h3>
<p>In this module, you'll master the foundational concepts essential to this subject. We'll cover:</p>
<ul>
<li>Core principles and theory</li>
<li>Basic terminology and concepts</li>
<li>Practical applications</li>
<li>Best practices for beginners</li>
</ul>
<h3>What You'll Accomplish</h3>
<p>By the end of this module, you'll be able to:</p>
<ul>
<li>✅ Understand core concepts</li>
<li>✅ Apply theory to practice</li>
<li>✅ Solve basic problems</li>
<li>✅ Complete hands-on exercises</li>
</ul>''',
        'video_url': 'https://www.youtube.com/embed/dQw4w9WgXcQ',
        'video_duration': '45 minutes',
        'learning_objectives': [
            'Understand the fundamentals and core concepts',
            'Learn industry standards and best practices',
            'Apply theoretical knowledge practically',
            'Complete foundational exercises'
        ],
        'quiz_questions': [
            {
                'question': 'What is the primary focus of this module?',
                'options': ['Advanced concepts', 'Fundamental principles', 'Specialized tools', 'Case studies'],
                'correct': 1,
                'explanation': 'This module focuses on building a strong foundation with fundamental principles.'
            },
            {
                'question': 'Which learning outcome is emphasized?',
                'options': ['Complex problem solving', 'Core concept understanding', 'Expert-level skills', 'Advanced applications'],
                'correct': 1,
                'explanation': 'The module emphasizes understanding core concepts before moving to advanced topics.'
            },
            {
                'question': 'What type of content is included?',
                'options': ['Only videos', 'Videos, reading, and exercises', 'Theory only', 'Practice problems only'],
                'correct': 1,
                'explanation': 'The module includes videos, reading materials, and practical exercises.'
            },
            {
                'question': 'How much time should you allocate?',
                'options': ['1-2 hours', '3-5 hours', '5-7 hours', '10+ hours'],
                'correct': 2,
                'explanation': 'This module requires approximately 5-7 hours of dedicated study.'
            }
        ]
    },
    'module2': {
        'title': 'Intermediate Techniques & Best Practices',
        'description': 'Advance your skills with practical techniques',
        'information': '''<h3>Building on Fundamentals</h3>
<p>Now that you've mastered the basics, it's time to explore intermediate techniques and industry best practices.</p>
<ul>
<li>Advanced techniques and methodologies</li>
<li>Real-world best practices</li>
<li>Optimization strategies</li>
<li>Common pitfalls and how to avoid them</li>
</ul>
<h3>Practical Skills</h3>
<p>You'll develop practical skills including:</p>
<ul>
<li>✅ Implement intermediate techniques</li>
<li>✅ Apply best practices effectively</li>
<li>✅ Optimize your approach</li>
<li>✅ Solve intermediate problems</li>
</ul>''',
        'video_url': 'https://www.youtube.com/embed/dQw4w9WgXcQ',
        'video_duration': '60 minutes',
        'learning_objectives': [
            'Master intermediate techniques',
            'Apply industry best practices',
            'Optimize your workflow',
            'Solve complex problems'
        ],
        'quiz_questions': [
            {
                'question': 'What makes intermediate techniques different from basics?',
                'options': ['They are more complex', 'They optimize efficiency', 'Both A and B', 'Neither A nor B'],
                'correct': 2,
                'explanation': 'Intermediate techniques are both more complex and focus on optimization.'
            },
            {
                'question': 'Why are best practices important?',
                'options': ['They save time', 'They improve quality', 'They prevent errors', 'All of the above'],
                'correct': 3,
                'explanation': 'Best practices benefit all aspects: time, quality, and error prevention.'
            },
            {
                'question': 'How should you approach optimization?',
                'options': ['Randomly try techniques', 'Follow a systematic approach', 'Copy from others', 'Guess and check'],
                'correct': 1,
                'explanation': 'A systematic approach to optimization ensures consistent improvements.'
            }
        ]
    },
    'module3': {
        'title': 'Advanced Concepts & Optimization',
        'description': 'Master advanced topics and optimization strategies',
        'information': '''<h3>Advanced Mastery</h3>
<p>Take your skills to the next level with advanced concepts and deep optimization strategies.</p>
<ul>
<li>Complex problem-solving approaches</li>
<li>Advanced optimization techniques</li>
<li>Performance tuning</li>
<li>Scalability considerations</li>
</ul>
<h3>Expert-Level Outcomes</h3>
<p>You'll achieve expert-level competency in:</p>
<ul>
<li>✅ Advanced problem analysis</li>
<li>✅ Strategic optimization</li>
<li>✅ Performance excellence</li>
<li>✅ Complex system design</li>
</ul>''',
        'video_url': 'https://www.youtube.com/embed/dQw4w9WgXcQ',
        'video_duration': '90 minutes',
        'learning_objectives': [
            'Master advanced concepts',
            'Implement optimization strategies',
            'Analyze complex problems',
            'Design scalable solutions'
        ],
        'quiz_questions': [
            {
                'question': 'What is the focus of advanced optimization?',
                'options': ['Speed only', 'Memory only', 'Multiple factors', 'User interface'],
                'correct': 2,
                'explanation': 'Advanced optimization considers multiple factors including speed, memory, and scalability.'
            },
            {
                'question': 'How should complex problems be approached?',
                'options': ['Quick solutions', 'Systematic analysis', 'Trial and error', 'Copy existing solutions'],
                'correct': 1,
                'explanation': 'Complex problems require systematic analysis and strategic thinking.'
            }
        ]
    },
    'module4': {
        'title': 'Frameworks & Tools',
        'description': 'Explore relevant frameworks and professional tools',
        'information': '''<h3>Framework Ecosystem</h3>
<p>Learn about popular frameworks and tools used in professional environments.</p>
<ul>
<li>Popular frameworks overview</li>
<li>Tool comparison and selection</li>
<li>Integration strategies</li>
<li>Real-world projects</li>
</ul>
<h3>Professional Development</h3>
<p>Prepare for professional work with:</p>
<ul>
<li>✅ Framework proficiency</li>
<li>✅ Tool expertise</li>
<li>✅ Integration knowledge</li>
<li>✅ Project management</li>
</ul>''',
        'video_url': 'https://www.youtube.com/embed/dQw4w9WgXcQ',
        'video_duration': '75 minutes',
        'learning_objectives': [
            'Understand major frameworks',
            'Master essential tools',
            'Integrate technologies effectively',
            'Develop professional projects'
        ],
        'quiz_questions': [
            {
                'question': 'What is the benefit of using established frameworks?',
                'options': ['Faster development', 'Better practices', 'Community support', 'All of the above'],
                'correct': 3,
                'explanation': 'Frameworks provide all these benefits: speed, best practices, and community.'
            }
        ]
    },
    'module5': {
        'title': 'Case Studies & Real-World Applications',
        'description': 'Learn from real-world case studies and applications',
        'information': '''<h3>Real-World Learning</h3>
<p>Explore how industry leaders apply these concepts in real-world scenarios.</p>
<ul>
<li>Industry case studies</li>
<li>Success stories</li>
<li>Lessons learned</li>
<li>Practical applications</li>
</ul>
<h3>Practical Experience</h3>
<p>Gain practical insights through:</p>
<ul>
<li>✅ Analyze real projects</li>
<li>✅ Learn from experts</li>
<li>✅ Understand challenges</li>
<li>✅ Apply lessons to your work</li>
</ul>''',
        'video_url': 'https://www.youtube.com/embed/dQw4w9WgXcQ',
        'video_duration': '60 minutes',
        'learning_objectives': [
            'Analyze real-world case studies',
            'Learn industry best practices',
            'Understand practical challenges',
            'Apply lessons to projects'
        ],
        'quiz_questions': [
            {
                'question': 'Why are case studies valuable?',
                'options': ['They are entertaining', 'They provide real-world context', 'They fill time', 'They are required'],
                'correct': 1,
                'explanation': 'Case studies provide valuable real-world context for learning.'
            }
        ]
    },
    'module6': {
        'title': 'Mastery & Capstone Project',
        'description': 'Complete your journey with a capstone project',
        'information': '''<h3>Final Mastery</h3>
<p>Demonstrate your complete understanding by completing a comprehensive capstone project.</p>
<ul>
<li>Project planning and scope</li>
<li>Implementation strategies</li>
<li>Quality assurance</li>
<li>Presentation and documentation</li>
</ul>
<h3>Achievement Goals</h3>
<p>Upon completion, you will have:</p>
<ul>
<li>✅ Completed a professional project</li>
<li>✅ Demonstrated mastery</li>
<li>✅ Built a portfolio piece</li>
<li>✅ Earned course certification</li>
</ul>''',
        'video_url': 'https://www.youtube.com/embed/dQw4w9WgXcQ',
        'video_duration': '45 minutes',
        'learning_objectives': [
            'Plan and design a capstone project',
            'Implement all learned concepts',
            'Apply quality standards',
            'Complete professional documentation'
        ],
        'quiz_questions': [
            {
                'question': 'What is the purpose of a capstone project?',
                'options': ['Fill time', 'Demonstrate mastery', 'Make it hard', 'Entertain students'],
                'correct': 1,
                'explanation': 'A capstone project demonstrates your complete understanding and mastery.'
            }
        ]
    }
}

@elearning.route('/')
def index():
    return render_template('elearning.html')

@elearning.route('/course/<course_id>')
def course_detail(course_id):
    course = COURSES.get(course_id, {})
    course_name = course.get('name', 'Course Not Found')
    
    if not course:
        return render_template('course_detail.html', course_name='Course Not Found'), 404
    
    # Check if user is enrolled
    if 'enrolled_courses' not in session:
        session['enrolled_courses'] = []
    
    is_enrolled = course_id in session['enrolled_courses']
    
    # For python-basics, show modules instead of code editor
    if course_id == 'python-basics':
        modules = PYTHON_BASICS_MODULES
        return render_template('course_modules.html', 
                             course_name=course_name,
                             course_id=course_id,
                             modules=modules,
                             is_enrolled=is_enrolled)
    
    # For python-advanced, show modules instead of code editor
    if course_id == 'python-advanced':
        modules = PYTHON_ADVANCED_MODULES
        return render_template('course_modules.html', 
                             course_name=course_name,
                             course_id=course_id,
                             modules=modules,
                             is_enrolled=is_enrolled)
    
    # For javascript, show modules instead of code editor
    if course_id == 'javascript':
        modules = JAVASCRIPT_MASTERY_MODULES
        return render_template('course_modules.html', 
                             course_name=course_name,
                             course_id=course_id,
                             modules=modules,
                             is_enrolled=is_enrolled)
    
    # For typescript, show modules instead of code editor
    if course_id == 'typescript':
        modules = TYPESCRIPT_MASTERY_MODULES
        return render_template('course_modules.html', 
                             course_name=course_name,
                             course_id=course_id,
                             modules=modules,
                             is_enrolled=is_enrolled)
    
    return render_template('course_detail.html', 
                         course_name=course_name, 
                         course_id=course_id,
                         is_enrolled=is_enrolled)

@elearning.route('/course/<course_id>/enroll')
def enroll_course(course_id):
    if 'enrolled_courses' not in session:
        session['enrolled_courses'] = []
    
    if course_id not in session['enrolled_courses']:
        session['enrolled_courses'].append(course_id)
        session.modified = True
    
    # For python-basics, python-advanced, javascript, and typescript, redirect to modules view
    if course_id in ['python-basics', 'python-advanced', 'javascript', 'typescript']:
        return redirect(url_for('elearning.course_detail', course_id=course_id))
    
    return render_template('course_detail.html', 
                         course_name=COURSES.get(course_id, {}).get('name', 'Course'),
                         course_id=course_id,
                         is_enrolled=True)

@elearning.route('/course/<course_id>/module/<module_id>')
def module_detail(course_id, module_id):
    """Display module details with information, video, and quiz"""
    course = COURSES.get(course_id, {})
    course_name = course.get('name', 'Course Not Found')
    
    if not course:
        return render_template('course_detail.html', course_name='Course Not Found'), 404
    
    # Check if user is enrolled - but allow preview if not enrolled
    if 'enrolled_courses' not in session:
        session['enrolled_courses'] = []
    
    is_enrolled = course_id in session['enrolled_courses']
    
    # Check if it's a Python-basics or python-advanced course and use Python-specific modules
    if course_id == 'python-basics':
        module = PYTHON_BASICS_MODULES.get(module_id, {'name': 'Module Not Found'})
        module_info = PYTHON_BASICS_MODULE_DETAILS.get(module_id, {})
    elif course_id == 'python-advanced':
        module = PYTHON_ADVANCED_MODULES.get(module_id, {'name': 'Module Not Found'})
        module_info = PYTHON_ADVANCED_MODULE_DETAILS.get(module_id, {})
    elif course_id == 'javascript':
        module = JAVASCRIPT_MASTERY_MODULES.get(module_id, {'name': 'Module Not Found'})
        module_info = JAVASCRIPT_MASTERY_MODULE_DETAILS.get(module_id, {})
    elif course_id == 'typescript':
        module = TYPESCRIPT_MASTERY_MODULES.get(module_id, {'name': 'Module Not Found'})
        module_info = TYPESCRIPT_MASTERY_MODULE_DETAILS.get(module_id, {})
    else:
        module = MODULES.get(module_id, {'name': 'Module Not Found'})
        module_info = MODULE_DETAILS.get(module_id, {})
    
    return render_template('module_detail.html',
                         course_name=course_name,
                         course_id=course_id,
                         module_name=module.get('name'),
                         module_id=module_id,
                         module_info=module_info,
                         is_enrolled=is_enrolled)

@elearning.route('/course/<course_id>/module/<module_id>/lesson/<lesson_id>')
def lesson(course_id, module_id, lesson_id):
    course = COURSES.get(course_id, {})
    course_name = course.get('name', 'Course Not Found')
    
    # Track enrollment in session if needed, but don't block access
    if 'enrolled_courses' not in session:
        session['enrolled_courses'] = []
    
    module = MODULES.get(module_id, {'name': 'Module Not Found'})
    module_info = MODULE_DETAILS.get(module_id, {})
    
    return render_template('module_lesson.html',
                         course_name=course_name,
                         course_id=course_id,
                         module_name=module.get('name'),
                         module_id=module_id,
                         lesson_title=f'Lesson {lesson_id}',
                         lesson_id=lesson_id,
                         module_info=module_info,
                         progress=int(lesson_id) * 33)

@elearning.route('/api/course/<course_id>/module/<module_id>/submit-quiz', methods=['POST'])
def submit_quiz(course_id, module_id):
    """API endpoint to submit quiz answers"""
    data = request.json
    answers = data.get('answers', [])
    
    # Get module info based on course type
    if course_id == 'python-basics':
        module_info = PYTHON_BASICS_MODULE_DETAILS.get(module_id, {})
    elif course_id == 'python-advanced':
        module_info = PYTHON_ADVANCED_MODULE_DETAILS.get(module_id, {})
    elif course_id == 'javascript':
        module_info = JAVASCRIPT_MASTERY_MODULE_DETAILS.get(module_id, {})
    elif course_id == 'typescript':
        module_info = TYPESCRIPT_MASTERY_MODULE_DETAILS.get(module_id, {})
    else:
        module_info = MODULE_DETAILS.get(module_id, {})
    
    quiz_questions = module_info.get('quiz_questions', [])
    
    if not quiz_questions:
        return jsonify({'error': 'No quiz found'}), 404
    
    # Calculate score
    correct_count = 0
    results = []
    
    for i, answer in enumerate(answers):
        if i < len(quiz_questions):
            question = quiz_questions[i]
            is_correct = answer == question['correct']
            if is_correct:
                correct_count += 1
            
            results.append({
                'question_index': i,
                'is_correct': is_correct,
                'explanation': question.get('explanation', '')
            })
    
    score = int((correct_count / len(quiz_questions)) * 100) if quiz_questions else 0
    
    return jsonify({
        'score': score,
        'correct_count': correct_count,
        'total_questions': len(quiz_questions),
        'results': results,
        'passed': score >= 70
    })


@elearning.route('/code-editor')
def code_editor():
    """Interactive code editor inspired by CodeMonkey"""
    return render_template('elearning_code_editor.html')

