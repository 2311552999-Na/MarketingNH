import streamlit as st
import pandas as pd
from datetime import datetime
from io import BytesIO


# =========================================================
# 1. CẤU HÌNH
# =========================================================

st.set_page_config(
    page_title="SmartBank CRM",
    page_icon="🏦",
    layout="wide"
)


# =========================================================
# 2. SESSION DATA
# =========================================================

if "customers" not in st.session_state:
    st.session_state.customers = []

if "admin" not in st.session_state:
    st.session_state.admin = False


# =========================================================
# 3. HÀM FORMAT TIỀN
# =========================================================

def format_money(value):
    try:
        value = int(value)
        return f"{value:,}".replace(",", ".") + " VNĐ"
    except:
        return "0 VNĐ"


# =========================================================
# 4. HÀM CHẤM ĐIỂM KHÁCH HÀNG
# =========================================================

def calculate_score(income, product, amount, urgency):

    score = 0

    # Thu nhập
    if income >= 50_000_000:
        score += 30
    elif income >= 30_000_000:
        score += 25
    elif income >= 15_000_000:
        score += 20
    else:
        score += 10

    # Sản phẩm
    if product in ["Vay mua nhà", "Vay kinh doanh"]:
        score += 25
    elif product in ["Vay mua ô tô", "Thẻ tín dụng"]:
        score += 20
    elif product == "Gửi tiết kiệm":
        score += 15
    else:
        score += 10

    # Giá trị nhu cầu
    if amount >= 2_000_000_000:
        score += 25
    elif amount >= 1_000_000_000:
        score += 20
    elif amount >= 500_000_000:
        score += 15
    else:
        score += 10

    # Mức độ cấp thiết
    if urgency == "Trong 1 tháng":
        score += 20
    elif urgency == "1 - 3 tháng":
        score += 15
    elif urgency == "3 - 6 tháng":
        score += 10
    else:
        score += 5

    if score >= 80:
        level = "HOT"
    elif score >= 50:
        level = "WARM"
    else:
        level = "COLD"

    return score, level


# =========================================================
# 5. CSS GIAO DIỆN
# =========================================================

st.markdown(
    """
    <style>

    /* ===== TOÀN BỘ APP ===== */

    .stApp {
        background-color: #F5F7FA;
    }

    /* ===== SIDEBAR ===== */

    section[data-testid="stSidebar"] {
        background-color: #0B1F3A;
    }

    section[data-testid="stSidebar"] * {
        color: white;
    }

    /* ===== HEADER ===== */

    .header {
        background: linear-gradient(
            135deg,
            #0B1F3A,
            #17395F
        );

        padding: 30px 35px;
        border-radius: 18px;
        margin-bottom: 25px;
    }

    .header-title {
        color: white;
        font-size: 30px;
        font-weight: 800;
        margin-bottom: 5px;
    }

    .header-subtitle {
        color: #B9C7D8;
        font-size: 14px;
    }

    /* ===== SECTION ===== */

    .section-title {
        font-size: 22px;
        font-weight: 800;
        color: #102A43;
        margin-top: 10px;
        margin-bottom: 15px;
    }

    /* ===== CARD ===== */

    .card {
        background: white;
        border-radius: 15px;
        padding: 22px;
        border: 1px solid #E4EAF0;
        box-shadow: 0 5px 18px rgba(16, 42, 67, 0.05);
    }

    /* ===== METRIC ===== */

    .metric {
        background: white;
        border-radius: 15px;
        padding: 22px;
        border: 1px solid #E4EAF0;
        box-shadow: 0 5px 18px rgba(16, 42, 67, 0.05);
    }

    .metric-label {
        color: #7A8899;
        font-size: 12px;
        font-weight: 700;
        text-transform: uppercase;
    }

    .metric-value {
        color: #102A43;
        font-size: 30px;
        font-weight: 800;
        margin-top: 7px;
    }

    .metric-small {
        color: #9AA6B2;
        font-size: 12px;
        margin-top: 4px;
    }

    /* ===== HOT / WARM / COLD ===== */

    .hot {
        display: inline-block;
        background: #FFF0EE;
        color: #C0392B;
        padding: 5px 11px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: 800;
    }

    .warm {
        display: inline-block;
        background: #FFF7E6;
        color: #A86600;
        padding: 5px 11px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: 800;
    }

    .cold {
        display: inline-block;
        background: #EDF4FF;
        color: #2864B0;
        padding: 5px 11px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: 800;
    }

    /* ===== CUSTOMER ===== */

    .customer {
        background: white;
        border-radius: 14px;
        padding: 18px;
        margin-bottom: 12px;
        border: 1px solid #E4EAF0;
    }

    .customer-name {
        color: #102A43;
        font-size: 17px;
        font-weight: 800;
    }

    .customer-info {
        color: #718096;
        font-size: 13px;
        margin-top: 5px;
    }

    /* ===== SCORE ===== */

    .score {
        text-align: center;
        background: #F7F9FC;
        border-radius: 12px;
        padding: 14px;
        border: 1px solid #E5EAF0;
    }

    .score-number {
        color: #102A43;
        font-size: 30px;
        font-weight: 800;
    }

    /* ===== GOLD ===== */

    .gold {
        color: #B18A45;
        font-weight: 800;
    }

    /* ===== BUTTON ===== */

    .stButton button {
        border-radius: 9px;
        font-weight: 700;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# =========================================================
# 6. SIDEBAR
# =========================================================

with st.sidebar:

    st.markdown(
        """
        <div style="text-align:center; padding:20px 0 25px 0;">

            <div style="font-size:38px;">
                🏦
            </div>

            <div style="
                font-size:20px;
                font-weight:800;
                letter-spacing:1px;
            ">
                SMARTBANK
            </div>

            <div style="
                color:#AFC0D4;
                font-size:10px;
                letter-spacing:2px;
                margin-top:5px;
            ">
                CUSTOMER CRM
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )

    st.divider()

    menu = st.radio(
        "MENU",
        [
            "Tổng quan",
            "Thêm khách hàng",
            "Danh sách khách hàng",
            "Pipeline",
            "Phân tích"
        ]
    )

    st.divider()

    st.caption("SmartBank CRM")
    st.caption("Customer Intelligence System")


