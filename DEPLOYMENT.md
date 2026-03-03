# Deployment Guide

Complete guide for deploying the AI Humanoid Textbook platform to production.

## Overview

- **Frontend**: GitHub Pages (static Docusaurus build)
- **Backend**: Cloud hosting (Render, Railway, or Vercel)
- **Database**: Neon (serverless PostgreSQL)
- **Vector DB**: Qdrant Cloud

## Prerequisites

- GitHub account
- Neon account (free tier available)
- Qdrant Cloud account (or local Qdrant for testing)
- Gemini API key
- Hosting platform account (Render/Railway/Vercel)

## Part 1: Database Setup

### 1.1 Neon PostgreSQL

1. **Create Database**
   - Go to [Neon Console](https://console.neon.tech/)
   - Click "New Project"
   - Name: `ai-textbook-prod`
   - Copy connection string

2. **Configure Connection String**
   ```
   postgresql://user:password@host:5432/database_name
   ```

3. **Create Tables**
   ```bash
   # In backend directory, update .env with Neon URL
   python init_db.py
   ```

### 1.2 Qdrant Cloud

1. **Create Cluster**
   - Go to [Qdrant Cloud](https://cloud.qdrant.io/)
   - Sign up/Login
   - Create new cluster (free tier available)
   - Copy API key and URL

2. **Configure Access**
   - Note cluster URL (e.g., `https://xxx.aws.cloud.qdrant.io`)
   - Copy API key from dashboard

## Part 2: Backend Deployment

### Option A: Render (Recommended)

1. **Prepare Repository**

   Create `render.yaml` in project root:

   ```yaml
   services:
     - type: web
       name: ai-textbook-backend
       env: python
       region: oregon
       plan: free
       branch: main
       buildCommand: |
         pip install -r backend/requirements.txt
       startCommand: |
         cd backend && uvicorn main:app --host 0.0.0.0 --port $PORT
       envVars:
         - key: DATABASE_URL
           sync: false
         - key: QDRANT_URL
           sync: false
         - key: QDRANT_API_KEY
           sync: false
         - key: GEMINI_API_KEY
           sync: false
         - key: APP_ENV
           value: production
   ```

2. **Create Production Requirements**

   Create `backend/requirements-prod.txt`:
   ```
   fastapi==0.109.0
   uvicorn[standard]==0.27.0
   python-dotenv==1.0.0
   psycopg2-binary==2.9.9
   sqlalchemy==2.0.25
   qdrant-client==1.7.0
   requests==2.31.0
   ```

3. **Deploy to Render**
   - Go to [Render Dashboard](https://dashboard.render.com/)
   - Click "New +" → "Blueprint"
   - Connect GitHub repository
   - Select `render.yaml`
   - Add environment variables:
     - `DATABASE_URL` (from Neon)
     - `QDRANT_URL` (from Qdrant Cloud)
     - `QDRANT_API_KEY`
     - `GEMINI_API_KEY`
   - Click "Apply"

4. **Wait for Deployment**
   - Build takes ~3-5 minutes
   - Service URL will be: `https://ai-textbook-backend.onrender.com`

### Option B: Railway

1. **Create Railway Project**
   - Go to [Railway](https://railway.app/)
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Choose repository

2. **Configure Service**
   - Root directory: `backend`
   - Start command: `uvicorn main:app --host 0.0.0.0 --port $PORT`
   - Build command: `pip install -r requirements.txt`

3. **Add Environment Variables**
   ```
   DATABASE_URL=postgresql://...
   QDRANT_URL=https://...
   QDRANT_API_KEY=your_key
   GEMINI_API_KEY=your_key
   APP_ENV=production
   ```

4. **Deploy**
   - Click "Deploy"
   - Railway provides URL: `https://xxx.railway.app`

### Option C: Vercel (Serverless)

1. **Create Vercel Configuration**

   Create `vercel.json` in project root:
   ```json
   {
     "version": 2,
     "functions": {
       "backend/main.py": {
         "runtime": "@vercel/python"
       }
     },
     "routes": [
       {
         "src": "/(.*)",
         "dest": "backend/main.py"
       }
     ]
   }
   ```

2. **Install Vercel**
   ```bash
   npm install -g vercel
   ```

3. **Deploy**
   ```bash
   vercel login
   vercel --prod
   ```

## Part 3: Frontend Deployment

### GitHub Pages

1. **Update Configuration**

   Edit `frontend/docusaurus.config.ts`:
   ```typescript
   const config: Config = {
     title: 'Physical AI & Humanoid Robotics',
     tagline: 'The Future of Embodied Intelligence',
     
     // Update these:
     url: 'https://abdullahzunorain.github.io',
     baseUrl: '/text-book-AI-humanoid/',
     organizationName: 'abdullahzunorain',
     projectName: 'text-book-AI-humanoid',
     deploymentBranch: 'gh-pages',
     trailingSlash: false,
     
     // ... rest of config
   };
   ```

2. **Update Chat API URL**

   Edit `frontend/src/theme/Layout.tsx`:
   ```tsx
   <Chat 
     apiUrl="https://your-backend-url.onrender.com"  // Your production backend
     userId={1} 
   />
   ```

3. **Build and Deploy**
   ```bash
   cd frontend
   
   # Build
   npm run build
   
   # Deploy (requires GIT_USER)
   GIT_USER=abdullahzunorain npm run deploy
   ```

4. **Enable GitHub Pages**
   - Go to repository Settings → Pages
   - Source: Select `gh-pages` branch
   - Save
   - Site will be live at: `https://abdullahzunorain.github.io/text-book-AI-humanoid/`

## Part 4: Post-Deployment

### 4.1 Ingest Textbook Content

After backend is deployed, you need to ingest content:

```bash
# If you can access backend directly
curl -X POST "https://your-backend-url.com/ingest"

# Or run locally with production DB
DATABASE_URL=your_prod_url \
QDRANT_URL=your_qdrant_url \
python backend/ingest_textbook.py
```

### 4.2 Test Production

1. **Health Check**
   ```bash
   curl https://your-backend-url.com/health
   ```

2. **Test Chat**
   ```bash
   curl -X POST "https://your-backend-url.com/chat/?user_id=1&message=Hello"
   ```

3. **Visit Frontend**
   - Navigate to GitHub Pages URL
   - Open chat widget
   - Test with textbook questions

### 4.3 Configure CORS

Update `backend/main.py` for production:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://abdullahzunorain.github.io",
        "http://localhost:3000"  # Keep for development
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## Part 5: Monitoring

### Backend Logs

**Render:**
- Dashboard → Logs tab
- Real-time streaming

**Railway:**
- Project → Deployments → View logs

### Database Monitoring

**Neon:**
- Dashboard → Insights
- Connection count
- Query performance

**Qdrant:**
- Cloud dashboard
- Vector count
- Search latency

### Frontend Analytics

Add Google Analytics to `docusaurus.config.ts`:

```typescript
presets: [
  [
    'classic',
    {
      // ... other config
      googleAnalytics: {
        trackingID: 'UA-XXXXXX-X',
      },
    },
  ],
],
```

## Part 6: CI/CD

### GitHub Actions

Create `.github/workflows/deploy.yml`:

```yaml
name: Deploy to Production

on:
  push:
    branches: [main]

jobs:
  deploy-backend:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Deploy to Render
        uses: render-oss/actions/deploy@v1
        with:
          service-id: ${{ secrets.RENDER_SERVICE_ID }}
          api-key: ${{ secrets.RENDER_API_KEY }}

  deploy-frontend:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
        with:
          node-version: '20'
      - name: Build and Deploy
        run: |
          cd frontend
          npm install
          npm run build
          git config --global user.name 'GitHub Actions'
          git config --global user.email 'actions@github.com'
          GIT_USER=abdullahzunorain npm run deploy
```

## Troubleshooting

### Backend Issues

**Service won't start:**
- Check logs for errors
- Verify all environment variables
- Test database connection locally

**Database connection errors:**
- Check Neon connection string
- Ensure IP is not blocked
- Verify database exists

**Qdrant errors:**
- Verify URL format (https://)
- Check API key is correct
- Ensure collection exists

### Frontend Issues

**Chat not connecting:**
- Check API URL in Layout.tsx
- Verify CORS settings
- Test backend URL directly

**Build fails:**
- Run `npm run build` locally first
- Check TypeScript errors
- Verify all imports

### Performance Issues

**Slow responses:**
- Check backend logs for slow queries
- Optimize chunk size
- Consider caching layer

**High latency:**
- Use CDN for frontend
- Choose backend region close to users
- Optimize database queries

## Cost Optimization

### Free Tier Resources

- **Neon**: 0.5 GB storage, 100K compute units/month
- **Qdrant**: Free tier with 1GB storage
- **Render**: Free tier with 750 hours/month
- **GitHub Pages**: Free for public repos
- **Gemini API**: Free tier available

### Cost-Saving Tips

1. Use free tiers for development
2. Scale down during low-traffic periods
3. Cache frequent queries
4. Optimize vector search parameters
5. Use connection pooling

## Security Checklist

- [ ] All environment variables set
- [ ] HTTPS enabled everywhere
- [ ] CORS configured for production domains
- [ ] Database credentials rotated
- [ ] API keys secured
- [ ] Rate limiting enabled
- [ ] Error messages don't leak info
- [ ] Regular backups configured

## Next Steps

After successful deployment:

1. Set up custom domain (optional)
2. Configure SSL certificates
3. Set up monitoring alerts
4. Implement user analytics
5. Plan content updates
6. Gather user feedback

## Support

For deployment issues:
- Check platform documentation
- Review error logs
- Test locally first
- Contact platform support
