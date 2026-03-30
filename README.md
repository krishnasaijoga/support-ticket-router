---
title: Support Ticket Router
emoji: 🚀
colorFrom: blue
colorTo: green
sdk: docker
app_port: 7860
pinned: false
---

# Support Ticket Router Environment

A simple OpenEnv-style environment for routing customer support tickets.

## Features
- reset, step, and state environment methods
- 3 tasks: easy, medium, hard
- simple reward logic
- grader endpoint
- baseline policy endpoint
- FastAPI server for interaction

## Run locally

```bash  
uvicorn app:app --host 0.0.0.0 --port 7860