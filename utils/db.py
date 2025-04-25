# utils/db.py

import os
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")  # Provided by Heroku

# Connect and return cursor+conn

def get_connection():
    try:
        conn = psycopg2.connect(DATABASE_URL, cursor_factory=RealDictCursor)
        return conn
    except Exception as e:
        print(f"❌ DB connection error: {e}")
        return None

# Example: create tables

def create_tables():
    conn = get_connection()
    if not conn:
        return
    cur = conn.cursor()
    try:
        cur.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                telegram_id BIGINT UNIQUE NOT NULL,
                username TEXT,
                role TEXT DEFAULT 'guest',
                joined_at TIMESTAMP DEFAULT NOW()
            );

            CREATE TABLE IF NOT EXISTS proposals (
                id SERIAL PRIMARY KEY,
                title TEXT NOT NULL,
                description TEXT,
                status TEXT DEFAULT 'open',
                created_at TIMESTAMP DEFAULT NOW()
            );

            CREATE TABLE IF NOT EXISTS votes (
                id SERIAL PRIMARY KEY,
                proposal_id INTEGER REFERENCES proposals(id) ON DELETE CASCADE,
                user_id BIGINT,
                vote TEXT CHECK (vote IN ('yes', 'no')),
                voted_at TIMESTAMP DEFAULT NOW()
            );
        ''')
        conn.commit()
        print("✅ Tables created or already exist.")
    except Exception as e:
        print(f"❌ Table creation error: {e}")
        conn.rollback()
    finally:
        cur.close()
        conn.close()

# Role check utility

def get_user_role(user_id):
    conn = get_connection()
    if not conn:
        return 'guest'
    cur = conn.cursor()
    try:
        cur.execute("SELECT role FROM users WHERE telegram_id = %s", (user_id,))
        result = cur.fetchone()
        return result['role'] if result else 'guest'
    except Exception as e:
        print(f"❌ Role lookup failed: {e}")
        return 'guest'
    finally:
        cur.close()
        conn.close()
