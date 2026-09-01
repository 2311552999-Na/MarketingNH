import streamlit as st
import pandas as pd
import sqlite3
from datetime import datetime
from io import BytesIO


# =========================================================
# CONFIG
# =========================================================

st.set_page_config(
    page_title="SmartBank CRM",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded"
)


# =========================================================
# DATABASE
# =========================================================

DB_NAME = "smartbank_crm.db"


def get_connection():
    return sqlite3.connect(DB_NAME, check_same_thread=False)


def init_database():

    conn = get_connection()

    conn.execute("""
        CREATE TABLE IF NOT EXISTS customers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_code TEXT,
            created_at TEXT,
            name TEXT,
            phone TEXT,
            email TEXT,
            gender TEXT,
            age INTEGER,
            occupation TEXT,
            income REAL,
            area TEXT,
            product TEXT,
            expected_amount REAL,
            need_time TEXT,
            score INTEGER,
            classification TEXT,
            status TEXT,
            employee TEXT,
            last_contact TEXT,
            next_contact TEXT,
            note TEXT
        )
    """)

    conn.commit()
    conn.close()


init_database()


# =========================================================
# DATABASE FUNCTIONS
# =========================================================

def load_customers():

    conn = get_connection()

    df = pd.read_sql_query(
        "SELECT * FROM customers ORDER BY id DESC",
        conn
    )

    conn.close()

    return df


