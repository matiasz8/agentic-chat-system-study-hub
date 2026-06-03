# Deployment Guide - Vercel

## 1. Setup Vercel Project

```bash
# Install Vercel CLI
npm i -g vercel

# Login to Vercel
vercel login

# Link project
vercel link

# Configure project name
# Answer: agentic-chat-system-study-hub
```

## 2. Environment Setup

Create `.env.local`:
```
NEXT_PUBLIC_SITE_URL=https://your-domain.vercel.app
```

## 3. Deploy

```bash
# Preview deploy
vercel --prod

# Or push to GitHub and auto-deploy
git push origin main
```

## 4. Production URL

After deployment:
- **Preview**: `https://agentic-chat-system-study-hub.vercel.app`
- **Custom domain**: Configure in Vercel dashboard

## 5. Auto-Deploy with GitHub Actions

Push to main branch → Vercel auto-deploys

## Build Info

- **Framework**: Next.js
- **Build command**: `npm run build`
- **Output**: `.next`
- **Install**: `npm install`

---

**Deployed at:** [Check Vercel Dashboard](https://vercel.com)
