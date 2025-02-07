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

# Cấu hình trang Streamlit
st.set_page_config(
    page_title="Báo Cáo Kết Quả Học Tập Trải Nghiệm Ngoài Trường",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Render sidebar (Quản lý Sidebar)
sidebar = SidebarManager()
sidebar.render_sidebar()

class ResourceManager:
    def __init__(self):
        self.base_dir = self.get_absolute_path()
        self.image_dir = self.base_dir / "images"
        self.font_dir = self.base_dir / "fonts"
        
        # Thiết lập đường dẫn file
        self.paths = {
            "MauHoSo": self.image_dir / "studywork003.png",  # "Mẫu đơn đăng ký": đường dẫn đến hình ảnh mẫu đơn đăng ký
            "MauDinhKem": self.image_dir / "studywork002.png",    # "Mẫu phụ lục": đường dẫn đến hình ảnh mẫu phụ lục (nếu cần)
            "Logo": self.image_dir / "logo.png",               # "Logo": đường dẫn đến hình ảnh logo trường
            #"Font": self.font_dir / "AppleGothic.ttf"            # "Phông chữ": đường dẫn đến file phông chữ
        }

    @staticmethod
    def get_absolute_path():
        """Lấy đường dẫn tuyệt đối cho ứng dụng."""
        if os.path.exists("/mount/src/study-work"):
            return pathlib.Path("/mount/src/study-work")
        elif os.path.exists("/workspaces/Study-work"):
            return pathlib.Path("/workspaces/Study-work")
        else:
            return pathlib.Path(__file__).parent.parent.resolve()

    def get_font_path(self):
        """Tìm và trả về đường dẫn file phông chữ."""
        if self.paths["폰트"].exists():
            return str(self.paths["폰트"])
        
        for system_font in self.system_font_paths:
            if os.path.exists(system_font):
                return system_font
        
        st.error("Không tìm thấy file phông chữ.")
        st.info("Hãy cài đặt phông chữ NanumGothic hoặc thêm file phông chữ vào thư mục fonts.")
        st.stop()

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

# Tạo instance ResourceManager
resources = ResourceManager()

# In thông tin debug (nếu cần)
if os.getenv('STREAMLIT_DEBUG') == 'true':
    resources.print_debug_info()

# Kiểm tra tài nguyên
resources.validate_resources()

# Thiết lập đường dẫn toàn cục
BASE_DIR = resources.base_dir
IMAGE_DIR = resources.image_dir
FONT_DIR = resources.font_dir
img_path = resources.paths["신청서 양식"]
extra_img_path = resources.paths["별지 양식"]
logo_path = resources.paths["로고"]
font_path = resources.font_path

# In đường dẫn để debug
if os.getenv('STREAMLIT_DEBUG') == 'true':
    st.write(f"""
    Đường dẫn đã thiết lập:
    - Đường dẫn cơ sở: {BASE_DIR}
    - Đường dẫn ảnh: {IMAGE_DIR}
    - Đường dẫn phông chữ: {FONT_DIR}
    - Mẫu đơn đăng ký: {img_path}
    - Mẫu phụ lục: {extra_img_path}
    - Logo: {logo_path}
    - Phông chữ: {font_path}
    """)

# 1. Sửa đổi phần khởi tạo trạng thái phiên
if 'student_canvas_key' not in st.session_state:
    st.session_state.student_canvas_key = 0
    st.session_state.student_canvas_initialized = False  # Cờ khởi tạo mới
if 'guardian_canvas_key' not in st.session_state:
    st.session_state.guardian_canvas_key = 100
    st.session_state.guardian_canvas_initialized = False  # Cờ khởi tạo mới
if 'student_signature_img' not in st.session_state:
    st.session_state.student_signature_img = None
if 'guardian_signature_img' not in st.session_state:
    st.session_state.guardian_signature_img = None

# Khởi tạo phiên cho bước hiện tại
if 'step' not in st.session_state:
    st.session_state.step = 1

# Khởi tạo để lưu kế hoạch học tập trải nghiệm ngoài trường
if 'plans' not in st.session_state:
    st.session_state.plans = {}

# Hiển thị tiêu đề chính
st.markdown("<h1 style='text-align: center;'>Báo Cáo Kết Quả Học Tập Trải Nghiệm Ngoài Trường</h1>", unsafe_allow_html=True)

# Xử lý ảnh logo
def get_base64_image(image_path):
    try:
        with open(image_path, "rb") as img_file:
            encoded = base64.b64encode(img_file.read()).decode()
        return encoded
    except FileNotFoundError:
        return None

# Hiển thị logo
logo_base64 = get_base64_image(logo_path) if logo_path.exists() else None

# Hiển thị logo và tên trường (như một tiêu đề phụ)
if logo_base64:
    st.markdown(f"""
        <div style="display: flex; align-items: center; justify-content: center;">
            <img src="data:image/png;base64,{logo_base64}" alt="Logo" style="margin-right: 10px; width: 40px; height: 40px;">
            <h3 style="margin: 0;">Trường THPT Onyang Hanool</h3>
        </div>
    """, unsafe_allow_html=True)
else:
    st.markdown("<h3 style='text-align: center;'>Trường THPT Onyang Hanool</h3>", unsafe_allow_html=True)

# Tạo các tab
tabs = st.tabs([
    "1. Nhập Thông Tin Học Sinh",
    "2. Thông Tin Đăng Ký",
    "3. Lịch Trình Học Tập",  # Phần nhập bảng Excel
    "4. Thông Tin Người Giám Hộ",
    "5. Nhập Chữ Ký",
    "6. Tải Ảnh Lên",
    "7. Xem Báo Cáo Kết Quả"
])

# Tab 1: Nhập thông tin học sinh
with tabs[0]:
    st.header("Nhập Thông Tin Học Sinh")
    st.text_input('Họ và Tên', key='student_name')  # key duy nhất
    st.selectbox('Lớp', ['Chọn lớp', 'Lớp 10', 'Lớp 11', 'Lớp 12'], key='student_grade')
    st.selectbox('Tổ', ['Chọn tổ'] + [f'Tổ {i}' for i in range(1, 13)], key='student_class')
    st.number_input('Số thứ tự', min_value=1, max_value=50, step=1, key='student_number')

# Tab 2: Nhập thông tin đăng ký
with tabs[1]:
    st.header("Nhập Thông Tin Đăng Ký Học Tập Trải Nghiệm Ngoài Trường")

    # Hai cột cho ngày bắt đầu và ngày kết thúc
    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input('Ngày Bắt Đầu',
                                 value=date.today(),
                                 min_value=date.today() - timedelta(days=365),  # Chọn tối đa 1 năm trước
                                 max_value=date.today(),  # Chọn tối đa đến hôm nay
                                 key='start_date')
    with col2:
        end_date = st.date_input('Ngày Kết Thúc',
                               value=start_date,
                               min_value=start_date,
                               max_value=date.today(),  # Chọn tối đa đến hôm nay
                               key='end_date')

    # Thêm giải thích cho ngày bắt đầu/kết thúc được công nhận
    st.markdown("""
    **Hướng dẫn Nhập Khoảng Thời Gian Được Công Nhận Đi Học**

    Hãy nhập khoảng thời gian được công nhận đi học bằng cách loại trừ 'ngày lễ' khỏi khoảng thời gian học tập trải nghiệm ngoài trường.
    Nếu ngày kết thúc học tập trải nghiệm ngoài trường là 'Chủ Nhật', hãy nhập khoảng thời gian được công nhận đi học đến 'Thứ Sáu'.
    """)

    # Hai cột cho ngày bắt đầu và ngày kết thúc được công nhận
    col3, col4 = st.columns(2)
    with col3:
        attendance_start_date = st.date_input('Ngày Bắt Đầu Được Công Nhận',
                                           value=start_date,
                                           min_value=date.today() - timedelta(days=365),  # Chọn tối đa 1 năm trước
                                           max_value=date.today(),  # Chọn tối đa đến hôm nay
                                           key='attendance_start_date')
    with col4:
        attendance_end_date = st.date_input('Ngày Kết Thúc Được Công Nhận',
                                         value=attendance_start_date,
                                         min_value=attendance_start_date,
                                         max_value=date.today(),  # Chọn tối đa đến hôm nay
                                         key='attendance_end_date')

    # Chọn hình thức học tập
    st.selectbox(
        'Chọn Hình Thức Học Tập',
        ['Chọn hình thức học tập', 'Du lịch cùng gia đình', 'Tham dự và thăm viếng sự kiện gia đình', 'Khám phá di tích', 'Du lịch văn học',
         'Trải nghiệm văn hóa trong nước và thế giới', 'Hành hương', 'Khám phá thiên nhiên', 'Trải nghiệm nghề nghiệp', 'Khác'],
        key='learning_type'
    )

    # Nhập mục đích và địa điểm
    st.text_input('Mục Đích', key='purpose')
    st.text_input('Địa Điểm', key='destination')

# Tab 3: Nhập Kế hoạch học tập (thêm động dựa trên form)
with tabs[2]:
    st.header("Nhập Lịch Trình Học Tập Trải Nghiệm Ngoài Trường")

    # Thêm đoạn văn giải thích
    st.markdown('<p style="color: red; font-size: small;">Nhập lịch trình và nhấn nút thêm để tạo kế hoạch</p>', unsafe_allow_html=True)

    start_date = st.session_state.get('start_date')
    end_date = st.session_state.get('end_date')

    if start_date and end_date:
        # Tạo danh sách ngày
        date_list = []
        current_date = start_date
        while current_date <= end_date:
            date_str = f"Ngày {(current_date - start_date).days + 1} ({current_date.strftime('%m/%d')})"
            date_list.append(date_str)
            current_date += timedelta(days=1)

        # Khởi tạo plans
        if 'plans' not in st.session_state:
            st.session_state.plans = {}

        # Container cho form nhập
        with st.container():
            # Dropdown chọn ngày
            selected_date = st.selectbox(
                "Chọn Ngày",
                date_list,
                key="selected_date"
            )

            # Widget chọn thời gian
            col1, col2, col3 = st.columns(3)
            with col1:
                # Tạo các tùy chọn thời gian (cách nhau 30 phút)
                time_options = []
                for hour in range(24):
                    for minute in [0, 30]:
                        time_str = f"{hour:02d}:{minute:02d}"
                        time_options.append(time_str)

                # Thiết lập giá trị mặc định là 9:00
                default_index = time_options.index("09:00")

                selected_time = st.selectbox(
                    "Thời Gian",
                    options=time_options,
                    index=default_index,
                    key="input_time"
                )

            with col2:
                location = st.text_input("Địa Điểm", key="input_location")
            with col3:
                activity = st.text_input("Nội Dung Hoạt Động", key="input_activity")

            # Nút thêm lịch trình
            if st.button("Thêm Lịch Trình"):
                day_key = selected_date.split()[0]  # Trích xuất dạng "Ngày 1"

                if day_key not in st.session_state.plans:
                    st.session_state.plans[day_key] = []

                new_plan = {
                    "Thời Gian": selected_time,
                    "Địa Điểm": location,
                    "Nội Dung Hoạt Động": activity
                }

                # Thêm lịch trình mới vào kế hoạch của ngày đó
                st.session_state.plans[day_key].append(new_plan)

                # Sắp xếp theo thời gian
                st.session_state.plans[day_key] = sorted(
                    st.session_state.plans[day_key],
                    key=lambda x: x['Thời Gian']
                )

                st.success(f"Đã thêm lịch trình vào {selected_date}.")

        # Hiển thị lịch trình hiện tại
        st.markdown("### Lịch Trình Hiện Tại")

        if st.session_state.plans:
            # Chuẩn bị dữ liệu cho dataframe
            df_data = []
            for day_key, plans in sorted(st.session_state.plans.items()):
                day_num = int(''.join(filter(str.isdigit, day_key)))
                current_date = start_date + timedelta(days=day_num - 1)
                date_str = current_date.strftime("%m/%d")

                # Sắp xếp kế hoạch của mỗi ngày theo thời gian
                sorted_plans = sorted(plans, key=lambda x: x['Thời Gian'])

                for plan in sorted_plans:
                    df_data.append({
                        "Ngày": f"{day_key} ({date_str})",
                        "Thời Gian": plan['Thời Gian'],
                        "Địa Điểm": plan['Địa Điểm'],
                        "Nội Dung Hoạt Động": plan['Nội Dung Hoạt Động']
                    })

            if df_data:
                df = pd.DataFrame(df_data)

                # Phân tách hoàn toàn hiển thị dataframe và UI xóa
                if df_data:
                    # 1. Phần hiển thị DataFrame
                    if len(df) > 15:
                        df1 = df.iloc[:15]
                        df2 = df.iloc[15:]

                        col1, col2 = st.columns(2)
                        with col1:
                            st.dataframe(
                                df1,
                                hide_index=True,
                                column_config={
                                    "Ngày": st.column_config.TextColumn("Ngày", width="medium"),
                                    "Thời Gian": st.column_config.TextColumn("Thời Gian", width="small"),
                                    "Địa Điểm": st.column_config.TextColumn("Địa Điểm", width="medium"),
                                    "Nội Dung Hoạt Động": st.column_config.TextColumn("Nội Dung Hoạt Động", width="large"),
                                }
                            )
                        with col2:
                            st.dataframe(
                                df2,
                                hide_index=True,
                                column_config={
                                    "Ngày": st.column_config.TextColumn("Ngày", width="medium"),
                                    "Thời Gian": st.column_config.TextColumn("Thời Gian", width="small"),
                                    "Địa Điểm": st.column_config.TextColumn("Địa Điểm", width="medium"),
                                    "Nội Dung Hoạt Động": st.column_config.TextColumn("Nội Dung Hoạt Động", width="large"),
                                }
                            )
                    else:
                        st.dataframe(
                            df,
                            hide_index=True,
                            column_config={
                                "Ngày": st.column_config.TextColumn("Ngày", width="medium"),
                                "Thời Gian": st.column_config.TextColumn("Thời Gian", width="small"),
                                "Địa Điểm": st.column_config.TextColumn("Địa Điểm", width="medium"),
                                "Nội Dung Hoạt Động": st.column_config.TextColumn("Nội Dung Hoạt Động", width="large"),
                            }
                        )

                    # 2. Phần UI xóa (tách biệt trong container riêng)
                    with st.container():
                        st.markdown("---")  # Đường phân cách
                        st.markdown("### Xóa Lịch Trình")

                        # Chọn lịch trình để xóa
                        delete_options = [f"{plan['Ngày']} - {plan['Thời Gian']} - {plan['Địa Điểm']} - {plan['Nội Dung Hoạt Động']}" for plan in df_data]
                        selected_plan_to_delete = st.selectbox(
                            "Chọn Lịch Trình Muốn Xóa",
                            delete_options,
                            key="selected_plan_to_delete"
                        )

                        # Nút xóa và logic
                        if st.button("Xóa Lịch Trình Đã Chọn", key="delete_plan_button"):
                            day_info = selected_plan_to_delete.split(" - ")[0]
                            time_info = selected_plan_to_delete.split(" - ")[1]
                            day_key = day_info.split(" ")[0]

                            if day_key in st.session_state.plans:
                                st.session_state.plans[day_key] = [
                                    plan for plan in st.session_state.plans[day_key]
                                    if plan['Thời Gian'] != time_info
                                ]

                                if not st.session_state.plans[day_key]:
                                    del st.session_state.plans[day_key]

                                st.success("Đã xóa lịch trình đã chọn.")
                                st.rerun()
                else:
                    st.info("Không có lịch trình nào được đăng ký.")

            else:
                st.warning("Hãy thiết lập ngày bắt đầu và ngày kết thúc học tập trải nghiệm ngoài trường.")

    else:
        st.warning("Hãy thiết lập ngày bắt đầu và ngày kết thúc học tập trải nghiệm ngoài trường.")

# Tab Nhập thông tin người giám hộ
with tabs[3]:
    st.header("Nhập Thông Tin Người Giám Hộ")

    # Thông tin người giám hộ
    col1, col2, col3 = st.columns(3)
    with col1:
        guardian_name = st.text_input('Tên Người Giám Hộ', key='guardian_name')
    with col2:
        guardian_relationship = st.text_input('Quan Hệ (với người giám hộ)', key='guardian_relationship')
    with col3:
        guardian_contact = st.text_input('Liên Hệ (người giám hộ)', key='guardian_contact')

    # Hàng thông tin người hướng dẫn
    col4, col5, col6 = st.columns(3)
    with col4:
        chaperone_name = st.text_input('Tên Người Hướng Dẫn', key='chaperone_name')
    with col5:
        chaperone_relationship = st.text_input('Quan Hệ (với người hướng dẫn)', key='chaperone_relationship')
    with col6:
        chaperone_contact = st.text_input('Liên Hệ (người hướng dẫn)', key='chaperone_contact')

# Triển khai Tab Chữ ký
with tabs[4]:
    st.header("Chữ Ký Cuối Cùng")

        # Đoạn văn giải thích
    st.markdown('<p style="color: black; font-size: small;">Nếu canvas chữ ký không hiển thị, hãy nhấn nút [Tải Canvas Chữ Ký]</p>', unsafe_allow_html=True)

    # Sửa đổi các hàm reset canvas
    def reset_student_canvas():
        st.session_state.student_canvas_key += 1
        st.session_state.student_signature_img = None
        st.session_state.student_canvas_initialized = True

    def reset_guardian_canvas():
        st.session_state.guardian_canvas_key += 1
        st.session_state.guardian_signature_img = None
        st.session_state.guardian_canvas_initialized = True

    # Logic khởi tạo tự động
    if not st.session_state.student_canvas_initialized:
        reset_student_canvas()
        st.rerun()

    if not st.session_state.guardian_canvas_initialized:
        reset_guardian_canvas()
        st.rerun()

    # Phần Chữ ký của Học sinh
    st.markdown("### Chữ Ký Học Sinh")
    col1, col2 = st.columns([4, 1])

    with col1:
        canvas_key = f"student_signature_canvas_{st.session_state.student_canvas_key}"
        student_canvas = st_canvas(
            fill_color="rgba(0, 0, 0, 0)",
            stroke_width=2,
            stroke_color="#000000",
            background_color="rgba(0, 0, 0, 0)",
            height=150,
            width=400,
            drawing_mode="freedraw",
            key=canvas_key
        )

        if student_canvas.image_data is not None:
            st.session_state.student_signature_img = student_canvas.image_data

    with col2:
        if st.button("Tải Canvas Chữ Ký", key=f"reset_student_btn_{st.session_state.student_canvas_key}"):
            reset_student_canvas()
            st.rerun()

    if st.session_state.student_signature_img is not None:
        st.markdown("✅ Hãy nhập chữ ký của học sinh.")

    # Thêm đường phân cách
    st.markdown("---")

    # Phần Chữ ký của Người Giám Hộ
    st.markdown("### Chữ Ký Người Giám Hộ")
    col3, col4 = st.columns([4, 1])

    with col3:
        # Sửa đổi key canvas của người giám hộ theo cách tương tự
        guardian_canvas_key = f"guardian_signature_canvas_{st.session_state.guardian_canvas_key}"
        guardian_canvas = st_canvas(
            fill_color="rgba(0, 0, 0, 0)",
            stroke_width=2,
            stroke_color="#000000",
            background_color="rgba(0, 0, 0, 0)",
            height=150,
            width=400,
            drawing_mode="freedraw",
            key=guardian_canvas_key
        )

        if guardian_canvas.image_data is not None:
            st.session_state.guardian_signature_img = guardian_canvas.image_data

    with col4:
        if st.button("Tải Canvas Chữ Ký", key=f"reset_guardian_btn_{st.session_state.guardian_canvas_key}"):
            reset_guardian_canvas()
            st.rerun()

    if st.session_state.guardian_signature_img is not None:
        st.markdown("✅ Hãy nhập chữ ký của người giám hộ.")

    # Xác nhận Hoàn thành Chữ ký
    if st.session_state.student_signature_img is not None and st.session_state.guardian_signature_img is not None:
        st.success("✅ Sau khi hoàn thành tất cả chữ ký, hãy chuyển sang bước tiếp theo.")

# Tab tải ảnh lên
with tabs[5]:  # Tab thứ 5 (chỉ số bắt đầu từ 0)
    st.header("Tải Ảnh Lên")

    # Hộp giải thích gọn gàng
    st.markdown("""
        <div style="
            background-color: #f8f9fa;
            border-radius: 10px;
            padding: 20px;
            margin: 20px auto;
            max-width: 600px;
            text-align: center;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        ">
            <div style="color: #1f1f1f; font-size: 1.1em; margin-bottom: 8px;">
                📸 Đính kèm ảnh cho báo cáo kết quả học tập trải nghiệm
            </div>
            <div style="color: #666; font-size: 0.9em;">
                Bạn có thể tải lên tối đa 4 ảnh
            </div>
        </div>
    """, unsafe_allow_html=True)

    # Khởi tạo danh sách để lưu trữ ảnh đã tải lên
    if 'uploaded_photos' not in st.session_state:
        st.session_state.uploaded_photos = []

    # Tạo 4 bộ tải file lên
    for i in range(4):
        uploaded_file = st.file_uploader(
            f"Chọn Ảnh {i+1}",
            type=["png", "jpg", "jpeg"],
            key=f"uploader_{i}"
        )

        if uploaded_file is not None:
            # Tạo cột để hiển thị ảnh
            col1, col2 = st.columns([3, 1])

            with col1:
                image = Image.open(uploaded_file)
                st.image(image, caption=f"Ảnh {i+1}", width=800)

            with col2:
                # Nút xóa
                if st.button(f"Xóa", key=f"delete_{i}"):
                    st.session_state[f"uploader_{i}"] = None
                    st.rerun()

            # Lưu vào session_state
            if uploaded_file not in st.session_state.uploaded_photos:
                if len(st.session_state.uploaded_photos) < 4:
                    st.session_state.uploaded_photos.append(uploaded_file)

    # Hiển thị số lượng ảnh đã tải lên
    num_uploaded = len([f for f in st.session_state.uploaded_photos if f is not None])
    st.info(f"Đã tải lên {num_uploaded}/4 ảnh.")

    # Nút xóa tất cả ảnh
    if num_uploaded > 0:
        if st.button("Xóa Tất Cả Ảnh"):
            st.session_state.uploaded_photos = []
            for i in range(4):
                st.session_state[f"uploader_{i}"] = None
            st.rerun()

# Tab xem báo cáo kết quả
with tabs[6]:
    st.header("Xem Báo Cáo Kết Quả")

    # Thêm hộp giải thích gọn gàng
    st.markdown("""
        <div style="
            background-color: #f8f9fa;
            border-radius: 10px;
            padding: 20px;
            margin: 20px auto;
            max-width: 600px;
            text-align: center;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        ">
            <div style="color: #1f1f1f; font-size: 1.1em; margin-bottom: 8px;">
                📄 Tải file PDF đã tạo và nộp cho giáo viên chủ nhiệm
            </div>
            <div style="color: #666; font-size: 0.9em;">
                Xem lại báo cáo kết quả và tải xuống
            </div>
        </div>
    """, unsafe_allow_html=True)

    # Thiết lập đường dẫn file ảnh
    img_path = IMAGE_DIR / "studywork003.png"
    extra_img_path = IMAGE_DIR / "studywork002.png"  # Ảnh mẫu phụ lục

    # Kiểm tra tính hợp lệ của dữ liệu bắt buộc
    required_fields = [
        "student_name", "student_grade", "student_class", "student_number",
        "start_date", "end_date", "attendance_start_date", "attendance_end_date", "plans"
    ]
    missing_fields = [field for field in required_fields if field not in st.session_state or not st.session_state[field]]

    if missing_fields:
        st.error(f"Các mục bắt buộc sau còn thiếu: {', '.join(missing_fields)}")
    else:
        try:
            # Xác minh sự tồn tại của file ảnh
            if not img_path.exists():
                st.error("Không tìm thấy ảnh mẫu đơn đăng ký.")
                st.stop()

            # Tải và thiết lập ảnh
            image = Image.open(img_path).convert("RGBA")
            draw = ImageDraw.Draw(image)

            # Thiết lập đường dẫn file font và xử lý dự phòng
            font_paths = [
                pathlib.Path("fonts/AppleGothic.ttf"),  # Mac AppleGothic
                pathlib.Path("fonts/AppleGothic.ttf"),  # Mac AppleGothic
                FONT_DIR / "AppleGothic.ttf",
                pathlib.Path("/fonts/NanumGothic.ttf"),  # Linux
                pathlib.Path("fonts\\malgun.ttf"),  # Windows
            ]

            font_path = None
            for path in font_paths:
                if path.exists():
                    font_path = path
                    break

            if font_path is None:
                st.error("""
                Không tìm thấy file font.
                Bạn có thể giải quyết bằng một trong các cách sau:
                1. Cài đặt font AppleGothic trên Mac OS
                2. Thêm file AppleGothic.ttf vào thư mục fonts của dự án
                """)
                st.stop()

            font = ImageFont.truetype(str(font_path), size=55)

            # Logic tính toán ngày (học tập trải nghiệm ngoài trường)
            start_date = st.session_state.get("start_date")
            end_date = st.session_state.get("end_date")

            today = date.today()  # Ngày nộp
            submit_date_formatted = today.strftime("%Y năm %m tháng %d ngày")

            try:
                if isinstance(start_date, datetime.date) and isinstance(end_date, datetime.date):
                    duration = (end_date - start_date).days + 1  # Bao gồm ngày bắt đầu và ngày kết thúc
                    start_date_formatted = start_date.strftime("%Y năm %m tháng %d ngày")
                    end_date_formatted = end_date.strftime("%Y năm %m tháng %d ngày")
                else:
                    raise ValueError("Ngày bắt đầu và ngày kết thúc không đúng định dạng ngày.")
            except Exception as e:
                st.error(f"Lỗi trong quá trình tính toán ngày: {e}")
                st.stop()

            # Tính toán thời gian được công nhận đi học (loại trừ ngày lễ)
            attendance_start_date = st.session_state.get("attendance_start_date")
            attendance_end_date = st.session_state.get("attendance_end_date")

            try:
                kr_holidays = holidays.KR(years=attendance_start_date.year)  # Ngày lễ của Hàn Quốc trong năm đó
                attendance_days = [
                    attendance_start_date + timedelta(days=i)
                    for i in range((attendance_end_date - attendance_start_date).days + 1)
                    if (attendance_start_date + timedelta(days=i)) not in kr_holidays
                    and (attendance_start_date + timedelta(days=i)).weekday() < 5  # Loại trừ ngày cuối tuần
                ]
                attendance_duration = len(attendance_days)
                attendance_start_formatted = attendance_start_date.strftime("%Y năm %m tháng %d ngày")
                attendance_end_formatted = attendance_end_date.strftime("%Y năm %m tháng %d ngày")
            except Exception as e:
                st.error(f"Lỗi trong quá trình tính toán thời gian được công nhận đi học: {e}")
                st.stop()

            # Vẽ thông tin cơ bản
            draw.text((750, 590), st.session_state.get("student_name", ""), fill="black", font=font)  # Tên học sinh
            draw.text((1830, 590), st.session_state.get("student_grade", "").replace('학년', ''), fill="black", font=font)  # Lớp (loại bỏ chữ "학년")
            draw.text((2020, 590), st.session_state.get("student_class", "").replace('반', ''), fill="black", font=font)  # Tổ (loại bỏ chữ "반")
            draw.text((2200, 590), str(st.session_state.get("student_number", "")), fill="black", font=font)  # Số thứ tự

            # Vẽ thời gian học tập trải nghiệm ngoài trường
            draw.text((1250, 690), start_date_formatted, fill="black", font=font)  # Ngày bắt đầu
            draw.text((1840, 690), end_date_formatted, fill="black", font=font)  # Ngày kết thúc
            draw.text((2400, 690), f"{duration}", fill="black", font=font)  # Tổng số ngày

            # Vẽ thời gian được công nhận đi học
            draw.text((1250, 800), attendance_start_formatted, fill="black", font=font)  # Ngày bắt đầu
            draw.text((1850, 800), attendance_end_formatted, fill="black", font=font)  # Ngày kết thúc
            draw.text((2400, 800), f"{attendance_duration}", fill="black", font=font)  # Tổng số ngày
            draw.text((1250, 3350), submit_date_formatted, fill="black", font=font)  # Ngày nộp (thêm vào)

            # Điều chỉnh vị trí của '0' theo hình thức học tập
            learning_type = st.session_state.get("learning_type", "")  # Lấy hình thức học tập đã chọn
            if learning_type == "가족 동반 여행":  # Du lịch cùng gia đình
                draw.text((940, 875), "0", fill="black", font=font)
            elif learning_type == "친인척 경조사 참석 및 방문":  # Tham dự và thăm viếng sự kiện gia đình
                draw.text((1700, 875), "0", fill="black", font=font)
            elif learning_type == "유적 탐방":  # Khám phá di tích
                draw.text((2075, 875), "0", fill="black", font=font)
            elif learning_type == "문학 기행":  # Du lịch văn học
                draw.text((2450, 875), "0", fill="black", font=font)
            elif learning_type == "우리 문화 및 세계 문화 체험":  # Trải nghiệm văn hóa trong nước và thế giới
                draw.text((1235, 945), "0", fill="black", font=font)
            elif learning_type == "국토 순례":  # Hành hương
                draw.text((1590, 945), "0", fill="black", font=font)
            elif learning_type == "자연 탐사":  # Khám phá thiên nhiên
                draw.text((1970, 945), "0", fill="black", font=font)
            elif learning_type == "직업 체험":  # Trải nghiệm nghề nghiệp
                draw.text((2350, 945), "0", fill="black", font=font)
            elif learning_type == "기타":  # Khác
                draw.text((2620, 945), "0", fill="black", font=font)
            else:
                draw.text((300, 460), "학습 태를 선택하세요", fill="red", font=font)  # Nhắc chọn hình thức học tập

            draw.text((580, 1050), st.session_state.get("purpose", ""), fill="black", font=font)  # Mục đích
            draw.text((580, 1200), st.session_state.get("destination", ""), fill="black", font=font)  # Địa điểm
            draw.text((710, 1330), st.session_state.get("guardian_name", ""), fill="black", font=font)  # Tên người giám hộ
            draw.text((2150, 1330), st.session_state.get("guardian_contact", ""), fill="black", font=font)  # Liên hệ người giám hộ
            draw.text((710, 1470), st.session_state.get("chaperone_name", ""), fill="black", font=font)  # Tên người hướng dẫn
            draw.text((2150, 1470), st.session_state.get("chaperone_contact", ""), fill="black", font=font)  # Liên hệ người hướng dẫn
            draw.text((1540, 1330), st.session_state.get("guardian_relationship", ""), fill="black", font=font)  # Quan hệ với người giám hộ
            draw.text((1540, 1470), st.session_state.get("chaperone_relationship", ""), fill="black", font=font)  # Quan hệ với người hướng dẫn
            draw.text((2250, 3460), st.session_state.get("student_name", ""), fill="black", font=font)  # Tên học sinh (chỗ chữ ký)
            draw.text((2250, 3600), st.session_state.get("guardian_name", ""), fill="black", font=font)  # Tên người giám hộ (chỗ chữ ký)

            def add_signatures(image):
                """Hàm hỗ trợ thêm hình ảnh chữ ký vào đơn đăng ký"""
                if 'student_signature_img' in st.session_state:  # Nếu có chữ ký học sinh
                    student_signature_img = Image.fromarray(np.array(st.session_state['student_signature_img']).astype('uint8')).convert("RGBA")
                    new_size = (int(student_signature_img.width), int(student_signature_img.height))  # Lấy kích thước mới
                    student_signature_img = student_signature_img.resize(new_size, Image.Resampling.LANCZOS)  # Thay đổi kích thước
                    image.paste(student_signature_img, (2400, 3450), student_signature_img)  # Dán chữ ký vào ảnh

                if 'guardian_signature_img' in st.session_state:  # Nếu có chữ ký người giám hộ
                    guardian_signature_img = Image.fromarray(np.array(st.session_state['guardian_signature_img']).astype('uint8')).convert("RGBA")
                    new_size = (int(guardian_signature_img.width), int(guardian_signature_img.height))  # Lấy kích thước mới
                    guardian_signature_img = guardian_signature_img.resize(new_size, Image.Resampling.LANCZOS)  # Thay đổi kích thước
                    image.paste(guardian_signature_img, (2400, 3600), guardian_signature_img)  # Dán chữ ký vào ảnh

            # Khởi tạo biến để xử lý dữ liệu kế hoạch học tập
            x_start, y_start = 180, 1800  # Vị trí bắt đầu của ô đầu tiên
            max_y = 3150
            font_size = 50
            min_font_size = 30
            extra_needed = False  # Cần phụ lục hay không
            first_section_plans = []  # Kế hoạch cho phần đầu tiên
            second_section_plans = []  # Kế hoạch cho phần thứ hai
            remaining_plans = []  # Kế hoạch còn lại (cho phụ lục)

            if 'plans' in st.session_state and isinstance(st.session_state.plans, dict):  # Nếu có kế hoạch và là một dictionary
                # Tạo text kế hoạch tổng thể
                start_date = st.session_state.start_date
                sorted_days = sorted(
                    [(day_key, (start_date + timedelta(days=int(''.join(filter(str.isdigit, day_key))) - 1)))
                     for day_key in st.session_state.plans.keys()],
                    key=lambda x: x[1]  # Sắp xếp theo ngày
                )

                # Chia kế hoạch tổng thể thành hai phần
                first_section_plans = []
                second_section_plans = []
                total_plans = []

                # Thêm tất cả các kế hoạch vào total_plans và sắp xếp theo thời gian
                for day_key, date in sorted_days:
                    plans = st.session_state.plans.get(day_key, [])
                    for i, plan in enumerate(plans):
                        plan_data = {
                            'day': day_key if i == 0 else '',  # Chỉ hiển thị ngày ở mục đầu tiên của mỗi ngày
                            'time': plan.get('시간', ''),  # Thời gian
                            'location': plan.get('장소', ''),  # Địa điểm
                            'activity': plan.get('활동내용', '')  # Nội dung hoạt động
                        }
                        total_plans.append(plan_data)

                # Chia kế hoạch tổng thể thành hai phần
                half_length = len(total_plans) // 2
                if len(total_plans) % 2 != 0:
                    half_length += 1  # Nếu số lẻ, phần đầu tiên sẽ có thêm 1 mục

                first_section_plans = total_plans[:half_length]
                second_section_plans = total_plans[half_length:]

                # Thiết lập vị trí bắt đầu cột và khoảng cách dòng
                # Tọa độ của phần đầu tiên (cột bên trái)
                x_time_first = 800    # Vị trí bắt đầu của thời gian
                x_location_first = 1000  # Vị trí bắt đầu của địa điểm
                x_activity_first = 1300  # Vị trí bắt đầu của nội dung hoạt động

                # Tọa độ của phần thứ hai (cột bên phải)
                x_time_second = 1800   # Vị trí bắt đầu của thời gian
                x_location_second = 2000  # Vị trí bắt đầu của địa điểm
                x_activity_second = 2300  # Vị trí bắt đầu của nội dung hoạt động

                line_height = 70
                current_y = y_start

                # Vẽ phần đầu tiên (cột bên trái)
                current_y = y_start
                current_day = None
                x_start_first = 580  # Tọa độ X bắt đầu của cột bên trái
                x_start_second = 1600  # Tọa độ X bắt đầu của cột bên phải

                for plan in first_section_plans:
                    if current_y >= max_y:  # Nếu vượt quá giới hạn, chuyển sang cột bên phải
                        current_y = y_start
                        x_start_first = x_start_second
                        continue

                    if plan['day'] and plan['day'] != current_day:  # Nếu bắt đầu một ngày mới
                        if current_y != y_start:  # Nếu không phải ngày đầu tiên, thêm khoảng cách
                            current_y += line_height
                        current_day = plan['day']
                        draw.text((x_start_first, current_y), current_day, fill="black", font=font)  # Hiển thị ngày
                        current_y += line_height  # Xuống dòng sau khi hiển thị ngày

                    # Thời gian/Địa điểm/Nội dung hoạt động bắt đầu ở cùng tọa độ X với ngày
                    draw.text((x_start_first, current_y), plan['time'], fill="black", font=font)  # Thời gian
                    draw.text((x_start_first + 220, current_y), plan['location'], fill="black", font=font)  # Địa điểm
                    draw.text((x_start_first + 440, current_y), plan['activity'], fill="black", font=font)  # Nội dung hoạt động
                    current_y += line_height

                # Vẽ phần thứ hai (cột bên phải)
                current_y = y_start
                current_day = None
                x_start_second = 1600  # Tọa độ X bắt đầu của phần bên phải

                for plan in second_section_plans:
                    if current_y >= max_y:  # Nếu vượt quá max_y, chuyển sang phụ lục
                        remaining_plans.append(plan)
                        extra_needed = True
                        continue

                    if plan['day'] and plan['day'] != current_day:  # Nếu bắt đầu một ngày mới
                        if current_y != y_start:  # Nếu không phải ngày đầu tiên, thêm khoảng cách
                            current_y += line_height
                        current_day = plan['day']
                        draw.text((x_start_second, current_y), current_day, fill="black", font=font)  # Hiển thị ngày
                        current_y += line_height  # Xuống dòng sau khi hiển thị ngày

                    # Thời gian/Địa điểm/Nội dung hoạt động bắt đầu ở cùng tọa độ X với ngày
                    draw.text((x_start_second, current_y), plan['time'], fill="black", font=font)  # Thời gian
                    draw.text((x_start_second + 220, current_y), plan['location'], fill="black", font=font)  # Địa điểm
                    draw.text((x_start_second + 440, current_y), plan['activity'], fill="black", font=font)  # Nội dung hoạt động
                    current_y += line_height

                # Nếu cần phụ lục, tạo ảnh phụ lục
                if extra_needed and remaining_plans:
                    extra_image = Image.open(extra_img_path).convert("RGBA")  # Tải ảnh phụ lục
                    extra_draw = ImageDraw.Draw(extra_image)  # Đối tượng để vẽ lên ảnh phụ lục

                    # Điều chỉnh vị trí bắt đầu cho phụ lục
                    current_y = 700  # Bắt đầu dưới tiêu đề của phụ lục

                    # Viết tuần tự vào phụ lục, bắt đầu từ bên trái
                    x_day = 580  # Vị trí X của ngày
                    x_time = 800  # Vị trí X của thời gian
                    x_location = 1000  # Vị trí X của địa điểm
                    x_activity = 1200  # Vị trí X của nội dung hoạt động

                    # Viết tất cả các kế hoạch còn lại vào phụ lục
                    for plan in remaining_plans:
                        extra_draw.text((x_day, current_y), plan['day'], fill="black", font=font)  # Ngày
                        extra_draw.text((x_time, current_y), plan['time'], fill="black", font=font)  # Thời gian
                        extra_draw.text((x_location, current_y), plan['location'], fill="black", font=font)  # Địa điểm
                        extra_draw.text((x_activity, current_y), plan['activity'], fill="black", font=font)  # Nội dung hoạt động
                        current_y += line_height

                        # Dừng nếu đạt đến cuối phụ lục
                        if current_y >= 3000:  # Giới hạn chiều cao tối đa của phụ lục
                            st.warning("Kế hoạch quá nhiều, một số nội dung không được đưa vào phụ lục.")
                            break

                # Hiển thị ảnh đơn đăng ký cơ bản sau khi thêm chữ ký
                add_signatures(image)
                st.image(image, caption='Đơn Đăng Ký Học Tập Trải Nghiệm Ngoài Trường', width=800)

                # Tạo phụ lục và thêm ảnh
                try:
                    extra_image = Image.open(extra_img_path).convert("RGBA")  # Tải ảnh phụ lục
                    extra_draw = ImageDraw.Draw(extra_image)  # Đối tượng để vẽ lên ảnh phụ lục

                    # Lấy kích thước của phụ lục
                    page_width, page_height = extra_image.size

                    # Tính toán các phần tư (có xem xét lề)
                    margin = 50  # Lề
                    section_width = (page_width - (3 * margin)) // 2  # Chiều rộng của mỗi phần
                    section_height = (page_height - (3 * margin)) // 2  # Chiều cao của mỗi phần

                    # Tọa độ bắt đầu của mỗi phần
                    sections = [
                        (margin, margin),  # Góc trên bên trái
                        (margin * 2 + section_width, margin),  # Góc trên bên phải
                        (margin, margin * 2 + section_height),  # Góc dưới bên trái
                        (margin * 2 + section_width, margin * 2 + section_height)  # Góc dưới bên phải
                    ]

                    # Thêm ảnh
                    if 'uploaded_photos' in st.session_state:
                        for idx, photo in enumerate(st.session_state.uploaded_photos):  # Duyệt qua các ảnh đã tải lên
                            if idx < 4:  # Chỉ xử lý tối đa 4 ảnh
                                try:
                                    photo_img = Image.open(photo).convert("RGBA")  # Tải và chuyển đổi ảnh

                                    # Điều chỉnh kích thước ảnh cho phù hợp với phần
                                    photo_width, photo_height = photo_img.size  # Kích thước ảnh
                                    ratio = min(section_width / photo_width, section_height / photo_height)  # Tỷ lệ
                                    new_width = int(photo_width * ratio)  # Chiều rộng mới
                                    new_height = int(photo_height * ratio)  # Chiều cao mới
                                    photo_img = photo_img.resize((new_width, new_height), Image.Resampling.LANCZOS)  # Thay đổi kích thước

                                    # Đặt ảnh ở giữa phần
                                    x, y = sections[idx]  # Tọa độ bắt đầu của phần
                                    x_center = x + (section_width - new_width) // 2  # Tọa độ X ở giữa
                                    y_center = y + (section_height - new_height) // 2  # Tọa độ Y ở giữa

                                    # Dán ảnh
                                    extra_image.paste(photo_img, (x_center, y_center), photo_img)  # Dán ảnh vào phụ lục

                                except Exception as e:
                                    st.error(f"Lỗi khi xử lý ảnh {idx+1}: {e}")  # Báo lỗi nếu có

                    # Hiển thị ảnh phụ lục
                    st.image(extra_image, caption='Ảnh Hoạt Động Học Tập', width=800)

                except FileNotFoundError:
                    st.error(f"Không tìm thấy ảnh phụ lục: {extra_img_path}")  # Báo lỗi nếu không tìm thấy ảnh phụ lục
                    st.stop()

        except Exception as e:
            st.error(f"Lỗi khi tải ảnh hoặc font: {e}")  # Báo lỗi nếu có
            st.stop()

    def generate_pdf():
        try:
            # Sử dụng thư mục tạm thời
            with tempfile.TemporaryDirectory() as temp_dir:
                temp_dir_path = pathlib.Path(temp_dir)  # Chuyển thành đối tượng Path

                # Thiết lập đường dẫn cho các file tạm thời
                main_image_path = temp_dir_path / "studywork_main.png"  # Đường dẫn ảnh chính
                extra_image_path = temp_dir_path / "studywork_extra.png"  # Đường dẫn ảnh phụ lục

                # Lưu các file ảnh
                image.save(main_image_path)  # Lưu ảnh chính
                extra_image.save(extra_image_path)  # Luôn lưu ảnh phụ lục

                # Danh sách các file ảnh để tạo PDF (luôn có 2 trang)
                image_list = [str(main_image_path), str(extra_image_path)]

                # Tạo file PDF trong bộ nhớ
                pdf_bytes = img2pdf.convert(image_list)  # Chuyển đổi ảnh thành PDF

                # Thêm nút tải PDF
                st.download_button(
                    label="Tải Báo Cáo Kết Quả PDF",  # Nhãn của nút
                    data=pdf_bytes,  # Dữ liệu PDF
                    file_name="교외체험학습_결과보고서.pdf",  # Tên file mặc định
                    mime="application/pdf"  # Loại MIME
                )
        except Exception as e:
            st.error(f"Lỗi khi tạo PDF: {e}")  # Báo lỗi nếu có

    if st.button("Tạo và Tải File PDF", key="pdf_download_button"):  # Nút tạo và tải PDF
        generate_pdf()  # Gọi hàm tạo PDF


# Thêm footer bằng HTML và CSS
footer = """
    <style>
        .footer {
            position: fixed;
            bottom: 0;
            left: 0;
            width: 100%;
            background-color: #f1f1f1;
            text-align: center;
            padding: 10px;
            font-size: 14px;
        }
    </style>
    <div class="footer">
        Người tạo: 박기윤 (Park Ki-yoon)
    </div>
"""
st.markdown(footer, unsafe_allow_html=True)  # Hiển thị footer