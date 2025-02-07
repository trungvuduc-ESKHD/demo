import streamlit as st

def render():
    st.header("Summarie Report")

    # ---------------------------------------------------------------------
    # Thông tin chung / General Information
    # ---------------------------------------------------------------------
    st.subheader("Thông tin chung / General Information")
    col1, col2 = st.columns(2)
    with col1:
        st.text_input("Nguồn gốc - Tên nhà cung cấp / Origine - Supplier name", key="supplier_name")
        st.text_input("Số hợp đồng / PI/ Contract number", key="contract_number")
        st.text_input("Số container /xe lạnh / Container number", key="container_number")
    with col2:
        st.text_input("Tên khách hàng / Partner's name", key="partner_name")
        st.text_input("Tổng lượng kiện được nhận / Received total quantity (carton)", key="total_quantity")
        st.date_input("Ngày hàng đến/ ETA", key="eta_date")

    st.text_input("Bộ phận chịu trách nhiệm / Responsible department", key="responsible_department")
    st.text_input("Địa điểm kiểm hàng / Inspection location", key="inspection_location")

    # ---------------------------------------------------------------------
    # Thông tin về sản phẩm/ Product information
    # ---------------------------------------------------------------------
    st.subheader("Thông tin về sản phẩm/ Product information")
    col3, col4 = st.columns(2)
    with col3:
        st.text_input("Tên sản phẩm 1 / Product name", key="product_name_1", value="FRESH GREEN GRAPES")  # Điền sẵn giá trị
    with col4:
        st.text_input("Kích cỡ / Size", key="size_1")
        st.text_input("Số lượng túi được nhận/Received quantity of bag for inspection", key="quantity_bag_1")
        st.text_input("Khối lượng tịnh của 1 túi theo đơn hàng/Net Weight of one bag as request (Kgs)", key="net_weight_1")

    col5, col6 = st.columns(2)
    with col5:
        st.text_input("Tên sản phẩm 2 / Product name", key="product_name_2", value="FRESH BLACK GRAPES") # Điền sẵn giá trị
    with col6:
        st.text_input("Kích cỡ / Size", key="size_2")
        st.text_input("Số lượng túi được nhận/Received quantity of bag for inspection", key="quantity_bag_2")
        st.text_input("Khối lượng tịnh của 1 túi theo đơn hàng/Net Weight of one bag as request (Kgs)", key="net_weight_2")

    # ---------------------------------------------------------------------
    # Tình trạng phương tiện vận chuyển/ Container status
    # ---------------------------------------------------------------------
    st.subheader("Tình trạng phương tiện vận chuyển/ Container status")
    st.text_input("Phương tiện sạch sẽ? / Container is clean?", key="container_clean")
    st.text_input("Hệ thống thông gió hoạt động tốt? / Ventilation system is ok?", key="ventilation_ok")
    st.text_input("Không rò rỉ? / No leakage?", key="no_leakage")
    st.text_input("Thiết bị ghi nhiệt hoạt động tốt? / Temperature recorder is good?", key="temp_recorder_ok")
    st.text_input("Tình trạng kiện hàng (móp méo, hư hại)? / Package status (deformed, damaged)?", key="package_status")
    st.text_input("Mùi lạ? / Any abnormal smell?", key="abnormal_smell")
    st.text_input("Nhiệt độ của phương tiện khi đến nơi? / Container temperature upon arrival?", key="container_temp")

    # ---------------------------------------------------------------------
    # Các trường giữ lại từ code cũ (nếu cần)
    # ---------------------------------------------------------------------
    # st.header("Thông tin bổ sung")
    # st.text_input("Tên", key="name")
    # st.date_input("Sinh Năm", key="birth_date")
    # st.text_input("Địa chỉ", key="address")
    # st.text_input("Liên hệ", key="contact")
    # st.date_input("Date", key="delegation_date")

# Để sử dụng hàm này trong ứng dụng Streamlit của bạn:
# info_input.render()