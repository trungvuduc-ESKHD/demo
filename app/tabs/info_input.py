import streamlit as st

def create_text_input(tab_name, label, key, default_value=""):
        full_key = f"{tab_name}_{key}"
        # Use st.session_state to manage input value
        if full_key not in st.session_state:
            st.session_state[full_key] = default_value
        return st.text_input(label, key=full_key)

def create_date_input(tab_name, label, key, default_value=None):
    full_key = f"{tab_name}_{key}"
    if full_key not in st.session_state:
        st.session_state[full_key] = default_value  # Or some default date
    return st.date_input(label, key=full_key) # Fix

def create_number_input(tab_name, label, key, default_value=0.0):
        full_key = f"{tab_name}_{key}"
        if full_key not in st.session_state:
            st.session_state[full_key] = default_value
        return st.number_input(label, key=full_key)

def render():
    st.header("Summarize Report")

    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "Inspection Report",
        "Quality Inspection Recap",
        "Sampling Plan Green",
        "Sampling Plan Black",
        "Defect Assessment Green",
        "Defect Assessment Black"
    ])

    # Store a mapping from tab label to form_type to make it easier to work with
    tab_form_type_mapping = {
        "Inspection Report": "templates_1", #default summarize.png
        "Quality Inspection": "templates_2", #new image file
        "Netweight1": "templates_3",# new image file
        "Netweight2": "templates_4", # new image file
        "Defect1": "templates_5", # new image file
        "Defect2": "templates_6" # new image file
    }

    # Determine the active tab
    active_tab = st.session_state.get('active_tab', "Inspection Report") # default to tab1 if none selected

    # Store the active tab in session state
    def set_active_tab(tab_name):
        st.session_state['active_tab'] = tab_name

    # Use callbacks to set the active tab
    tab1_button = tab1.button("Select Tab 1", on_click=lambda: set_active_tab("Inspection Report"))
    tab2_button = tab2.button("Select Tab 2", on_click=lambda: set_active_tab("Quality Inspection"))
    tab3_button = tab3.button("Select Tab 3", on_click=lambda: set_active_tab("Netweight1"))
    tab4_button = tab4.button("Select Tab 4", on_click=lambda: set_active_tab("Netweight2"))
    tab5_button = tab5.button("Select Tab 5", on_click=lambda: set_active_tab("Defect1"))
    tab6_button = tab6.button("Select Tab 6", on_click=lambda: set_active_tab("Defect2"))

   
    # Inspection Report / General Information (Tab 1)
    # ---------------------------------------------------------------------
    with tab1:
        st.subheader("Inspection Report")
        col1, col2 = st.columns(2)
        with col1:
            create_text_input("Inspection Report", "Nguồn gốc - Tên nhà cung cấp / Origine - Supplier name", "supplier_name")
            create_text_input("Inspection Report", "Số hợp đồng / PI/ Contract number", "contract_number")
            create_text_input("Inspection Report", "Số container /xe lạnh / Container number", "container_number")
            create_text_input("Inspection Report", "Bộ phận chịu trách nhiệm / Responsible department", "responsible_department")
            create_text_input("Inspection Report", "Địa điểm kiểm hàng / Inspection location", "inspection_location")
        with col2:
            create_text_input("Inspection Report", "Tên khách hàng / Partner's name", "partner_name")
            create_text_input("Inspection Report", "Tổng lượng kiện được nhận / Received total quantity (carton)", "total_quantity")
            eta_date = create_date_input("Inspection Report", "Ngày hàng đến/ ETA", "eta_date")
            create_text_input("Inspection Report", "Kiểm hàng bởi / Inspected by", "inspected_by")
            str_date = create_date_input("Inspection Report", "Ngày kiểm hàng / Inspection date", "str_date")

        st.subheader("Product Information")
        col3, col4, col5, col6 = st.columns(4)
        with col3:
            create_text_input("Inspection Report", "Tên sản phẩm 1 / Product name", "product_name_1", default_value="FRESH GREEN GRAPES")
        with col4:
            create_text_input("Inspection Report", "Kích cỡ / Size", "size_1")
        with col5:
            create_text_input("Inspection Report", "Số lượng túi được nhận", "quantity_bag_1")
        with col6:
            create_text_input("Inspection Report", "Net Weight of one bag as request (Kgs)", "net_weight_1")
        st.subheader("Container Status")
        create_text_input("Inspection Report", "Phương tiện sạch sẽ? / Container is clean?", "container_clean")
        create_text_input("Inspection Report", "Hệ thống thông gió hoạt động tốt? / Ventilation system is ok?", "ventilation_ok")
        create_text_input("Inspection Report", "Không rò rỉ? / No leakage?", "no_leakage")
        create_text_input("Inspection Report", "Thiết bị ghi nhiệt hoạt động tốt? / Temperature recorder is good?", "temp_recorder_ok")
        create_text_input("Inspection Report", "Tình trạng kiện hàng (móp méo, hư hại)? / Package status (deformed, damaged)?", "package_status")
        create_text_input("Inspection Report", "Mùi lạ? / Any abnormal smell?", "abnormal_smell")
        create_text_input("Inspection Report", "Nhiệt độ của phương tiện khi đến nơi? / Container temperature upon arrival?", "container_temp")

    # ---------------------------------------------------------------------
    # Quality Inspection Recap (Tab 2)
    # ---------------------------------------------------------------------
    with tab2:
        st.subheader("Quality Inspection Recap")

        create_text_input("Quality Inspection Recap", "Product Name 1", "product_name_1",)
        #create_text_input("Quality Inspection Recap", "Product Name 2", "product_name_2")
        create_text_input("Quality Inspection Recap", "Size 1", "size_1")
        #create_text_input("Quality Inspection Recap", "Size 2", "size_2")
        create_text_input("Quality Inspection Recap", "Variety Char. 1", "variety_char_1")
        #create_text_input("Quality Inspection Recap", "Variety Char. 2", "variety_char_2")
        create_text_input("Quality Inspection Recap", "Juicy 1", "juicy_1")
        #create_text_input("Quality Inspection Recap", "Juicy 2", "juicy_2")
        create_text_input("Quality Inspection Recap", "Brix degree 1", "brix_degree_1")
        #create_text_input("Quality Inspection Recap", "Brix degree 2", "brix_degree_2")
        create_text_input("Quality Inspection Recap", "Aerage Firmness 1", "aerage_firmness_1")
        #create_text_input("Quality Inspection Recap", "Aerage Firmness 2", "aerage_firmness_2")

        st.subheader("Net Weight Checking Recap")
        create_text_input("Quality Inspection Recap", "Average net weight (kg) 1", "average_net_weight_1")
        #create_text_input("Quality Inspection Recap", "Average net weight (kg) 2", "average_net_weight_2")
        create_text_input("Quality Inspection Recap", "Target (kg) 1", "target_kg_1")
        #create_text_input("Quality Inspection Recap", "Target (kg) 2", "target_kg_2")
        create_text_input("Quality Inspection Recap", "Status 1", "status_1")
        #create_text_input("Quality Inspection Recap", "Status 2", "status_2")

        st.subheader("Defects Assessment Recap")
        create_text_input("Quality Inspection Recap", "Total Serious Defects 1", "total_serious_defects_1")
        #create_text_input("Quality Inspection Recap", "Total Serious Defects 2", "total_serious_defects_2")
        create_text_input("Quality Inspection Recap", "Total Major Defects 1", "total_major_defects_1")
        #create_text_input("Quality Inspection Recap", "Total Major Defects 2", "total_major_defects_2")
        create_text_input("Quality Inspection Recap", "Total Minor Defects 1", "total_minor_defects_1")
        #create_text_input("Quality Inspection Recap", "Total Minor Defects 2", "total_minor_defects_2")
        create_text_input("Quality Inspection Recap", "Shattering (Loosing) Berries 1", "shattering_berries_1")
        create_text_input("Quality Inspection Recap", "Shattering (Loosing) Berries 2", "shattering_berries_2")

    # ---------------------------------------------------------------------
    # Sampling Plan Green (Tab 3)
    # ---------------------------------------------------------------------
    with tab3:
        st.subheader("Sampling Plan & Weight Checking - Green Grapes")
        create_text_input("Sampling Plan Green", "Product Name", "product_name")
        create_text_input("Sampling Plan Green", "Size/Caliber", "size_caliber")
        create_text_input("Sampling Plan Green", "Sampling Plan", "sampling_plan")
        create_text_input("Sampling Plan Green", "Qty of Bags", "qty_of_bags")

        create_number_input("Sampling Plan Green", "Empty weight of bag (3 bags)", "empty_weight_of_bag", default_value=0.0)
        create_number_input("Sampling Plan Green", "Total gross weight", "total_gross_weight", default_value=0.0)
        create_number_input("Sampling Plan Green", "Total net weight", "total_net_weight", default_value=0.0)
        create_number_input("Sampling Plan Green", "Average of net weight (kg)", "average_of_net_weight", default_value=0.0)

        # Add input fields for the table data
        for i in range(1, 6):  # Assuming 5 rows in the table
            create_number_input("Sampling Plan Green", f"Gross Weight Bag {i}", f"gross_weight_bag_{i}", default_value=0.0)
            create_number_input("Sampling Plan Green", f"Net Weight Bag {i}", f"net_weight_bag_{i}", default_value=0.0)

    # ---------------------------------------------------------------------
    # Sampling Plan Black (Tab 4)
    # ---------------------------------------------------------------------
    with tab4:
        st.subheader("Sampling Plan & Weight Checking - Black Grapes")
        create_text_input("Sampling Plan Black", "Product Name", "product_name")
        create_text_input("Sampling Plan Black", "Size/Caliber", "size_caliber")
        create_text_input("Sampling Plan Black", "Sampling Plan", "sampling_plan")
        create_text_input("Sampling Plan Black", "Qty of Bags", "qty_of_bags")

        create_number_input("Sampling Plan Black", "Empty weight of bag (3 bags)", "empty_weight_of_bag", default_value=0.0)
        create_number_input("Sampling Plan Black", "Total gross weight", "total_gross_weight", default_value=0.0)
        create_number_input("Sampling Plan Black", "Total net weight", "total_net_weight", default_value=0.0)
        create_number_input("Sampling Plan Black", "Average of net weight (kg)", "average_of_net_weight", default_value=0.0)

        # Add input fields for the table data
        for i in range(1, 6):  # Assuming 5 rows in the table
            create_number_input("Sampling Plan Black", f"Gross Weight Bag {i}", f"gross_weight_bag_{i}", default_value=0.0)
            create_number_input("Sampling Plan Black", f"Net Weight Bag {i}", f"net_weight_bag_{i}", default_value=0.0)

    # ---------------------------------------------------------------------
    # Defect Assessment Green (Tab 5)
    # ---------------------------------------------------------------------
    with tab5:
        st.subheader("Defect Assessment - Green Grapes")
        create_text_input("Defect Assessment Green", "Product Name", "product_name")
        create_text_input("Defect Assessment Green", "Size", "size")

        # Add input fields for each defect type
        defect_types = ["Serious", "Major1", "Major2", "Major3", "Minor", "Shattering"]
        for defect in defect_types:
            create_text_input("Defect Assessment Green", f"Detail {defect}", f"detail_{defect}")
            create_number_input("Defect Assessment Green", f"Weight (kg) {defect}", f"weight_{defect}", default_value=0.0)
            create_number_input("Defect Assessment Green", f"Percentage (%) {defect}", f"percentage_{defect}", default_value=0.0)

    # ---------------------------------------------------------------------
    # Defect Assessment Black (Tab 6)
    # ---------------------------------------------------------------------
    with tab6:
        st.subheader("Defect Assessment - Black Grapes")
        create_text_input("Defect Assessment Black", "Product Name", "product_name")
        create_text_input("Defect Assessment Black", "Size", "size")

        # Add input fields for each defect type
        defect_types = ["Serious", "Major1", "Major2", "Major3", "Minor", "Shattering"]
        for defect in defect_types:
            create_text_input("Defect Assessment Black", f"Detail {defect}", f"detail_{defect}")
            create_number_input("Defect Assessment Black", f"Weight (kg) {defect}", f"weight_{defect}", default_value=0.0)
            create_number_input("Defect Assessment Black", f"Percentage (%) {defect}", f"percentage_{defect}", default_value=0.0)

    st.query_params["form_type"] = tab_form_type_mapping.get(active_tab, "templates_1") #default
    st.write(f"Current Form Type: {st.query_params.get('form_type')}") # debug
