import streamlit as st
from PIL import Image
import base64
from io import BytesIO
from app.sidebar_manager import SidebarManager
from app.auth_manager import AuthManager
import qrcode

# Cấu hình trang
st.set_page_config(
    page_title="Hệ Thống Quản Lý Hồ Sơ",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Kiểm tra tham số URL và chuyển hướng
query_params = st.query_params
redirect_to = query_params.get("page", None)

if redirect_to:
    if redirect_to == "field_trip_request":
        st.switch_page("pages/field_trip_request.py")
    elif redirect_to == "field_trip_report":
        st.switch_page("pages/field_trip_report.py")

# Khởi tạo trạng thái phiên
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

# Render sidebar
sidebar = SidebarManager()
sidebar.render_sidebar()

# Load logo và điều chỉnh kích thước
logo = Image.open("images/sidebar_logo.png")
logo_height = 40
aspect_ratio = logo.size[0] / logo.size[1]
logo_width = int(logo_height * aspect_ratio)
logo = logo.resize((logo_width, logo_height))

def image_to_base64(image):
    buffered = BytesIO()
    image.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode()

# Tiêu đề chính và header
st.markdown("<h1 style='text-align: center;'>Hệ Thống Quản Lý Văn Bản Thông Minh</h1>", unsafe_allow_html=True)

# CSS cho layout logo
st.markdown("""
    <style>
        .header-container {
            display: flex;
            justify-content: center;
            margin: 0 auto;
            max-width: 300px;
        }
    </style>
""", unsafe_allow_html=True)

# Hiển thị logo
st.markdown(
    f"""
    <div class="header-container">
        <img src="data:image/png;base64,{image_to_base64(logo)}"
             width="{logo_width}px"
             height="{logo_height}px"
             style="object-fit: contain;">
    </div>
    """,
    unsafe_allow_html=True
)
st.markdown("---")

# Hiển thị nội dung dựa trên trạng thái đăng nhập
if not st.session_state.get("authenticated", False):
    # Form đăng nhập
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("<h2 style='text-align: center;'>Đăng Nhập</h2>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center;'>Vui lòng đăng nhập để sử dụng các chức năng.</p>", unsafe_allow_html=True)
        with st.form("login_form"):
            username = st.text_input("Tên đăng nhập")
            password = st.text_input("Mật khẩu", type="password")
            submit = st.form_submit_button("Đăng nhập")

            if submit:
                auth_manager = AuthManager()
                if auth_manager.authenticate(username, password):
                    st.success("Đăng nhập thành công!")
                    st.rerun()
                else:
                    st.error("Tên đăng nhập hoặc mật khẩu không đúng.")
else:
    st.markdown("---")
    # Dashboard
    st.markdown("<h2 style='text-align: center;'>Dashboard Admin</h2>", unsafe_allow_html=True)

    # Tạo tab
    tab1, tab2 = st.tabs(["Dashboard", "Liên Kết Trực Tiếp"])

    # Tab 1: Dashboard
    with tab1:
        st.markdown("### Chào mừng!")
        st.write("Bạn có thể sử dụng các chức năng quản lý dành cho admin.")

        # Các thẻ chức năng
        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown("""
            <div style='padding: 20px; border-radius: 10px; border: 1px solid #ddd; margin: 10px 0;'>
                <h3>📝 INSPECTION REPORT MANAGE</h3>
                <p>Tạo & quản lý Form</p>
            </div>
            """, unsafe_allow_html=True)
            if st.button("Truy cập →", key="goto_delegation"):
                st.switch_page("pages/delegation_login.py")

        with col2:
            st.markdown("""
            <div style='padding: 20px; border-radius: 10px; border: 1px solid #ddd; margin: 10px 0;'>
                <h3>📋 Báo Cáo</h3>
                <p>Quản lý và xử lý báo cáo</p>
            </div>
            """, unsafe_allow_html=True)
            if st.button("Truy cập →", key="goto_absence"):
                st.switch_page("pages/absence.py")

        with col3:
            st.markdown("""
            <div style='padding: 20px; border-radius: 10px; border: 1px solid #ddd; margin: 10px 0;'>
                <h3>📝 Trải Nghiệm </h3>
                <p>Soạn thảo và báo cáo kết quả</p>
            </div>
            """, unsafe_allow_html=True)
            col1, col2 = st.columns(2)
            with col1:
                if st.button("Truy cập →", key="goto_field_request"):
                    st.switch_page("pages/camera_photo.py")

    # Tab 2: Liên kết trực tiếp
    with tab2:
        st.write("### 🔗 Liên Kết Trực Tiếp Đến Trải Nghiệm")

        # URL gốc cố định (chỉ lưu trong session, không hiển thị)
        if 'base_url' not in st.session_state:
            st.session_state.base_url = "https://github.com/trungvuduc-ESKHD/demo.git"

        # Tạo và hiển thị liên kết (tự động)
        col1, col2 = st.columns(2)

        with col1:
            st.write("#### Báo Cáo ")
            request_link = f"{st.session_state.base_url}?page=camera"
            st.text_input("Chọn và sao chép liên kết:", value=request_link, key="request_link_input", label_visibility="collapsed")

        with col2:
            st.write("#### Báo Cáo Kết Quả")
            report_link = f"{st.session_state.base_url}?page=field_trip_report"
            st.text_input("Chọn và sao chép liên kết:", value=report_link, key="report_link_input", label_visibility="collapsed")

        # Tạo QR code (giữ nguyên)
        if st.checkbox("Tạo Mã QR"):
            try:
                col1, col2 = st.columns(2)

                with col1:
                    st.write("QR Đơn Xin")
                    qr = qrcode.QRCode(version=1, box_size=10, border=5)
                    qr.add_data(request_link)
                    qr.make(fit=True)
                    img = qr.make_image(fill_color="black", back_color="white")
                    buffered = BytesIO()
                    img.save(buffered, format="PNG")
                    st.image(buffered)

                with col2:
                    st.write("QR Báo Cáo")
                    qr = qrcode.QRCode(version=1, box_size=10, border=5)
                    qr.add_data(report_link)
                    qr.make(fit=True)
                    img = qr.make_image(fill_color="black", back_color="white")
                    buffered = BytesIO()
                    img.save(buffered, format="PNG")
                    st.image(buffered)
            except ImportError:
                st.error("Vui lòng cài đặt gói 'qrcode' để tạo mã QR.")

# Giới thiệu chức năng cho người dùng thông thường (luôn hiển thị)
st.markdown("---")
st.markdown("### 📌 Chức Năng Dành Cho Người Dùng")
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    #### ✍️ Soạn Thảo Báo Cáo
    - Viết Báo Cáo trực tuyến
    - Dễ dàng nộp
    """)

with col2:
    st.markdown("""
    #### 📝 Báo Cáo Inspection
    - Soạn đơn theo mẫu
    - Tự động tạo văn bản
    """)

with col3:
    st.markdown("""
    #### 📋 Báo Cáo Kết Kiểm Định
    - Viết báo cáo kết quả
    - Nộp dễ dàng
    """)

st.markdown("---")
st.markdown("<div style='text-align: right;'>Người thực hiện: Trung Vũ </div>", unsafe_allow_html=True)