# Hugging Face Deployment - اردو گائیڈ

## ضروری چیزیں

1. **Hugging Face Account**: https://huggingface.co/join پر اکاؤنٹ بنائیں
2. **Git**: آپ کے سسٹم پر انسٹال ہو
3. **Neon Database**: PostgreSQL connection string تیار ہو

---

## Step 1: Hugging Face Space بنائیں

1. https://huggingface.co/spaces پر جائیں
2. **"Create new Space"** پر کلک کریں
3. تفصیلات بھریں:
   - **Space name**: `todo-api-backend` (یا اپنی پسند کا نام)
   - **License**: MIT
   - **Select SDK**: **Docker** منتخب کریں
   - **Space hardware**: CPU basic (مفت)
   - **Visibility**: Public یا Private
4. **"Create Space"** پر کلک کریں

---

## Step 2: Secrets Configure کریں

Space بننے کے بعد، **Settings** → **Repository secrets** میں جائیں:

یہ secrets شامل کریں:

1. **DATABASE_URL**
   ```
   postgresql://username:password@host/database
   ```
   (آپ کی Neon PostgreSQL connection string)

2. **BETTER_AUTH_SECRET**
   ```
   your-secret-key-minimum-32-characters-long
   ```
   (وہی secret جو frontend میں استعمال کیا)

3. **FRONTEND_URL**
   ```
   http://localhost:3000
   ```
   (بعد میں deployed frontend URL سے اپڈیٹ کریں)

---

## Step 3: Space Repository Clone کریں

```bash
# Space repository clone کریں
git clone https://huggingface.co/spaces/YOUR_USERNAME/todo-api-backend
cd todo-api-backend
```

---

## Step 4: Backend Files Copy کریں

اپنے project کی backend directory سے تمام files Space directory میں copy کریں:

```bash
# Windows میں:
# Manually copy کریں یہ files/folders:
# - main.py
# - requirements.txt
# - Dockerfile
# - README_HF.md
# - src/ (پوری directory)
```

یا manually:
1. `backend` folder کھولیں
2. تمام files select کریں
3. `todo-api-backend` folder میں paste کریں

---

## Step 5: README Rename کریں

```bash
cd todo-api-backend

# README_HF.md کو README.md میں rename کریں
# Windows میں file explorer سے rename کر سکتے ہیں
```

---

## Step 6: Git Commit اور Push کریں

```bash
# تمام files add کریں
git add .

# Commit کریں
git commit -m "Deploy FastAPI backend to Hugging Face"

# Hugging Face پر push کریں
git push
```

---

## Step 7: Build کا انتظار کریں

1. اپنے Space page پر جائیں: `https://huggingface.co/spaces/YOUR_USERNAME/todo-api-backend`
2. **"Logs"** tab میں build logs دیکھیں
3. "Running on http://0.0.0.0:7860" message کا انتظار کریں
4. Space "Running" status دکھائے گا جب تیار ہو

---

## Step 8: API Test کریں

Deploy ہونے کے بعد، آپ کا API یہاں available ہوگا:
```
https://YOUR_USERNAME-todo-api-backend.hf.space
```

Test endpoints:
- **API Docs**: `https://YOUR_USERNAME-todo-api-backend.hf.space/docs`
- **Health Check**: `https://YOUR_USERNAME-todo-api-backend.hf.space/`

---

## Step 9: Frontend Update کریں

Frontend کی `.env.local` file میں update کریں:
```env
BETTER_AUTH_URL=https://YOUR_USERNAME-todo-api-backend.hf.space
```

---

## مسائل کا حل

### Build Fail ہو جائے
- "Logs" tab میں errors چیک کریں
- requirements.txt میں تمام dependencies verify کریں
- Dockerfile syntax صحیح ہے چیک کریں

### Database Connection Error
- DATABASE_URL secret صحیح ہے verify کریں
- Neon database active ہے چیک کریں
- IP whitelist میں 0.0.0.0/0 allow کریں

### CORS Errors
- FRONTEND_URL secret اپنے deployed frontend URL سے update کریں
- Secrets update کرنے کے بعد Space restart کریں

---

## اہم نوٹس

1. **Free Tier کی حدود**:
   - CPU basic (مفت)
   - Inactivity کے بعد sleep ہو سکتا ہے
   - محدود compute resources

2. **Security**:
   - .env files کبھی commit نہ کریں
   - Sensitive data کے لیے Space secrets استعمال کریں
   - BETTER_AUTH_SECRET محفوظ رکھیں

3. **Database**:
   - Neon database external connections allow کرے
   - Production کے لیے connection pooling consider کریں

---

## اگلے قدم

1. Frontend کو Vercel/Netlify پر deploy کریں
2. Production frontend URL کے ساتھ CORS settings update کریں
3. End-to-end authentication flow test کریں
4. API performance monitor کریں

---

یہ guide follow کر کے آپ اپنا backend Hugging Face پر deploy کر سکتے ہیں! 🚀
