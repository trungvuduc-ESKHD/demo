import streamlit as st
from streamlit_drawable_canvas import st_canvas
import numpy as np

def render():
    st.header("Nhập Chữ Ký")
    
    st.info("Nhấn nút Tải lại Khung Chữ Ký để vẽ chữ ký của bạn trên khung.")
    
    # Khởi tạo trạng thái phiên
    if "canvas_key" not in st.session_state:
        st.session_state.canvas_key = 0
    
    # Nút Tải lại Khung Chữ Ký
    if st.button("Tải lại Khung Chữ Ký"):
        st.session_state.canvas_key += 1
        st.session_state.pop("signature_img", None)
        st.rerun()
    
    # Tạo khung vẽ (nền trong suốt)
    canvas_result = st_canvas(
        stroke_width=2,
        stroke_color="#000000",
        background_color="rgba(0, 0, 0, 0)",  # Nền trong suốt
        height=150,
        width=400,
        drawing_mode="freedraw",
        key=f"canvas_{st.session_state.canvas_key}"
    )
    
    # Xử lý dữ liệu chữ ký
    if canvas_result is not None and canvas_result.image_data is not None:
        if np.any(canvas_result.image_data):
            st.session_state["signature_img"] = canvas_result.image_data
            st.success("Chữ ký đã được lưu.")