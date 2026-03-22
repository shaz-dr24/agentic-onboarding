from flask import Flask
from flask_cors import CORS

from routes.employee_routes import employee_bp
from routes.workflow_routes import workflow_bp

# -----------------------------------
# 🚀 INIT APP
# -----------------------------------
app = Flask(__name__)

# 🔥 Enable CORS (frontend connection)
CORS(app)

# -----------------------------------
# 📦 REGISTER ROUTES
# -----------------------------------
app.register_blueprint(employee_bp)
app.register_blueprint(workflow_bp)

# -----------------------------------
# 🏠 HOME ROUTE (MUST BE ABOVE RUN)
# -----------------------------------
@app.route("/")
def home():
    return "🚀 Agentic AI Backend Running Successfully!"

# -----------------------------------
# ▶️ RUN SERVER
# -----------------------------------
if __name__ == "__main__":
    print("🚀 Server running on http://127.0.0.1:5000")
    app.run(debug=True)