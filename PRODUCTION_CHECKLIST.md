# Production Launch Checklist

Use this checklist before deploying to production to ensure everything is ready.

## Pre-Deployment

### Environment Setup

- [ ] Neon database created and connection string saved
- [ ] Qdrant Cloud cluster created and API key saved
- [ ] Gemini API key obtained
- [ ] GitHub repository is public (for GitHub Pages)
- [ ] Hosting platform account created (Render/Railway/Vercel)

### Backend Preparation

- [ ] All environment variables documented in `.env.example`
- [ ] Database migrations tested locally
- [ ] Textbook ingestion tested locally
- [ ] RAG chat tested with real queries
- [ ] API endpoints tested via Swagger UI
- [ ] Health check endpoint working
- [ ] CORS configured for production domains
- [ ] Error handling implemented for all endpoints
- [ ] Logging configured

### Frontend Preparation

- [ ] Backend API URL updated in `Layout.tsx`
- [ ] GitHub Pages configuration correct in `docusaurus.config.ts`
- [ ] Build tested locally (`npm run build`)
- [ ] No TypeScript errors
- [ ] All links working
- [ ] Chat component tested
- [ ] Mobile responsiveness verified
- [ ] Favicon and logos added

### Content Preparation

- [ ] Textbook content complete for MVP
- [ ] All markdown files linted
- [ ] Images optimized
- [ ] Links validated
- [ ] Table of contents updated

## Security Checklist

- [ ] No hardcoded secrets in code
- [ ] `.env` file in `.gitignore`
- [ ] API keys rotated from test to production
- [ ] HTTPS enforced
- [ ] CORS restricted to known domains
- [ ] SQL injection protection (using ORM)
- [ ] Input validation on all endpoints
- [ ] Error messages don't leak sensitive info
- [ ] Rate limiting considered for production

## Database Checklist

- [ ] Neon database created
- [ ] Tables created (`init_db.py`)
- [ ] Connection pooling configured
- [ ] Backup strategy defined
- [ ] Connection string tested from deployment environment

## Vector Database Checklist

- [ ] Qdrant Cloud cluster created
- [ ] Collection initialized (`init_qdrant.py`)
- [ ] Textbook content ingested (`ingest_textbook.py`)
- [ ] Search tested with various queries
- [ ] Vector count verified

## Testing Checklist

### Backend Tests

- [ ] Health check: `GET /health`
- [ ] User creation: `POST /users/`
- [ ] Chat endpoint: `POST /chat/`
- [ ] Chat history: `GET /chat/history/{user_id}`
- [ ] RAG components: `python test_rag.py`
- [ ] All endpoints via Swagger UI

### Frontend Tests

- [ ] Homepage loads
- [ ] Navigation works
- [ ] Chat widget appears
- [ ] Chat sends messages
- [ ] Chat displays responses
- [ ] Chat shows sources
- [ ] Mobile view works
- [ ] No console errors

### Integration Tests

- [ ] Frontend connects to backend
- [ ] Chat responses are textbook-based
- [ ] User registration works
- [ ] Chat history persists
- [ ] Load time acceptable (<3s)

## Deployment Steps

### Backend Deployment

- [ ] Environment variables set in hosting platform
- [ ] Build completed successfully
- [ ] Service started without errors
- [ ] Health check accessible from internet
- [ ] Logs show no errors
- [ ] Database connected
- [ ] Qdrant connected

### Frontend Deployment

- [ ] Build completed successfully
- [ ] Deployed to gh-pages branch
- [ ] GitHub Pages enabled in settings
- [ ] Site accessible via public URL
- [ ] Chat widget connects to backend
- [ ] No mixed content warnings (HTTPS)

## Post-Deployment

### Immediate Checks (First Hour)

- [ ] Visit production URL
- [ ] Test chat with multiple questions
- [ ] Verify responses are accurate
- [ ] Check backend logs for errors
- [ ] Monitor database connections
- [ ] Test on mobile device
- [ ] Test on different browsers

### Monitoring Setup (First Day)

- [ ] Backend logging verified
- [ ] Error tracking configured (optional)
- [ ] Uptime monitoring set up
- [ ] Performance metrics reviewed
- [ ] Database query performance checked

### Documentation (First Week)

- [ ] README.md updated with production URL
- [ ] API documentation accessible
- [ ] User guide created (optional)
- [ ] Troubleshooting guide updated

## Performance Optimization

- [ ] Response time < 2 seconds
- [ ] Frontend load time < 3 seconds
- [ ] Vector search optimized
- [ ] Database queries optimized
- [ ] Images compressed
- [ ] Caching considered for frequent queries

## Backup & Recovery

- [ ] Database backup schedule configured
- [ ] Backup restoration tested
- [ ] Deployment rollback plan documented
- [ ] Emergency contacts identified

## Compliance & Legal

- [ ] Privacy policy added (if collecting user data)
- [ ] Terms of service considered
- [ ] Cookie consent (if using analytics)
- [ ] Accessibility checked (WCAG 2.1 AA)

## Launch Communication

- [ ] Stakeholders notified
- [ ] Users informed (if applicable)
- [ ] Social media announcement prepared
- [ ] Documentation published

## Ongoing Maintenance

### Weekly

- [ ] Review error logs
- [ ] Check database size
- [ ] Monitor API usage
- [ ] Review user feedback

### Monthly

- [ ] Update dependencies
- [ ] Review performance metrics
- [ ] Backup verification
- [ ] Security audit

### Quarterly

- [ ] Content review and updates
- [ ] Feature planning
- [ ] Technical debt assessment
- [ ] User satisfaction survey

## Rollback Plan

If deployment fails:

1. **Identify Issue**
   - Check logs
   - Test locally
   - Reproduce error

2. **Quick Fix**
   - Fix bug locally
   - Test thoroughly
   - Redeploy

3. **Rollback**
   - Revert to previous commit
   - Redeploy previous version
   - Notify stakeholders

4. **Post-Mortem**
   - Document what went wrong
   - Create prevention plan
   - Update checklist

## Success Criteria

Deployment is considered successful when:

- ✅ Frontend accessible via public URL
- ✅ Backend API responding to requests
- ✅ Chat functionality working end-to-end
- ✅ No critical errors in logs
- ✅ Response time < 3 seconds
- ✅ Mobile experience acceptable
- ✅ All MVP features functional

## Emergency Contacts

- **Technical Lead**: [Name/Contact]
- **DevOps**: [Name/Contact]
- **On-Call**: [Name/Contact]

## Notes

Add any project-specific items here:

- [ ] Custom requirement 1
- [ ] Custom requirement 2
- [ ] Custom requirement 3

---

**Last Updated**: 2026-03-03
**Version**: 1.0.0