# =========================================================
# 7. HEADER
# =========================================================

st.markdown(
    """
    <div class="header">

        <div class="header-title">
            SMARTBANK CRM
        </div>

        <div class="header-subtitle">
            Hệ thống quản lý và phân tích khách hàng tiềm năng
        </div>

    </div>
    """,
    unsafe_allow_html=True
)


# =========================================================
# 8. TỔNG QUAN
# =========================================================

if menu == "Tổng quan":

    customers = st.session_state.customers

    total = len(customers)

    hot = sum(
        1 for x in customers
        if x["Phân loại"] == "HOT"
    )

    warm = sum(
        1 for x in customers
        if x["Phân loại"] == "WARM"
    )

    converted = sum(
        1 for x in customers
        if x["Trạng thái"] == "Đã chuyển đổi"
    )

    total_amount = sum(
        x["Nhu cầu tài chính"]
        for x in customers
    )

    st.markdown(
        '<div class="section-title">Tổng quan hoạt động</div>',
        unsafe_allow_html=True
    )

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.markdown(
            f"""
            <div class="metric">

                <div class="metric-label">
                    Tổng khách hàng
                </div>

                <div class="metric-value">
                    {total}
                </div>

                <div class="metric-small">
                    Tổng số lead trong hệ thống
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )

    with c2:
        st.markdown(
            f"""
            <div class="metric">

                <div class="metric-label">
                    Khách hàng HOT
                </div>

                <div class="metric-value">
                    {hot}
                </div>

                <div class="metric-small">
                    Cần ưu tiên chăm sóc
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )

    with c3:
        st.markdown(
            f"""
            <div class="metric">

                <div class="metric-label">
                    Đã chuyển đổi
                </div>

                <div class="metric-value">
                    {converted}
                </div>

                <div class="metric-small">
                    Khách hàng thành công
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )

    with c4:
        st.markdown(
            f"""
            <div class="metric">

                <div class="metric-label">
                    Tổng nhu cầu
                </div>

                <div class="metric-value"
                     style="font-size:22px;">
                    {format_money(total_amount)}
                </div>

                <div class="metric-small">
                    Tổng giá trị tài chính dự kiến
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )

    st.write("")

    # PIPELINE

    st.markdown(
        '<div class="section-title">Customer Pipeline</div>',
        unsafe_allow_html=True
    )

    statuses = [
        "Mới tiếp nhận",
        "Đã liên hệ",
        "Đang tư vấn",
        "Tiềm năng",
        "Đã chuyển đổi"
    ]

    cols = st.columns(5)

    for col, status in zip(cols, statuses):

        count = sum(
            1 for x in customers
            if x["Trạng thái"] == status
        )

        with col:

            st.markdown(
                f"""
                <div class="card"
                     style="text-align:center;">

                    <div style="
                        color:#7A8899;
                        font-size:12px;
                        font-weight:700;
                    ">
                        {status}
                    </div>

                    <div style="
                        color:#102A43;
                        font-size:28px;
                        font-weight:800;
                        margin-top:8px;
                    ">
                        {count}
                    </div>

                </div>
                """,
                unsafe_allow_html=True
            )

    st.write("")

    # KHÁCH HÀNG ƯU TIÊN

    st.markdown(
        '<div class="section-title">Khách hàng ưu tiên</div>',
        unsafe_allow_html=True
    )

    hot_customers = [
        x for x in customers
        if x["Phân loại"] == "HOT"
    ]

    hot_customers = sorted(
        hot_customers,
        key=lambda x: x["Điểm tiềm năng"],
        reverse=True
    )

    if not hot_customers:

        st.info(
            "Chưa có khách hàng HOT trong hệ thống."
        )

    else:

        for customer in hot_customers[:5]:

            st.markdown(
                f"""
                <div class="customer">

                    <div style="
                        display:flex;
                        justify-content:space-between;
                        align-items:center;
                    ">

                        <div>

                            <div class="customer-name">
                                {customer["Tên khách hàng"]}
                            </div>

                            <div class="customer-info">
                                {customer["Số điện thoại"]}
                                &nbsp; • &nbsp;
                                {customer["Sản phẩm"]}
                            </div>

                        </div>

                        <div class="score">

                            <div class="score-number">
                                {customer["Điểm tiềm năng"]}
                            </div>

                            <span class="hot">
                                HOT
                            </span>

                        </div>

                    </div>

                </div>
                """,
                unsafe_allow_html=True
            )


