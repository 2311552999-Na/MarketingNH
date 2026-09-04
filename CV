import streamlit as st

# =========================================================
# CẤU HÌNH TRANG
# =========================================================

st.set_page_config(
    page_title="CV - Trần Diệu Linh",
    page_icon="👩‍💼",
    layout="wide"
)

# =========================================================
# CSS
# =========================================================

st.markdown("""
<style>

    /* Toàn bộ trang */
    .stApp {
        background-color: white;
    }

    .main {
        padding-top: 20px;
    }

    /* Font */
    html, body, [class*="css"] {
        font-family: Arial, sans-serif;
    }

    /* Tên */
    .name {
        font-size: 38px;
        font-weight: bold;
        color: #c6283d;
        margin-bottom: 5px;
    }

    /* Chức danh */
    .job {
        font-size: 22px;
        color: #222222;
        margin-bottom: 15px;
    }

    /* Giới thiệu */
    .intro {
        font-size: 16px;
        line-height: 1.6;
        text-align: justify;
        color: #222222;
    }

    /* Tiêu đề section */
    .section-title {
        font-size: 21px;
        font-weight: bold;
        color: #111111;
        border-top: 3px solid #c6283d;
        border-bottom: 3px solid #c6283d;
        padding: 7px 5px;
        margin-top: 20px;
        margin-bottom: 15px;
    }

    /* Nội dung */
    .content {
        font-size: 16px;
        line-height: 1.55;
        color: #222222;
    }

    /* Tên trường / công ty */
    .bold {
        font-weight: bold;
    }

    /* Kinh nghiệm */
    .experience-date {
        font-size: 16px;
        font-weight: bold;
    }

    .company {
        font-size: 16px;
        font-weight: bold;
    }

    /* Bullet */
    .bullet {
        margin-left: 15px;
        line-height: 1.5;
        font-size: 15px;
    }

    /* Kỹ năng */
    .skill-title {
        font-size: 16px;
        font-weight: bold;
        margin-top: 12px;
    }

    .skill-content {
        font-size: 15px;
        line-height: 1.5;
    }

    /* Thông tin cá nhân */
    .info-row {
        font-size: 16px;
        margin-bottom: 10px;
    }

    .icon {
        color: #c6283d;
        font-weight: bold;
        margin-right: 10px;
    }

    /* Ảnh */
    .profile-img {
        width: 100%;
        max-width: 300px;
        border: 1px solid #dddddd;
    }

    /* Timeline */
    .timeline {
        border-left: 3px solid #777777;
        margin-left: 10px;
        padding-left: 25px;
    }

    .dot {
        width: 12px;
        height: 12px;
        background-color: #c6283d;
        border-radius: 50%;
        position: absolute;
        margin-left: -33px;
        margin-top: 5px;
    }

    /* Ẩn menu Streamlit */
    #MainMenu {
        visibility: hidden;
    }

    footer {
        visibility: hidden;
    }

    header {
        visibility: hidden;
    }

</style>
""", unsafe_allow_html=True)


# =========================================================
# PHẦN 1: ẢNH + THÔNG TIN GIỚI THIỆU
# =========================================================

col1, col2 = st.columns([1, 2.2], gap="large")

with col1:

    st.image(
        "photo.jpg",
        width=300
    )

with col2:

    st.markdown(
        '<div class="name">TRẦN DIỆU LINH</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="job">Nhân viên tín dụng</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<hr style="border: 1px solid #222222;">',
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="intro">
        Hiện tôi là sinh viên năm 3 Trường Đại học Nguyễn Tất Thành.
        Trong hơn hai năm học tập và đồng hành cùng các thầy cô giảng viên,
        tôi đã được trang bị những kiến thức nền tảng về lĩnh vực ngân hàng,
        tài chính cùng các kỹ năng cơ bản như giao tiếp, làm việc nhóm,
        xử lý tình huống và sử dụng tin học văn phòng.
        Tôi mong muốn được tham gia môi trường làm việc chuyên nghiệp để
        vận dụng những kiến thức đã học vào thực tế, không ngừng học hỏi,
        tích lũy kinh nghiệm và phát triển các kỹ năng chuyên môn.
        Mục tiêu của tôi là trở thành một nhân viên có tinh thần trách nhiệm,
        chủ động, luôn hoàn thành tốt công việc được giao và từng bước
        phát triển sự nghiệp lâu dài trong lĩnh vực ngân hàng.
        </div>
        """,
        unsafe_allow_html=True
    )


# =========================================================
# PHẦN 2: THÔNG TIN CÁ NHÂN - HỌC VẤN - CHỨNG CHỈ
# =========================================================

col1, col2, col3 = st.columns([1, 1.15, 1.1], gap="large")


# ---------------------------------------------------------
# THÔNG TIN CÁ NHÂN
# ---------------------------------------------------------

with col1:

    st.markdown(
        '<div class="section-title">THÔNG TIN CÁ NHÂN</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="info-row">
            <span class="icon">●</span>
            04/04/2005
        </div>

        <div class="info-row">
            <span class="icon">✉</span>
            trandieulinh34@gmail.com
        </div>

        <div class="info-row">
            <span class="icon">☎</span>
            0889905402
        </div>

        <div class="info-row">
            <span class="icon">📍</span>
            98 Nguyễn Văn Săng
        </div>
        """,
        unsafe_allow_html=True
    )


