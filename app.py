import streamlit as st
import pandas as pd
from io import BytesIO
from datetime import datetime
import uuid


# =========================================================
# CẤU HÌNH
# =========================================================

st.set_page_config(
    page_title="CRM - Quản lý khách hàng",
    page_icon="👥",
    layout="wide"
)


# =========================================================
# CSS GIAO DIỆN
# =========================================================

st.markdown("""
<style>

.main-title {
    font-size: 38px;
    font-weight: 700;
    margin-bottom: 5px;
}

.sub-title {
    color: #666;
    font-size: 17px;
    margin-bottom: 25px;
}

.card {
    padding: 20px;
    border-radius: 15px;
    background-color: #f7f9fc;
    border: 1px solid #e5e7eb;
    margin-bottom: 15px;
}

.status {
    padding: 5px 10px;
    border-radius: 20px;
    font-weight: 600;
}

</style>
""", unsafe_allow_html=True)


# =========================================================
# KHỞI TẠO SESSION
# =========================================================

if "customers" not in st.session_state:
    st.session_state.customers = []

if "admin_logged_in" not in st.session_state:
    st.session_state.admin_logged_in = False


# =========================================================
# HÀM XUẤT EXCEL
# =========================================================

def export_excel():

    df = pd.DataFrame(st.session_state.customers)

    if not df.empty:
        df = df.drop(columns=["ID"], errors="ignore")

    output = BytesIO()

    with pd.ExcelWriter(
        output,
        engine="openpyxl"
    ) as writer:

        df.to_excel(
            writer,
            index=False,
            sheet_name="Khách hàng"
        )

    return output.getvalue()


# =========================================================
# HÀM THÊM KHÁCH HÀNG
# =========================================================

def add_customer(
    phone,
    name,
    address,
    gender,
    customer_type,
    priority,
    note
):

    customer = {

        "ID": str(uuid.uuid4()),

        "Số điện thoại": phone.strip(),

        "Tên khách hàng": name.strip(),

        "Giới tính": gender,

        "Địa chỉ": address.strip(),

        "Phân loại": customer_type,

        "Mức độ ưu tiên": priority,

        "Ngày nhập": datetime.now().strftime("%d/%m/%Y %H:%M"),

        "Ghi chú": note.strip()
    }

    st.session_state.customers.append(customer)


# =========================================================
# SIDEBAR
# =========================================================

st.sidebar.title("👥 MINI CRM")

st.sidebar.caption(
    "Hệ thống quản lý khách hàng"
)

st.sidebar.divider()

page = st.sidebar.radio(
    "📋 Chức năng",
    [
        "🏠 Tổng quan",
        "👤 Thêm khách hàng",
        "🔎 Tra cứu khách hàng",
        "🔐 Admin"
    ]
)

st.sidebar.divider()

st.sidebar.info(
    f"👥 Khách hàng hiện có: "
    f"{len(st.session_state.customers)}"
)


# =========================================================
# TRANG TỔNG QUAN
# =========================================================

if page == "🏠 Tổng quan":

    st.markdown(
        '<div class="main-title">👥 MINI CRM</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="sub-title">'
        'Hệ thống quản lý và chăm sóc khách hàng'
        '</div>',
        unsafe_allow_html=True
    )

    customers = st.session_state.customers

    total = len(customers)

    potential = sum(
        x["Phân loại"] == "Tiềm năng"
        for x in customers
    )

    caring = sum(
        x["Phân loại"] == "Đang chăm sóc"
        for x in customers
    )

    traded = sum(
        x["Phân loại"] == "Đã giao dịch"
        for x in customers
    )


    # -----------------------------------------------------
    # METRIC
    # -----------------------------------------------------

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "👥 Tổng khách hàng",
        total
    )

    col2.metric(
        "🔥 Tiềm năng",
        potential
    )

    col3.metric(
        "💬 Đang chăm sóc",
        caring
    )

    col4.metric(
        "💰 Đã giao dịch",
        traded
    )


    st.divider()


    # -----------------------------------------------------
    # BIỂU ĐỒ
    # -----------------------------------------------------

    if total > 0:

        df = pd.DataFrame(customers)

        col1, col2 = st.columns(2)

        with col1:

            st.subheader(
                "📊 Khách hàng theo trạng thái"
            )

            status_data = (
                df["Phân loại"]
                .value_counts()
            )

            st.bar_chart(status_data)


        with col2:

            st.subheader(
                "⭐ Mức độ ưu tiên"
            )

            priority_data = (
                df["Mức độ ưu tiên"]
                .value_counts()
            )

            st.bar_chart(priority_data)


    else:

        st.info(
            "📭 Chưa có dữ liệu khách hàng. "
            "Hãy thêm khách hàng đầu tiên!"
        )


