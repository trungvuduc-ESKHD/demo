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
