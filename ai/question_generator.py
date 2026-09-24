"""AI Question Generator for CareerPrep AI."""
import random
from .ai_service import ai_service

# Comprehensive local question bank for offline demo mode
LOCAL_QUESTION_BANK = {
    "python": [
        {
            "question": "Explain the difference between mutable and immutable types in Python with examples.",
            "type": "Technical",
            "difficulty": "Easy",
            "topic": "Data Types",
            "expected_answer_points": [
                "Mutable objects (lists, dicts, sets) can be changed in place without changing their id",
                "Immutable objects (integers, strings, tuples) cannot be altered after creation",
                "Reassignment creates a new object in memory for immutable types",
            ],
        },
        {
            "question": "What are Python decorators and how do you write a simple timing decorator?",
            "type": "Technical",
            "difficulty": "Medium",
            "topic": "Functional Programming",
            "expected_answer_points": [
                "A decorator is a callable that takes a function as input and returns an extended function",
                "Uses @wrapper syntax and functools.wraps to preserve function metadata",
                "Takes *args and **kwargs in the inner wrapper",
            ],
        },
        {
            "question": "How does memory management and garbage collection work in Python (GIL & reference counting)?",
            "type": "Theory",
            "difficulty": "Hard",
            "topic": "Internals & Memory",
            "expected_answer_points": [
                "Reference counting tracks references to each object",
                "Cyclic garbage collector detects and cleans circular references",
                "Global Interpreter Lock (GIL) synchronizes thread execution for CPython",
            ],
        },
        {
            "question": "What is the difference between shallow copy and deep copy in Python?",
            "type": "Technical",
            "difficulty": "Easy",
            "topic": "Memory & Copying",
            "expected_answer_points": [
                "Shallow copy constructs a new compound object and inserts references to original objects",
                "Deep copy recursively copies all nested objects",
                "Handled via the copy module (copy.copy vs copy.deepcopy)",
            ],
        },
        {
            "question": "How do Python generators differ from regular functions, and what is the role of the yield keyword?",
            "type": "Technical",
            "difficulty": "Medium",
            "topic": "Iterators & Generators",
            "expected_answer_points": [
                "Generators return an iterator that yields one value at a time on demand",
                "Yield pauses execution and preserves function stack state",
                "Provides high memory efficiency for large datasets",
            ],
        },
        {
            "question": "How would you optimize a Python API that suffers from slow database queries?",
            "type": "Coding",
            "difficulty": "Hard",
            "topic": "Performance & Databases",
            "expected_answer_points": [
                "Add database indexes on frequently filtered columns",
                "Avoid N+1 queries using joinedload or selectinload",
                "Implement Redis caching for repeated read queries",
                "Use connection pooling and asynchronous query execution",
            ],
        },
    ],
    "java": [
        {
            "question": "What is the difference between JDK, JRE, and JVM in Java?",
            "type": "Theory",
            "difficulty": "Easy",
            "topic": "Architecture",
            "expected_answer_points": [
                "JVM executes compiled Java bytecode and manages memory",
                "JRE provides the runtime libraries and JVM needed to run applications",
                "JDK is the complete development kit including compiler (javac), tools, and JRE",
            ],
        },
        {
            "question": "Explain the four pillars of Object-Oriented Programming and how Java implements them.",
            "type": "Theory",
            "difficulty": "Easy",
            "topic": "OOP Concepts",
            "expected_answer_points": [
                "Encapsulation: private fields with getters and setters",
                "Inheritance: extends keyword for code reuse",
                "Polymorphism: method overloading and overriding",
                "Abstraction: abstract classes and interfaces",
            ],
        },
        {
            "question": "What is the difference between HashMap and ConcurrentHashMap in multi-threaded environments?",
            "type": "Technical",
            "difficulty": "Medium",
            "topic": "Collections & Concurrency",
            "expected_answer_points": [
                "HashMap is not thread-safe and can cause race conditions or infinite loops",
                "ConcurrentHashMap uses bucket/segment locking for concurrent reads and writes",
                "Does not lock the whole map unlike synchronized Hashtable",
            ],
        },
        {
            "question": "How does Garbage Collection work in Java, and what are the Eden, Survivor, and Tenured spaces?",
            "type": "Technical",
            "difficulty": "Hard",
            "topic": "JVM Memory Management",
            "expected_answer_points": [
                "Generational GC divides heap into Young and Old generations",
                "Young generation contains Eden space and two Survivor spaces (S0, S1)",
                "Objects surviving minor GC cycles are promoted to Tenured generation",
            ],
        },
    ],
    "javascript": [
        {
            "question": "Explain the JavaScript Event Loop, Call Stack, Microtask Queue, and Callback Queue.",
            "type": "Theory",
            "difficulty": "Medium",
            "topic": "Asynchronous JS",
            "expected_answer_points": [
                "Call Stack processes synchronous code execution",
                "Microtask queue handles resolved Promises and queueMicrotask with higher priority",
                "Callback/Macrotask queue handles setTimeout, setInterval, and I/O events",
                "Event loop pushes tasks onto the call stack when it becomes empty",
            ],
        },
        {
            "question": "What is the difference between '==' and '===' in JavaScript?",
            "type": "Technical",
            "difficulty": "Easy",
            "topic": "Operators & Types",
            "expected_answer_points": [
                "== performs type coercion before comparison",
                "=== checks both value and type without coercion",
                "=== is recommended for predictable equality checks",
            ],
        },
        {
            "question": "What are Closures in JavaScript and how are they used in practical frontend development?",
            "type": "Technical",
            "difficulty": "Medium",
            "topic": "Scope & Closures",
            "expected_answer_points": [
                "A closure gives a function access to its outer lexical scope even after the outer function has closed",
                "Used for data privacy, currying, and maintaining state in event handlers",
            ],
        },
    ],
    "sql": [
        {
            "question": "What is the difference between WHERE and HAVING clauses in SQL?",
            "type": "Technical",
            "difficulty": "Easy",
            "topic": "Queries & Aggregation",
            "expected_answer_points": [
                "WHERE filters rows before aggregation occurs",
                "HAVING filters groups after GROUP BY aggregation has been applied",
                "HAVING can use aggregate functions like COUNT, SUM, AVG",
            ],
        },
        {
            "question": "Explain the four ACID properties in relational database transactions.",
            "type": "Theory",
            "difficulty": "Medium",
            "topic": "Database Transactions",
            "expected_answer_points": [
                "Atomicity: all operations succeed or all roll back",
                "Consistency: database transitions only from one valid state to another",
                "Isolation: concurrent transactions do not interfere with each other",
                "Durability: committed changes are permanently preserved even during system crash",
            ],
        },
    ],
    "ai/ml": [
        {
            "question": "What is the difference between Supervised, Unsupervised, and Reinforcement Learning?",
            "type": "Theory",
            "difficulty": "Easy",
            "topic": "Machine Learning Paradigms",
            "expected_answer_points": [
                "Supervised learning trains on labeled input-output pairs",
                "Unsupervised learning finds hidden patterns in unlabeled data (clustering)",
                "Reinforcement learning learns optimal actions via rewards and penalties in an environment",
            ],
        },
        {
            "question": "How do you detect and prevent overfitting in deep learning models?",
            "type": "Technical",
            "difficulty": "Medium",
            "topic": "Model Optimization",
            "expected_answer_points": [
                "Use dropout layers and L1/L2 regularization",
                "Apply early stopping on validation loss",
                "Perform data augmentation to increase training diversity",
                "Simplify model architecture or gather more training samples",
            ],
        },
    ],
    "behavioral": [
        {
            "question": "Tell me about a challenging technical bug you encountered in a college project and how you resolved it.",
            "type": "Behavioral",
            "difficulty": "Medium",
            "topic": "Problem Solving (STAR Method)",
            "expected_answer_points": [
                "Situation: Context of the project and issue",
                "Task: Candidate's direct responsibility",
                "Action: Debugging methodology, root cause discovery, and code fix",
                "Result: Outcome, performance gain, or lesson learned",
            ],
        },
        {
            "question": "How do you prioritize your work when facing multiple overlapping deadlines for submissions and projects?",
            "type": "Behavioral",
            "difficulty": "Easy",
            "topic": "Time Management",
            "expected_answer_points": [
                "Assessing task urgency versus impact",
                "Breaking complex tasks into incremental milestones",
                "Clear communication with teammates or mentors",
            ],
        },
    ],
}


