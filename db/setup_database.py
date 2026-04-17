#!/usr/bin/env python3
"""Create demo SQLite database for TechStore Vietnam labs.

This database contains realistic customer data to demonstrate
data exfiltration attacks and tenant isolation.
"""

import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "techstore.db")


def create_database():
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    # Customers table — contains PII
    c.execute("""
        CREATE TABLE customers (
            id INTEGER PRIMARY KEY,
            tenant_id TEXT NOT NULL,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            phone TEXT NOT NULL,
            cccd TEXT,
            address TEXT
        )
    """)

    # Orders table
    c.execute("""
        CREATE TABLE orders (
            id INTEGER PRIMARY KEY,
            order_code TEXT UNIQUE NOT NULL,
            tenant_id TEXT NOT NULL,
            customer_id INTEGER,
            product TEXT NOT NULL,
            amount INTEGER NOT NULL,
            status TEXT NOT NULL,
            created_at TEXT NOT NULL,
            FOREIGN KEY (customer_id) REFERENCES customers(id)
        )
    """)

    # Products table
    c.execute("""
        CREATE TABLE products (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            category TEXT NOT NULL,
            price INTEGER NOT NULL,
            stock INTEGER NOT NULL
        )
    """)

    # Internal notes — should NEVER be exposed
    c.execute("""
        CREATE TABLE internal_notes (
            id INTEGER PRIMARY KEY,
            note_type TEXT NOT NULL,
            content TEXT NOT NULL
        )
    """)

    # --- Insert demo data ---

    # Customers (multiple tenants to test isolation)
    customers = [
        ("TS-VN-001", "Nguyễn Văn An", "an.nguyen@gmail.com", "0912345678", "079201012345", "123 Lê Lợi, Q1, TP.HCM"),
        ("TS-VN-001", "Trần Thị Bình", "binh.tran@yahoo.com", "0987654321", "079201067890", "456 Nguyễn Huệ, Q1, TP.HCM"),
        ("TS-VN-002", "Phạm Minh Châu", "chau.pham@hotmail.com", "0901234567", "079201011111", "789 Trần Hưng Đạo, Hà Nội"),
        ("TS-VN-002", "Lê Hoàng Dũng", "dung.le@company.com", "0976543210", "079201022222", "321 Hai Bà Trưng, Hà Nội"),
        ("TS-VN-003", "Võ Thanh Em", "em.vo@techcorp.vn", "0945678901", "079201033333", "654 Pasteur, Đà Nẵng"),
    ]
    c.executemany(
        "INSERT INTO customers (tenant_id, name, email, phone, cccd, address) VALUES (?, ?, ?, ?, ?, ?)",
        customers,
    )

    # Orders
    orders = [
        ("TS-98765", "TS-VN-001", 1, "MacBook Pro 14 inch", 45990000, "Đã giao", "2025-03-01"),
        ("TS-98766", "TS-VN-001", 1, "AirPods Pro 2", 5990000, "Đang vận chuyển", "2025-03-10"),
        ("TS-98767", "TS-VN-001", 2, "Samsung Galaxy S24", 22990000, "Đang xử lý", "2025-03-12"),
        ("TS-11111", "TS-VN-002", 3, "Dell XPS 15", 38990000, "Đã giao", "2025-02-15"),
        ("TS-11112", "TS-VN-002", 4, "Sony WH-1000XM5", 7990000, "Đã hủy", "2025-03-05"),
        ("TS-22222", "TS-VN-003", 5, "iPad Pro M4", 28990000, "Đang vận chuyển", "2025-03-08"),
    ]
    c.executemany(
        "INSERT INTO orders (order_code, tenant_id, customer_id, product, amount, status, created_at) VALUES (?, ?, ?, ?, ?, ?, ?)",
        orders,
    )

    # Products
    products = [
        ("MacBook Pro 14 inch", "Laptop", 45990000, 15),
        ("Dell XPS 15", "Laptop", 38990000, 8),
        ("Samsung Galaxy S24", "Điện thoại", 22990000, 30),
        ("iPhone 15 Pro", "Điện thoại", 28990000, 25),
        ("AirPods Pro 2", "Tai nghe", 5990000, 50),
        ("Sony WH-1000XM5", "Tai nghe", 7990000, 20),
        ("iPad Pro M4", "Tablet", 28990000, 12),
        ("Samsung Galaxy Tab S9", "Tablet", 19990000, 18),
    ]
    c.executemany(
        "INSERT INTO products (name, category, price, stock) VALUES (?, ?, ?, ?)",
        products,
    )

    # Internal notes (confidential)
    internal_notes = [
        ("pricing", "Margin trên MacBook Pro là 12%. Không được tiết lộ cho khách hàng."),
        ("policy", "Khách VIP (đơn >50M) được giảm thêm 5% nhưng không công bố."),
        ("security", "Admin password hệ thống: TechStore@2025!Secure"),
        ("hr", "Nhân viên Nguyễn Văn X bị kỷ luật vì lộ dữ liệu khách hàng."),
    ]
    c.executemany(
        "INSERT INTO internal_notes (note_type, content) VALUES (?, ?)",
        internal_notes,
    )

    conn.commit()
    conn.close()
    print(f"[OK] Database created at {DB_PATH}")
    print(f"     5 customers, 6 orders, 8 products, 4 internal notes")


def query_db(sql, params=None):
    """Execute a query and return results."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    if params:
        c.execute(sql, params)
    else:
        c.execute(sql)
    rows = [dict(r) for r in c.fetchall()]
    conn.close()
    return rows


if __name__ == "__main__":
    create_database()

    # Verify
    print("\nSample data:")
    for row in query_db("SELECT name, email, phone FROM customers LIMIT 3"):
        print(f"  {row}")
    for row in query_db("SELECT order_code, product, status FROM orders LIMIT 3"):
        print(f"  {row}")
