"""Flask application serving static marketing pages for AI & Data Science courses."""
from __future__ import annotations

import os
from datetime import datetime
from pathlib import Path
from typing import Any

from flask import Flask, render_template, url_for


def create_app() -> Flask:
    """Application factory to create and configure the Flask app."""
    app = Flask(__name__)

    # Basic configuration toggled via environment variable.
    debug_setting = os.getenv("FLASK_DEBUG") or os.getenv("DEBUG") or "0"
    app.config["DEBUG"] = debug_setting.lower() in {"1", "true", "yes", "on"}

    @app.context_processor
    def inject_utilities() -> dict[str, Any]:
        """Attach a version query string to static assets for basic cache busting."""

        def dated_url_for(endpoint: str, **values: Any) -> str:
            if endpoint == "static":
                filename = values.get("filename")
                if filename:
                    file_path = Path(app.static_folder) / filename
                    if file_path.exists():
                        values["v"] = int(file_path.stat().st_mtime)
            return url_for(endpoint, **values)

        return {
            "url_for": dated_url_for,
            "current_year": datetime.utcnow().year,
        }

    @app.route("/")
    def index() -> str:
        """Render the homepage."""
        return render_template(
            "index.html",
            page_title="AI & Data Science Courses | Quantum Leap Institute",
            page_description="Join immersive AI and Data Science courses designed to take you from fundamentals to production-ready deployments.",
        )

    @app.route("/about")
    def about() -> str:
        """Render the about page."""
        return render_template(
            "about.html",
            page_title="About Our AI Instructors | Quantum Leap Institute",
            page_description="Meet veteran AI practitioners, explore our teaching philosophy, and learn how we prepare you for real-world data roles.",
        )

    @app.route("/gallery")
    def gallery() -> str:
        """Render the gallery page."""
        return render_template(
            "gallery.html",
            page_title="AI & Data Science Course Gallery | Quantum Leap Institute",
            page_description="Peek inside our AI and Data Science learning experience with project highlights and cohort memories.",
            generated_at=datetime.utcnow(),
        )

    return app


app = create_app()


if __name__ == "__main__":
    # Running with Flask's built-in server for local development.
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", "5000")), debug=app.config["DEBUG"])
