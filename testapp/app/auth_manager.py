import json
import streamlit as st
from pathlib import Path

class AuthManager:
    def __init__(self):
        config_path = Path(__file__).parent.parent / "config" / "page_access.json"
        with open(config_path, 'r', encoding='utf-8') as f:
            self.access_config = json.load(f)

    def is_admin_page(self, page_name):
        """Kiểm tra xem trang có phải chỉ dành cho admin hay không"""
        return self.access_config.get(page_name, []) == ["admin"]

    def check_page_access(self, page_name):
        """Kiểm tra quyền truy cập trang"""
        if self.is_admin_page(page_name):
            if not st.session_state.get("authenticated", False):
                st.error("Trang này yêu cầu đăng nhập admin.")
                st.switch_page("Home.py")
                st.stop()

    def authenticate(self, username, password):
        """Xác thực người dùng"""
        if username == "admin" and password == "admin@123":
            st.session_state["authenticated"] = True
            return True
        return False

    def logout(self):
        """Đăng xuất"""
        st.session_state["authenticated"] = False
        st.session_state["username"] = None