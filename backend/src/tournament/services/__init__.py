"""Domain logic: bracket generation, standings, scheduling, tiebreakers.

Hard rule (see specs/05-adr/001-background-work.md): modules in this package must NOT
import FastAPI or boto3. They are pure domain logic, callable from an HTTP route and
from a Lambda handler alike, and unit-testable without HTTP or a database.
"""
