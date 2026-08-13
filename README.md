# TripPal Global Travel & Tourism — Website

A small Flask site: one landing page plus Contact, Privacy Policy,
Terms & Conditions, Refund & Cancellation Policy, and Shipping &
Delivery Policy. No CMS, no theme — everything is hand-built
HTML/CSS/JS served through Flask templates.

```
trippal/
├── app.py                 ← the whole application (routes)
├── requirements.txt
├── templates/              ← one .html file per page, sharing base.html
├── static/
│   ├── css/style.css
│   ├── js/script.js
│   └── img/logo.jpg, favicon.png
└── README.md
```

---

## Part 1 — Run it on your own computer first

You need Python 3.9+ installed. Check with:

```bash
python3 --version
```

### 1. Open a terminal in the project folder

```bash
cd path/to/trippal
```

### 2. Create a virtual environment

A virtual environment keeps this project's Python packages separate
from everything else on your machine.

```bash
python3 -m venv venv
```

This creates a `venv/` folder — that's your isolated Python.

### 3. Activate it

**macOS / Linux:**
```bash
source venv/bin/activate
```

**Windows (Command Prompt):**
```bat
venv\Scripts\activate.bat
```

**Windows (PowerShell):**
```powershell
venv\Scripts\Activate.ps1
```

Your terminal prompt should now start with `(venv)`. Every command
below assumes it's still there — if you close the terminal, just
`cd` back into the folder and activate again before continuing.

### 4. Install Flask into the virtual environment

```bash
pip install -r requirements.txt
```

### 5. Run the site

```bash
python app.py
```

You'll see something like:

```
 * Running on http://127.0.0.1:5000
```

Open **http://127.0.0.1:5000** in your browser. Resize the window
(or open dev tools' device toolbar) to check phone, tablet and
desktop widths.

### 6. Making changes

- Text and structure → edit the matching file in `templates/`
- Colors, spacing, fonts → edit `static/css/style.css`
- Logo → replace `static/img/logo.jpg` (keep the filename, or update
  the references in `templates/base.html`)

Flask's dev server auto-reloads — save the file, refresh the browser.

### 7. Stop the server

`Ctrl + C` in the terminal. To leave the virtual environment:

```bash
deactivate
```

---

## Part 2 — Deploy to PythonAnywhere

### 1. Create a PythonAnywhere account

Go to [pythonanywhere.com](https://www.pythonanywhere.com) and sign
up (the free "Beginner" plan is enough for this site).

### 2. Upload the project

Easiest path with no Git needed:

1. On the PythonAnywhere dashboard, open the **Files** tab.
2. Create a folder, e.g. `trippal`.
3. Zip your local `trippal` folder on your computer, then use the
   **Upload a file** button to upload the zip into that folder.
4. Open a **Bash console** from the **Consoles** tab and unzip it:
   ```bash
   cd ~/trippal
   unzip trippal.zip -d .
   # if the zip contained a nested trippal/ folder, move its contents up a level
   ```

(Alternatively, if you're comfortable with Git: push this folder to
GitHub, then in a PythonAnywhere Bash console run
`git clone <your-repo-url> trippal`.)

### 3. Create the virtual environment on PythonAnywhere

In the same Bash console:

```bash
cd ~/trippal
python3.10 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

(If `python3.10` isn't available, run `python3 --version` first and
use whichever 3.x version PythonAnywhere offers.)

### 4. Create the web app

1. Go to the **Web** tab → **Add a new web app**.
2. Choose your domain (on the free plan it will be
   `yourusername.pythonanywhere.com` — you can point
   `trippalglobal.com` at it later from a paid account, or use it as
   the Razorpay-verification build first).
3. When asked, choose **Manual configuration** (not "Flask" — manual
   config gives you full control to point at this exact `app.py`).
4. Pick the same Python version you used for the virtual environment.

### 5. Point the web app at your virtual environment

Still on the **Web** tab, find **Virtualenv** and enter:

```
/home/yourusername/trippal/venv
```

(Replace `yourusername` with your actual PythonAnywhere username.)

### 6. Edit the WSGI configuration file

On the **Web** tab, click the WSGI configuration file link (something
like `/var/www/yourusername_pythonanywhere_com_wsgi.py`). Delete its
contents and replace with:

```python
import sys

project_home = '/home/yourusername/trippal'
if project_home not in sys.path:
    sys.path.insert(0, project_home)

from app import app as application
```

Replace `yourusername` with your actual username. Save the file.

### 7. Set the static files mapping (optional but recommended)

Still on the **Web** tab, under **Static files**, add:

| URL       | Directory                              |
|-----------|-----------------------------------------|
| `/static/`| `/home/yourusername/trippal/static/`   |

This lets PythonAnywhere serve CSS/JS/images directly, which is
faster than routing them through Flask.

### 8. Reload and check

Click the big green **Reload** button at the top of the **Web** tab,
then visit `https://yourusername.pythonanywhere.com`. Check all six
pages and the mobile menu.

### 9. Custom domain (trippalglobal.com)

The free PythonAnywhere plan can't map a custom domain — that needs
a paid plan. Once upgraded: **Web tab → Add a new web app** with
your domain, or edit the existing app's domain field, then update
your DNS at your domain registrar to point to PythonAnywhere's
address (they'll show you the exact CNAME/A record once you add the
domain).

### 10. Updating the live site later

```bash
cd ~/trippal
source venv/bin/activate
# edit files, or git pull / re-upload changed files
```

Then go back to the **Web** tab and click **Reload** — changes to
Python code and templates only take effect after a reload.

---

## Notes for the Razorpay review

- All five policy pages (Privacy, Terms, Refund & Cancellation,
  Shipping & Delivery) and the Contact page are live and linked from
  both the header and footer of every page.
- The footer shows the business email and phone on every page.
- No card or banking data is collected or stored by this site —
  the "Book Now" button opens a pre-filled email; payment will route
  through Razorpay's own hosted checkout once that's wired up in
  Phase 2.
