import streamlit as st
from app.sidebar_manager import SidebarManager
from streamlit_drawable_canvas import st_canvas
import tempfile
from datetime import date, timedelta
import pandas as pd
from PIL import Image, ImageDraw, ImageFont, ImageOps
import numpy as np
import datetime
import holidays
import img2pdf
import os
import io
import tempfile
import base64
import pathlib
import sys
import re
from app.helper_functions import validate_required_fields
from app.helper_functions import render_signature_image
from app.pdf_generator import generate_pdf

# Cấu hình trang Streamlit
st.set_page_config(
    page_title="Quality Inspection Recap",  # Tiêu đề trang
    layout="wide",  # Bố cục rộng
    initial_sidebar_state="expanded"  # Sidebar mở mặc định
)
class ResourceManager:
    def __init__(self):
        self.base_dir = self.get_absolute_path()
        self.image_dir = self.base_dir / "images"
        self.font_dir = self.base_dir / "fonts"
        self.paths = {
            "MauDonXin": pathlib.Path("/path/to/your/project/app/images/report002.png"),  # Kiểm tra lại tên file
            #"Font": self.font_dir / "HANDotum.ttf",  # Kiểm tra lại tên file
            #"FontDam": self.font_dir / "HANDotumB.ttf"  # Kiểm tra lại tên file
        }

    def get_absolute_path(self):
        """Lấy đường dẫn tuyệt đối cho ứng dụng."""
        if os.path.exists("/mount/src/study-work"):
            return pathlib.Path("/mount/src/study-work")
        elif os.path.exists("/workspaces/Study-work"):
            return pathlib.Path("/workspaces/Study-work")
        else:
            return pathlib.Path(__file__).parent.parent.resolve()

    def validate_resources(self):
        """Kiểm tra tính hợp lệ của file tài nguyên."""
        for name, path in self.paths.items():
            if name != "폰트" and not path.exists():
                st.error(f"Không tìm thấy {name}. Đường dẫn: {path}")
                st.stop()

        self.font_path = self.get_font_path()

    def print_debug_info(self):
        """In thông tin debug."""
        st.write("Thông tin đường dẫn hiện tại:")
        st.write(f"BASE_DIR: {self.base_dir}")
        st.write(f"IMAGE_DIR: {self.image_dir}")
        st.write(f"FONT_DIR: {self.font_dir}")
        st.write(f"Đường dẫn phông chữ đang sử dụng: {self.font_path}")

    def get_font_path(self):
            """Tìm và trả về đường dẫn file phông chữ."""
            system_font_paths = [
                "/usr/share/fonts/truetype/nanum/NanumGothic.ttf",  # Linux (Nanum Gothic)
                "/Library/Fonts/Arial Unicode.ttf",  # macOS (Arial Unicode)
                "C:\\Windows\\Fonts\\arial.ttf"  # Windows (Arial)
            ]

            for system_font in system_font_paths:
                if os.path.exists(system_font):
                    return system_font

            return None

# Tạo instance ResourceManager
resources = ResourceManager()

# In thông tin debug (nếu cần)
if os.getenv('STREAMLIT_DEBUG') == 'true':
    resources.print_debug_info()

# Thay đổi đường dẫn hình ảnh thành biểu mẫu mới
#resources.paths["MauDonXin"] = resources.image_dir / "quality_inspection_recap.png" # comment dòng này lại

