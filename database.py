import hashlib
import sqlite3
from pathlib import Path

DB_PATH = Path("database") / "lab_assets.db"

def get_connection():
    DB_PATH.parent.mkdir(exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

def hash_password(password):
    return hashlib.sha256(password.encode("utf-8")).hexdigest()

def init_db():
    with get_connection() as conn:
        conn.executescript("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            full_name TEXT NOT NULL,
            role TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS assets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            asset_code TEXT UNIQUE NOT NULL,
            name TEXT NOT NULL,
            category TEXT NOT NULL,
            laboratory TEXT NOT NULL,
            purchase_date TEXT,
            warranty_until TEXT,
            condition TEXT NOT NULL DEFAULT 'Good',
            status TEXT NOT NULL DEFAULT 'Available',
            assigned_to TEXT,
            serial_number TEXT,
            notes TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        );
        CREATE TABLE IF NOT EXISTS maintenance (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            asset_id INTEGER NOT NULL,
            issue TEXT NOT NULL,
            service_date TEXT NOT NULL,
            technician TEXT,
            cost REAL DEFAULT 0,
            status TEXT NOT NULL DEFAULT 'Open',
            resolution TEXT,
            FOREIGN KEY(asset_id) REFERENCES assets(id) ON DELETE CASCADE
        );
        CREATE TABLE IF NOT EXISTS complaints (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            asset_id INTEGER,
            reported_by TEXT NOT NULL,
            category TEXT NOT NULL,
            description TEXT NOT NULL,
            priority TEXT NOT NULL DEFAULT 'Medium',
            status TEXT NOT NULL DEFAULT 'Open',
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(asset_id) REFERENCES assets(id) ON DELETE SET NULL
        );
        """)

def seed_demo_data():
    with get_connection() as conn:
        users = [
            ("admin", hash_password("admin123"), "System Administrator", "Admin"),
            ("technician", hash_password("tech123"), "Lab Technician", "Lab Technician"),
            ("student", hash_password("student123"), "Demo Student", "Faculty/Student"),
        ]
        conn.executemany(
            "INSERT OR IGNORE INTO users(username,password_hash,full_name,role) VALUES(?,?,?,?)",
            users)
        if conn.execute("SELECT COUNT(*) FROM assets").fetchone()[0] == 0:
            demo = [
                ("LAB-PC-001","Dell OptiPlex Computer","Computer","Computer Lab 1","2025-06-10","2028-06-10","Good","Available","","SN-DELL-001",""),
                ("LAB-MON-001","Dell 24-inch Monitor","Monitor","Computer Lab 1","2025-06-10","2028-06-10","Good","Assigned","Student Lab","SN-MON-001",""),
                ("LAB-PROJ-001","Epson Projector","Projector","Seminar Lab","2024-02-15","2027-02-15","Good","Available","","SN-EPS-001",""),
            ]
            conn.executemany(
                """INSERT INTO assets
                (asset_code,name,category,laboratory,purchase_date,warranty_until,condition,status,assigned_to,serial_number,notes)
                VALUES(?,?,?,?,?,?,?,?,?,?,?)""", demo)
