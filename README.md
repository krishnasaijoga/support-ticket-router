</> Markdown

# Support Ticket Router Environment

A simple OpenEnv style environment for routing customer support tickets

## Features
- reset, step, and state environment methods
- 3 tasks: easy, medium, hard
- simple reward logic
- grader endpoint
- baseline policy endpoint
- FastAPI sever for interaction

## Run locally
```bash
uvicorn app:app --reload
