from datetime import datetime
from flask import Flask, render_template

app = Flask(__name__)


@app.context_processor
def inject_globals():
    """Values every template can use (e.g. the footer copyright year)."""
    return {"year": datetime.now().year}


@app.route("/")
def home():
    return render_template("index.html", active="home")


@app.route("/contact")
def contact():
    return render_template("contact.html", active="contact")


@app.route("/privacy-policy")
def privacy():
    return render_template("privacy.html", active="privacy")


@app.route("/terms-conditions")
def terms():
    return render_template("terms.html", active="terms")


@app.route("/refund-policy")
def refund():
    return render_template("refund.html", active="refund")


@app.route("/shipping-policy")
def shipping():
    return render_template("shipping.html", active="shipping")


if __name__ == "__main__":
    # Local development only. On PythonAnywhere, the WSGI file imports
    # this same `app` object instead of running this block.
    app.run(debug=True)
