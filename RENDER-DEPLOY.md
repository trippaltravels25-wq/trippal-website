# Deploying to Render (Step by Step)

This assumes you've never used GitHub or Render before. Follow every
step in order — nothing is skipped.

## Part 1 — Put the code on GitHub

Render deploys your site *from a GitHub repository*, not from a zip
file, so this has to happen first.

### 1. Create a GitHub account

Go to [github.com](https://github.com) → **Sign up** → follow the
prompts (email, password, username). Verify your email if asked.

### 2. Create a new repository

1. Once logged in, click the **+** icon top-right → **New repository**.
2. **Repository name:** `trippal-website`
3. Leave it **Public** (Render's free tier needs this unless you pay
   for private-repo support — public is fine, nothing sensitive is
   in this code).
4. Do **not** tick "Add a README" — leave everything else as default.
5. Click **Create repository**.

You'll land on an empty repo page with an "uploading an existing
file" link.

### 3. Unzip the project on your computer

Find `trippal-website.zip` (the file I gave you) and extract/unzip
it. You should end up with a folder called `trippal` containing
`app.py`, `templates/`, `static/`, `requirements.txt`, `README.md`.

### 4. Upload the files to GitHub

1. On your new repo's page, click **uploading an existing file**
   (or **Add file → Upload files**).
2. Open the `trippal` folder on your computer, select **everything
   inside it** (`app.py`, `requirements.txt`, `README.md`, the
   `templates` folder, the `static` folder — select all, not the
   `trippal` folder itself) and drag them into the browser window.
3. Wait for the upload bar to finish.
4. Scroll down, click **Commit changes**.

Refresh the repo page — you should now see `app.py`, `templates/`,
`static/`, `requirements.txt` listed there directly (not nested
inside another folder). This matters: Render needs `app.py` at the
top level of the repo.

---

## Part 2 — Deploy on Render

### 1. Create a Render account

Go to [render.com](https://render.com) → **Get Started** → sign up
using **"Sign up with GitHub"** (simplest — it connects the two
automatically).

### 2. Create a new Web Service

1. On the Render dashboard, click **New +** (top right) → **Web
   Service**.
2. It will ask to connect a repository. Find and select
   `trippal-website` (the one you just created). If you don't see
   it, click **Configure account** and grant Render access to that
   repo.

### 3. Fill in the settings

| Field | Value |
|---|---|
| **Name** | `trippal-website` (or anything — this becomes part of a temporary Render URL) |
| **Region** | Pick the one closest to your customers (e.g. Singapore/Mumbai if available) |
| **Branch** | `main` |
| **Root Directory** | leave blank |
| **Runtime** | `Python 3` |
| **Build Command** | `pip install -r requirements.txt` |
| **Start Command** | `gunicorn app:app --bind 0.0.0.0:$PORT` |
| **Instance Type** | **Free** |

### 4. Deploy

Click **Create Web Service** at the bottom. Render will now build
and start your site — you'll see logs scrolling. This takes 1–3
minutes the first time. When it says **"Live"** at the top, click
the link shown (something like
`https://trippal-website-xxxx.onrender.com`) — your site is now
public.

**Note on the free tier:** if nobody visits for 15 minutes, the free
instance goes to sleep. The next visitor waits about 30–60 seconds
while it wakes back up, then it's normal speed again. This is a
free-tier limitation only — fine for a formality/verification site,
but worth knowing.

---

## Part 3 — Connect your GoDaddy domain

### 1. Add the domain in Render

1. On your Web Service's page in Render, click **Settings** in the
   left sidebar.
2. Scroll to **Custom Domains** → click **+ Add Custom Domain**.
3. Type `www.trippalglobal.com` → **Save**.
   - Render will automatically also add `trippalglobal.com` (no
     www) and set it to redirect to the `www` version — you don't
     need to add that one separately.
4. Leave this tab open — it shows the DNS records you need next.

### 2. Add the DNS records in GoDaddy

1. Open a new tab, log into GoDaddy → **My Products** → find
   `trippalglobal.com` → **DNS** (sometimes labeled "Manage DNS").
2. You need to add/edit **two** records. First, check for and
   **delete** any existing records that use the same names below —
   GoDaddy often ships a domain with default "parked page" records
   that will conflict.

   **Record 1 — the `www` version:**
   | Field | Value |
   |---|---|
   | Type | CNAME |
   | Name | `www` |
   | Value | your Render subdomain, e.g. `trippal-website-xxxx.onrender.com` (copy this exactly from the Render tab) |
   | TTL | 1 hour (or lowest option) |

   **Record 2 — the bare domain:**
   | Field | Value |
   |---|---|
   | Type | A |
   | Name | `@` |
   | Value | `216.24.57.1` |
   | TTL | 1 hour |

3. Also check for any **AAAA** records (Type = AAAA) on `@` or
   `www` — if any exist, **delete them**. Render doesn't use these
   and they can break things.
4. Save.

### 3. Verify in Render

1. Go back to the Render tab (Settings → Custom Domains).
2. Click **Verify** next to `www.trippalglobal.com`.
3. If it says DNS not found yet, wait 15–30 minutes (DNS changes
   take time to spread across the internet) and click **Verify**
   again.
4. Once verified, Render automatically issues a free HTTPS
   certificate — no action needed from you. This can take a few
   more minutes after verification succeeds.

### 4. Test it

Visit `https://www.trippalglobal.com` and `https://trippalglobal.com`
in a browser — both should show your site with a padlock icon (secure).

---

## Updating the site later

Whenever you want to change something:

1. Edit the files, or upload new versions to the same GitHub repo
   (GitHub's web interface lets you edit files directly, or delete
   and re-upload).
2. Render automatically notices the change and redeploys within a
   minute or two — no extra steps needed.

## If something doesn't work

- **Render build fails:** click into the failed deploy and read the
  log — it usually names the exact missing file or typo.
- **"Not Found" on the live URL:** double check `app.py` is at the
  top level of the GitHub repo, not inside a nested `trippal` folder.
- **Domain not verifying after an hour+:** double-check you deleted
  any conflicting default GoDaddy records for `@` and `www`, and
  that there's no leftover AAAA record.
