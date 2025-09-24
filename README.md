# Quantum Leap Institute — AI & Data Science Courses

A static-first Flask marketing site for promoting the Quantum Leap Institute&apos;s AI and Data Science programs. The application renders HTML templates only (no database) and is production-ready for deployment on platforms like Heroku, Render, Railway, or Docker-based hosting.

## Quickstart

```bash
python3 -m venv .venv
source .venv/bin/activate  # On Windows use: .venv\\Scripts\\activate
pip install -r requirements.txt
export FLASK_APP=app.py
export FLASK_DEBUG=1  # optional
flask run
```

### Run with Gunicorn locally

```bash
gunicorn app:app -b 0.0.0.0:8000
```

## Environment Variables

| Variable      | Description                               | Default |
| ------------- | ----------------------------------------- | ------- |
| `FLASK_DEBUG` | Toggle Flask debug mode (`0` or `1`).     | `0`     |
| `PORT`        | Port for the web server (when using `app.run`). | `5000` |

## Deployment

### Heroku

```bash
heroku create your-app-name
heroku config:set FLASK_DEBUG=0
heroku git:remote -a your-app-name
git push heroku main
```

The included `Procfile` and `runtime.txt` ensure Heroku uses Python 3.11.9 and Gunicorn.

### Render

1. Create a new **Web Service** on Render.
2. Connect your repository and select the main branch.
3. Set the build command to `pip install -r requirements.txt`.
4. Set the start command to `gunicorn app:app`.
5. Add environment variable `FLASK_DEBUG=0` (optional).

### Railway

1. Create a new project and select **Deploy from Repo**.
2. Add the repository and choose the default deployment settings.
3. Railway detects the `Procfile`; confirm the start command `gunicorn app:app`.
4. Configure environment variables as needed (e.g., `FLASK_DEBUG=0`).

### Vercel

1. Install the [Vercel CLI](https://vercel.com/docs/cli) and run `vercel init` in this project.
2. When prompted, select **Python** as the framework and point the entry to `app.py`.
3. Set the build command to `pip install -r requirements.txt` and the output command to `gunicorn app:app`.
4. Deploy with `vercel --prod`. Vercel provisions a serverless container that serves the Gunicorn entrypoint.

### Docker (optional)

```bash
# Build image
docker build -t qlinst-site .

# Run container
docker run -p 8000:8000 -e FLASK_DEBUG=0 qlinst-site
```

## Project Structure

```
app.py
Procfile
README.md
requirements.txt
runtime.txt
static/
  css/styles.css
  js/main.js
  img/
    hero.jpg
    logo.svg
    course-1.jpg
    course-2.jpg
    course-3.jpg
    banner-ai.jpg
    banner-ds.jpg
    favicon.ico
  icons/
templates/
  base.html
  index.html
  about.html
  gallery.html
  partials/
    navbar.html
    footer.html
    banner.html
```

