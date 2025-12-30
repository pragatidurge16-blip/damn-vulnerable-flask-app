import pickle
import base64
import html
from flask import Flask, request, render_template, redirect, session
import sqlite3, json

app = Flask(__name__, template_folder='templates')
app.secret_key = "secret_key_for_demo"

# ---------------- DATABASE ----------------
def db():
    return sqlite3.connect("users.db")

con = db()

con.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    email TEXT,
    password TEXT,
    role TEXT
)
""")

# 🔹 Safe: agar table purani ho toh columns add ho jayenge
try:
    con.execute("ALTER TABLE users ADD COLUMN email TEXT")
except:
    pass

try:
    con.execute("ALTER TABLE users ADD COLUMN role TEXT")
except:
    pass

con.commit()
con.close()

# ---------------- HOME ----------------
@app.route('/')
def home():
    return redirect('/login')

# ---------------- REGISTER ----------------
@app.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'POST':
        con = db()
        con.execute(
            "INSERT INTO users(username,email,password,role) VALUES(?,?,?,?)",
            (
                request.form['username'],
                request.form['email'],
                request.form['password'],
                'user'
            )
        )
        con.commit()
        con.close()
        return redirect('/login')
    return render_template("register.html")

# ---------------- LOGIN (VULNERABLE - SQL INJECTION) ----------------
@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        con = db()
        # ❌ VULNERABLE QUERY
        query = "SELECT * FROM users WHERE username='" + request.form['username'] + "' AND password='" + request.form['password'] + "'"
        user = con.execute(query).fetchone()
        if user:
            session['uid'] = user[0]
            return redirect('/dashboard')
    return render_template("login.html")

# ---------------- DASHBOARD ----------------
@app.route('/dashboard')
def dashboard():
    if 'uid' not in session:
        return redirect('/login')   # ✅ correct

    return render_template("dashboard.html")
# ---------------- SQL INJECTION FIX ----------------
@app.route('/secure_login', methods=['POST'])
def secure_login():
    con = db()
    user = con.execute(
        "SELECT * FROM users WHERE username=? AND password=?",
        (request.form['username'], request.form['password'])
    ).fetchone()

    if user:
        session['secure_uid'] = user[0]
        return "SQL Injection FIXED – Secure Login"
    else:
        return "Login Failed – Injection Blocked"

# ---------------- IDOR (VULNERABLE) ----------------
@app.route('/user')
def user():
    con = db()
    uid = request.args.get('id')
    user = con.execute("SELECT * FROM users WHERE id=" + uid).fetchone()
    return str(user)

# ---------------- IDOR FIX ----------------
@app.route('/secure_user')
def secure_user():
    if 'uid' not in session:
        return "Not Logged In – Access Denied"

    requested_id = request.args.get('id')
    logged_in_id = str(session['uid'])

    if requested_id != logged_in_id:
        return "IDOR FIXED – Unauthorized Access Blocked"

    return "Access Granted – This is your own data"

# ---------------- DESERIALIZATION (VULNERABLE) ----------------
@app.route('/deserialize', methods=['POST'])
def deserialize():
    data = json.loads(request.form['data'])
    return "Role: " + data.get('role','')

# ---------------- DESERIALIZATION FIX ----------------
@app.route('/secure_deserialize', methods=['POST'])
def secure_deserialize():
    data = json.loads(request.form['data'])

    allowed_roles = ['user', 'guest']

    if data.get('role') not in allowed_roles:
        return "Deserialization FIXED – Invalid role blocked"

    return "Safe Role: " + data.get('role')
@app.route('/pickle_login', methods=['POST'])
def pickle_login():
    payload = request.form.get('pickled')

    data = base64.urlsafe_b64decode(payload + "===")
    obj = pickle.loads(data)   # ❌ VULNERABLE

    return "Logged in as: " + str(obj)
# ---------------- OPEN REDIRECT (VULNERABLE) ----------------
@app.route('/redirect')
def open_redirect():
    next_url = request.args.get('next')
    return redirect(next_url)

# ---------------- OPEN REDIRECT FIX ----------------
@app.route('/secure_redirect')
def secure_redirect():
    next_url = request.args.get('next')

    allowed_paths = ['/dashboard', '/profile']

    if next_url not in allowed_paths:
        return "Open Redirect FIXED – Invalid redirect blocked"

    return redirect(next_url)
# ---------------- BROKEN AUTHENTICATION (VULNERABLE) ----------------
@app.route('/broken_dashboard')
def broken_dashboard():
    # ❌ No authentication / session check
    return "Welcome to Dashboard (BROKEN AUTH – No Login Required)"


@app.route('/secure_dashboard')
def secure_dashboard():
    if 'uid' not in session:
        return """
        <h2>🔐 Access Denied</h2>
        <p>You must login first to access dashboard.</p>
        <a href="/login">Go to Login</a>
        """

    return """
    <h2>✅ Secure Dashboard</h2>
    <p>Authentication Verified</p>
    """
# ---------------- XSS (VULNERABLE) ----------------
@app.route('/xss_vuln', methods=['GET', 'POST'])
def xss_vuln():
    name = ""
    if request.method == 'POST':
        name = request.form['name']   # ❌ NO validation / escaping

    return f"""
    <h2>🔴 XSS Vulnerable Page</h2>

    <form method="POST">
        <input name="name" placeholder="Enter your name">
        <button>Submit</button>
    </form>

    <p>Welcome {name}</p>
    """
# ---------------- XSS FIX (SECURE) ----------------
@app.route('/xss_secure', methods=['GET', 'POST'])
def xss_secure():
    name = ""
    if request.method == 'POST':
        # ✅ Escape user input (script execute nahi hoga)
        name = html.escape(request.form['name'])

    return f"""
    <h2>🟢 XSS Secure Page</h2>

    <form method="POST">
        <input name="name" placeholder="Enter your name">
        <button>Submit</button>
    </form>

    <p>Welcome {name}</p>
    """


# ---------------- RUN APP (LAST LINE) ----------------
app.run(debug=True)