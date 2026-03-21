import functools
from flask import request, jsonify
import jwt
import time

SECRET = "dev-secret"

def signup(store, data):
    email = data.get("email")
    password = data.get("password")
    plan = data.get("plan", "free")  # free | pro | enterprise
    if not email or not password:
        return jsonify({"error": "Email and password required"}), 400
    user = store.create_user(email, password, plan)
    token = _issue_token(user)
    return jsonify({"user": {"id": user["id"], "email": email, "plan": plan}, "token": token})

def login(store, data):
    email = data.get("email")
    password = data.get("password")
    user = store.find_user(email)
    if not user or user["password"] != password:
        return jsonify({"error": "Invalid credentials"}), 401
    token = _issue_token(user)
    return jsonify({"user": {"id": user["id"], "email": email, "plan": user["plan"]}, "token": token})

def require_auth(f):
    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        auth = request.headers.get("Authorization", "")
        if not auth.startswith("Bearer "):
            return jsonify({"error": "Unauthorized"}), 401
        token = auth.split(" ", 1)[1]
        try:
            payload = jwt.decode(token, SECRET, algorithms=["HS256"])
            user = {"id": payload["sub"], "email": payload["email"], "plan": payload["plan"]}
        except Exception:
            return jsonify({"error": "Invalid token"}), 401
        return f(*args, **kwargs, user=user)
    return wrapper

def _issue_token(user):
    payload = {"sub": user["id"], "email": user["email"], "plan": user["plan"], "iat": int(time.time())}
    return jwt.encode(payload, SECRET, algorithm="HS256")