# =========================================================
# TRANG THÊM KHÁCH HÀNG
# =========================================================

elif page == "👤 Thêm khách hàng":

    st.markdown(
        '<div class="main-title">'
        '👤 THÊM KHÁCH HÀNG'
        '</div>',
        unsafe_allow_html=True
    )

    st.write(
        "Nhập thông tin để tạo hồ sơ khách hàng mới."
    )

    st.divider()


    # -----------------------------------------------------
    # THÔNG TIN CƠ BẢN
    # -----------------------------------------------------

    st.subheader("📋 Thông tin cơ bản")

    col1, col2 = st.columns(2)

    with col1:

        name = st.text_input(
            "👤 Tên khách hàng *",
            placeholder="Nguyễn Văn A"
        )

        phone = st.text_input(
            "📱 Số điện thoại *",
            placeholder="09xxxxxxxx"
        )

        gender = st.selectbox(
            "⚥ Giới tính",
            [
                "Nam",
                "Nữ",
                "Khác"
            ]
        )

    with col2:

        address = st.text_input(
            "📍 Địa chỉ",
            placeholder="Nhập địa chỉ khách hàng"
        )

        customer_type = st.selectbox(
            "🏷️ Phân loại khách hàng",
            [
                "Tiềm năng",
                "Đang chăm sóc",
                "Đã giao dịch"
            ]
        )

        priority = st.selectbox(
            "⭐ Mức độ ưu tiên",
            [
                "Cao",
                "Trung bình",
                "Thấp"
            ]
        )


    st.divider()


    # -----------------------------------------------------
    # GHI CHÚ
    # -----------------------------------------------------

    st.subheader("📝 Thông tin chăm sóc")

    note = st.text_area(
        "Ghi chú",
        placeholder=(
            "Ví dụ: "
            "Khách hàng quan tâm đến sản phẩm vay mua nhà..."
        ),
        height=120
    )


    st.divider()


    # -----------------------------------------------------
    # LƯU
    # -----------------------------------------------------

    if st.button(
        "💾 LƯU KHÁCH HÀNG",
        type="primary",
        use_container_width=True
    ):

        if name.strip() == "":
            st.error(
                "❌ Vui lòng nhập tên khách hàng."
            )

        elif phone.strip() == "":
            st.error(
                "❌ Vui lòng nhập số điện thoại."
            )

        elif not phone.isdigit():
            st.error(
                "❌ Số điện thoại chỉ được chứa chữ số."
            )

        else:

            # Kiểm tra trùng số điện thoại

            duplicate = any(
                c["Số điện thoại"] == phone.strip()
                for c in st.session_state.customers
            )

            if duplicate:

                st.warning(
                    "⚠️ Số điện thoại này đã tồn tại."
                )

            else:

                add_customer(
                    phone,
                    name,
                    address,
                    gender,
                    customer_type,
                    priority,
                    note
                )

                st.success(
                    "🎉 Đã thêm khách hàng thành công!"
                )


# =========================================================
# TRA CỨU KHÁCH HÀNG
# =========================================================

elif page == "🔎 Tra cứu khách hàng":

    st.markdown(
        '<div class="main-title">'
        '🔎 TRA CỨU KHÁCH HÀNG'
        '</div>',
        unsafe_allow_html=True
    )

    st.write(
        "Tìm kiếm nhanh khách hàng theo tên hoặc số điện thoại."
    )

    st.divider()


    if len(st.session_state.customers) == 0:

        st.info(
            "📭 Chưa có khách hàng."
        )

    else:

        df = pd.DataFrame(
            st.session_state.customers
        )


        # -------------------------------------------------
        # TÌM KIẾM
        # -------------------------------------------------

        keyword = st.text_input(
            "🔎 Tìm kiếm",
            placeholder="Nhập tên hoặc số điện thoại..."
        )


        # -------------------------------------------------
        # BỘ LỌC
        # -------------------------------------------------

        col1, col2 = st.columns(2)

        with col1:

            filter_type = st.selectbox(
                "🏷️ Phân loại",
                [
                    "Tất cả",
                    "Tiềm năng",
                    "Đang chăm sóc",
                    "Đã giao dịch"
                ]
            )

        with col2:

            filter_priority = st.selectbox(
                "⭐ Ưu tiên",
                [
                    "Tất cả",
                    "Cao",
                    "Trung bình",
                    "Thấp"
                ]
            )


        result = df.copy()


        # Tìm kiếm

        if keyword.strip() != "":

            mask = (

                result["Tên khách hàng"]
                .str.contains(
                    keyword,
                    case=False,
                    na=False
                )

                |

                result["Số điện thoại"]
                .str.contains(
                    keyword,
                    case=False,
                    na=False
                )
            )

            result = result[mask]


        # Lọc loại

        if filter_type != "Tất cả":

            result = result[
                result["Phân loại"] == filter_type
            ]


        # Lọc ưu tiên

        if filter_priority != "Tất cả":

            result = result[
                result["Mức độ ưu tiên"] == filter_priority
            ]


        st.divider()


        st.subheader(
            f"📋 Kết quả: {len(result)} khách hàng"
        )


        if len(result) == 0:

            st.warning(
                "Không tìm thấy khách hàng phù hợp."
            )

        else:

            st.dataframe(
                result.drop(
                    columns=["ID"],
                    errors="ignore"
                ),
                use_container_width=True,
                hide_index=True
            )


