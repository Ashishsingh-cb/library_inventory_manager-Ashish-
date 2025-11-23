# Library Inventory Manager

Lightweight CLI-based library inventory manager (Python).

Features:
- Object-oriented Book class and LibraryInventory manager
- Persistent storage using CSV and a human-readable TXT file
- Menu-driven CLI for add/issue/return/search/display
- Robust file handling with logging

How to run:
1. Ensure you have Python 3.8+ installed.
2. From project root run: `python -m cli.main` or `python cli/main.py`
3. Data files are stored in `data/catalog.csv` and `data/catalog.txt`

Notes:
- This project uses CSV/TXT for persistence (as requested).
- A sample empty catalog is created automatically.
