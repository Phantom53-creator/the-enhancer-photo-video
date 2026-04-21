# The Enhancer - Photo & Video Enhancement Service

## Live URLs

### Main Pages:
- **Home**: https://your-site.vercel.app/
- **Variation 1 (Dark Premium)**: https://your-site.vercel.app/v1
- **Variation 2 (Light SaaS)**: https://your-site.vercel.app/v2
- **Variation 3 (Bold High-Energy)**: https://your-site.vercel.app/v3

### API Endpoints:
- **Status**: https://your-site.vercel.app/api/status

## URL Structure (Permanent)

The Flask app is configured to serve pages at these routes:
- `/` → salespage-v1.html (main landing page)
- `/v1` → salespage-v1.html (dark theme)
- `/v2` → salespage-v2.html (light theme)
- `/v3` → salespage-v3.html (bold theme)

This structure is permanent and will not change between deployments.

## For Client Sharing

When sharing with clients, always use the `/v1`, `/v2`, or `/v3` format:
- Dark theme: `/v1`
- Light theme: `/v2`
- Bold theme: `/v3`

## Deployment Notes

- Vercel auto-deploys on every push to main branch
- URLs remain consistent across deployments
- Static HTML files are served via Flask routes
- 404 errors are handled gracefully

---
Built with OpenClaw | The Enhancer 2026
# Deployment trigger Tue Apr 21 09:31:35 UTC 2026
