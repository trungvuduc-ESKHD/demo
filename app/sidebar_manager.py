import streamlit as st
from app.auth_manager import AuthManager
import base64
from pathlib import Path

class SidebarManager:
    def __init__(self):
        self.auth_manager = AuthManager()

    def get_base64_image(self, image_path):
        try:
            with open(image_path, "rb") as img_file:
                return base64.b64encode(img_file.read()).decode()
        except FileNotFoundError:
            return None

    def render_sidebar(self):
        with st.sidebar:
            # Thêm ảnh
            ROOT_DIR = Path(__file__).parent.parent.absolute()
            SIDEBAR_IMAGE_PATH = ROOT_DIR / "images" / "sidebar_logo.png"

            if SIDEBAR_IMAGE_PATH.exists():
                image_base64 = self.get_base64_image(SIDEBAR_IMAGE_PATH)
                if image_base64:
                    st.markdown(f"""
                        <div style="text-align: center; margin-bottom: 20px;">
                            <img src="data:image/png;base64,{image_base64}"
                                 style="width: 180px; margin: auto;">
                        </div>
                    """, unsafe_allow_html=True)

        st.markdown("### Menu Chung")

            # Menu chung (luôn hiển thị)
        if st.button("✍️ INSPECTION REPORT", key="write"):
            st.switch_page("pages/write_delegation.py")
        if st.button("📝 GENERAL PHOTO", key="field_request"):
            st.switch_page("pages/camera_photo.py")

        # Nút đăng nhập/đăng xuất
        st.markdown("---")
        if st.session_state.get("authenticated", False):
            if st.button("Đăng Xuất", key="logout"):
                self.auth_manager.logout()
                st.rerun()

    def logout(self):
        st.session_state.authenticated = False
        st.rerun()
