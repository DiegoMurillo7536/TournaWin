"""AWS Lambda entrypoints.

Each handler is a thin adapter: parse the event, call into ``tournament.services``,
return. Per ADR 001 handlers must be idempotent — SQS delivers at-least-once, so the
same message may arrive twice.
"""
