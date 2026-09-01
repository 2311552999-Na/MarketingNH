from datetime import date, datetime
from io import BytesIO
import sqlite3
import pandas as pd
import streamlit as st

# =========================================================
# 1. CẤU HÌNH TRANG STREAMLIT
# =========================================================

st.set_page_config(
    page_title="MB Bank Lead Manager",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded",
)


# =========================================================
# 2. GIAO DIỆN (CSS CUSTOM STYLES)
# =========================================================

st.markdown(
    """
<style>
.main {
    background-color: #f5f7fb;
}

.block-container {
    padding-top: 1.5rem;
    padding-bottom: 2rem;
}

[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #071b3a 0%, #0d2b5c 100%);
}

[data-testid="stSidebar"] * {
    color: white !important;
}

.crm-header {
    background: linear-gradient(135deg, #0b3d91, #1261c9);
    padding: 28px 32px;
    border-radius: 18px;
    color: white;
    margin-bottom: 25px;
    box-shadow: 0 8px 25px rgba(0, 60, 140, 0.15);
}

.crm-header h1 {
    margin: 0;
    font-size: 32px;
}

.crm-header p {
    margin-top: 8px;
    opacity: 0.9;
}

.card {
    background: white;
    padding: 22px;
    border-radius: 16px;
    box-shadow: 0 4px 18px rgba(0,0,0,0.06);
    border: 1px solid #edf0f5;
    margin-bottom: 18px;
}

.hot-card {
    background: linear-gradient(135deg, #fff1f1, #ffffff);
    border-left: 5px solid #ef4444;
}

.warm-card {
    background: linear-gradient(135deg, #fff9e6, #ffffff);
    border-left: 5px solid #f59e0b;
}

.cold-card {
    background: linear-gradient(135deg, #eef7ff, #ffffff);
    border-left: 5px solid #3b82f6;
}

.score {
    font-size: 32px;
    font-weight: 800;
}

.small-text {
    color: #6b7280;
    font-size: 14px;
}

.section-title {
    font-size: 22px;
    font-weight: 700;
    margin-top: 15px;
    margin-bottom: 15px;
}

.pipeline {
    background: white;
    padding: 18px;
    border-radius: 15px;
    text-align: center;
    border: 1px solid #e8ebf0;
}

.pipeline-number {
    font-size: 28px;
    font-weight: 800;
}

.badge-hot {
    background: #fee2e2;
    color: #b91c1c;
    padding: 5px 10px;
    border-radius: 20px;
    font-weight: 700;
}

.badge-warm {
    background: #fef3c7;
    color: #b45309;
    padding: 5px 10px;
    border-radius: 20px;
    font-weight: 700;
}

.badge-cold {
    background: #dbeafe;
    color: #1d4ed8;
    padding: 5px 10px;
    border-radius: 20px;
    font-weight: 700;
}
</style>
""",
    unsafe_allow_html=True,
)


# =========================================================
# 3. KẾT NỐI CƠ SỞ DỮ LIỆU SQLITE
# =========================================================

DB_NAME = "smart_banking_crm.db"


def get_connection():
    return sqlite3.connect(DB_NAME, check_same_thread=False)


def init_database():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
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
# 4. HÀM XỬ LÝ QUY ĐỔI VÀ ĐỊNH DẠNG TIỀN TỆ DẠNG .000.000 VNĐ
# =========================================================


def format_currency_vnd(amount):
    """Quy đổi tự động số tiền nhập vào (nếu nhỏ hơn 1.000.000 sẽ tự nhân 1.000.000)

    và định dạng bằng dấu chấm phân cách hàng nghìn chuẩn VNĐ.
    """
    if pd.isna(amount) or amount is None:
        return "0 VNĐ"

    try:
        val = float(amount)
        if val < 1000000:
            val = val * 1_000_000
        return f"{int(val):,}".replace(",", ".") + " VNĐ"
    except ValueError:
        return "0 VNĐ"


