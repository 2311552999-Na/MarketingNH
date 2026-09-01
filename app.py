import streamlit as st
import pandas as pd
from io import BytesIO
from datetime import datetime

# ==========================================
# CẤU HÌNH TRANG
# ==========================================
st.set_page_config(
    page_title="Hệ Thống Quản Lý Khách Hàng Ngân Hàng",
    page_icon="🏦",
    layout="wide"
)

# ==========================================
# KHỞI TẠO DỮ LIỆU SỐNG (SESSION STATE)
# ==========================================
if "customers" not in st.session_state:
    st.session_state.customers = []

if "admin_logged_in" not in st.session_state:
    st.session_state.admin_logged_in = False

# ==========================================
# HÀM XỬ LÝ NGHỆP VỤ & TÍNH TOÁN
# ==========================================
def danh_gia_tiem_nang(income, service):
    score = 0
    if income >= 30:
        score += 50
    elif income >= 15:
        score += 30
    else:
        score += 10

    if service in ["Vay mua nhà / Ô tô", "Gửi tiết kiệm (trên 500tr)"]:
        score += 50
    elif service in ["Thẻ tín dụng Hạng Vàng/Bạch Kim", "Vay kinh doanh"]:
        score += 30
    else:
        score += 20

    if score >= 80:
        return "🔥 HOT (Gọi ngay)", score
    elif score >= 50:
        return "⚡ WARM (Chăm sóc tuần)", score
    else:
        return "❄️ COLD (Gửi email/SMS)", score

def export_excel():
    df = pd.DataFrame(st.session_state.customers)
    output = BytesIO()
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name="Khách_Hàng")
    return output.getvalue()

# ==========================================
# SIDEBAR MENU
# ==========================================
st.sidebar.title("📌 MENU QUẢN LÝ")
page = st.sidebar.radio(
    "Chọn chức năng:",
    [
        "📝 Nhập Khách Hàng Mới",
        "🔍 Tra Cứu & Tìm Kiếm",
        "🔐 Trang Admin & Báo Cáo"
    ]
)

# ==========================================
# TRANG 1: NHẬP KHÁCH HÀNG MỚI
# ==========================================
if page == "📝 Nhập Khách Hàng Mới":
    st.title("🏦 NHẬP THÔNG TIN KHÁCH HÀNG TIỀM NĂNG")
    st.caption("Điền thông tin bên dưới để hệ thống tự động phân loại mức độ ưu tiên.")
    st.divider()

    col1, col2 = st.columns(2)
    
    with col1:
        phone = st.text_input("📱 Số điện thoại (*)", placeholder="Ví dụ: 0912345678")
        name = st.text_input("👤 Tên khách hàng (*)", placeholder="Ví dụ: Nguyễn Văn A")
        email = st.text_input("📧 Email liên hệ", placeholder="example@gmail.com")
        address = st.text_input("📍 Địa chỉ / Khu vực", placeholder="Quận/Huyện, Tỉnh/TP")

    with col2:
        income = st.number_input("💰 Thu nhập hàng tháng (Triệu VNĐ)", min_value=0, value=15, step=1)
        service = st.selectbox(
