# Deployment Guide for Render

This guide will help you deploy your PervoChat application to Render.

## Prerequisites

1. A GitHub account
2. A Render account (https://render.com)

## Deployment Steps

### 1. Prepare Your Repository

1. Make sure all your changes are committed to your GitHub repository
2. Ensure the following files are in your repository:
   - `app.py` (main Flask application)
   - `wsgi.py` (WSGI entry point)
   - `requirements.txt` (dependencies)
   - `render.yaml` (Render configuration)
   - `Procfile` (process file)
   - `runtime.txt` (Python version)
   - `.buildpacks` (buildpack specification)

### 2. Create a New Web Service on Render

1. Go to https://dashboard.render.com
2. Click "New" and select "Web Service"
3. Connect your GitHub repository
4. Configure the service:
   - **Name**: Choose a name for your service (e.g., "pervochat")
   - **Region**: Choose the region closest to your users
   - **Branch**: Select the branch to deploy (usually "main" or "master")
   - **Root Directory**: Leave empty if the app is in the root directory
   - **Environment**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn --worker-class eventlet -w 1 wsgi:app`

### 3. Environment Variables

Add the following environment variables in the Render dashboard:

1. Go to your service dashboard
2. Click on "Environment" in the sidebar
3. Add these variables:
   - `FLASK_ENV`: `production`
   - `PYTHON_VERSION`: `3.9.15`

### 4. Deploy

1. Click "Create Web Service"
2. Render will automatically start building and deploying your application
3. The build process will:
   - Clone your repository
   - Install dependencies from requirements.txt
   - Start your application using the specified start command

### 5. Monitor Deployment

1. Watch the build logs in the Render dashboard
2. Once deployment is complete, your app will be available at the provided URL
3. The URL will be in the format: `https://your-app-name.onrender.com`

## Troubleshooting

### Common Issues

1. **Build Failures**:
   - Check that all dependencies are listed in requirements.txt
   - Ensure there are no syntax errors in your Python files
   - Verify that your build command is correct

2. **Application Not Starting**:
   - Check the application logs in Render dashboard
   - Ensure your wsgi.py file exports the application correctly
   - Verify that your start command is correct

3. **Database Issues**:
   - Your application uses SQLite which is stored in the file system
   - Note that Render's filesystem is ephemeral, so data may be lost when the service restarts
   - For production use, consider migrating to a persistent database like PostgreSQL

### Logs

To view logs:
1. Go to your service dashboard on Render
2. Click "Logs" in the sidebar
3. You can also use the Render CLI to view logs in real-time

## Scaling

Render automatically scales your application based on traffic. For more control:

1. Go to your service dashboard
2. Click "Settings" in the sidebar
3. Adjust the instance count and instance type as needed

## Custom Domain (Optional)

To use a custom domain:

1. Go to your service dashboard
2. Click "Settings" in the sidebar
3. Scroll to "Custom Domains"
4. Follow the instructions to add your domain
5. Update your DNS records as instructed

## Environment-Specific Configuration

For different environments (development, staging, production):

1. Use environment variables to configure your application
2. Set different values for each environment in Render
3. Access them in your code using `os.environ.get('VARIABLE_NAME')`

## Updating Your Application

To deploy updates:

1. Push changes to your GitHub repository
2. Render will automatically detect the changes and start a new deployment
3. You can also manually trigger a deployment from the Render dashboard

## Support

If you encounter issues:
1. Check the Render documentation: https://render.com/docs
2. Contact Render support through their dashboard
3. Verify your code works locally before deploying