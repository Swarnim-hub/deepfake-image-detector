# Deepfake Image Detector

A full-stack web application for real-time Deepfake and AI-generated image detection.
Powered by a pre-trained **Hugging Face Vision Transformer / Deepfake Classifier**, served using **FastAPI**, with a reactive **React + Tailwind CSS** interface.

## ✨ Features

- **100% Free to Host & Maintain**: Zero server, database, or storage costs.
  - Frontend hosted on **Vercel** (Free edge hosting).
  - Backend API hosted on **Hugging Face Spaces** (Free Docker Space).
- **No Training Required**: Uses top pre-trained model weights (`prithivMLmods/Deep-Fake-Detector-v2-Model`) from Hugging Face directly.
- **Instant & Anonymous Access**: No login, signups, or tokens required.
- **In-Memory Analysis**: No user images stored on disk.
- **Modern Responsive UI**: Clean drag-and-drop file upload, animated gauge meters, and fast results.

---

## 🏗️ Architecture

- **Backend**: FastAPI, PyTorch, Hugging Face `transformers`, Pillow
- **Frontend**: React, Vite, Tailwind CSS, Lucide Icons, Axios
- **ML Engine**: `prithivMLmods/Deep-Fake-Detector-v2-Model` (auto-loaded on startup from Hugging Face Hub)

---

## 🚀 Free Deployment Guide

### 1. Backend on Hugging Face Spaces (Free)
1. Sign up on [Hugging Face](https://huggingface.co/) (100% Free).
2. Click **New Space** -> Choose **Docker SDK** -> Blank template.
3. Upload/push the contents of the `backend/` directory to your Space repository.
4. Hugging Face will automatically build and start the Docker container at:
   `https://<your-username>-<space-name>.hf.space`

### 2. Frontend on Vercel (Free)
1. Sign up on [Vercel](https://vercel.com/) (100% Free).
2. Connect your GitHub repository.
3. Set the Root Directory to `frontend`.
4. Add the Environment Variable:
   - `VITE_API_URL`: `https://<your-username>-<space-name>.hf.space`
5. Click **Deploy**. Your site will be live on `https://<your-project>.vercel.app`.

---

## 💻 Local Development

### Backend
```bash
cd backend
python -m venv venv
# Windows:
.\venv\Scripts\activate
# Linux/Mac:
# source venv/bin/activate

pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```
