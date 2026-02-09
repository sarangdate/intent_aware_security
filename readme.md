# Intent-Aware Security Engine

This repository contains a simple, cloud-agnostic intent reasoning engine
for security-relevant events (e.g. IAM changes).

## What this project does

Given a structured security event, the engine:
- evaluates potential intent
- assigns a risk score
- explains reasoning factors

The focus is on **reasoning and explainability**, not infrastructure.

## Files

- `intent_engine.py` – core intent evaluation logic
- `test_events.json` – sample security event
- `test_intent.py` – local test runner

## How to run

```bash
python test_intent.py