# Các hàm
def show_input_form():
    """Hiển thị form nhập liệu."""
    st.header("Nhập Thông Tin")
    st.subheader("1. Product specifications")
    col1, col2 = st.columns(2)
    with col1:
        st.text_input("Product Name 1", value="FRESH GREEN GRAPES", key="product_name_1")
        st.text_input("Size 1", key="size_1")
        st.text_input("Variety characteristics 1", key="variety_characteristics_1")

    with col2:
        st.text_input("Juicy 1", key="juicy_1")
        st.text_input("Brix degree 1", key="brix_degree_1")
        st.text_input("Aerage Firmness 1", key="aerage_firmness_1")

    col3, col4 = st.columns(2)
    with col3:
        st.text_input("Product Name 2", value="FRESH BLACK GRAPES", key="product_name_2")
        st.text_input("Size 2", key="size_2")
        st.text_input("Variety characteristics 2", key="variety_characteristics_2")

    with col4:
        st.text_input("Juicy 2", key="juicy_2")
        st.text_input("Brix degree 2", key="brix_degree_2")
        st.text_input("Aerage Firmness 2", key="aerage_firmness_2")

    st.text_input("Comments (if Rejected or Pending)", key="comments")

    st.subheader("2. Net weight checking recap")
    col5, col6 = st.columns(2)
    with col5:
        st.text_input("Size 1 NW", key="size_nw_1")
        st.text_input("Average of net weight (kg) 1", key="average_nw_1")

    with col6:
        st.text_input("Target (kg) 1", key="target_1")
        st.text_input("Status 1", key="status_1")

    col7, col8 = st.columns(2)
    with col7:
        st.text_input("Size 2 NW", key="size_nw_2")
        st.text_input("Average of net weight (kg) 2", key="average_nw_2")

    with col8:
        st.text_input("Target (kg) 2", key="target_2")
        st.text_input("Status 2", key="status_2")

    st.subheader("3. Defects assessment recap")
    col9, col10 = st.columns(2)
    with col9:
        st.text_input("Size 1 DA", key="size_da_1")
        st.text_input("Total Serious Defects 1", key="total_serious_1")
        st.text_input("Total Major Defects 1", key="total_major_1")

    with col10:
        st.text_input("Total Minor Defects 1", key="total_minor_1")
        st.text_input("Total Shattering Berries 1", key="total_shattering_1")

    col11, col12 = st.columns(2)
    with col11:
        st.text_input("Size 2 DA", key="size_da_2")
        st.text_input("Total Serious Defects 2", key="total_serious_2")
        st.text_input("Total Major Defects 2", key="total_major_2")

    with col12:
        st.text_input("Total Minor Defects 2", key="total_minor_2")
        st.text_input("Total Shattering Berries 2", key="total_shattering_2")

def show_preview_and_download():
    """Hiển thị bản xem trước và nút tải xuống."""
    st.header("Xem Trước và Tải Xuống")
    # Lấy các trường từ session
    required_fields = ["product_name_1","size_1","variety_characteristics_1", "juicy_1","brix_degree_1","aerage_firmness_1", "product_name_2","size_2","variety_characteristics_2", "juicy_2","brix_degree_2","aerage_firmness_2",
                "comments", "size_nw_1", "average_nw_1", "target_1", "status_1", "size_nw_2", "average_nw_2", "target_2", "status_2", "size_da_1", "total_serious_1", "total_major_1", "total_minor_1", "total_shattering_1", "size_da_2", "total_serious_2", "total_major_2", "total_minor_2", "total_shattering_2"]  # Add the key that You have
    
    missing_fields = validate_required_fields(required_fields)
    if st.button("Chuyển Đổi và Tải Đơn PDF"):
            if missing_fields:
                st.error(f"Vui lòng nhập các thông tin sau: {', '.join(missing_fields)}")
                return

    #form_config = {"title": "Báo cáo mới" , "image_texts": []}
    if "form_configs" not in st.session_state:
        form_config = {"title": "Báo Cáo Inspection" , "image_texts": []}
    else:
        form_config = st.session_state["form_configs"]

        preview_image = render_signature_image(return_image=True, preview_only=True, form_config=form_config)

        if preview_image:
            st.image(preview_image, caption="Xem Trước Đơn", width=None)

            if st.button("Tải xuống file PDF", key="download_pdf"):
                #Làm sạch các ký tự đặc biệt trong tên
                file_name = form_config['title']
                file_name = re.sub(r'[\\/*?<>:"|]', "_", file_name) #Remove special file

                #Xử lý tạo file PDF
                with io.BytesIO() as buffer:
                    preview_image.save(buffer, format="PDF")#Save image in buffer
                    buffer.seek(0)

                    #Tạo button tải xuống
                    st.download_button(
                        label="Tải xuống file PDF",
                        data=buffer,  # Truyền buffer chứa dữ liệu PDF
                        file_name=f"{file_name}.pdf",
                        mime="application/pdf"
                    )
        else:
            st.error("Không thể tạo ảnh xem trước.")

#Main function to run
def main():
    #Tabs View
    tab1, tab2 = st.tabs(["Nhập Thông Tin", "Xem và Tải Xuống"])

    with tab1:
        show_input_form()

    with tab2:
        show_preview_and_download()

#Running the Streamlit App
# Sidebar config must run outside the main function
#It must be called before main function, or app will return error
sidebar = SidebarManager()
sidebar.render_sidebar()
if __name__ == "__main__":
     main()