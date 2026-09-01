import streamlit as st
import pandas as pd
from datetime import datetime
from io import BytesIO

# ==============================
# CẤU HÌNH
# ==============================

st.set_page_config(
    page_title="SmartBank CRM",
    page_icon="🏦",
    layout="wide"
)

# ==============================
# SESSION
# ==============================

if "customers" not in st.session_state:
    st.session_state.customers = []

# ==============================
# HÀM ĐỊNH DẠNG TIỀN
# ==============================

def tien_vnd(so_tien):
    return f"{int(so_tien):,}".replace(",", ".") + " VNĐ"


# ==============================
# HÀM CHẤM ĐIỂM
# ==============================

def cham_diem(thu_nhap, san_pham, nhu_cau):

    diem = 0

    if thu_nhap >= 50_000_000:
        diem += 40
    elif thu_nhap >= 30_000_000:
        diem += 30
    elif thu_nhap >= 15_000_000:
        diem += 20
    else:
        diem += 10

    if san_pham in ["Vay mua nhà", "Vay kinh doanh"]:
        diem += 30
    elif san_pham in ["Vay mua ô tô", "Thẻ tín dụng"]:
        diem += 25
    else:
        diem += 15

    if nhu_cau >= 2_000_000_000:
        diem += 30
    elif nhu_cau >= 1_000_000_000:
        diem += 25
    elif nhu_cau >= 500_000_000:
        diem += 20
    else:
        diem += 10

    if diem >= 80:
        xep_loai = "HOT"
    elif diem >= 50:
        xep_loai = "WARM"
    else:
        xep_loai = "COLD"

    return diem, xep_loai


# ==============================
# GIAO DIỆN
# ==============================

st.markdown(
    """
    <style>
    .stApp {
        background-color: #F4F6F9;
    }

    .main-title {
        background: #0B1F3A;
        padding: 30px;
        border-radius: 16px;
        color: white;
        margin-bottom: 25px;
    }

    .main-title h1 {
        margin: 0;
        font-size: 32px;
    }

    .main-title p {
        color: #B9C7D8;
        margin-bottom: 0;
    }

    .card {
        background: white;
        padding: 22px;
        border-radius: 15px;
        border: 1px solid #E3E8EF;
        margin-bottom: 15px;
    }

    .number {
        font-size: 30px;
        font-weight: bold;
        color: #0B1F3A;
    }

    .label {
        color: #718096;
        font-size: 13px;
        font-weight: bold;
    }

    .hot {
        color: #C0392B;
        font-weight: bold;
    }

    .warm {
        color: #A66A00;
        font-weight: bold;
    }

    .cold {
        color: #2864B0;
        font-weight: bold;
    }
    </style>
    """,
    unsafe_allow_html=True
)


# ==============================
# SIDEBAR
# ==============================

st.sidebar.markdown(
    """
    <div style="text-align:center;padding:20px;">
        <div style="font-size:40px;">🏦</div>
        <h2 style="margin:5px;">SMARTBANK</h2>
        <small>CUSTOMER CRM</small>
    </div>
    """,
    unsafe_allow_html=True
)

st.sidebar.divider()

menu = st.sidebar.radio(
    "MENU",
    [
        "Tổng quan",
        "Thêm khách hàng",
        "Danh sách khách hàng",
        "Pipeline",
        "Phân tích"
    ]
)


# ==============================
# HEADER
# ==============================

st.markdown(
    """
    <div class="main-title">
        <h1>SMARTBANK CRM</h1>
        <p>Hệ thống quản lý khách hàng tiềm năng</p>
    </div>
    """,
    unsafe_allow_html=True
)


# =========================================================
# TRANG TỔNG QUAN
# =========================================================