def generate_interview_questions(role, technology, difficulty="Medium", question_type="Mixed", count=5):
    """Generates structured interview questions tailored to role, technology, difficulty.

    Uses Google Gemini if available, or intelligently draws from the local question bank.
    """
    tech_key = (technology or "Python").lower().strip()
    if "python" in tech_key:
        matched_key = "python"
    elif "java" in tech_key:
        matched_key = "java"
    elif any(k in tech_key for k in ["js", "javascript", "node", "web", "react"]):
        matched_key = "javascript"
    elif any(k in tech_key for k in ["sql", "data", "db"]):
        matched_key = "sql"
    elif any(k in tech_key for k in ["ai", "ml", "machine"]):
        matched_key = "ai/ml"
    else:
        matched_key = "python"

    # Try generating with Gemini if configured
    if not ai_service.is_demo_mode:
        prompt = f"""
You are an expert technical interviewer conducting an interview for the role '{role}'.
Target Technology: {technology}
Target Difficulty Level: {difficulty}
Target Question Type: {question_type}
Number of Questions: {count}

Generate exactly {count} realistic, insightful interview questions suitable for a college student applying for an internship.
Return ONLY a valid JSON array of objects with no surrounding markdown or explanation.
Each object in the array must follow this exact schema:
[
  {{
    "question": "The question text",
    "type": "Technical|Coding|Theory|Behavioral",
    "difficulty": "{difficulty}",
    "topic": "Specific technical topic",
    "expected_answer_points": [
      "Key concept point 1",
      "Key concept point 2",
      "Key concept point 3"
    ]
  }}
]
"""
        generated = ai_service.generate_json(prompt)
        if isinstance(generated, list) and len(generated) >= 1:
            return generated[:count]

    # Fallback / Demo Mode: Assemble from local bank
    pool = list(LOCAL_QUESTION_BANK.get(matched_key, LOCAL_QUESTION_BANK["python"]))

    # If mixed or behavioral, mix in behavioral questions
    if question_type in ("Behavioral", "Mixed", "HR") or "hr" in (role or "").lower():
        pool.extend(LOCAL_QUESTION_BANK["behavioral"])

    # If coding/technical requested, add from other pools if needed to satisfy count
    if len(pool) < count:
        pool.extend(LOCAL_QUESTION_BANK["sql"])
        pool.extend(LOCAL_QUESTION_BANK["javascript"])

    # Filter or prioritize by difficulty if possible
    diff_pool = [q for q in pool if q.get("difficulty", "").lower() == difficulty.lower()]
    if len(diff_pool) >= count:
        selected = random.sample(diff_pool, count)
    else:
        # Fallback to general pool
        random.shuffle(pool)
        selected = pool[:count]

    # Adjust format
    results = []
    for q in selected:
        results.append({
            "question": q["question"],
            "type": q.get("type", "Technical"),
            "difficulty": q.get("difficulty", difficulty),
            "topic": q.get("topic", technology or "Core CS"),
            "expected_answer_points": q.get("expected_answer_points", [
                "Accurate technical definition and conceptual clarity",
                "Practical real-world usage or code example",
                "Understanding of trade-offs or performance impact",
            ]),
        })

    return results