def load_customers():
    conn = get_connection()
    df = pd.read_sql_query("SELECT * FROM customers ORDER BY id DESC", conn)
    conn.close()
    return df


def add_customer(data):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO customers (
            customer_code, created_at, name, phone, email, gender, age, occupation,
            income, area, product, expected_amount, need_time, score, classification,
            status, employee, last_contact, next_contact, note
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """,
        tuple(data.values()),
    )

    conn.commit()
    conn.close()


def update_status(customer_id, new_status):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE customers SET status = ? WHERE id = ?", (new_status, customer_id)
    )
    conn.commit()
    conn.close()


def delete_customer(customer_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM customers WHERE id = ?", (customer_id,))
    conn.commit()
    conn.close()


# =========================================================
# 5. CHẤM ĐIỂM TIỀM NĂNG (LEAD SCORING)
# =========================================================


def calculate_score(income, product, amount, need_time):
    score = 0

    # Thu nhập (đơn vị triệu)
    if income >= 50:
        score += 30
    elif income >= 30:
        score += 25
    elif income >= 15:
        score += 18
    else:
        score += 10

    # Sản phẩm quan tâm
    if product in ["Vay mua nhà", "Vay kinh doanh"]:
        score += 25
    elif product in ["Vay mua ô tô", "Thẻ tín dụng"]:
        score += 20
    elif product == "Gửi tiết kiệm":
        score += 18
    else:
        score += 10

    # Giá trị nhu cầu (đơn vị triệu)
    if amount >= 2000:
        score += 25
    elif amount >= 1000:
        score += 20
    elif amount >= 500:
        score += 15
    else:
        score += 8

    # Thời gian nhu cầu
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
# 6. KHỞI TẠO DỮ LIỆU
# =========================================================

df = load_customers()


# =========================================================
# 7. THANH MENU BÊN TRÁI (SIDEBAR)
# =========================================================

with st.sidebar:
    st.markdown(
        """
        <div style="text-align:center; padding:20px 0;">
            <div style="font-size:48px;">🏦</div>
            <h2>MB BANK</h2>
            <p style="opacity:0.8;">Lead Manager</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.divider()

    menu = st.radio(
        "MENU CHỨC NĂNG",
        [
            "🏠 Tổng quan",
            "👥 Khách hàng",
            "➕ Thêm khách hàng",
            "🎯 Pipeline",
            "📊 Phân tích",
            "📞 Cần chăm sóc",
        ],
    )

    st.divider()
    st.caption("MB Bank Lead Manager\nPhiên bản 2.0 (Đã fix định dạng tiền VNĐ)")


# =========================================================
# 8. TIÊU ĐỀ TRANG CRM
# =========================================================

st.markdown(
    """
    <div class="crm-header">
        <h1>🏦 MB BANK LEAD MANAGER</h1>
        <p>Hệ thống quản lý và chăm sóc khách hàng tiềm năng Ngân hàng MB</p>
    </div>
    """,
    unsafe_allow_html=True,
)


# =========================================================
# 9. GIAO DIỆN TỪNG CHỨC NĂNG
# =========================================================

# --- A. TRANG TỔNG QUAN ---
if menu == "🏠 Tổng quan":
    total = len(df)
    hot = len(df[df["classification"] == "HOT"]) if total else 0
    warm = len(df[df["classification"] == "WARM"]) if total else 0
    cold = len(df[df["classification"] == "COLD"]) if total else 0

    st.markdown(
        '<div class="section-title">📊 Tổng quan khách hàng</div>',
        unsafe_allow_html=True,
    )

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.metric("👥 Tổng khách hàng", total)
    with c2:
        st.metric("🔥 Khách HOT", hot)
    with c3:
        st.metric("⚡ Khách WARM", warm)
    with c4:
        st.metric("❄️ Khách COLD", cold)

    st.divider()

    # PIPELINE MINI
    st.markdown(
        '<div class="section-title">📌 Pipeline tiến độ</div>',
        unsafe_allow_html=True,
    )
    statuses = [
        "Mới tiếp nhận",
        "Đã liên hệ",
        "Đang tư vấn",
        "Tiềm năng",
        "Đã chuyển đổi",
    ]
    cols = st.columns(5)
    for col, status in zip(cols, statuses):
        count = len(df[df["status"] == status]) if total else 0
        with col:
            st.markdown(
                f"""
                <div class="pipeline">
                    <div class="small-text">{status}</div>
                    <div class="pipeline-number">{count}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.divider()

    # DANH SÁCH HOT LEAD
    st.markdown(
        '<div class="section-title">🔥 Khách hàng ưu tiên xử lý (HOT Lead)</div>',
        unsafe_allow_html=True,
    )
    if total == 0:
        st.info("Chưa có dữ liệu. Vui lòng thêm khách hàng mới.")
    else:
        hot_df = df[df["classification"] == "HOT"].head(5)
        if hot_df.empty:
            st.info("Hiện chưa có khách hàng thuộc nhóm HOT.")
        else:
            for _, row in hot_df.iterrows():
                st.markdown(
                    f"""
                    <div class="card hot-card">
                        <b>🔥 {row['name']}</b>
                        <br>
                        <span class="small-text">{row['product']} · 📱 {row['phone']}</span>
                        <br>
                        <span class="small-text">Nhu cầu: <b>{format_currency_vnd(row['expected_amount'])}</b></span>
                        <br><br>
                        ⭐ Điểm tiềm năng: <b>{row['score']}/100</b>
                        &nbsp;&nbsp; | &nbsp;&nbsp;
                        📌 Trạng thái: <b>{row['status']}</b>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )


# --- B. TRANG THÊM KHÁCH HÀNG ---
elif menu == "➕ Thêm khách hàng":
    st.markdown(
        '<div class="section-title">➕ Tạo hồ sơ khách hàng mới</div>',
        unsafe_allow_html=True,
    )
    st.info(
        "💡 Hệ thống sẽ tự động tính điểm tiềm năng dựa trên thông tin thu nhập, sản phẩm và nhu cầu vay/gửi."
    )

    with st.form("customer_form"):
        col1, col2, col3 = st.columns(3)

        with col1:
            name = st.text_input("👤 Họ và tên *")
            phone = st.text_input("📱 Số điện thoại *")
            email = st.text_input("📧 Email")
            gender = st.selectbox("⚧ Giới tính", ["Nam", "Nữ", "Khác"])

        with col2:
            age = st.number_input(
                "🎂 Tuổi", min_value=18, max_value=100, value=25
            )
            occupation = st.text_input("💼 Nghề nghiệp")
            income = st.number_input(
                "💰 Thu nhập/tháng (Triệu VNĐ)",
                min_value=0.0,
                value=15.0,
                step=1.0,
            )
            area = st.text_input("📍 Khu vực (Quận/Huyện, Tỉnh/TP)")

        with col3:
            product = st.selectbox(
                "💳 Sản phẩm quan tâm",
                [
                    "Vay mua nhà",
                    "Vay mua ô tô",
                    "Vay kinh doanh",
                    "Thẻ tín dụng",
                    "Gửi tiết kiệm",
                    "Tài khoản thanh toán",
                ],
            )
            amount = st.number_input(
                "💵 Nhu cầu dự kiến (Triệu VNĐ)",
                min_value=0.0,
                value=500.0,
                step=50.0,
            )
            need_time = st.selectbox(
                "📅 Thời gian dự kiến",
                [
                    "Trong 1 tháng",
                    "1 - 3 tháng",
                    "3 - 6 tháng",
                    "Trên 6 tháng",
                ],
            )
            employee = st.text_input("👨‍💼 Nhân viên phụ trách")

        note = st.text_area("📝 Ghi chú chi tiết")
        submitted = st.form_submit_button(
            "🚀 LƯU VÀ PHÂN LOẠI KHÁCH HÀNG", use_container_width=True
        )

    if submitted:
        if name.strip() == "":
            st.error("⚠️ Vui lòng nhập Họ tên khách hàng.")
        elif phone.strip() == "":
            st.error("⚠️ Vui lòng nhập Số điện thoại khách hàng.")
        else:
            score, classification = calculate_score(
                income, product, amount, need_time
            )
            code = "KH" + datetime.now().strftime("%y%m%d%H%M%S")
            created = datetime.now().strftime("%Y-%m-%d %H:%M")

            data = {
                "customer_code": code,
                "created_at": created,
                "name": name,
                "phone": phone,
                "email": email,
                "gender": gender,
                "age": age,
                "occupation": occupation,
                "income": income,
                "area": area,
                "product": product,
                "expected_amount": amount,
                "need_time": need_time,
                "score": score,
                "classification": classification,
                "status": "Mới tiếp nhận",
                "employee": employee,
                "last_contact": "",
                "next_contact": "",
                "note": note,
            }

            add_customer(data)

            st.success(f"🎉 Đã tạo thành công khách hàng {name}!")

            if classification == "HOT":
                st.error(f"🔥 KHÁCH HÀNG HOT — Điểm đánh giá: {score}/100")
            elif classification == "WARM":
                st.warning(f"⚡ KHÁCH HÀNG WARM — Điểm đánh giá: {score}/100")
            else:
                st.info(f"❄️ KHÁCH HÀNG COLD — Điểm đánh giá: {score}/100")

            st.balloons()


# --- C. TRANG QUẢN LÝ DANH SÁCH KHÁCH HÀNG ---
elif menu == "👥 Khách hàng":
    st.markdown(
        '<div class="section-title">👥 Danh sách khách hàng</div>',
        unsafe_allow_html=True,
    )

    df = load_customers()

    if df.empty:
        st.info("Chưa có thông tin khách hàng nào.")
    else:
        # BỘ LỌC DỮ LIỆU
        col1, col2, col3 = st.columns(3)
        with col1:
            keyword = st.text_input(
                "🔎 Tìm kiếm", placeholder="Nhập Họ tên hoặc SĐT..."
            )
        with col2:
            classification_filter = st.selectbox(
                "🎯 Phân loại Lead", ["Tất cả", "HOT", "WARM", "COLD"]
            )
        with col3:
            status_filter = st.selectbox(
                "📌 Trạng thái",
                [
                    "Tất cả",
                    "Mới tiếp nhận",
                    "Đã liên hệ",
                    "Đang tư vấn",
                    "Tiềm năng",
                    "Đã chuyển đổi",
                ],
            )

        filtered = df.copy()

        if keyword:
            filtered = filtered[
                filtered["name"].str.contains(keyword, case=False, na=False)
                | filtered["phone"].str.contains(keyword, case=False, na=False)
            ]

        if classification_filter != "Tất cả":
            filtered = filtered[
                filtered["classification"] == classification_filter
            ]

        if status_filter != "Tất cả":
            filtered = filtered[filtered["status"] == status_filter]

        st.write(f"Tìm thấy **{len(filtered)}** khách hàng phù hợp")

        # BẢNG HIỂN THỊ CHÍNH
        display_df = filtered[
            [
                "customer_code",
                "name",
                "phone",
                "product",
                "income",
                "expected_amount",
                "score",
                "classification",
                "status",
            ]
        ].copy()

        display_df["income"] = display_df["income"].apply(format_currency_vnd)
        display_df["expected_amount"] = display_df["expected_amount"].apply(
            format_currency_vnd
        )

        display_df.columns = [
            "Mã KH",
            "Họ và Tên",
            "Số điện thoại",
            "Sản phẩm",
            "Thu nhập",
            "Nhu cầu",
            "Điểm",
            "Phân loại",
            "Trạng thái",
        ]

        st.dataframe(
            display_df, use_container_width=True, hide_index=True
        )

        st.divider()

        # XEM HỒ SƠ CHI TIẾT & CẬP NHẬT TRẠNG THÁI
        st.markdown("### 👤 Chi tiết hồ sơ & Thao tác")

        customer_options = filtered["name"].tolist()

        if customer_options:
            selected_name = st.selectbox(
                "Chọn khách hàng để xem", customer_options
            )
            selected = filtered[filtered["name"] == selected_name].iloc[0]

            col1, col2 = st.columns([2, 1])

            with col1:
                st.markdown(
                    f"""
                    <div class="card">
                        <h2>👤 {selected['name']}</h2>
                        <p>🆔 Mã KH: <b>{selected['customer_code']}</b></p>
                        <p>📱 Điện thoại: <b>{selected['phone']}</b></p>
                        <p>📧 Email: <b>{selected['email']}</b></p>
                        <p>📍 Địa chỉ/Khu vực: <b>{selected['area']}</b></p>
                        <p>💼 Nghề nghiệp: <b>{selected['occupation']}</b></p>
                        <hr>
                        <p>💰 Thu nhập: <b>{format_currency_vnd(selected['income'])} / tháng</b></p>
                        <p>💳 Sản phẩm quan tâm: <b>{selected['product']}</b></p>
                        <p>💵 Nhu cầu dự kiến: <b>{format_currency_vnd(selected['expected_amount'])}</b></p>
                        <p>📅 Thời gian dự kiến: <b>{selected['need_time']}</b></p>
                        <p>📝 Ghi chú: {selected['note']}</p>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

            with col2:
                st.markdown(
                    f"""
                    <div class="card">
                        <div class="small-text">ĐIỂM TIỀM NĂNG</div>
                        <div class="score">⭐ {selected['score']}/100</div>
                        <br>
                        Phân loại: <b>{selected['classification']}</b>
                        <br><br>
                        <div class="small-text">Trạng thái hiện tại</div>
                        📌 <b>{selected['status']}</b>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

                new_status = st.selectbox(
                    "🔄 Cập nhật trạng thái mới",
                    [
                        "Mới tiếp nhận",
                        "Đã liên hệ",
                        "Đang tư vấn",
                        "Tiềm năng",
                        "Đã chuyển đổi",
                    ],
                    index=[
                        "Mới tiếp nhận",
                        "Đã liên hệ",
                        "Đang tư vấn",
                        "Tiềm năng",
                        "Đã chuyển đổi",
                    ].index(selected["status"]),
                )

                if st.button("💾 CẬP NHẬT TRẠNG THÁI", use_container_width=True):
                    update_status(int(selected["id"]), new_status)
                    st.success("Đã cập nhật trạng thái thành công!")
                    st.rerun()

                if st.button("🗑️ XÓA KHÁCH HÀNG NÀY", use_container_width=True):
                    delete_customer(int(selected["id"]))
                    st.success("Đã xóa dữ liệu khách hàng!")
                    st.rerun()


# --- D. TRANG PIPELINE KANBAN ---
elif menu == "🎯 Pipeline":
    st.markdown(
        '<div class="section-title">🎯 Quy trình chuyển đổi (Pipeline)</div>',
        unsafe_allow_html=True,
    )

    df = load_customers()

    if df.empty:
        st.info("Chưa có dữ liệu.")
    else:
        stages = [
            "Mới tiếp nhận",
            "Đã liên hệ",
            "Đang tư vấn",
            "Tiềm năng",
            "Đã chuyển đổi",
        ]
        cols = st.columns(5)

        for col, stage in zip(cols, stages):
            stage_df = df[df["status"] == stage]

            with col:
                st.markdown(
                    f"""
                    <div class="pipeline">
                        <div class="small-text">{stage}</div>
                        <div class="pipeline-number">{len(stage_df)}</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

                st.write("")

                for _, row in stage_df.head(10).iterrows():
                    icon = (
                        "🔥"
                        if row["classification"] == "HOT"
                        else ("⚡" if row["classification"] == "WARM" else "❄️")
                    )

                    st.markdown(
                        f"""
                        <div class="card">
                            <b>{icon} {row['name']}</b>
                            <br>
                            <span class="small-text">{row['product']}</span>
                            <br>
                            <span class="small-text">{format_currency_vnd(row['expected_amount'])}</span>
                            <br>
                            ⭐ <b>{row['score']}/100</b>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )


# --- E. TRANG PHÂN TÍCH THỐNG KÊ ---
elif menu == "📊 Phân tích":
    st.markdown(
        '<div class="section-title">📊 Phân tích dữ liệu kinh doanh</div>',
        unsafe_allow_html=True,
    )

    df = load_customers()

    if df.empty:
        st.info("Chưa có dữ liệu để thực hiện phân tích.")
    else:
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("🎯 Tỷ lệ phân loại Lead")
            classification_chart = df["classification"].value_counts()
            st.bar_chart(classification_chart)

        with col2:
            st.subheader("💳 Nhu cầu Sản phẩm Ngân hàng")
            product_chart = df["product"].value_counts()
            st.bar_chart(product_chart)

        st.divider()

        st.subheader("📌 Tiến độ Pipeline chuyển đổi")
        status_chart = df["status"].value_counts()
        st.bar_chart(status_chart)

        st.divider()

        avg_score = df["score"].mean()

        total_value = 0.0
        for val in df["expected_amount"]:
            if pd.notna(val) and val is not None:
                v = float(val)
                total_value += v * 1_000_000 if v < 1000000 else v

        c1, c2, c3 = st.columns(3)
        c1.metric("⭐ Điểm tiềm năng trung bình", f"{avg_score:.1f}/100")
        c2.metric(
            "💰 Tổng nhu cầu dự kiến",
            f"{int(total_value):,}".replace(",", ".") + " VNĐ",
        )
        c3.metric(
            "🔥 Tỷ lệ Lead HOT",
            f"{(len(df[df['classification']=='HOT']) / len(df) * 100):.1f}%",
        )


# --- F. TRANG CẦN CHĂM SÓC (PRIORITY LEADS) ---
elif menu == "📞 Cần chăm sóc":
    st.markdown(
        '<div class="section-title">📞 Danh sách ưu tiên chăm sóc ngay</div>',
        unsafe_allow_html=True,
    )

    df = load_customers()

    if df.empty:
        st.info("Chưa có thông tin khách hàng.")
    else:
        priority_df = df[
            df["classification"].isin(["HOT", "WARM"])
        ].sort_values("score", ascending=False)

        if priority_df.empty:
            st.success("🎉 Tất cả các lead HOT và WARM đã được chăm sóc xong!")
        else:
            for _, row in priority_df.iterrows():
                card_style = (
                    "hot-card"
                    if row["classification"] == "HOT"
                    else "warm-card"
                )
                icon = "🔥" if row["classification"] == "HOT" else "⚡"

                st.markdown(
                    f"""
                    <div class="card {card_style}">
                        <h3>{icon} {row['name']}</h3>
                        <b>⭐ Điểm: {row['score']}/100</b>
                        <br>
                        📱 Điện thoại: <b>{row['phone']}</b>
                        <br>
                        💳 Nhu cầu: <b>{row['product']}</b> ({format_currency_vnd(row['expected_amount'])})
                        <br>
                        📌 Trạng thái: <b>{row['status']}</b>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )


# =========================================================
# 10. CHỨC NĂNG XUẤT EXCEL TRÊN SIDEBAR
# =========================================================

st.sidebar.divider()
df_export = load_customers()

if not df_export.empty:
    output = BytesIO()
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        df_export.to_excel(writer, index=False, sheet_name="Khach_Hang")

    st.sidebar.download_button(
        "📥 Xuất báo cáo Excel",
        data=output.getvalue(),
        file_name="MB_Bank_Lead_Report.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        use_container_width=True,
    )
