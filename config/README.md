# Configuration Files

This directory contains configuration files for the Document-Aware GenAI Assistant.

## Files

- `logging.yaml` - Logging configuration
- `model_config.yaml` - AI model configuration
- `deployment.yaml` - Deployment configuration

## Usage

These configuration files are loaded by the application based on the environment:
- Development: Uses default configurations
- Production: Override with production-specific settings

## Environment Variables

Key environment variables are defined in `.env`:
- `OPENAI_API_KEY` - Your OpenAI API key
- `DATABASE_URL` - Database connection string
- `UPLOAD_DIR` - Directory for uploaded files
- `LOG_LEVEL` - Logging level (DEBUG, INFO, WARNING, ERROR)