# =========================================================
# 9. THÊM KHÁCH HÀNG
# =========================================================

elif menu == "Thêm khách hàng":

    st.markdown(
        '<div class="section-title">Tạo khách hàng tiềm năng</div>',
        unsafe_allow_html=True
    )

    st.caption(
        "Nhập thông tin để hệ thống tự động đánh giá mức độ tiềm năng."
    )

    st.divider()

    with st.form("customer_form"):

        st.markdown("### Thông tin khách hàng")

        col1, col2 = st.columns(2)

        with col1:

            name = st.text_input(
                "Họ và tên *",
                placeholder="Nguyễn Văn A"
            )

            phone = st.text_input(
                "Số điện thoại *",
                placeholder="0912345678"
            )

            email = st.text_input(
                "Email",
                placeholder="example@gmail.com"
            )

            area = st.text_input(
                "Khu vực",
                placeholder="Quận / Huyện / Tỉnh"
            )

        with col2:

            age = st.number_input(
                "Tuổi",
                min_value=18,
                max_value=100,
                value=25
            )

            occupation = st.text_input(
                "Nghề nghiệp",
                placeholder="Nhân viên / Kinh doanh..."
            )

            income = st.number_input(
                "Thu nhập hàng tháng (VNĐ)",
                min_value=0,
                value=15_000_000,
                step=1_000_000
            )

        st.divider()

        st.markdown("### Nhu cầu tài chính")

        col1, col2 = st.columns(2)

        with col1:

            product = st.selectbox(
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

            amount = st.number_input(
                "Số tiền dự kiến (VNĐ)",
                min_value=0,
                value=500_000_000,
                step=50_000_000
            )

        with col2:

            urgency = st.selectbox(
                "Thời gian có nhu cầu",
                [
                    "Trong 1 tháng",
                    "1 - 3 tháng",
                    "3 - 6 tháng",
                    "Trên 6 tháng"
                ]
            )

            note = st.text_area(
                "Ghi chú",
                placeholder="Thông tin thêm về nhu cầu..."
            )

        st.divider()

        submitted = st.form_submit_button(
            "LƯU KHÁCH HÀNG",
            type="primary",
            use_container_width=True
        )

    if submitted:

        if name.strip() == "":
            st.error("Vui lòng nhập họ và tên.")

        elif phone.strip() == "":
            st.error("Vui lòng nhập số điện thoại.")

        else:

            score, level = calculate_score(
                income,
                product,
                amount,
                urgency
            )

            code = (
                "KH"
                + datetime.now().strftime("%Y%m%d%H%M%S")
            )

            customer = {
                "Mã KH": code,
                "Ngày tạo": datetime.now().strftime(
                    "%d/%m/%Y %H:%M"
                ),
                "Tên khách hàng": name.strip(),
                "Số điện thoại": phone.strip(),
                "Email": email.strip(),
                "Tuổi": age,
                "Nghề nghiệp": occupation.strip(),
                "Thu nhập": income,
                "Khu vực": area.strip(),
                "Sản phẩm": product,
                "Nhu cầu tài chính": amount,
                "Thời gian nhu cầu": urgency,
                "Điểm tiềm năng": score,
                "Phân loại": level,
                "Trạng thái": "Mới tiếp nhận",
                "Ghi chú": note.strip()
            }

            st.session_state.customers.append(customer)

            st.success(
                f"Đã lưu khách hàng {name} thành công."
            )

            st.markdown(
                f"""
                <div class="card">

                    <div style="
                        color:#7A8899;
                        font-size:12px;
                        font-weight:700;
                    ">
                        KẾT QUẢ ĐÁNH GIÁ
                    </div>

                    <br>

                    <div style="
                        font-size:28px;
                        font-weight:800;
                        color:#102A43;
                    ">
                        {name}
                    </div>

                    <br>

                    <b>Điểm tiềm năng:</b>
                    {score}/100

                    <br><br>

                    <b>Mức độ:</b>
                    <span class="{
                        "hot" if level == "HOT"
                        else "warm" if level == "WARM"
                        else "cold"
                    }">
                        {level}
                    </span>

                    <br><br>

                    <b>Nhu cầu tài chính:</b>
                    {format_money(amount)}

                </div>
                """,
                unsafe_allow_html=True
            )


# =========================================================
# 10. DANH SÁCH KHÁCH HÀNG
# =========================================================

elif menu == "Danh sách khách hàng":

    st.markdown(
        '<div class="section-title">Danh sách khách hàng</div>',
        unsafe_allow_html=True
    )

    customers = st.session_state.customers

    if not customers:

        st.info(
            "Chưa có dữ liệu khách hàng. Hãy tạo khách hàng đầu tiên."
        )

    else:

        df = pd.DataFrame(customers)

        col1, col2 = st.columns(2)

        with col1:

            keyword = st.text_input(
                "Tìm kiếm",
                placeholder="Nhập tên hoặc số điện thoại..."
            )

        with col2:

            filter_level = st.selectbox(
                "Phân loại",
                [
                    "Tất cả",
                    "HOT",
                    "WARM",
                    "COLD"
                ]
            )

        filtered = df.copy()

        if keyword:

            filtered = filtered[
                filtered["Tên khách hàng"].str.contains(
                    keyword,
                    case=False,
                    na=False
                )
                |
                filtered["Số điện thoại"].str.contains(
                    keyword,
                    case=False,
                    na=False
                )
            ]

        if filter_level != "Tất cả":

            filtered = filtered[
                filtered["Phân loại"] == filter_level
            ]

        display_df = filtered[
            [
                "Mã KH",
                "Tên khách hàng",
                "Số điện thoại",
                "Sản phẩm",
                "Thu nhập",
                "Nhu cầu tài chính",
                "Điểm tiềm năng",
                "Phân loại",
                "Trạng thái"
            ]
        ].copy()

        display_df["Thu nhập"] = display_df[
            "Thu nhập"
        ].apply(format_money)

        display_df["Nhu cầu tài chính"] = display_df[
            "Nhu cầu tài chính"
        ].apply(format_money)

        display_df.columns = [
            "Mã KH",
            "Khách hàng",
            "Số điện thoại",
            "Sản phẩm",
            "Thu nhập",
            "Nhu cầu",
            "Điểm",
            "Phân loại",
            "Trạng thái"
        ]

        st.dataframe(
            display_df,
            use_container_width=True,
            hide_index=True
        )

        st.caption(
            f"Hiển thị {len(display_df)} khách hàng"
        )

        st.divider()

        # XUẤT EXCEL

        export_df = df.copy()

        export_df["Thu nhập"] = export_df[
            "Thu nhập"
        ].apply(format_money)

        export_df["Nhu cầu tài chính"] = export_df[
            "Nhu cầu tài chính"
        ].apply(format_money)

        output = BytesIO()

        with pd.ExcelWriter(
            output,
            engine="openpyxl"
        ) as writer:

            export_df.to_excel(
                writer,
                index=False,
                sheet_name="Khach_Hang"
            )

        st.download_button(
            "XUẤT DỮ LIỆU EXCEL",
            data=output.getvalue(),
            file_name="SmartBank_CRM.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True
        )


# =========================================================
# 11. PIPELINE
# =========================================================

elif menu == "Pipeline":

    st.markdown(
        '<div class="section-title">Customer Pipeline</div>',
        unsafe_allow_html=True
    )

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
                <div class="card"
                     style="text-align:center;">

                    <div style="
                        font-size:13px;
                        font-weight:700;
                        color:#718096;
                    ">
                        {stage}
                    </div>

                    <div style="
                        font-size:30px;
                        font-weight:800;
                        color:#102A43;
                        margin-top:8px;
                    ">
                        {
                            sum(
                                1 for x in customers
                                if x["Trạng thái"] == stage
                            )
                        }
                    </div>

                </div>
                """,
                unsafe_allow_html=True
            )

            st.write("")

            stage_customers = [
                x for x in customers
                if x["Trạng thái"] == stage
            ]

            for customer in stage_customers:

                level = customer["Phân loại"]

                css_class = (
                    "hot"
                    if level == "HOT"
                    else "warm"
                    if level == "WARM"
                    else "cold"
                )

                st.markdown(
                    f"""
                    <div class="customer">

                        <div class="customer-name">
                            {customer["Tên khách hàng"]}
                        </div>

                        <div class="customer-info">
                            {customer["Sản phẩm"]}
                        </div>

                        <br>

                        <span class="{css_class}">
                            {level}
                        </span>

                        <br><br>

                        <b>
                            {customer["Điểm tiềm năng"]}/100
                        </b>

                        <br><br>

                        <span style="
                            color:#718096;
                            font-size:12px;
                        ">
                            {format_money(
                                customer["Nhu cầu tài chính"]
                            )}
                        </span>

                    </div>
                    """,
                    unsafe_allow_html=True
                )


# =========================================================
# 12. PHÂN TÍCH
# =========================================================

elif menu == "Phân tích":

    st.markdown(
        '<div class="section-title">Phân tích khách hàng</div>',
        unsafe_allow_html=True
    )

    customers = st.session_state.customers

    if not customers:

        st.info("Chưa có dữ liệu để phân tích.")

    else:

        df = pd.DataFrame(customers)

        col1, col2 = st.columns(2)

        with col1:

            st.markdown("### Phân loại khách hàng")

            chart = df[
                "Phân loại"
            ].value_counts()

            st.bar_chart(chart)

        with col2:

            st.markdown("### Sản phẩm được quan tâm")

            chart = df[
                "Sản phẩm"
            ].value_counts()

            st.bar_chart(chart)

        st.divider()

        total_money = df[
            "Nhu cầu tài chính"
        ].sum()

        avg_score = df[
            "Điểm tiềm năng"
        ].mean()

        hot_rate = (
            len(
                df[
                    df["Phân loại"] == "HOT"
                ]
            )
            / len(df)
            * 100
        )

        c1, c2, c3 = st.columns(3)

        with c1:

            st.markdown(
                f"""
                <div class="metric">

                    <div class="metric-label">
                        Tổng nhu cầu tài chính
                    </div>

                    <div class="metric-value"
                         style="font-size:23px;">
                        {format_money(total_money)}
                    </div>

                </div>
                """,
                unsafe_allow_html=True
            )

        with c2:

            st.markdown(
                f"""
                <div class="metric">

                    <div class="metric-label">
                        Điểm trung bình
                    </div>

                    <div class="metric-value">
                        {avg_score:.1f}
                    </div>

                    <div class="metric-small">
                        Trên thang điểm 100
                    </div>

                </div>
                """,
                unsafe_allow_html=True
            )

        with c3:

            st.markdown(
                f"""
                <div class="metric">

                    <div class="metric-label">
                        Tỷ lệ HOT
                    </div>

                    <div class="metric-value">
                        {hot_rate:.1f}%
                    </div>

                </div>
                """,
                unsafe_allow_html=True
            )
