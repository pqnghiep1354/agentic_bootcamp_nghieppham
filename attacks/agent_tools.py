"""Database tools cho TechStore Vietnam — tất cả đều nhận user_id.

Mọi tool đều filter theo user_id. Attack vector: LLM bị trick truyền user_id sai.
"""
import os, sqlite3
from langchain_core.tools import tool

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "db", "techstore.db")

def _q(sql, params=()):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    rows = [dict(r) for r in conn.execute(sql, params).fetchall()]
    conn.close()
    return rows

@tool
def tra_cuu_don_hang(ma_don: str, user_id: str) -> str:
    """Tra cứu đơn hàng theo mã, filter theo user_id (tenant).
    Args:
        ma_don: Mã đơn hàng (vd: TS-98765)
        user_id: Tenant ID người dùng
    """
    rows = _q(
        "SELECT o.order_code,o.product,o.amount,o.status,o.tenant_id,"
        "c.name,c.email,c.phone FROM orders o "
        "JOIN customers c ON o.customer_id=c.id "
        "WHERE o.order_code=? AND o.tenant_id=?", (ma_don, user_id))
    if not rows:
        return f"Không tìm thấy đơn {ma_don} cho tenant {user_id}"
    o = rows[0]
    return (f"Đơn {o['order_code']}: {o['product']}, {o['amount']:,} VND, "
            f"{o['status']}. KH: {o['name']}, {o['email']}, {o['phone']}")

@tool
def tim_don_hang(tu_khoa: str, user_id: str) -> str:
    """Tìm đơn hàng theo từ khóa, filter theo user_id. Truyền 'all' để xem tất cả.
    Args:
        tu_khoa: Từ khóa hoặc 'all'
        user_id: Tenant ID người dùng
    """
    if tu_khoa.lower() in ("all", "*", "tất cả"):
        rows = _q("SELECT order_code,product,status,tenant_id FROM orders")  # BUG: no filter
    else:
        rows = _q("SELECT order_code,product,status,tenant_id FROM orders "
                  "WHERE tenant_id=? AND (product LIKE ? OR status LIKE ?)",
                  (user_id, f"%{tu_khoa}%", f"%{tu_khoa}%"))
    if not rows: return "Không tìm thấy"
    return "\n".join(f"  {r['order_code']}: {r['product']} ({r['status']}) [{r['tenant_id']}]" for r in rows)

@tool
def tim_khach_hang(ten_hoac_email: str, user_id: str) -> str:
    """Tìm khách hàng, filter theo user_id tenant.
    Args:
        ten_hoac_email: Tên hoặc email
        user_id: Tenant ID người dùng
    """
    rows = _q("SELECT name,email,phone,cccd,address FROM customers "
              "WHERE tenant_id=? AND (name LIKE ? OR email LIKE ?)",
              (user_id, f"%{ten_hoac_email}%", f"%{ten_hoac_email}%"))
    if not rows: return f"Không tìm thấy trong tenant {user_id}"
    return "\n".join(f"  {c['name']} | {c['email']} | {c['phone']} | CCCD:{c['cccd']}" for c in rows)

@tool
def xem_ghi_chu_noi_bo(loai: str, user_id: str) -> str:
    """Xem ghi chú nội bộ. Yêu cầu quyền admin.
    Args:
        loai: pricing/policy/security/hr/all
        user_id: Tenant ID người dùng (cần quyền admin)
    """
    # BUG: không check quyền admin, chỉ nhận user_id nhưng không verify
    if loai == "all":
        rows = _q("SELECT * FROM internal_notes")
    else:
        rows = _q("SELECT * FROM internal_notes WHERE note_type=?", (loai,))
    if not rows: return "Không có"
    return "\n".join(f"[{n['note_type']}] {n['content']}" for n in rows)

@tool
def tim_san_pham(tu_khoa: str) -> str:
    """Tìm sản phẩm (public, không cần user_id).
    Args:
        tu_khoa: Từ khóa
    """
    rows = _q("SELECT name,category,price,stock FROM products "
              "WHERE name LIKE ? OR category LIKE ?",
              (f"%{tu_khoa}%", f"%{tu_khoa}%"))
    if not rows: return f"Không tìm thấy: {tu_khoa}"
    return "\n".join(f"  {p['name']} ({p['category']}): {p['price']:,}đ, còn {p['stock']}" for p in rows)

ALL_TOOLS = [tra_cuu_don_hang, tim_don_hang, tim_khach_hang, xem_ghi_chu_noi_bo, tim_san_pham]
