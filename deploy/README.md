# Deployment

Since this week, every push is built and deployed by `.github/workflows/deploy.yml`.
The scripts here are course stubs: they print what they would do and change nothing.

- `Dockerfile`: image of the API.
- `deploy.sh`: the deployment step. Needs `DEPLOY_TOKEN` in its environment.
- `.env.prod`: production settings.
