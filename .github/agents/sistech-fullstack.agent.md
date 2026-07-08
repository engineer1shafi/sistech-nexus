# SISTECH NEXUS Agent Instructions

You are working on SISTECH NEXUS, an Enterprise Network Operations Platform.

## Stack

- Backend: Python, FastAPI, SQLAlchemy Async, PostgreSQL, Alembic
- Frontend: React, TypeScript, Vite, Tailwind CSS
- Monitoring: SNMP v2c/v3, Interface Discovery, Topology, Alerts
- Architecture: Repository Pattern, Service Layer, Clean Architecture

## Rules

- Do not rewrite unrelated files.
- Do not remove existing features.
- Follow the existing folder structure.
- Keep backend APIs backward compatible.
- Use async database access.
- Use service layer for business logic.
- Use repository layer for database operations.
- Add schemas for request/response validation.
- Add migrations when models change.
- Keep frontend components modular.
- Avoid mock data unless explicitly requested.
- Never commit `.env`, `.venv`, `node_modules`, or build output.

## Current Goals

Sprint 4:
1. Interface Inventory
2. SNMP Walk Engine
3. Interface Discovery
4. Interface UI
5. LLDP/Topology Foundation

## Coding Style

- Python: type hints, clean imports, small functions
- FastAPI: APIRouter per module
- React: functional components, hooks, TypeScript types
- UI: dark NOC style, enterprise dashboard look