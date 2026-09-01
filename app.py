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
"💳 Dịch vụ ngân hàng quan tâm (*)",
            [
                "Vay mua nhà / Ô tô",
                "Gửi tiết kiệm (trên 500tr)",
                "Thẻ tín dụng Hạng Vàng/Bạch Kim",
                "Vay kinh doanh",
                "Mở tài khoản thanh toán / Thẻ chuẩn"
            ]
        )
        note = st.text_area("📝 Ghi chú chi tiết nhu cầu", placeholder="Thời gian tiện nghe máy, hạn mức mong muốn...")

    st.divider()

    if st.button("💾 LƯU VÀ PHÂN LOẠI KHÁCH HÀNG", type="primary", use_container_width=True):
        if phone.strip() == "":
            st.error("❌ Vui lòng nhập Số điện thoại.")
        elif name.strip() == "":
            st.error("❌ Vui lòng nhập Tên khách hàng.")
        else:
            rank, score = danh_gia_tiem_nang(income, service)
            now_str = datetime.now().strftime("%Y-%m-%d %H:%M")
            
            new_customer = {
                "Mã KH": f"KH{len(st.session_state.customers) + 101}",
                "Ngày tạo": now_str,
                "Số điện thoại": phone.strip(),
                "Tên khách hàng": name.strip(),
                "Email": email.strip(),
                "Địa chỉ": address.strip(),
                "Thu nhập (Tr)": income,
                "Dịch vụ quan tâm": service,
                "Điểm tiềm năng": score,
                "Phân loại": rank,
                "Ghi chú": note.strip()
            }
            
            st.session_state.customers.append(new_customer)
            st.success(f"✅ Đã lưu thành công khách hàng **{name}** | Phân loại: **{rank}**")

# ==========================================
# TRANG 2: TRA CỨU & TÌM KIẾM
# ==========================================
elif page == "🔍 Tra Cứu & Tìm Kiếm":
    st.title("🔍 TRUY XUẤT NHANH KHÁCH HÀNG")
    st.divider()

    if not st.session_state.customers:
        st.info("📭 Chưa có dữ liệu khách hàng nào trong hệ thống.")
    else:
        df = pd.DataFrame(st.session_state.customers)
        
        search_kw = st.text_input("🔎 Nhập Tên hoặc Số điện thoại để tìm kiếm:", placeholder="Nhập từ khóa...")
        
        if search_kw:
            filtered_df = df[
                df["Tên khách hàng"].str.contains(search_kw, case=False, na=False) |
                df["Số điện thoại"].str.contains(search_kw, case=False, na=False)
            ]
            st.write(f"Tìm thấy **{len(filtered_df)}** kết quả phù hợp:")
            st.dataframe(filtered_df, use_container_width=True, hide_index=True)
        else:
            st.dataframe(df, use_container_width=True, hide_index=True)

# ==========================================
# TRANG 3: ADMIN & BÁO CÁO
# ==========================================
elif page == "🔐 Trang Admin & Báo Cáo":
    st.title("🔐 HỆ THỐNG QUẢN TRỊ ADMIN")
st.divider()

    if not st.session_state.admin_logged_in:
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.subheader("🔑 Đăng nhập hệ thống")
            password = st.text_input("Mật khẩu quản trị", type="password")
            if st.button("ĐĂNG NHẬP", type="primary", use_container_width=True):
                if password == "123456":
                    st.session_state.admin_logged_in = True
                    st.rerun()
                else:
                    st.error("❌ Mật khẩu không chính xác.")
    else:
        top_col, logout_col = st.columns([5, 1])
        with top_col:
            st.subheader("📊 BÁO CÁO & DỮ LIỆU TỔNG HỢP")
        with logout_col:
            if st.button("🚪 Đăng xuất", use_container_width=True):
                st.session_state.admin_logged_in = False
                st.rerun()

        st.divider()

        if len(st.session_state.customers) == 0:
            st.info("📭 Chưa có dữ liệu khách hàng để hiển thị báo cáo.")
        else:
            df = pd.DataFrame(st.session_state.customers)

            # METRICS THỐNG KÊ
            m1, m2, m3, m4 = st.columns(4)
            total_cust = len(df)
            hot_cust = len(df[df["Phân loại"].str.contains("HOT")])
            warm_cust = len(df[df["Phân loại"].str.contains("WARM")])
            cold_cust = len(df[df["Phân loại"].str.contains("COLD")])

            m1.metric("Tổng số Khách hàng", f"{total_cust}")
            m2.metric("Khách HOT 🔥", f"{hot_cust}")
            m3.metric("Khách WARM ⚡", f"{warm_cust}")
            m4.metric("Khách COLD ❄️", f"{cold_cust}")

            st.divider()

            # BẢNG DỮ LIỆU & QUẢN LÝ
            st.write("### 📋 Danh sách chi tiết")
            st.dataframe(df, use_container_width=True, hide_index=True)

            # THAO TÁC XÓA DỮ LIỆU
            with st.expander("🗑️ Bảng điều khiển xóa / reset dữ liệu"):
                st.warning("Cảnh báo: Hành động xóa không thể khôi phục lại.")
                if st.button("❌ Xóa tất cả dữ liệu khách hàng"):
                    st.session_state.customers = []
                    st.success("Đã xóa toàn bộ dữ liệu!")
                    st.rerun()

            st.divider()

            # XUẤT EXCEL
            excel_file = export_excel()
            st.download_button(
                label="📥 XUẤT BÁO CÁO BẢNG TÍNH EXCEL (.XLSX)",
                data=excel_file,
                file_name="Bao_Cao_Khach_Hang_Ngan_Hang.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True
            )
