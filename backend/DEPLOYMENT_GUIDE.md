# Hugging Face Deployment Guide - Backend

## Prerequisites

1. **Hugging Face Account**: Create account at https://huggingface.co/join
2. **Git**: Installed on your system
3. **Neon Database**: Your PostgreSQL connection string ready

---

## Step 1: Create Hugging Face Space

1. Go to https://huggingface.co/spaces
2. Click **"Create new Space"**
3. Fill in details:
   - **Space name**: `todo-api-backend` (or your choice)
   - **License**: MIT
   - **Select SDK**: Choose **Docker**
   - **Space hardware**: CPU basic (free tier)
   - **Visibility**: Public or Private
4. Click **"Create Space"**

---

## Step 2: Configure Space Secrets

After creating the Space, go to **Settings** → **Repository secrets**:

Add these secrets:

1. **DATABASE_URL**
   ```
   postgresql://username:password@host/database
   ```
   (Your Neon PostgreSQL connection string)

2. **BETTER_AUTH_SECRET**
   ```
   your-secret-key-minimum-32-characters-long
   ```
   (Same secret used in your frontend)

3. **FRONTEND_URL**
   ```
   http://localhost:3000
   ```
   (Update this with your deployed frontend URL later)

---

## Step 3: Prepare Backend Files

Your backend directory should have these files:
- ✅ `requirements.txt` (created)
- ✅ `Dockerfile` (created)
- ✅ `README_HF.md` (created)
- ✅ `main.py` (existing)
- ✅ `src/` directory (existing)

---

## Step 4: Clone Your Space Repository

```bash
# Clone the Space repository
git clone https://huggingface.co/spaces/YOUR_USERNAME/todo-api-backend
cd todo-api-backend
```

---

## Step 5: Copy Backend Files

```bash
# Copy all backend files to the Space directory
# From your project root:
cp -r backend/* todo-api-backend/

# Or manually copy these files:
# - main.py
# - requirements.txt
# - Dockerfile
# - README_HF.md (rename to README.md)
# - src/ (entire directory)
```

---

## Step 6: Commit and Push to Hugging Face

```bash
cd todo-api-backend

# Rename README_HF.md to README.md
mv README_HF.md README.md

# Add all files
git add .

# Commit
git commit -m "Deploy FastAPI backend to Hugging Face"

# Push to Hugging Face
git push
```

---

## Step 7: Wait for Build

1. Go to your Space page: `https://huggingface.co/spaces/YOUR_USERNAME/todo-api-backend`
2. Watch the build logs in the **"Logs"** tab
3. Wait for "Running on http://0.0.0.0:7860" message
4. Space will show "Running" status when ready

---

## Step 8: Test Your API

Once deployed, your API will be available at:
```
https://YOUR_USERNAME-todo-api-backend.hf.space
```

Test endpoints:
- **API Docs**: `https://YOUR_USERNAME-todo-api-backend.hf.space/docs`
- **Health Check**: `https://YOUR_USERNAME-todo-api-backend.hf.space/`

---

## Step 9: Update Frontend Configuration

Update your frontend `.env.local`:
```env
BETTER_AUTH_URL=https://YOUR_USERNAME-todo-api-backend.hf.space
```

---

## Troubleshooting

### Build Fails
- Check logs in the "Logs" tab
- Verify all dependencies in requirements.txt
- Ensure Dockerfile syntax is correct

### Database Connection Error
- Verify DATABASE_URL secret is correct
- Check Neon database is active
- Ensure IP whitelist allows Hugging Face IPs (or set to 0.0.0.0/0)

### CORS Errors
- Update FRONTEND_URL secret with your deployed frontend URL
- Restart the Space after updating secrets

### Port Issues
- Hugging Face Spaces require port 7860
- Dockerfile already configured correctly

---

## Alternative: Deploy via Hugging Face CLI

```bash
# Install Hugging Face CLI
pip install huggingface_hub

# Login
huggingface-cli login

# Create Space
huggingface-cli repo create --type space --space_sdk docker todo-api-backend

# Push files
cd backend
git init
git remote add space https://huggingface.co/spaces/YOUR_USERNAME/todo-api-backend
git add .
git commit -m "Initial deployment"
git push space main
```

---

## Important Notes

1. **Free Tier Limitations**:
   - CPU basic (free)
   - May sleep after inactivity
   - Limited compute resources

2. **Security**:
   - Never commit .env files
   - Use Space secrets for sensitive data
   - Keep BETTER_AUTH_SECRET secure

3. **Database**:
   - Ensure Neon database allows external connections
   - Consider connection pooling for production

4. **Monitoring**:
   - Check logs regularly
   - Monitor API response times
   - Set up error tracking

---

## Next Steps

1. Deploy frontend to Vercel/Netlify
2. Update CORS settings with production frontend URL
3. Test end-to-end authentication flow
4. Monitor API performance
5. Set up custom domain (optional)

---

## Support

- Hugging Face Docs: https://huggingface.co/docs/hub/spaces
- FastAPI Docs: https://fastapi.tiangolo.com
- Your GitHub Repo: https://github.com/KhalidGhani333/The-Evolution-of-Todo
