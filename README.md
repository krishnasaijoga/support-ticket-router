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
- extra_hard
- hard_missing_info
- vip_priority
- repeat_failure

## Grader
Compares action history with current flow and outputs score from 0.0 to 1.0

## Baseline
Rule-based policy using keywords from ticket text.

## Agent comparison

We evaluate 2 agents:
### 1. Baseline Agent
- Rule based
- keyword matching
- limited reasoning

### 2. LLM Agent
- context aware
- handles ambiguity
- adapts to multi-step tasks

### Comparison
Basline
task                baseline_grade      llm_grade
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

## Run locally

```bash  
uvicorn app:app --host 0.0.0.0 --port 7860