if menu == "Tổng quan":

    customers = st.session_state.customers

    tong_kh = len(customers)

    hot = sum(
        1 for kh in customers
        if kh["Phân loại"] == "HOT"
    )

    warm = sum(
        1 for kh in customers
        if kh["Phân loại"] == "WARM"
    )

    da_chuyen_doi = sum(
        1 for kh in customers
        if kh["Trạng thái"] == "Đã chuyển đổi"
    )

    tong_nhu_cau = sum(
        kh["Nhu cầu tài chính"]
        for kh in customers
    )

    st.subheader("Tổng quan")

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.markdown(
            f"""
            <div class="card">
                <div class="label">TỔNG KHÁCH HÀNG</div>
                <div class="number">{tong_kh}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with c2:
        st.markdown(
            f"""
            <div class="card">
                <div class="label">KHÁCH HÀNG HOT</div>
                <div class="number">{hot}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with c3:
        st.markdown(
            f"""
            <div class="card">
                <div class="label">KHÁCH WARM</div>
                <div class="number">{warm}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with c4:
        st.markdown(
            f"""
            <div class="card">
                <div class="label">ĐÃ CHUYỂN ĐỔI</div>
                <div class="number">{da_chuyen_doi}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.divider()

    st.subheader("Tổng nhu cầu tài chính")

    st.markdown(
        f"""
        <div class="card">
            <div class="label">GIÁ TRỊ NHU CẦU DỰ KIẾN</div>
            <div class="number">
                {tien_vnd(tong_nhu_cau)}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.subheader("Khách hàng ưu tiên")

    hot_customers = [
        kh for kh in customers
        if kh["Phân loại"] == "HOT"
    ]

    hot_customers.sort(
        key=lambda x: x["Điểm tiềm năng"],
        reverse=True
    )

    if not hot_customers:
        st.info("Chưa có khách hàng HOT.")

    else:

        for kh in hot_customers[:5]:

            st.markdown(
                f"""
                <div class="card">

                    <h3>{kh["Tên khách hàng"]}</h3>

                    <p>
                        📱 {kh["Số điện thoại"]}
                        &nbsp;&nbsp; | &nbsp;&nbsp;
                        💳 {kh["Sản phẩm"]}
                    </p>

                    <p>
                        💰 Nhu cầu:
                        <b>{tien_vnd(kh["Nhu cầu tài chính"])}</b>
                    </p>

                    <p>
                        Điểm tiềm năng:
                        <b>{kh["Điểm tiềm năng"]}/100</b>
                        &nbsp;&nbsp;
                        <span class="hot">● HOT</span>
                    </p>

                </div>
                """,
                unsafe_allow_html=True
            )


# =========================================================
# THÊM KHÁCH HÀNG
# =========================================================

elif menu == "Thêm khách hàng":

    st.subheader("Tạo khách hàng tiềm năng")

    with st.form("form_khach_hang"):

        st.markdown("### 01. Thông tin khách hàng")

        col1, col2 = st.columns(2)

        with col1:

            ten = st.text_input(
                "Họ và tên *",
                placeholder="Nguyễn Văn A"
            )

            sdt = st.text_input(
                "Số điện thoại *",
                placeholder="0912345678"
            )

            email = st.text_input(
                "Email",
                placeholder="example@gmail.com"
            )

        with col2:

            tuoi = st.number_input(
                "Tuổi",
                min_value=18,
                max_value=100,
                value=25
            )

            nghe_nghiep = st.text_input(
                "Nghề nghiệp",
                placeholder="Nhân viên văn phòng"
            )

            thu_nhap = st.number_input(
                "Thu nhập hàng tháng (VNĐ)",
                min_value=0,
                value=15_000_000,
                step=1_000_000
            )

        st.divider()

        st.markdown("### 02. Nhu cầu tài chính")

        col1, col2 = st.columns(2)

        with col1:

            san_pham = st.selectbox(
                "Sản phẩm quan tâm",
                [
                    "Vay mua nhà",
                    "Vay mua ô tô",
                    "Vay kinh doanh",
                    "Thẻ tín dụng",
                    "Gửi tiết kiệm",
                    "Tài khoản thanh toán"
                ]
            )

        with col2:

            nhu_cau = st.number_input(
                "Số tiền dự kiến (VNĐ)",
                min_value=0,
                value=500_000_000,
                step=50_000_000
            )

        khu_vuc = st.text_input(
            "Khu vực",
            placeholder="Hà Nội / TP.HCM..."
        )

        ghi_chu = st.text_area(
            "Ghi chú",
            placeholder="Nhu cầu hoặc thông tin thêm..."
        )

        submit = st.form_submit_button(
            "LƯU KHÁCH HÀNG",
            use_container_width=True
        )

    if submit:

        if ten.strip() == "":
            st.error("Vui lòng nhập họ và tên.")

        elif sdt.strip() == "":
            st.error("Vui lòng nhập số điện thoại.")

        else:

            diem, phan_loai = cham_diem(
                thu_nhap,
                san_pham,
                nhu_cau
            )

            khach_hang = {
                "Mã KH": "KH" + datetime.now().strftime(
                    "%Y%m%d%H%M%S"
                ),

                "Ngày tạo": datetime.now().strftime(
                    "%d/%m/%Y %H:%M"
                ),

                "Tên khách hàng": ten.strip(),

                "Số điện thoại": sdt.strip(),

                "Email": email.strip(),

                "Tuổi": tuoi,

                "Nghề nghiệp": nghe_nghiep.strip(),

                "Thu nhập": thu_nhap,

                "Khu vực": khu_vuc.strip(),

                "Sản phẩm": san_pham,

                "Nhu cầu tài chính": nhu_cau,

                "Điểm tiềm năng": diem,

                "Phân loại": phan_loai,

                "Trạng thái": "Mới tiếp nhận",

                "Ghi chú": ghi_chu.strip()
            }

            st.session_state.customers.append(
                khach_hang
            )

            st.success(
                "Đã lưu khách hàng thành công!"
            )

            st.markdown(
                f"""
                <div class="card">

                    <h2>{ten}</h2>

                    <p>
                        Điểm tiềm năng:
                        <b>{diem}/100</b>
                    </p>

                    <p>
                        Phân loại:
                        <b>{phan_loai}</b>
                    </p>

                    <p>
                        Nhu cầu:
                        <b>{tien_vnd(nhu_cau)}</b>
                    </p>

                    <p>
                        Thu nhập:
                        <b>{tien_vnd(thu_nhap)}</b>
                    </p>

                </div>
                """,
                unsafe_allow_html=True
            )


# =========================================================
# DANH SÁCH
# =========================================================

elif menu == "Danh sách khách hàng":

    st.subheader("Danh sách khách hàng")

    customers = st.session_state.customers

    if not customers:

        st.info("Chưa có khách hàng.")

    else:

        df = pd.DataFrame(customers)

        search = st.text_input(
            "Tìm kiếm",
            placeholder="Nhập tên hoặc số điện thoại..."
        )

        level = st.selectbox(
            "Lọc theo phân loại",
            [
                "Tất cả",
                "HOT",
                "WARM",
                "COLD"
            ]
        )

        if search:

            df = df[
                df["Tên khách hàng"].str.contains(
                    search,
                    case=False,
                    na=False
                )
                |
                df["Số điện thoại"].str.contains(
                    search,
                    case=False,
                    na=False
                )
            ]

        if level != "Tất cả":

            df = df[
                df["Phân loại"] == level
            ]

        display_df = df.copy()

        display_df["Thu nhập"] = display_df[
            "Thu nhập"
        ].apply(tien_vnd)

        display_df["Nhu cầu tài chính"] = display_df[
            "Nhu cầu tài chính"
        ].apply(tien_vnd)

        st.dataframe(
            display_df,
            use_container_width=True,
            hide_index=True
        )

        # ==========================
        # XUẤT EXCEL
        # ==========================

        excel_df = df.copy()

        excel_df["Thu nhập"] = excel_df[
            "Thu nhập"
        ].apply(tien_vnd)

        excel_df["Nhu cầu tài chính"] = excel_df[
            "Nhu cầu tài chính"
        ].apply(tien_vnd)

        output = BytesIO()

        with pd.ExcelWriter(
            output,
            engine="openpyxl"
        ) as writer:

            excel_df.to_excel(
                writer,
                index=False,
                sheet_name="Khach_Hang"
            )

        st.download_button(
            "📥 XUẤT FILE EXCEL",
            data=output.getvalue(),
            file_name="SmartBank_CRM.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True
        )


# =========================================================
# PIPELINE
# =========================================================

elif menu == "Pipeline":

    st.subheader("Customer Pipeline")

    customers = st.session_state.customers

    stages = [
        "Mới tiếp nhận",
        "Đã liên hệ",
        "Đang tư vấn",
        "Tiềm năng",
        "Đã chuyển đổi"
    ]

    cols = st.columns(5)

    for col, stage in zip(cols, stages):

        with col:

            st.markdown(
                f"""
                <div class="card" style="text-align:center">

                    <div class="label">
                        {stage}
                    </div>

                    <div class="number">
                        {
                            sum(
                                1
                                for kh in customers
                                if kh["Trạng thái"] == stage
                            )
                        }
                    </div>

                </div>
                """,
                unsafe_allow_html=True
            )


# =========================================================
# PHÂN TÍCH
# =========================================================

elif menu == "Phân tích":

    st.subheader("Phân tích khách hàng")

    customers = st.session_state.customers

    if not customers:

        st.info("Chưa có dữ liệu.")

    else:

        df = pd.DataFrame(customers)

        col1, col2 = st.columns(2)

        with col1:

            st.markdown("### Phân loại khách hàng")

            chart1 = df[
                "Phân loại"
            ].value_counts()

            st.bar_chart(chart1)

        with col2:

            st.markdown("### Sản phẩm quan tâm")

            chart2 = df[
                "Sản phẩm"
            ].value_counts()

            st.bar_chart(chart2)

        st.divider()

        tong_nhu_cau = df[
            "Nhu cầu tài chính"
        ].sum()

        diem_tb = df[
            "Điểm tiềm năng"
        ].mean()

        c1, c2 = st.columns(2)

        with c1:

            st.metric(
                "Tổng nhu cầu tài chính",
                tien_vnd(tong_nhu_cau)
            )

        with c2:

            st.metric(
                "Điểm tiềm năng trung bình",
                f"{diem_tb:.1f}/100"
            )
