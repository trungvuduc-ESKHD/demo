import streamlit as st
from PIL import Image
from app.resource_manager import ResourceManager
from app.tabs import info_input, signature_input, application_preview
import base64
import json
from io import BytesIO
import sys
from pathlib import Path
from app.sidebar_manager import SidebarManager
from app.auth_manager import AuthManager

# Thêm thư mục hiện tại vào đường dẫn Python
current_dir = Path(__file__).parent
sys.path.append(str(current_dir))

# Import các hàm hỗ trợ
try:
    from app.helper_functions import render_signature_image
    print("Import helper_functions thành công")
except ImportError as e:
    print(f"Lỗi import: {e}")
    print(f"Đường dẫn Python hiện tại: {sys.path}")
    st.error("Không thể tải các module cần thiết.")

# Cấu hình layout trang
st.set_page_config(layout="wide")

# Khởi tạo tài nguyên
resources = ResourceManager()
resources.validate_resources()

# Đọc tham số từ URL
query_params = st.query_params
form_type = query_params.get("form_type", "templates") 

# Tải file cấu hình JSON
with open("form_config.json", "r", encoding="utf-8") as f:
    form_configs = json.load(f)

# Lấy cấu hình form
if form_type in form_configs:
    form_config = form_configs[form_type]
else:
    form_config = form_configs["templates_3"] 

# Load logo và điều chỉnh kích thước
logo = Image.open("images/logo.png")
# Điều chỉnh kích thước theo chiều cao của tiêu đề phụ (khoảng 40px)
logo_height = 40
aspect_ratio = logo.size[0] / logo.size[1]
logo_width = int(logo_height * aspect_ratio)
logo = logo.resize((logo_width, logo_height))

# Container cho tiêu đề và logo
col1, col2, col3 = st.columns([1, 6, 1])

def image_to_base64(image):
    buffered = BytesIO()
    image.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode()

with col2:
    # Lấy tiêu đề từ cấu hình form
    title_text = form_config.get("title", "Demo") + " Inspection"
    st.markdown(f"<h1 style='text-align: center;'>{title_text}</h1>", unsafe_allow_html=True)

    # CSS cho layout responsive
    st.markdown("""
        <style>
            .header-container {
                display: flex;
                align-items: center;
                justify-content: center;
                flex-wrap: nowrap;
                gap: 5px;
                margin: 0 auto;
                max-width: 300px;
            }
            .logo-container {
                flex: 0 0 auto;
                display: flex;
                align-items: center;
                margin-right: -5px;
            }
            .title-container {
                flex: 0 0 auto;
                text-align: left;
            }
            @media (max-width: 640px) {
                .header-container {
                    gap: 0px;
                }
            }
        </style>
    """, unsafe_allow_html=True)

    # Hiển thị logo và tiêu đề phụ trong cùng một container
    st.markdown(
        f"""
        <div class="header-container">
            <div class="logo-container">
                <img src="data:image/png;base64,{image_to_base64(logo)}"
                     width="{logo_width}px"
                     height="{logo_height}px"
                     style="object-fit: contain;">
            </div>
            <div class="title-container">
                <h3 style="margin: 0; padding-left: 5px;">Eurofins SKHD</h3>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

# Kiểm tra quyền truy cập
auth_manager = AuthManager()
auth_manager.check_page_access("Lưu ý") # Giữ nguyên tiếng Hàn, xem phần lưu ý

# Render sidebar
sidebar_manager = SidebarManager()
sidebar_manager.render_sidebar()

# Cấu hình các tab
tabs = st.tabs(["1. Nhập Thông Tin", "2. Nhập Chữ Ký", "3. Xem và Tải Đơn"])

# Liên kết các tab với chức năng tương ứng
with tabs[0]:
    info_input.render()

with tabs[1]:
    signature_input.render()

with tabs[2]:
    application_preview.render()

# Thêm footer
st.markdown("---")  # Đường phân cách
st.markdown(
    """
    <div style='text-align: center; color: #666666; padding: 10px;'>
    Mọi thắc mắc xin liên hệ: <a href='Trungvuu204:@gmail.com'>gmail.com</a>
    </div>
    """,
    unsafe_allow_html=True
)