# =========================================================
# TRANG ADMIN
# =========================================================

elif page == "🔐 Admin":

    st.title("🔐 QUẢN TRỊ HỆ THỐNG")

    st.divider()


    # =====================================================
    # LOGIN
    # =====================================================

    if not st.session_state.admin_logged_in:

        st.subheader(
            "🔑 Đăng nhập Admin"
        )

        password = st.text_input(
            "Mật khẩu",
            type="password"
        )


        if st.button(
            "🔐 ĐĂNG NHẬP",
            type="primary"
        ):

            if password == "123456":

                st.session_state.admin_logged_in = True

                st.success(
                    "✅ Đăng nhập thành công!"
                )

                st.rerun()

            else:

                st.error(
                    "❌ Mật khẩu không chính xác."
                )


    # =====================================================
    # ADMIN
    # =====================================================

    else:

        col1, col2 = st.columns([5, 1])

        with col1:

            st.subheader(
                "📊 QUẢN LÝ KHÁCH HÀNG"
            )

        with col2:

            if st.button(
                "🚪 Đăng xuất"
            ):

                st.session_state.admin_logged_in = False

                st.rerun()


        st.divider()


        if len(st.session_state.customers) == 0:

            st.info(
                "📭 Chưa có dữ liệu khách hàng."
            )

        else:

            df = pd.DataFrame(
                st.session_state.customers
            )


            # -------------------------------------------------
            # THỐNG KÊ
            # -------------------------------------------------

            col1, col2, col3 = st.columns(3)

            col1.metric(
                "👥 Tổng khách hàng",
                len(df)
            )

            col2.metric(
                "🔥 Khách tiềm năng",
                len(
                    df[
                        df["Phân loại"]
                        == "Tiềm năng"
                    ]
                )
            )

            col3.metric(
                "⭐ Ưu tiên cao",
                len(
                    df[
                        df["Mức độ ưu tiên"]
                        == "Cao"
                    ]
                )
            )


            st.divider()


            # -------------------------------------------------
            # DANH SÁCH
            # -------------------------------------------------

            st.subheader(
                "📋 Danh sách khách hàng"
            )

            st.dataframe(
                df.drop(
                    columns=["ID"],
                    errors="ignore"
                ),
                use_container_width=True,
                hide_index=True
            )


            st.divider()


            # -------------------------------------------------
            # XÓA KHÁCH HÀNG
            # -------------------------------------------------

            st.subheader(
                "🗑️ Xóa khách hàng"
            )

            customer_names = [
                f'{c["Tên khách hàng"]} - '
                f'{c["Số điện thoại"]}'
                for c in st.session_state.customers
            ]


            selected = st.selectbox(
                "Chọn khách hàng cần xóa",
                customer_names
            )


            if st.button(
                "🗑️ XÓA KHÁCH HÀNG",
                type="secondary"
            ):

                index = customer_names.index(
                    selected
                )

                deleted_name = (
                    st.session_state.customers[
                        index
                    ]["Tên khách hàng"]
                )

                st.session_state.customers.pop(
                    index
                )

                st.success(
                    f"✅ Đã xóa khách hàng "
                    f"{deleted_name}."
                )

                st.rerun()


            st.divider()


            # -------------------------------------------------
            # XUẤT EXCEL
            # -------------------------------------------------

            st.subheader(
                "📥 Xuất dữ liệu"
            )

            excel_file = export_excel()


            st.download_button(
                label="📥 XUẤT DANH SÁCH EXCEL",
                data=excel_file,
                file_name=(
                    "quan_ly_khach_hang.xlsx"
                ),
                mime=(
                    "application/vnd.openxmlformats-officedocument."
                    "spreadsheetml.sheet"
                ),
                use_container_width=True
            )
