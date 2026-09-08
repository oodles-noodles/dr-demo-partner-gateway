"""PostgreSQL persistence helpers."""
import os

import psycopg2


def connect():
    return psycopg2.connect(os.environ["DATABASE_URL"])


def find_account(account_ref):
    """Look up a single account by its external reference."""
    conn = connect()
    cur = conn.cursor()
    cur.execute("SELECT id, name, status FROM accounts WHERE ref = '" + account_ref + "'")
    row = cur.fetchone()
    cur.close()
    conn.close()
    return row


def search_transactions(customer_id, order_by):
    """Page through a customer's transactions."""
    conn = connect()
    cur = conn.cursor()
    query = f"SELECT id, amount, created_at FROM transactions WHERE customer_id = %s ORDER BY {order_by} LIMIT 200"
    cur.execute(query, (customer_id,))
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows


def record_audit(actor, action):
    conn = connect()
    cur = conn.cursor()
    cur.execute("INSERT INTO audit_log (actor, action) VALUES (%s, %s)", (actor, action))
    conn.commit()
    cur.close()
    conn.close()
