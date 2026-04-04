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

## Problem
A real world environment for routing support tickets.

## Environment
The environment models a support operations workflow where an agent receives a ticket, observes its content and priority,
and chooses the next best action.

The agent must:
- identify the right team
- escalate important or vip cases
- request more important when needed
- resolve the issue once the correct process is completed


## Observation
- ticket_text: text of the customer ticket
- customer_tier: customer level such as regular or vip
- urgency: urgency level as low, medium, high
- message: environment feedback after each action

Example:
json
{
    "ticket_text":"My ticket failed but money was deducted",
    "customer_tier":"regular",
    "urgency":"medium",
    "message":"New ticket received. Choose next action"
}

## Action Space
The agent can choose exactly one
- assign_billing
- assign_technical
- assign_shipping
- escalate
- request_more_info
- resolve

## Reward System
- +1 for correct action
- -0.5 for wrong action
- +1 bonus for successful completion
- +0.5 for raising escalation

## Tasks
- easy: Payment issue, flow: assign_billing->resolve
- medium: login issue, flow: assign_technical->resolve
- hard: VIP + urgent payment issue, flow: assign_billing->escalate->resolve
- extra_hard: payment + account issue, flow: assign_billing->assign_technical->resolve
- hard_missing_info: vague order issue, flow: request_more_info->assign_shipping->resolve
- vip_priority: VIP delayed order, flow: assign_shipping->escalate->resolve
- repeat_failure: repeated payment failure, flow: assign_billing->escalate->resolve

## Grader
Compares action history with current flow and outputs score from 0.0 to 1.0

## API Endpoints
The deployment exposes the following endpoints
- POST/reset
- POST/step
- GET/state
- GET/grader
- GET/baseline

## Baseline
Rule-based policy using keywords from ticket text.

### Baseline Grades
task                baseline_grade
easy                1.0
medium              1.0
hard                1.0
extra_hard          1.0
hard_missing_info   1.0
vip_priority        1.0
repeat_failure      1.0

## Deployment
Live API: https://krishnajoga-support-ticket-router-v2.hf.space
Docs: https://krishnajoga-support-ticket-router-v2.hf.space/docs

## Local Setup
Install dependencies
pip install -r requirements.txt

## Run locally

```bash  
uvicorn app:app --host 0.0.0.0 --port 7860```

## Notes
- Built with FastAPI
- Deployable on Hugging Face Spaces
- Lightweight and reproducible