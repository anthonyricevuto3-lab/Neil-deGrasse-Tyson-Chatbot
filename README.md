
# Neil deGrasse Tyson ChatBot

This project is a full-stack chatbot application inspired by Neil deGrasse Tyson. It features a FastAPI backend and a React (Vite) frontend, deployed to Azure using GitHub Actions.

## Features
- Conversational AI chatbot with context and memory
- FastAPI backend (Python)
- React frontend (TypeScript, Vite)
- Containerized with Docker
- CI/CD with GitHub Actions
- Deployed to Azure Container Apps and Azure Static Web Apps

## Deployment
- Backend: Azure Container Apps
- Frontend: Azure Static Web Apps
- Docker images published to GitHub Container Registry

## Secrets Required
- `AZURE_CREDENTIALS`: Azure service principal credentials (JSON)
- `AZURE_STATIC_WEB_APPS_API_TOKEN`: Deployment token from Azure Static Web App
- `OPENAI_API_KEY`: API key for OpenAI

## Quick Start
1. Clone the repository
2. Set up required secrets in your GitHub repository
3. Push to `main` to trigger deployment

## License
See [LICENSE](LICENSE) for details.
