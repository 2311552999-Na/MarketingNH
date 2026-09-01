import streamlit as st
import pandas as pd
from datetime import datetime

# Cấu hình trang
st.set_page_config(page_title="App Lưu Thông Tin Khách Hàng", layout="centered")

st.title("📋 App Lưu Thông Tin Khách Hàng Tiềm Năng")

# Khởi tạo bộ nhớ tạm để lưu dữ liệu
if "danh_sach" not in st.session_state:
    st.session_state.danh_sach = []

# --- FORM NHẬP THÔNG TIN KHÁCH HÀNG ---
with st.form("form_khach_hang", clear_on_submit=True):
    st.subheader("Nhập thông tin khách hàng mới")
    ho_ten = st.text_input("Họ và tên *")
    sdt = st.text_input("Số điện thoại *")
    email = st.text_input("Email")
    san_pham = st.selectbox(
        "Sản phẩm/Dịch vụ quan tâm", 
        ["Thẻ tín dụng", "Vay tiêu dùng", "Gửi tiết kiệm", "Mở tài khoản thanh toán", "Vay mua nhà/xe"]
    )
    ghi_chu = st.text_area("Ghi chú cuộc gọi / Nhu cầu chi tiết")
    
    btn_submit = st.form_submit_button("Lưu thông tin")

# Xử lý nút lưu
if btn_submit:
    if not ho_ten or not sdt:
        st.error("Vui lòng điền Họ tên và Số điện thoại!")
    else:
        st.session_state.danh_sach.append({
            "Thời gian": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "Họ tên": ho_ten,
            "Số điện thoại": sdt,
            "Email": email,
            "Sản phẩm": san_pham,
            "Ghi chú": ghi_chu
        })
        st.success(f"Đã lưu thành công khách hàng: {ho_ten}")

# --- HIỂN THỊ DANH SÁCH & XUẤT FILE ---
st.divider()
st.subheader("📊 Danh sách khách hàng đã lưu")

if st.session_state.danh_sach:
    df = pd.DataFrame(st.session_state.danh_sach)
    st.dataframe(df, use_container_width=True, hide_index=True)
    
    # Nút xuất file Excel/CSV
    csv = df.to_csv(index=False).encode('utf-8-sig')
    st.download_button(
        label="📥 XUẤT FILE EXCEL / CSV",
        data=csv,
        file_name="danh_sach_khach_hang.csv",
        mime="text/csv",
        use_container_width=True
    )
else:
    st.info("Chưa có dữ liệu khách hàng nào.")
