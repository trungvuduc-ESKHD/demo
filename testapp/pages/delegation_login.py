import streamlit as st
import json
import os
from app.auth_manager import AuthManager
from app.sidebar_manager import SidebarManager
from io import BytesIO

# Kiểm tra quyền truy cập
auth_manager = AuthManager()
auth_manager.check_page_access("delegation_login") # Kiểm tra lại tên này trong auth_manager

# Render sidebar
sidebar_manager = SidebarManager()
sidebar_manager.render_sidebar()

# Nếu chưa đăng nhập, chuyển hướng
if not st.session_state.get("authenticated", False):
    st.error("Trang này yêu cầu đăng nhập ADMIN.")
    st.switch_page("Home.py")

def show_teacher_page():
    """Trang chính của ADMIN"""
    st.markdown("<h1 style='text-align: center;'>Quản Lý Hồ Sơ</h1>", unsafe_allow_html=True)
# Hộp mô ta
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
                🔗 Thêm và tạo liên kết cho admin
            </div>
            <div style="color: #666; font-size: 0.9em;">
                Chia sẻ liên kết cho user
            </div>
        </div>
    """, unsafe_allow_html=True)

    # Đường dẫn file JSON
    json_file = "form_config.json"

    # Hiển thị danh sách ủy ban
    st.subheader("📋 Danh Sách Ủy Ban")
    if os.path.exists(json_file):
        with open(json_file, "r", encoding="utf-8") as f:
            form_configs = json.load(f)

        # Hiển thị danh sách ủy ban dưới dạng lưới
        cols = st.columns(3)  # Lưới 3 cột
        for idx, (committee_name, config) in enumerate(form_configs.items()):
            with cols[idx % 3]:
                with st.container():
                    st.markdown(f"""
                        <div style="
                            padding: 20px;
                            border-radius: 10px;
                            border: 1px solid #ddd;
                            margin: 10px 0;
                            background-color: white;">
                            <h3 style="margin: 0 0 10px 0;">{committee_name}</h3>
                            <p style="color: #666; margin: 5px 0;">Tiêu đề: {config['title']} </p>
                        </div>
                        """, unsafe_allow_html=True)
                    if st.button("Xóa", key=f"delete_{committee_name}"):
                        del form_configs[committee_name]
                        with open(json_file, "w", encoding="utf-8") as f:
                            json.dump(form_configs, f, ensure_ascii=False, indent=4)
                        st.success(f"Đã xóa '{committee_name}'.")
                        st.rerun()
    else:
        st.error("Không tìm thấy file cấu hình.")

    # Thêm ủy ban
    st.write("---")
    st.subheader("➕ Thêm ")
    with st.form("new_form"):
        committee_name = st.text_input("Tên")
        submit_button = st.form_submit_button("Thêm")

        if submit_button:
            if committee_name:
                # Tạo tiêu đề và văn bản động
                form_configs[committee_name] = {
                    "title": committee_name,
                    "image_texts": [
                        f"Tôi đồng ý {committee_name}"
                    ]
                }
                with open(json_file, "w", encoding="utf-8") as f:
                    json.dump(form_configs, f, ensure_ascii=False, indent=4)
                st.success(f"Đã thêm '{committee_name}'.")
                st.rerun()
            else:
                st.error("Vui lòng nhập tên.")

    # Tạo liên kết
    st.write("---")
    st.subheader("🔗 Tạo Liên Kết")
    if os.path.exists(json_file):
        # Khởi tạo trạng thái phiên
        if "generated_link" not in st.session_state:
            st.session_state.generated_link = None

        # Khởi tạo liên kết khi thay đổi lựa chọn
        selected_form = st.selectbox(
            "Chọn Form",
            list(form_configs.keys()),
            key="selected_form"
        )

        # URL gốc
        base_url = "https://github.com/trungvuduc-ESKHD/demoapp.git"

        # Xóa liên kết khi selectbox thay đổi
        if "last_selected_form" not in st.session_state:
            st.session_state.last_selected_form = selected_form

        if st.session_state.last_selected_form != selected_form:
            st.session_state.generated_link = None
            st.session_state.last_selected_form = selected_form

        # Nút tạo liên kết
        if st.button("Tạo Liên Kết"):
            if selected_form:
                st.session_state.generated_link = f"{base_url}?form_type={selected_form}"

        # Hiển thị liên kết sau khi tạo
        if st.session_state.generated_link is not None:
            st.write("Liên Kết Đã Tạo:")
            st.text_input(
                "Chọn và sao chép liên kết:",
                value=st.session_state.generated_link,
                key="link_input",
                label_visibility="collapsed"
            )

            # Tạo mã QR
            if st.checkbox("Tạo Mã QR"):
                try:
                    import qrcode
                    qr = qrcode.QRCode(version=1, box_size=10, border=5)
                    qr.add_data(st.session_state.generated_link)
                    qr.make(fit=True)
                    img = qr.make_image(fill_color="black", back_color="white")
                    buffered = BytesIO()
                    img.save(buffered, format="PNG")

                    # Hiển thị hình ảnh QR
                    st.write(f"**Mã QR cho {selected_form}**")
                    st.image(buffered)

                except ImportError:
                    st.error("Vui lòng cài đặt gói 'qrcode' để tạo mã QR.")

# Main logic
if st.session_state.authenticated:
    show_teacher_page()
else:
    st.switch_page("Home.py")  # Chuyển hướng nếu chưa đăng nhập