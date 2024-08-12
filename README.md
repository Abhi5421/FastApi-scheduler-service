# FastAPI Scheduler Microservice

## Overview

### This microservice is designed to handle job scheduling and execution using FastAPI, Celery, or APScheduler. It provides API endpoints for job management and integrates with both Celery and APScheduler for periodic job execution. Jobs can be scheduled to run at various intervals, such as daily or weekly

## Features

## Job Scheduling:
### Schedule jobs to run at specified intervals using both Celery and APScheduler.

## API Endpoints:

### GET /jobs-list: List all jobs.
### GET /jobs/{job_id}: Retrieve details of a specific job by ID.
### POST /create-jobs: Create new jobs.

## Database Integration: 
### Store job details in a database.
## Job Execution: 
### Perform job execution using Celery tasks or APScheduler.

# Setup and Installation

## Prerequisites
## Python 3.8+

### Clone the Repository

### Create and Activate a Virtual Environment

## Install Dependencies
### pip install -r requirements.txt

### Configure Environment Variables

## to run
### sh run.sh




