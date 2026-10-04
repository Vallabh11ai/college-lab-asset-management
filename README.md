# College Laboratory Equipment & Asset Management System

A Python + Streamlit + SQLite project for managing college laboratory equipment.

## Objectives
- Centralized laboratory asset inventory
- Track condition, status, assignment and warranty
- Record maintenance and repair history
- Manage damage/complaint reports
- Provide dashboard analytics
- Demonstrate Agile/Kanban development with GitHub

## Technology
Python 3.14, Streamlit, SQLite, Pandas, Plotly, pytest, GitHub.

## Demo accounts
- Admin: `admin` / `admin123`
- Lab Technician: `technician` / `tech123`
- Faculty/Student: `student` / `student123`

These accounts are for local demonstration only.

## Run
```powershell
pip install -r requirements.txt
streamlit run app.py
```

## Test
```powershell
pytest -q
```

## AM workflow
Backlog -> Todo -> In Progress -> Testing -> Done

GitHub Issues are used as work items, with labels plus Priority and Work Type project fields.
