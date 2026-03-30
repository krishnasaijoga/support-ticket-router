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

## Observation
- ticket_text
- customer_tier
- urgency
- message

## Actions
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

## Tasks
- easy
- medium
- hard

## Grader
Compares action history with current flow and outputs score from 0.0 to 1.0

## Baseline
Rule-based policy using keywords from ticket text.

## Deployment
Live API: https://krishnajoga-support-ticket-router-v2.hf.space
Docs: https://krishnajoga-support-ticket-router-v2.hf.space/docs

## Run locally

```bash  
uvicorn app:app --host 0.0.0.0 --port 7860