# ---------------------------------------------------------
# HỌC VẤN
# ---------------------------------------------------------

with col2:

    st.markdown(
        '<div class="section-title">HỌC VẤN</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="content">

        <div class="bold">
        Đại học Nguyễn Tất Thành
        </div>

        Tài chính - Ngân hàng

        <br>

        2023 - 2027

        <br>

        Chuyên ngành Tài chính ngân hàng

        </div>
        """,
        unsafe_allow_html=True
    )


# ---------------------------------------------------------
# CHỨNG CHỈ
# ---------------------------------------------------------

with col3:

    st.markdown(
        '<div class="section-title">CHỨNG CHỈ</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="content">

        Tin học:

        <br>

        Word, Excel, PDF

        </div>
        """,
        unsafe_allow_html=True
    )


# =========================================================
# =========================================================
# KINH NGHIỆM LÀM VIỆC
# =========================================================

st.markdown("## KINH NGHIỆM LÀM VIỆC")
st.divider()

col_time, col_content = st.columns([1, 3])

with col_time:
    st.markdown("🔴 **03/2025 - 04/2026**")

with col_content:
    st.markdown("### Doanh nghiệp tư nhân Thắt lưng giá tốt")
    
    st.markdown("**Nhân viên tư vấn và chăm sóc khách hàng**")
    
    st.markdown("""
    - Liên hệ tệp **+1000 khách hàng tiềm năng** và tư vấn khách hàng sử dụng các sản phẩm.
    
    - Tiếp nhận và xử lý các yêu cầu của khách hàng về sản phẩm.
    
    - Chăm sóc khách hàng cũ, hỗ trợ giải đáp mọi thắc mắc của khách hàng đối với sản phẩm đang sử dụng.
    """)
    
# =========================================================
# PHẦN 4: KỸ NĂNG + NGƯỜI THAM KHẢO
# =========================================================

col1, col2 = st.columns([1, 1], gap="large")


# ---------------------------------------------------------
# KỸ NĂNG
# ---------------------------------------------------------

with col1:

    st.markdown(
        '<div class="section-title">KỸ NĂNG</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="skill-title">
            Kỹ năng giao tiếp
        </div>

        <div class="skill-content">
            Giao tiếp và giải đáp thắc mắc của khách hàng
        </div>


        <div class="skill-title">
            Kỹ năng làm việc nhóm
        </div>

        <div class="skill-content">
            Control được công việc trong nhóm, phân chia cho các
            thành viên trong nhóm hoặc có trách nhiệm với nhiệm vụ
            được giao
        </div>


        <div class="skill-title">
            Kỹ năng quản lý thời gian
        </div>

        <div class="skill-content">
            Phân bổ thời gian hợp lý cho từng công việc
        </div>


        <div class="skill-title">
            Kỹ năng tin học
        </div>

        <div class="skill-content">
            Soạn thảo văn bảng, làm sile
        </div>
        """,
        unsafe_allow_html=True
    )


# ---------------------------------------------------------
# NGƯỜI THAM KHẢO
# ---------------------------------------------------------

with col2:

    st.markdown(
        '<div class="section-title">NGƯỜI THAM KHẢO</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="content">

        <div class="bold">
            Cao Thị Mỹ Huê
        </div>

        Giám đốc phòng kinh doanh (SM) - Ngân hàng TMCP
        Quốc Tế Việt Nam (VIB)

        </div>
        """,
        unsafe_allow_html=True
    )
