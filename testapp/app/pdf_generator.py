import tempfile
import streamlit as st
from app.helper_functions import render_signature_image
import io
import re  # Import thư viện re
import time

def generate_pdf(form_config):
    try:
        # Lấy ảnh từ hàm render_signature_image
        preview_image = render_signature_image(
            return_image=True,
            preview_only=False,
            form_config=form_config
        )

        if preview_image is None:
            st.error("Không thể tạo ảnh xem trước.")
            return False

        # Tạo tên file hợp lệ
        title = form_config['title']
        file_name_without_ext = re.sub(r'[\\/*?<>:"|]', "_", title)  # Loại bỏ ký tự đặc biệt
        file_name = f"{file_name_without_ext}.pdf"

        # Tạo đối tượng BytesIO để lưu PDF vào bộ nhớ
        buffer = io.BytesIO()
        preview_image.save(buffer, format="PDF")  # Lưu vào buffer
        buffer.seek(0)  # Đặt con trỏ về đầu buffer

        # Tạo nút tải xuống
        st.download_button(
            label="Tải xuống file PDF",
            data=buffer,  # Truyền buffer chứa dữ liệu PDF
            file_name=file_name,
            mime="application/pdf"
        )
        return True
    except Exception as e:
        st.error(f"Lỗi khi tạo file PDF: {e}")
        return False