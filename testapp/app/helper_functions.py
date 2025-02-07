import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import numpy as np
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.colors import black
from app.resource_manager import ResourceManager
from datetime import datetime

def validate_required_fields(required_fields):
    """Kiểm tra xem tất cả các trường bắt buộc đã được điền hay chưa và trả về danh sách các trường còn thiếu."""
    missing_fields = []
    for field in required_fields:
        if field not in st.session_state:
            missing_fields.append(field)
        else:
            value = st.session_state[field]
            if value is None:
                missing_fields.append(field)
            elif isinstance(value, (str, list, dict)) and not value:
                missing_fields.append(field)
            elif isinstance(value, np.ndarray) and value.size == 0:
                missing_fields.append(field)
    return missing_fields

def wrap_text(text, font, max_width):
    """Xuống dòng văn bản sao cho vừa với độ rộng tối đa cho trước."""
    result = []
    current_line = ""

    for char in text:
        test_line = current_line + char
        if font.getlength(test_line) <= max_width:
            current_line = test_line
        else:
            result.append(current_line)
            current_line = char

    if current_line:
        result.append(current_line)

    return result

def get_adjusted_font_size(text, max_width, font_path, initial_size=70, min_size=50):
    """Trả về kích thước font phù hợp dựa trên độ dài văn bản."""
    current_size = initial_size
    font = ImageFont.truetype(str(font_path), size=current_size)

    # Giảm kích thước font nếu văn bản vượt quá độ rộng tối đa
    while font.getlength(text) > max_width and current_size > min_size:
        current_size -= 2
        font = ImageFont.truetype(str(font_path), size=current_size)

    return font

def format_date(date_str):
    """Chuyển đổi ngày tháng sang định dạng 'YYYY năm MM tháng DD ngày'."""
    if not date_str:
        return ""
    try:
        # Chuyển đổi chuỗi thành đối tượng datetime
        date_obj = datetime.strptime(date_str, '%Y-%m-%d')
        # Chuyển đổi sang định dạng mong muốn
        return date_obj.strftime('%Y năm %m tháng %d ngày')
    except:
        return date_str

def render_signature_image(preview_only=False, form_config=None, return_image=False):
    """Tạo và hiển thị ảnh của đơn."""
    # Thông tin gỡ lỗi
    print("render_signature_image được gọi")
    print("form_config nhận được:", form_config)

    # Thiết lập giá trị mặc định
    if form_config is None:
        form_config = {"title": "Báo Cáo Inspection", "image_texts": []}

    try:
        resources = ResourceManager()
        img_path = resources.paths["MauDonXin"] # Cần kiểm tra lại tên file
        font_path = resources.paths["Font"] # Cần kiểm tra lại tên file

        # Tải hình ảnh
        image = Image.open(img_path).convert("RGBA")

        # Chuyển đổi sang nền trắng
        background = Image.new('RGB', image.size, (255, 255, 255))  #RGBA là Red, Green, Blue, Alpha
        background.paste(image, (0,0), image) #alpha_composite(image,(0,0),dest=(0,0))
        image = background
        draw = ImageDraw.Draw(image)

        # Thêm viền chỉ trong chế độ xem trước
        if preview_only:
            width, height = image.size
            draw.rectangle([(0, 0), (width-1, height-1)], outline="black", width=5)

        # Định nghĩa font
        font = ImageFont.truetype(str(resources.paths["Font"]), size=24)  # Font thường, giảm kích thước
        name_font = ImageFont.truetype(str(resources.paths["FontDam"]), size=26) # Font in đậm để hiển thị tên, giảm kích thước

        # Thêm thông tin chung
        draw.text((800, 570), f"{st.session_state.get('supplier_name', '')}", font=font, fill="black")
        draw.text((1900, 570), f"{st.session_state.get('partner_name', '')}", font=font, fill="black")
        draw.text((800, 650), f"{st.session_state.get('contract_number', '')}", font=font, fill="black")
        draw.text((1900, 650), f"{st.session_state.get('total_quantity', '')}", font=font, fill="black")

        # Thay đổi định dạng ngày tháng
        eta_date = format_date(str(st.session_state.get('eta_date', '')))
        draw.text((1900, 740), f"{eta_date}", font=font, fill="black")
        draw.text((800, 740), f"{st.session_state.get('container_number', '')}", font=font, fill="black")

        draw.text((800, 830), f"{st.session_state.get('responsible_department', '')}", font=font, fill="black")
        draw.text((800, 950), f"{st.session_state.get('inspection_location', '')}", font=font, fill="black")

        # Thông tin sản phẩm
        draw.text((400, 1165), f"{st.session_state.get('product_name_1', '')}", font=font, fill="black")
        draw.text((980, 1165), f"{st.session_state.get('size_1', '')}", font=font, fill="black")
        draw.text((1530, 1165), f"{st.session_state.get('quantity_bag_1', '')}", font=font, fill="black")
        draw.text((2100, 1165), f"{st.session_state.get('net_weight_1', '')}", font=font, fill="black")

        draw.text((400, 1230), f"{st.session_state.get('product_name_2', '')}", font=font, fill="black")
        draw.text((980, 1230), f"{st.session_state.get('size_2', '')}", font=font, fill="black")
        draw.text((1530, 1230), f"{st.session_state.get('quantity_bag_2', '')}", font=font, fill="black")
        draw.text((2100, 1230), f"{st.session_state.get('net_weight_2', '')}", font=font, fill="black")

        # Tình trạng container
        draw.text((1530, 1500), f"{st.session_state.get('container_clean', '')}", font=font, fill="black")
        draw.text((1530, 1580), f"{st.session_state.get('package_status', '')}", font=font, fill="black")

        draw.text((1530, 1660), f"{st.session_state.get('ventilation_ok', '')}", font=font, fill="black")
        draw.text((1530, 1740), f"{st.session_state.get('abnormal_smell', '')}", font=font, fill="black")

        draw.text((1530, 1820), f"{st.session_state.get('no_leakage', '')}", font=font, fill="black")
        draw.text((1530, 1895), f"{st.session_state.get('container_temp', '')}", font=font, fill="black")

        draw.text((1530, 1975), f"{st.session_state.get('temp_recorder_ok', '')}", font=font, fill="black")

        # Thêm chữ ký
        if "signature_img" in st.session_state and st.session_state["signature_img"] is not None:
            signature_data = st.session_state["signature_img"]
            if isinstance(signature_data, np.ndarray):
                # Chuyển đổi trực tiếp vì đã ở định dạng RGBA
                signature_img = Image.fromarray(signature_data)
                signature_resized = signature_img.resize((400, 250), Image.Resampling.LANCZOS)

                # Điều chỉnh vị trí chữ ký (tọa độ x, y cần được điều chỉnh cho phù hợp)
                image.paste(signature_resized, (500, 2570), signature_resized)

        # Chỉ hiển thị bản xem trước khi preview_only là True
        if preview_only:
            st.image(image, caption="Xem Trước Đơn", width=None) # width=None để giữ kích thước gốc

        if return_image:
            return image

    except Exception as e:
        st.error(f"Lỗi khi tạo bản xem trước: {str(e)}")
        if return_image:
            return None