def add_customer(data):

    conn = get_connection()

    conn.execute("""
        INSERT INTO customers (
            customer_code,
            created_at,
            name,
            phone,
            email,
            gender,
            age,
            occupation,
            income,
            area,
            product,
            expected_amount,
            need_time,
            score,
            classification,
            status,
            employee,
            last_contact,
            next_contact,
            note
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, tuple(data.values()))

    conn.commit()
    conn.close()


def update_status(customer_id, status):

    conn = get_connection()

    conn.execute(
        "UPDATE customers SET status = ? WHERE id = ?",
        (status, customer_id)
    )

    conn.commit()
    conn.close()


def delete_customer(customer_id):

    conn = get_connection()

    conn.execute(
        "DELETE FROM customers WHERE id = ?",
        (customer_id,)
    )

    conn.commit()
    conn.close()


# =========================================================
# FORMAT TIỀN VIỆT NAM
# =========================================================

def money_vnd(value):

    if pd.isna(value):
        return "0 VNĐ"

    return f"{int(value):,}".replace(",", ".") + " VNĐ"


def money_short(value):

    if pd.isna(value):
        return "0"

    value = float(value)

    if value >= 1_000_000_000:
        return f"{value / 1_000_000_000:.1f} tỷ"

    if value >= 1_000_000:
        return f"{value / 1_000_000:.1f} triệu"

    return money_vnd(value)


# =========================================================
# LEAD SCORING
# =========================================================

def calculate_score(income, product, amount, need_time):

    score = 0

    # THU NHẬP
    if income >= 50_000_000:
        score += 30
    elif income >= 30_000_000:
        score += 25
    elif income >= 15_000_000:
        score += 18
    else:
        score += 10

    # SẢN PHẨM
    if product in ["Vay mua nhà", "Vay kinh doanh"]:
        score += 25

    elif product in ["Vay mua ô tô", "Thẻ tín dụng"]:
        score += 20

    elif product == "Gửi tiết kiệm":
        score += 18

    else:
        score += 10

    # GIÁ TRỊ NHU CẦU
    if amount >= 2_000_000_000:
        score += 25
    elif amount >= 1_000_000_000:
        score += 20
    elif amount >= 500_000_000:
        score += 15
    else:
        score += 8

    # THỜI GIAN
    if need_time == "Trong 1 tháng":
        score += 20

    elif need_time == "1 - 3 tháng":
        score += 15

    elif need_time == "3 - 6 tháng":
        score += 10

    else:
        score += 5

    score = min(score, 100)

    if score >= 80:
        classification = "HOT"

    elif score >= 50:
        classification = "WARM"

    else:
        classification = "COLD"

    return score, classification


# =========================================================
# CSS PREMIUM
# =========================================================

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background: #F6F7F9;
}

/* SIDEBAR */

section[data-testid="stSidebar"] {
    background: #081B33;
    border-right: 1px solid #183452;
}

section[data-testid="stSidebar"] * {
    color: #FFFFFF !important;
}

section[data-testid="stSidebar"] .stRadio label {
    padding: 9px 10px;
    border-radius: 8px;
}

/* HEADER */

.crm-header {
    background: linear-gradient(
        135deg,
        #081B33 0%,
        #0D2D50 100%
    );

    padding: 34px 38px;

    border-radius: 18px;

    margin-bottom: 28px;

    box-shadow:
        0 10px 30px rgba(8, 27, 51, 0.14);
}

.crm-title {
    color: #FFFFFF;
    font-size: 32px;
    font-weight: 800;
    letter-spacing: -1px;
}

.crm-subtitle {
    color: #B8C7D9;
    margin-top: 7px;
    font-size: 14px;
}


/* SECTION */

.section-title {
    font-size: 22px;
    font-weight: 800;
    color: #10243E;
    margin-top: 15px;
    margin-bottom: 18px;
}


/* METRIC CARD */

.metric-card {
    background: #FFFFFF;
    padding: 22px;
    border-radius: 16px;

    border: 1px solid #E8ECF1;

    box-shadow:
        0 5px 18px rgba(16, 36, 62, 0.05);

    min-height: 130px;
}

.metric-label {
    color: #78879A;
    font-size: 13px;
    font-weight: 600;
}

.metric-number {
    color: #10243E;
    font-size: 29px;
    font-weight: 800;
    margin-top: 9px;
}

.metric-description {
    color: #9AA6B5;
    font-size: 12px;
    margin-top: 5px;
}


/* CUSTOMER CARD */

.customer-card {
    background: #FFFFFF;

    padding: 21px;

    border-radius: 15px;

    border: 1px solid #E7EBF0;

    margin-bottom: 12px;

    transition: all 0.2s ease;
}

.customer-card:hover {
    box-shadow: 0 8px 25px rgba(16,36,62,0.09);
    transform: translateY(-1px);
}

.customer-name {
    font-size: 17px;
    font-weight: 750;
    color: #10243E;
}

.customer-info {
    color: #758396;
    font-size: 13px;
    margin-top: 5px;
}


/* SCORE */

.score-box {
    background: #F7F9FC;
    border: 1px solid #E5EAF0;
    border-radius: 13px;
    padding: 14px;
    text-align: center;
}

.score-number {
    font-size: 26px;
    font-weight: 800;
    color: #10243E;
}


/* HOT */

.hot {
    color: #B42318;
    background: #FFF1F0;
    padding: 6px 11px;
    border-radius: 20px;
    font-weight: 700;
    font-size: 12px;
}


/* WARM */

.warm {
    color: #A15C00;
    background: #FFF8E8;
    padding: 6px 11px;
    border-radius: 20px;
    font-weight: 700;
    font-size: 12px;
}


/* COLD */

.cold {
    color: #2457A6;
    background: #EEF5FF;
    padding: 6px 11px;
    border-radius: 20px;
    font-weight: 700;
    font-size: 12px;
}


/* PIPELINE */

.pipeline-card {
    background: #FFFFFF;

    border-radius: 14px;

    padding: 18px;

    border: 1px solid #E5E9EF;

    min-height: 125px;

    text-align: center;
}

.pipeline-title {
    font-size: 13px;
    color: #7C8897;
    font-weight: 600;
}

.pipeline-number {
    font-size: 30px;
    font-weight: 800;
    color: #10243E;
    margin-top: 8px;
}


/* GOLD LINE */

.gold-line {
    width: 45px;
    height: 3px;
    background: #C6A15B;
    border-radius: 10px;
    margin: 10px 0 20px 0;
}


/* FORM */

.form-box {
    background: #FFFFFF;
    padding: 28px;
    border-radius: 17px;
    border: 1px solid #E7EBF0;
    box-shadow: 0 5px 20px rgba(16,36,62,0.04);
}


/* RECOMMENDATION */

.recommendation {
    background: linear-gradient(
        135deg,
        #F8F3E8,
        #FFFDF8
    );

    border: 1px solid #E7D9B8;

    padding: 18px;

    border-radius: 14px;

    color: #4D4029;
}


/* BUTTON */

.stButton > button {
    border-radius: 9px;
    font-weight: 700;
}


/* DATAFRAME */

[data-testid="stDataFrame"] {
    border-radius: 12px;
}


/* DIVIDER */

hr {
    border-color: #E5E9EF;
}

</style>
""", unsafe_allow_html=True)


