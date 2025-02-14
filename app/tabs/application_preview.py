import streamlit as st
from app.pdf_generator import generate_pdf
from app.helper_functions import validate_required_fields, render_signature_image
from app.resource_manager import ResourceManager
import json

def render():
    st.header("Xem Trước Đơn và Tạo File PDF")

    # Lưu ResourceManager vào session state
    if 'resources' not in st.session_state:
        st.session_state['resources'] = ResourceManager()

    # Nếu chưa có form_configs, tải từ file JSON
    if 'form_configs' not in st.session_state:
        try:
            with open("form_config.json", "r", encoding="utf-8") as f:
                st.session_state['form_configs'] = json.load(f)
        except Exception as e:
            st.error(f"Lỗi khi tải file cấu hình: {str(e)}")
            return

    # Lấy form_config
    form_configs = st.session_state['form_configs']
    query_params = st.query_params
    form_type = query_params.get("form_type", "templates_1") # Default to templates_1

    # Cấu hình form_config
    if form_type in form_configs:
        form_config = form_configs[form_type]
    else:
        form_config = form_configs["templates_1"]

    # Dynamically determine required fields based on form_type
    # (This assumes your form_config.json now contains the required fields for each template)
    required_fields = form_config.get("required_fields", [])
    missing_fields = validate_required_fields(required_fields)

    if missing_fields:
        st.error(f"Vui lòng nhập các thông tin sau: {', '.join(missing_fields)}")
        return

    # =================================================================
    # Skip render_signature_image for templates_7
    # =================================================================
    # Tạo và tải file PDF
    if st.button("Chuyển Đổi và Tải Đơn PDF"):
        with st.spinner("Đang chuyển đổi sang PDF..."):
            pdf_generated = generate_pdf(form_config=form_config)
            if pdf_generated:
                st.success("Đã sẵn sàng để tải file PDF!")
