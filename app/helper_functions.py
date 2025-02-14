import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import numpy as np
from datetime import datetime

from app.resource_manager import ResourceManager

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

def get_session_state_value(tab_name, key):
    full_key = f"{tab_name}_{key}"
    return st.session_state.get(full_key, '')

def render_signature_image(preview_only=False, form_config=None, form_type=None, return_image=False):
    """Tạo và hiển thị ảnh của đơn."""
    # Thông tin gỡ lỗi
    print("render_signature_image được gọi")
    print("form_config nhận được:", form_config)
    print("form_type nhận được:", form_type)

    # Thiết lập giá trị mặc định
    if form_config is None:
        form_config = {"title": "Báo Cáo Inspection", "image_texts": []}

    try:
        resources = ResourceManager()

        # Dynamically choose image path based on form_type
        if form_type == "templates_1":
            img_path = resources.paths["MauDonXin"]  # Original image
        elif form_type == "templates_2":
            img_path = resources.paths["QualityInspect"] # Quality Inspection Recap
        elif form_type == "templates_3":
            img_path = resources.paths["netweight_form"] # Sampling Plan Green
        elif form_type == "templates_4":
            img_path = resources.paths["netweight2_form"] # Sampling Plan Black
        elif form_type == "templates_5":
            img_path = resources.paths["defects1_form"] # Defect Assessment Green
        elif form_type == "templates_6":
            img_path = resources.paths["defects2_form"] # Defect Assessment Black
        else:
            img_path = resources.paths["MauDonXin"]

        font_path = resources.paths["Font"]  # Cần kiểm tra lại tên file

        # Tải hình ảnh
        image = Image.open(img_path).convert("RGBA")

        # Chuyển đổi sang nền trắng
        background = Image.new('RGB', image.size, (255, 255, 255))  # RGBA là Red, Green, Blue, Alpha
        background.paste(image, (0, 0), image)  # alpha_composite(image,(0,0),dest=(0,0))
        image = background
        draw = ImageDraw.Draw(image)

        #Thêm các hình khác
        if form_type == "templates_1":
            image1 = get_session_state_value("Inspection Report", "image_1")
            image2 = get_session_state_value("Inspection Report", "image_2")
        # Check if camera images have value, if not do not render.
            if image1 != "" and image1 is not None:
                # Add camera to images
                cameraImage1 = Image.fromarray(cameraImage1)
                resized_camera_image = cameraImage1.resize((400, 250), Image.Resampling.LANCZOS)
                image.paste(resized_camera_image, (500, 2000), resized_camera_image)

            if image2 != "" and image2 is not None:
            # Add camera to images
                cameraImage2 = Image.fromarray(cameraImage2)
                resized_camera_image = cameraImage2.resize((400, 250), Image.Resampling.LANCZOS)
                image.paste(resized_camera_image, (500, 2300), resized_camera_image)

        # Thêm viền chỉ trong chế độ xem trước
        if preview_only:
            width, height = image.size
            draw.rectangle([(0, 0), (width - 1, height - 1)], outline="black", width=5)

        # Định nghĩa font
        font = ImageFont.truetype(str(resources.paths["Font"]), size=24)  # Font thường, giảm kích thước
        name_font = ImageFont.truetype(str(resources.paths["FontDam"]), size=26)  # Font in đậm để hiển thị tên, giảm kích thước

        # =========================
        # Form specific overlays
        # =========================
        if form_type == "templates_1":
            # Inspection Report
            supplier_name = get_session_state_value("Inspection Report", "supplier_name")
            partner_name = get_session_state_value("Inspection Report", "partner_name")
            contract_number = get_session_state_value("Inspection Report", "contract_number")
            total_quantity = get_session_state_value("Inspection Report", "total_quantity")
            eta_date_str = get_session_state_value("Inspection Report", "eta_date")
            container_number = get_session_state_value("Inspection Report", "container_number")
            responsible_department = get_session_state_value("Inspection Report", "responsible_department")
            inspection_location = get_session_state_value("Inspection Report", "inspection_location")
            product_name_1 = get_session_state_value("Inspection Report", "product_name_1")
            size_1 = get_session_state_value("Inspection Report", "size_1")
            quantity_bag_1 = get_session_state_value("Inspection Report", "quantity_bag_1")
            net_weight_1 = get_session_state_value("Inspection Report", "net_weight_1")
            product_name_2 = get_session_state_value("Inspection Report", "product_name_2")
            size_2 = get_session_state_value("Inspection Report", "size_2")
            quantity_bag_2 = get_session_state_value("Inspection Report", "quantity_bag_2")
            net_weight_2 = get_session_state_value("Inspection Report", "net_weight_2")
            container_clean = get_session_state_value("Inspection Report", "container_clean")
            ventilation_ok = get_session_state_value("Inspection Report", "ventilation_ok")
            no_leakage = get_session_state_value("Inspection Report", "no_leakage")
            temp_recorder_ok = get_session_state_value("Inspection Report", "temp_recorder_ok")
            package_status = get_session_state_value("Inspection Report", "package_status")
            abnormal_smell = get_session_state_value("Inspection Report", "abnormal_smell")
            container_temp = get_session_state_value("Inspection Report", "container_temp")

            # Format the date string
            eta_date = format_date(str(eta_date_str))

            # Add thông tin chung
            draw.text((400, 570), f"{supplier_name}", font=font, fill="black")
            draw.text((1900, 570), f"{partner_name}", font=font, fill="black")
            draw.text((800, 650), f"{contract_number}", font=font, fill="black")
            draw.text((1900, 650), f"{total_quantity}", font=font, fill="black")
            draw.text((1900, 740), f"{eta_date}", font=font, fill="black")
            draw.text((800, 740), f"{container_number}", font=font, fill="black")
            draw.text((800, 830), f"{responsible_department}", font=font, fill="black")
            draw.text((800, 950), f"{inspection_location}", font=font, fill="black")

            # Add thông tin sản phẩm
            draw.text((400, 1165), f"{product_name_1}", font=font, fill="black")
            draw.text((980, 1165), f"{size_1}", font=font, fill="black")
            draw.text((1530, 1165), f"{quantity_bag_1}", font=font, fill="black")
            draw.text((2100, 1165), f"{net_weight_1}", font=font, fill="black")
            draw.text((400, 1230), f"{product_name_2}", font=font, fill="black")
            draw.text((980, 1230), f"{size_2}", font=font, fill="black")
            draw.text((1530, 1230), f"{quantity_bag_2}", font=font, fill="black")
            draw.text((2100, 1230), f"{net_weight_2}", font=font, fill="black")

            # Add tình trạng container
            draw.text((1530, 1500), f"{container_clean}", font=font, fill="black")
            draw.text((1530, 1580), f"{package_status}", font=font, fill="black")
            draw.text((1530, 1660), f"{ventilation_ok}", font=font, fill="black")
            draw.text((1530, 1740), f"{abnormal_smell}", font=font, fill="black")
            draw.text((1530, 1820), f"{no_leakage}", font=font, fill="black")
            draw.text((1530, 1895), f"{container_temp}", font=font, fill="black")
            draw.text((1530, 1975), f"{temp_recorder_ok}", font=font, fill="black")

            # Add chữ ký
            if "signature_img" in st.session_state and st.session_state["signature_img"] is not None:
                signature_data = st.session_state["signature_img"]
                if isinstance(signature_data, np.ndarray):
                    # Chuyển đổi trực tiếp vì đã ở định dạng RGBA
                    signature_img = Image.fromarray(signature_data)
                    signature_resized = signature_img.resize((400, 250), Image.Resampling.LANCZOS)

                    # Điều chỉnh vị trí chữ ký (tọa độ x, y cần được điều chỉnh cho phù hợp)
                    image.paste(signature_resized, (500, 2570), signature_resized)

        elif form_type == "templates_2":
            # Quality Inspection Recap

            # Add values from the Quality Inspection Recap Tab
            product_name_1 = get_session_state_value("Quality Inspection Recap", "product_name_1")
            product_name_2 = get_session_state_value("Quality Inspection Recap", "product_name_2")
            size_1 = get_session_state_value("Quality Inspection Recap", "size_1")
            size_2 = get_session_state_value("Quality Inspection Recap", "size_2")
            variety_char_1 = get_session_state_value("Quality Inspection Recap", "variety_char_1")
            variety_char_2 = get_session_state_value("Quality Inspection Recap", "variety_char_2")
            juicy_1 = get_session_state_value("Quality Inspection Recap", "juicy_1")
            juicy_2 = get_session_state_value("Quality Inspection Recap", "juicy_2")
            brix_degree_1 = get_session_state_value("Quality Inspection Recap", "brix_degree_1")
            brix_degree_2 = get_session_state_value("Quality Inspection Recap", "brix_degree_2")
            aerage_firmness_1 = get_session_state_value("Quality Inspection Recap", "aerage_firmness_1")
            aerage_firmness_2 = get_session_state_value("Quality Inspection Recap", "aerage_firmness_2")
            average_net_weight_1 = get_session_state_value("Quality Inspection Recap", "average_net_weight_1")
            average_net_weight_2 = get_session_state_value("Quality Inspection Recap", "average_net_weight_2")
            target_kg_1 = get_session_state_value("Quality Inspection Recap", "target_kg_1")
            target_kg_2 = get_session_state_value("Quality Inspection Recap", "target_kg_2")
            status_1 = get_session_state_value("Quality Inspection Recap", "status_1")
            status_2 = get_session_state_value("Quality Inspection Recap", "status_2")
            total_serious_defects_1 = get_session_state_value("Quality Inspection Recap", "total_serious_defects_1")
            total_serious_defects_2 = get_session_state_value("Quality Inspection Recap", "total_serious_defects_2")
            total_major_defects_1 = get_session_state_value("Quality Inspection Recap", "total_major_defects_1")
            total_major_defects_2 = get_session_state_value("Quality Inspection Recap", "total_major_defects_2")
            total_minor_defects_1 = get_session_state_value("Quality Inspection Recap", "total_minor_defects_1")
            total_minor_defects_2 = get_session_state_value("Quality Inspection Recap", "total_minor_defects_2")
            shattering_berries_1 = get_session_state_value("Quality Inspection Recap", "shattering_berries_1")
            shattering_berries_2 = get_session_state_value("Quality Inspection Recap", "shattering_berries_2")

            # Table 1
            draw.text((200, 300), f"{product_name_1}", font=font, fill="black") # Fake Coordinates, you must change these
            draw.text((200, 400), f"{product_name_2}", font=font, fill="black") # Fake Coordinates, you must change these
            draw.text((300, 300), f"{size_1}", font=font, fill="black") # Fake Coordinates, you must change these
            draw.text((300, 400), f"{size_2}", font=font, fill="black") # Fake Coordinates, you must change these
            draw.text((400, 300), f"{variety_char_1}", font=font, fill="black") # Fake Coordinates, you must change these
            draw.text((400, 400), f"{variety_char_2}", font=font, fill="black") # Fake Coordinates, you must change these
            draw.text((500, 300), f"{juicy_1}", font=font, fill="black") # Fake Coordinates, you must change these
            draw.text((500, 400), f"{juicy_2}", font=font, fill="black") # Fake Coordinates, you must change these
            draw.text((600, 300), f"{brix_degree_1}", font=font, fill="black") # Fake Coordinates, you must change these
            draw.text((600, 400), f"{brix_degree_2}", font=font, fill="black") # Fake Coordinates, you must change these
            draw.text((700, 300), f"{aerage_firmness_1}", font=font, fill="black") # Fake Coordinates, you must change these
            draw.text((700, 400), f"{aerage_firmness_2}", font=font, fill="black") # Fake Coordinates, you must change these

            # Table 2
            draw.text((200, 500), f"{product_name_1}", font=font, fill="black") # Fake Coordinates, you must change these
            draw.text((200, 600), f"{product_name_2}", font=font, fill="black") # Fake Coordinates, you must change these
            draw.text((300, 500), f"{size_1}", font=font, fill="black") # Fake Coordinates, you must change these
            draw.text((300, 600), f"{size_2}", font=font, fill="black") # Fake Coordinates, you must change these
            draw.text((400, 500), f"{average_net_weight_1}", font=font, fill="black") # Fake Coordinates, you must change these
            draw.text((400, 600), f"{average_net_weight_2}", font=font, fill="black") # Fake Coordinates, you must change these
            draw.text((500, 500), f"{target_kg_1}", font=font, fill="black") # Fake Coordinates, you must change these
            draw.text((500, 600), f"{target_kg_2}", font=font, fill="black") # Fake Coordinates, you must change these
            draw.text((600, 500), f"{status_1}", font=font, fill="black") # Fake Coordinates, you must change these
            draw.text((600, 600), f"{status_2}", font=font, fill="black") # Fake Coordinates, you must change these

            # Table 3
            draw.text((200, 700), f"{product_name_1}", font=font, fill="black") # Fake Coordinates, you must change these
            draw.text((200, 800), f"{product_name_2}", font=font, fill="black") # Fake Coordinates, you must change these
            draw.text((300, 700), f"{size_1}", font=font, fill="black") # Fake Coordinates, you must change these
            draw.text((300, 800), f"{size_2}", font=font, fill="black") # Fake Coordinates, you must change these
            draw.text((400, 700), f"{total_serious_defects_1}", font=font, fill="black") # Fake Coordinates, you must change these
            draw.text((400, 800), f"{total_serious_defects_2}", font=font, fill="black") # Fake Coordinates, you must change these
            draw.text((500, 700), f"{total_major_defects_1}", font=font, fill="black") # Fake Coordinates, you must change these
            draw.text((500, 800), f"{total_major_defects_2}", font=font, fill="black") # Fake Coordinates, you must change these
            draw.text((600, 700), f"{total_minor_defects_1}", font=font, fill="black") # Fake Coordinates, you must change these
            draw.text((600, 800), f"{total_minor_defects_2}", font=font, fill="black") # Fake Coordinates, you must change these
            draw.text((700, 700), f"{shattering_berries_1}", font=font, fill="black") # Fake Coordinates, you must change these
            draw.text((700, 800), f"{shattering_berries_2}", font=font, fill="black") # Fake Coordinates, you must change these

        elif form_type == "templates_3":
            # Sampling Plan Green
            product_name = get_session_state_value("Sampling Plan Green", "product_name")
            size_caliber = get_session_state_value("Sampling Plan Green", "size_caliber")
            sampling_plan = get_session_state_value("Sampling Plan Green", "sampling_plan")
            qty_of_bags = get_session_state_value("Sampling Plan Green", "qty_of_bags")
            empty_weight_of_bag = get_session_state_value("Sampling Plan Green", "empty_weight_of_bag")
            total_gross_weight = get_session_state_value("Sampling Plan Green", "total_gross_weight")
            total_net_weight = get_session_state_value("Sampling Plan Green", "total_net_weight")
            average_of_net_weight = get_session_state_value("Sampling Plan Green", "average_of_net_weight")

            draw.text((200, 300), f"{product_name}", font=font, fill="black") # Fake Coordinates, you must change these
            draw.text((400, 300), f"{size_caliber}", font=font, fill="black") # Fake Coordinates, you must change these
            draw.text((600, 300), f"{sampling_plan}", font=font, fill="black") # Fake Coordinates, you must change these
            draw.text((800, 300), f"{qty_of_bags}", font=font, fill="black") # Fake Coordinates, you must change these
            draw.text((200, 400), f"{empty_weight_of_bag}", font=font, fill="black") # Fake Coordinates, you must change these
            draw.text((200, 500), f"{total_gross_weight}", font=font, fill="black") # Fake Coordinates, you must change these
            draw.text((200, 600), f"{total_net_weight}", font=font, fill="black") # Fake Coordinates, you must change these
            draw.text((200, 700), f"{average_of_net_weight}", font=font, fill="black") # Fake Coordinates, you must change these

            for i in range(1, 6):
                gross_weight = get_session_state_value("Sampling Plan Green", f"gross_weight_bag_{i}")
                net_weight = get_session_state_value("Sampling Plan Green", f"net_weight_bag_{i}")
                draw.text((300 + (i*100), 400), f"{gross_weight}", font=font, fill="black") # Fake Coordinates, you must change these
                draw.text((300 + (i*100), 500), f"{net_weight}", font=font, fill="black") # Fake Coordinates, you must change these

        elif form_type == "templates_4":
            # Sampling Plan Black
            product_name = get_session_state_value("Sampling Plan Black", "product_name")
            size_caliber = get_session_state_value("Sampling Plan Black", "size_caliber")
            sampling_plan = get_session_state_value("Sampling Plan Black", "sampling_plan")
            qty_of_bags = get_session_state_value("Sampling Plan Black", "qty_of_bags")
            empty_weight_of_bag = get_session_state_value("Sampling Plan Black", "empty_weight_of_bag")
            total_gross_weight = get_session_state_value("Sampling Plan Black", "total_gross_weight")
            total_net_weight = get_session_state_value("Sampling Plan Black", "total_net_weight")
            average_of_net_weight = get_session_state_value("Sampling Plan Black", "average_of_net_weight")

            draw.text((200, 300), f"{product_name}", font=font, fill="black") # Fake Coordinates, you must change these
            draw.text((400, 300), f"{size_caliber}", font=font, fill="black") # Fake Coordinates, you must change these
            draw.text((600, 300), f"{sampling_plan}", font=font, fill="black") # Fake Coordinates, you must change these
            draw.text((800, 300), f"{qty_of_bags}", font=font, fill="black") # Fake Coordinates, you must change these
            draw.text((200, 400), f"{empty_weight_of_bag}", font=font, fill="black") # Fake Coordinates, you must change these
            draw.text((200, 500), f"{total_gross_weight}", font=font, fill="black") # Fake Coordinates, you must change these
            draw.text((200, 600), f"{total_net_weight}", font=font, fill="black") # Fake Coordinates, you must change these
            draw.text((200, 700), f"{average_of_net_weight}", font=font, fill="black") # Fake Coordinates, you must change these

            for i in range(1, 6):
                gross_weight = get_session_state_value("Sampling Plan Black", f"gross_weight_bag_{i}")
                net_weight = get_session_state_value("Sampling Plan Black", f"net_weight_bag_{i}")
                draw.text((300 + (i*100), 400), f"{gross_weight}", font=font, fill="black") # Fake Coordinates, you must change these
                draw.text((300 + (i*100), 500), f"{net_weight}", font=font, fill="black") # Fake Coordinates, you must change these

        elif form_type == "templates_5":
            # Defect Assessment Green
            product_name = get_session_state_value("Defect Assessment Green", "product_name")
            size = get_session_state_value("Defect Assessment Green", "size")

            draw.text((200, 300), f"{product_name}", font=font, fill="black") # Fake Coordinates, you must change these
            draw.text((400, 300), f"{size}", font=font, fill="black") # Fake Coordinates, you must change these

            defect_types = ["Serious", "Major1", "Major2", "Major3", "Minor", "Shattering"]
            y_offset = 400 #Starting Y coordinate
            for defect in defect_types:
                detail = get_session_state_value("Defect Assessment Green", f"detail_{defect}")
                weight = get_session_state_value("Defect Assessment Green", f"weight_{defect}")
                percentage = get_session_state_value("Defect Assessment Green", f"percentage_{defect}")
                draw.text((300, y_offset), f"{detail}", font=font, fill="black") # Fake Coordinates, you must change these
                draw.text((500, y_offset), f"{weight}", font=font, fill="black") # Fake Coordinates, you must change these
                draw.text((700, y_offset), f"{percentage}", font=font, fill="black") # Fake Coordinates, you must change these
                y_offset += 100 # Increment Y for the next defect

        elif form_type == "templates_6":
            # Defect Assessment Black
            product_name = get_session_state_value("Defect Assessment Black", "product_name")
            size = get_session_state_value("Defect Assessment Black", "size")

            draw.text((200, 300), f"{product_name}", font=font, fill="black") # Fake Coordinates, you must change these
            draw.text((400, 300), f"{size}", font=font, fill="black") # Fake Coordinates, you must change these

            defect_types = ["Serious", "Major1", "Major2", "Major3", "Minor", "Shattering"]
            y_offset = 400 #Starting Y coordinate
            for defect in defect_types:
                detail = get_session_state_value("Defect Assessment Black", f"detail_{defect}")
                weight = get_session_state_value("Defect Assessment Black", f"weight_{defect}")
                percentage = get_session_state_value("Defect Assessment Black", f"percentage_{defect}")
                draw.text((300, y_offset), f"{detail}", font=font, fill="black") # Fake Coordinates, you must change these
                draw.text((500, y_offset), f"{weight}", font=font, fill="black") # Fake Coordinates, you must change these
                draw.text((700, y_offset), f"{percentage}", font=font, fill="black") # Fake Coordinates, you must change these
                y_offset += 100 # Increment Y for the next defect


        # Only display the preview when preview_only is True
        if preview_only:
            st.image(image, caption="Xem Trước Đơn", width=None)  # width=None to keep original size

        if return_image:
            return image

    except Exception as e:
        st.error(f"Lỗi khi tạo bản xem trước: {str(e)}")
        if return_image:
            return None