# =========================================================
# LOAD DATA
# =========================================================

df = load_customers()


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.markdown(
        """
        <div style="
            text-align:center;
            padding:18px 0 25px 0;
        ">

            <div style="
                font-size:38px;
                margin-bottom:8px;
            ">
                🏦
            </div>

            <div style="
                font-size:19px;
                font-weight:800;
                letter-spacing:1px;
            ">
                SMARTBANK
            </div>

            <div style="
                color:#9FB2C8;
                font-size:11px;
                margin-top:5px;
                letter-spacing:1px;
            ">
                CUSTOMER INTELLIGENCE
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )

    st.divider()

    menu = st.radio(
        "NAVIGATION",
        [
            "Overview",
            "Customers",
            "New Lead",
            "Pipeline",
            "Analytics",
            "Follow-up"
        ]
    )

    st.divider()

    st.markdown(
        """
        <div style="
            color:#9FB2C8;
            font-size:11px;
            line-height:1.6;
        ">
        SMARTBANK CRM<br>
        Lead Management System<br>
        <br>
        Version 2.0
        </div>
        """,
        unsafe_allow_html=True
    )


# =========================================================
# HEADER
# =========================================================

st.markdown(
    """
    <div class="crm-header">

        <div class="crm-title">
            SMARTBANK CRM
        </div>

        <div class="crm-subtitle">
            Customer Intelligence & Lead Management Platform
        </div>

    </div>
    """,
    unsafe_allow_html=True
)


# =========================================================
# OVERVIEW
# =========================================================

if menu == "Overview":

    total = len(df)

    hot = len(
        df[df["classification"] == "HOT"]
    ) if total else 0

    warm = len(
        df[df["classification"] == "WARM"]
    ) if total else 0

    converted = len(
        df[df["status"] == "Đã chuyển đổi"]
    ) if total else 0

    total_value = (
        df["expected_amount"].sum()
        if total else 0
    )

    st.markdown(
        """
        <div class="section-title">
            Tổng quan khách hàng
        </div>
        """,
        unsafe_allow_html=True
    )

    c1, c2, c3, c4 = st.columns(4)

    with c1:

        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-label">
                    TỔNG KHÁCH HÀNG
                </div>

                <div class="metric-number">
                    {total:,}
                </div>

                <div class="metric-description">
                    Khách hàng tiềm năng
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with c2:

        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-label">
                    LEAD ƯU TIÊN
                </div>

                <div class="metric-number">
                    {hot}
                </div>

                <div class="metric-description">
                    Khách hàng HOT
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with c3:

        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-label">
                    ĐANG CHĂM SÓC
                </div>

                <div class="metric-number">
                    {warm}
                </div>

                <div class="metric-description">
                    Khách hàng WARM
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with c4:

        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-label">
                    GIÁ TRỊ NHU CẦU
                </div>

                <div class="metric-number"
                     style="font-size:24px;">
                    {money_short(total_value)}
                </div>

                <div class="metric-description">
                    Tổng nhu cầu dự kiến
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.write("")

    # PIPELINE

    st.markdown(
        """
        <div class="section-title">
            Customer Pipeline
        </div>
        """,
        unsafe_allow_html=True
    )

    stages = [
        "Mới tiếp nhận",
        "Đã liên hệ",
        "Đang tư vấn",
        "Tiềm năng",
        "Đã chuyển đổi"
    ]

    cols = st.columns(5)

    for col, stage in zip(cols, stages):

        count = (
            len(df[df["status"] == stage])
            if total else 0
        )

        with col:

            st.markdown(
                f"""
                <div class="pipeline-card">

                    <div class="pipeline-title">
                        {stage}
                    </div>

                    <div class="pipeline-number">
                        {count}
                    </div>

                </div>
                """,
                unsafe_allow_html=True
            )

    st.write("")

    # PRIORITY CUSTOMERS

    st.markdown(
        """
        <div class="section-title">
            Khách hàng ưu tiên
        </div>
        """,
        unsafe_allow_html=True
    )

    if df.empty:

        st.info(
            "Chưa có dữ liệu khách hàng."
        )

    else:

        priority = df[
            df["classification"] == "HOT"
        ].sort_values(
            "score",
            ascending=False
        ).head(5)

        if priority.empty:

            st.info(
                "Hiện chưa có khách hàng HOT."
            )

        else:

            for _, row in priority.iterrows():

                st.markdown(
                    f"""
                    <div class="customer-card">

                        <div style="
                            display:flex;
                            justify-content:space-between;
                            align-items:center;
                        ">

                            <div>

                                <div class="customer-name">
                                    {row['name']}
                                </div>

                                <div class="customer-info">
                                    {row['phone']}
                                    &nbsp; · &nbsp;
                                    {row['product']}
                                </div>

                            </div>

                            <div class="score-box">

                                <div class="score-number">
                                    {row['score']}
                                </div>

                                <div class="hot">
                                    HOT
                                </div>

                            </div>

                        </div>

                    </div>
                    """,
                    unsafe_allow_html=True
                )


# =========================================================
# NEW LEAD
# =========================================================

elif menu == "New Lead":

    st.markdown(
        """
        <div class="section-title">
            Tạo khách hàng tiềm năng
        </div>

        <div class="gold-line"></div>
        """,
        unsafe_allow_html=True
    )

    with st.form("new_customer"):

        st.markdown(
            "### Thông tin cá nhân"
        )

        col1, col2, col3 = st.columns(3)

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
                placeholder="customer@email.com"
            )

        with col2:

            gender = st.selectbox(
                "Giới tính",
                ["Nam", "Nữ", "Khác"]
            )

            age = st.number_input(
                "Tuổi",
                min_value=18,
                max_value=100,
                value=25
            )

            occupation = st.text_input(
                "Nghề nghiệp",
                placeholder="Kinh doanh / Nhân viên..."
            )

        with col3:

            income = st.number_input(
                "Thu nhập hàng tháng (VNĐ)",
                min_value=0,
                value=15_000_000,
                step=1_000_000,
                format="%d"
            )

            area = st.text_input(
                "Khu vực",
                placeholder="Hà Nội / TP.HCM..."
            )

            employee = st.text_input(
                "Chuyên viên phụ trách"
            )

        st.divider()

        st.markdown(
            "### Nhu cầu tài chính"
        )

        col1, col2, col3 = st.columns(3)

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

        with col2:

            amount = st.number_input(
                "Nhu cầu tài chính dự kiến (VNĐ)",
                min_value=0,
                value=500_000_000,
                step=50_000_000,
                format="%d"
            )

        with col3:

            need_time = st.selectbox(
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
            placeholder="Thông tin bổ sung về nhu cầu của khách hàng..."
        )

        submitted = st.form_submit_button(
            "TẠO KHÁCH HÀNG",
            use_container_width=True
        )

    if submitted:

        if not name.strip():

            st.error(
                "Vui lòng nhập họ và tên."
            )

        elif not phone.strip():

            st.error(
                "Vui lòng nhập số điện thoại."
            )

        else:

            score, classification = calculate_score(
                income,
                product,
                amount,
                need_time
            )

            code = (
                "KH"
                + datetime.now().strftime(
                    "%y%m%d%H%M%S"
                )
            )

            created = datetime.now().strftime(
                "%d/%m/%Y %H:%M"
            )

            data = {
                "customer_code": code,
                "created_at": created,
                "name": name.strip(),
                "phone": phone.strip(),
                "email": email.strip(),
                "gender": gender,
                "age": age,
                "occupation": occupation.strip(),
                "income": income,
                "area": area.strip(),
                "product": product,
                "expected_amount": amount,
                "need_time": need_time,
                "score": score,
                "classification": classification,
                "status": "Mới tiếp nhận",
                "employee": employee.strip(),
                "last_contact": "",
                "next_contact": "",
                "note": note.strip()
            }

            add_customer(data)

            st.success(
                f"Đã tạo thành công khách hàng {name}."
            )

            if classification == "HOT":

                st.markdown(
                    f"""
                    <div class="recommendation">

                        <b>KHÁCH HÀNG HOT</b>

                        <br><br>

                        Điểm tiềm năng:
                        <b>{score}/100</b>

                        <br><br>

                        Hệ thống khuyến nghị
                        ưu tiên liên hệ khách hàng
                        trong thời gian sớm nhất.

                    </div>
                    """,
                    unsafe_allow_html=True
                )

            elif classification == "WARM":

                st.warning(
                    f"Khách hàng WARM — {score}/100 điểm."
                )

            else:

                st.info(
                    f"Khách hàng COLD — {score}/100 điểm."
                )


# =========================================================
# CUSTOMERS
# =========================================================

elif menu == "Customers":

    st.markdown(
        """
        <div class="section-title">
            Danh sách khách hàng
        </div>
        """,
        unsafe_allow_html=True
    )

    df = load_customers()

    if df.empty:

        st.info(
            "Chưa có khách hàng nào."
        )

    else:

        c1, c2, c3 = st.columns(3)

        with c1:

            keyword = st.text_input(
                "Tìm kiếm",
                placeholder="Tên hoặc số điện thoại..."
            )

        with c2:

            level = st.selectbox(
                "Mức độ",
                [
                    "Tất cả",
                    "HOT",
                    "WARM",
                    "COLD"
                ]
            )

        with c3:

            status = st.selectbox(
                "Trạng thái",
                [
                    "Tất cả",
                    "Mới tiếp nhận",
                    "Đã liên hệ",
                    "Đang tư vấn",
                    "Tiềm năng",
                    "Đã chuyển đổi"
                ]
            )

        filtered = df.copy()

        if keyword:

            filtered = filtered[
                filtered["name"].str.contains(
                    keyword,
                    case=False,
                    na=False
                )
                |
                filtered["phone"].str.contains(
                    keyword,
                    case=False,
                    na=False
                )
            ]

        if level != "Tất cả":

            filtered = filtered[
                filtered["classification"] == level
            ]

        if status != "Tất cả":

            filtered = filtered[
                filtered["status"] == status
            ]

        st.caption(
            f"{len(filtered)} khách hàng"
        )

        display = filtered[
            [
                "customer_code",
                "name",
                "phone",
                "product",
                "income",
                "expected_amount",
                "score",
                "classification",
                "status"
            ]
        ].copy()

        display["income"] = display["income"].apply(
            money_vnd
        )

        display["expected_amount"] = display[
            "expected_amount"
        ].apply(
            money_vnd
        )

        display.columns = [
            "Mã KH",
            "Họ tên",
            "Số điện thoại",
            "Sản phẩm",
            "Thu nhập",
            "Nhu cầu dự kiến",
            "Điểm",
            "Phân loại",
            "Trạng thái"
        ]

        st.dataframe(
            display,
            use_container_width=True,
            hide_index=True
        )

        st.divider()

        if not filtered.empty:

            selected_name = st.selectbox(
                "Xem hồ sơ khách hàng",
                filtered["name"].tolist()
            )

            customer = filtered[
                filtered["name"] == selected_name
            ].iloc[0]

            left, right = st.columns([2, 1])

            with left:

                st.markdown(
                    f"""
                    <div class="customer-card">

                        <div class="customer-name"
                             style="font-size:24px;">
                            {customer['name']}
                        </div>

                        <div class="customer-info">
                            Mã khách hàng:
                            {customer['customer_code']}
                        </div>

                        <br>

                        <b>Thông tin liên hệ</b>

                        <br><br>

                        📱 {customer['phone']}
                        <br>
                        📧 {customer['email']}
                        <br>
                        📍 {customer['area']}
                        <br>
                        💼 {customer['occupation']}

                        <br><br>

                        <b>Thông tin tài chính</b>

                        <br><br>

                        Thu nhập:
                        <b>{money_vnd(customer['income'])}</b>

                        <br>

                        Nhu cầu dự kiến:
                        <b>{money_vnd(customer['expected_amount'])}</b>

                        <br>

                        Sản phẩm:
                        <b>{customer['product']}</b>

                    </div>
                    """,
                    unsafe_allow_html=True
                )

            with right:

                level_class = (
                    "hot"
                    if customer["classification"] == "HOT"
                    else
                    "warm"
                    if customer["classification"] == "WARM"
                    else
                    "cold"
                )

                st.markdown(
                    f"""
                    <div class="score-box">

                        <div class="metric-label">
                            LEAD SCORE
                        </div>

                        <div class="score-number"
                             style="font-size:42px;">
                            {customer['score']}
                        </div>

                        <br>

                        <span class="{level_class}">
                            {customer['classification']}
                        </span>

                        <br><br>

                        <div class="customer-info">
                            Trạng thái
                        </div>

                        <b>
                            {customer['status']}
                        </b>

                    </div>
                    """,
                    unsafe_allow_html=True
                )

                new_status = st.selectbox(
                    "Cập nhật trạng thái",
                    [
                        "Mới tiếp nhận",
                        "Đã liên hệ",
                        "Đang tư vấn",
                        "Tiềm năng",
                        "Đã chuyển đổi"
                    ],
                    index=[
                        "Mới tiếp nhận",
                        "Đã liên hệ",
                        "Đang tư vấn",
                        "Tiềm năng",
                        "Đã chuyển đổi"
                    ].index(
                        customer["status"]
                    )
                )

                if st.button(
                    "Cập nhật trạng thái",
                    use_container_width=True
                ):

                    update_status(
                        int(customer["id"]),
                        new_status
                    )

                    st.success(
                        "Đã cập nhật."
                    )

                    st.rerun()

                if st.button(
                    "Xóa khách hàng",
                    use_container_width=True
                ):

                    delete_customer(
                        int(customer["id"])
                    )

                    st.success(
                        "Đã xóa khách hàng."
                    )

                    st.rerun()


# =========================================================
# PIPELINE
# =========================================================

elif menu == "Pipeline":

    st.markdown(
        """
        <div class="section-title">
            Customer Pipeline
        </div>
        """,
        unsafe_allow_html=True
    )

    df = load_customers()

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

            stage_df = df[
                df["status"] == stage
            ]

            st.markdown(
                f"""
                <div class="pipeline-card">

                    <div class="pipeline-title">
                        {stage}
                    </div>

                    <div class="pipeline-number">
                        {len(stage_df)}
                    </div>

                </div>
                """,
                unsafe_allow_html=True
            )

            st.write("")

            for _, row in stage_df.head(8).iterrows():

                level_class = (
                    "hot"
                    if row["classification"] == "HOT"
                    else
                    "warm"
                    if row["classification"] == "WARM"
                    else
                    "cold"
                )

                st.markdown(
                    f"""
                    <div class="customer-card">

                        <div class="customer-name">
                            {row['name']}
                        </div>

                        <div class="customer-info">
                            {row['product']}
                        </div>

                        <br>

                        <span class="{level_class}">
                            {row['classification']}
                        </span>

                        <br><br>

                        <b>{row['score']}/100</b>

                    </div>
                    """,
                    unsafe_allow_html=True
                )


# =========================================================
# ANALYTICS
# =========================================================

elif menu == "Analytics":

    st.markdown(
        """
        <div class="section-title">
            Phân tích khách hàng
        </div>
        """,
        unsafe_allow_html=True
    )

    df = load_customers()

    if df.empty:

        st.info(
            "Chưa có dữ liệu."
        )

    else:

        c1, c2 = st.columns(2)

        with c1:

            st.markdown(
                "### Phân loại khách hàng"
            )

            chart = (
                df["classification"]
                .value_counts()
            )

            st.bar_chart(chart)

        with c2:

            st.markdown(
                "### Sản phẩm quan tâm"
            )

            chart = (
                df["product"]
                .value_counts()
            )

            st.bar_chart(chart)

        st.divider()

        c1, c2, c3 = st.columns(3)

        avg_score = df["score"].mean()

        total_amount = df[
            "expected_amount"
        ].sum()

        hot_rate = (
            len(
                df[
                    df["classification"] == "HOT"
                ]
            )
            /
            len(df)
            * 100
        )

        with c1:

            st.metric(
                "Điểm tiềm năng trung bình",
                f"{avg_score:.1f}/100"
            )

        with c2:

            st.metric(
                "Tổng nhu cầu dự kiến",
                money_short(total_amount)
            )

        with c3:

            st.metric(
                "Tỷ lệ khách HOT",
                f"{hot_rate:.1f}%"
            )

        st.divider()

        st.markdown(
            "### Giá trị nhu cầu theo sản phẩm"
        )

        product_value = (
            df.groupby("product")[
                "expected_amount"
            ].sum()
        )

        product_value.index.name = None

        st.bar_chart(
            product_value
        )


# =========================================================
# FOLLOW-UP
# =========================================================

elif menu == "Follow-up":

    st.markdown(
        """
        <div class="section-title">
            Khách hàng cần chăm sóc
        </div>
        """,
        unsafe_allow_html=True
    )

    df = load_customers()

    if df.empty:

        st.info(
            "Chưa có khách hàng."
        )

    else:

        priority = df[
            df["classification"].isin(
                ["HOT", "WARM"]
            )
        ].sort_values(
            "score",
            ascending=False
        )

        if priority.empty:

            st.success(
                "Hiện không có khách hàng cần ưu tiên."
            )

        else:

            for _, row in priority.iterrows():

                level_class = (
                    "hot"
                    if row["classification"] == "HOT"
                    else
                    "warm"
                )

                st.markdown(
                    f"""
                    <div class="customer-card">

                        <div style="
                            display:flex;
                            justify-content:space-between;
                        ">

                            <div>

                                <div class="customer-name">
                                    {row['name']}
                                </div>

                                <div class="customer-info">
                                    📱 {row['phone']}
                                    <br>
                                    💳 {row['product']}
                                    <br>
                                    💰 Nhu cầu:
                                    {money_vnd(row['expected_amount'])}
                                </div>

                            </div>

                            <div style="
                                text-align:right;
                            ">

                                <span class="{level_class}">
                                    {row['classification']}
                                </span>

                                <br><br>

                                <b>
                                    {row['score']}/100
                                </b>

                            </div>

                        </div>

                    </div>
                    """,
                    unsafe_allow_html=True
                )


# =========================================================
# EXPORT EXCEL
# =========================================================

st.sidebar.divider()

df_export = load_customers()

if not df_export.empty:

    export_df = df_export.copy()

    export_df["income"] = export_df[
        "income"
    ].apply(money_vnd)

    export_df["expected_amount"] = export_df[
        "expected_amount"
    ].apply(money_vnd)

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

    st.sidebar.download_button(
        "Xuất dữ liệu Excel",
        data=output.getvalue(),
        file_name="SmartBank_CRM.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        use_container_width=True
    )
