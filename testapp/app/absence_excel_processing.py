import pandas as pd  # Thư viện xử lý dữ liệu, đặc biệt là làm việc với bảng (DataFrames)
from datetime import datetime  # Thư viện làm việc với ngày và giờ

def process_excel(file_path):  # Hàm này xử lý file Excel, đường dẫn file được truyền vào

    # Load the Excel file with explicit header definition
    # Tải file Excel, chỉ định rõ dòng nào là header (tiêu đề cột)
    df = pd.read_excel(
        file_path,  # Đường dẫn tới file Excel
        sheet_name=0,  # Tên sheet cần đọc (ở đây là sheet đầu tiên, index 0)
        header=0  # Dòng nào là header (dòng đầu tiên, index 0)
    )

    print("1. Giá trị của cột Phân loại điểm danh trong dữ liệu gốc:", df['Trung'].unique())
    # In ra các giá trị duy nhất trong cột '출결구분' (Phân loại điểm danh) của dữ liệu gốc

    # Step 1: Unmerge B, C columns (columns 'Số thứ tự', 'Tên')
    # Bước 1: Hủy trộn các ô ở cột B và C (cột 'Số thứ tự', 'Tên')
    # ffill() dùng để điền các giá trị bị thiếu (NaN) bằng giá trị liền kề trước đó
    df[['번호', '성명']] = df[['번호', '성명']].ffill()

    # Step 2: Tiền xử lý và lọc dữ liệu ở cột Phân loại điểm danh
    # Bước 2: Tiền xử lý và lọc dữ liệu ở cột 'Phân loại điểm danh'
    df['출결구분'] = df['출결구분'].astype(str).apply(
        lambda x: 'Vắng do bệnh' if ('bệnh' in x and 'vắng' in x) else x.strip()
    )
    # Chuyển đổi cột '출결구분' sang kiểu string, sau đó áp dụng một hàm
    # Hàm này kiểm tra nếu có cả 'bệnh' và 'vắng' trong giá trị, thì đổi thành 'Vắng do bệnh'
    # Nếu không, thì loại bỏ khoảng trắng ở đầu và cuối chuỗi

    print("2. Giá trị của cột Phân loại điểm danh sau khi tiền xử lý:", df['출결구분'].unique())
    # In ra các giá trị duy nhất trong cột 'Phân loại điểm danh' sau khi tiền xử lý

    # Step 3: Filter valid data rows
    # Bước 3: Lọc các dòng dữ liệu hợp lệ
    valid_types = ['Vắng được chấp nhận', 'Vắng do bệnh', 'Vắng khác']
    # Các loại 'Phân loại điểm danh' được coi là hợp lệ
    filtered_data = df[df['출결구분'].isin(valid_types)].copy()
    # Lọc ra các dòng có 'Phân loại điểm danh' nằm trong danh sách valid_types và tạo một bản sao (copy())

    print("3. Giá trị của cột Phân loại điểm danh sau khi lọc:", filtered_data['출결구분'].unique())
    # In ra các giá trị duy nhất trong cột 'Phân loại điểm danh' sau khi lọc
    print("4. Số lượng dòng dữ liệu sau khi lọc:", len(filtered_data))
    # In ra số lượng dòng dữ liệu sau khi lọc

    if filtered_data.empty:
        print("Cảnh báo: Sau khi lọc, dữ liệu trống!")
        # Nếu sau khi lọc không còn dữ liệu nào, in ra cảnh báo
        return pd.DataFrame(columns=['번호', '성명', '일자', '출결구분', '사유', '결석시작일', '결석종료일', '결석일수'])
        # Trả về một DataFrame rỗng với các cột được chỉ định

    # Step 4: Convert 'Ngày' column to datetime format
    # Bước 4: Chuyển đổi cột 'Ngày' sang định dạng datetime
    filtered_data['일자'] = pd.to_datetime(
        filtered_data['일자'].str.strip('.'),  # Loại bỏ dấu chấm ở cuối chuỗi ngày
        format='%Y.%m.%d',  # Định dạng của chuỗi ngày (năm.tháng.ngày)
        errors='coerce'  # Nếu có lỗi trong quá trình chuyển đổi, thay thế bằng NaT (Not a Time)
    )

    print("5. Số lượng dòng dữ liệu sau khi chuyển đổi ngày:", len(filtered_data))
    # In ra số lượng dòng dữ liệu sau khi chuyển đổi ngày

    # Step 5: Add new columns
    # Bước 5: Thêm các cột mới
    filtered_data['결석시작일'] = None  # Ngày bắt đầu vắng mặt
    filtered_data['결석종료일'] = None  # Ngày kết thúc vắng mặt
    filtered_data['결석일수'] = None  # Số ngày vắng mặt

    # Step 6: Group by columns and process
    # Bước 6: Nhóm dữ liệu theo các cột và xử lý
    group_columns = ['번호', '출결구분']  # '사유' 컬럼 제외
    # Các cột dùng để nhóm dữ liệu (Số thứ tự, Phân loại điểm danh, bỏ qua cột Lý do)
    merged_rows = []  # Danh sách để lưu trữ các dòng dữ liệu đã được xử lý

    # Nhóm hóa trước khi kiểm tra dữ liệu
    print("\nKiểm tra dữ liệu Vắng do bệnh:")
    # In ra thông tin về dữ liệu 'Vắng do bệnh' trước khi nhóm
    sick_data = filtered_data[filtered_data['출결구분'] == 'Vắng do bệnh']
    print(sick_data[['번호', '출결구분', '사유', '일자']].to_string())
    # In ra các cột 'Số thứ tự', 'Phân loại điểm danh', 'Lý do', 'Ngày' của dữ liệu 'Vắng do bệnh'

    for name, group_data in filtered_data.groupby(group_columns):
        # Lặp qua các nhóm dữ liệu đã được nhóm theo group_columns
        # 'name' là tuple chứa giá trị của các cột nhóm (Số thứ tự, Phân loại điểm danh)
        # 'group_data' là DataFrame chứa dữ liệu của nhóm đó

        print(f"\n6. Nhóm đang xử lý: {name}")
        # In ra thông tin về nhóm đang được xử lý
        print(f"   - Phân loại điểm danh: {name[1]}")
        # In ra loại điểm danh của nhóm
        print(f"   - Số lượng dòng dữ liệu: {len(group_data)}")
        # In ra số lượng dòng dữ liệu trong nhóm
        print(f"   - Dữ liệu ngày: {group_data['일자'].tolist()}")
        # In ra danh sách các ngày trong nhóm

        group_data = group_data.sort_values('일자')
        # Sắp xếp dữ liệu trong nhóm theo ngày
        dates = group_data['일자'].dropna().tolist()
        # Lấy danh sách các ngày (loại bỏ các giá trị NaN)

        if not dates:
            print(f"   - Nhóm {name} không có ngày hợp lệ")
            # Nếu không có ngày hợp lệ trong nhóm, in ra thông báo
            continue  # Chuyển sang nhóm tiếp theo

        # Tìm kiếm các nhóm ngày liên tiếp
        # Tìm các nhóm ngày liên tiếp
        current_group = []  # Danh sách để lưu trữ nhóm ngày liên tiếp hiện tại
        current_group.append(dates[0])  # Thêm ngày đầu tiên vào nhóm

        for i in range(1, len(dates)):
            # Lặp qua các ngày còn lại trong danh sách
            if (dates[i] - dates[i-1]).days == 1:
                # Nếu ngày hiện tại và ngày trước đó cách nhau 1 ngày (liên tiếp)
                current_group.append(dates[i])  # Thêm ngày hiện tại vào nhóm
            else:
                # Xử lý nhóm hiện tại
                # Xử lý nhóm hiện tại
                if current_group:
                    start_date = current_group[0]  # Ngày bắt đầu của nhóm
                    end_date = current_group[-1]  # Ngày kết thúc của nhóm

                    base_row = group_data[group_data['일자'] == start_date].iloc[0].copy()
                    # Lấy một dòng dữ liệu gốc làm cơ sở
                    base_row['결석시작일'] = start_date.strftime('%Y.%m.%d')  # Định dạng ngày bắt đầu
                    base_row['결석종료일'] = end_date.strftime('%Y.%m.%d')  # Định dạng ngày kết thúc

                    days_diff = (end_date - start_date).days + 1
                    # Tính số ngày vắng mặt
                    base_row['결석일수'] = days_diff

                    if start_date != end_date:
                        # Nếu ngày bắt đầu khác ngày kết thúc (vắng nhiều ngày)
                        base_row['일자'] = f"{start_date.strftime('%Y.%m.%d')} ~ {end_date.strftime('%Y.%m.%d')}"
                    else:
                        # Nếu ngày bắt đầu và ngày kết thúc giống nhau (vắng 1 ngày)
                        base_row['일자'] = start_date.strftime('%Y.%m.%d')

                    # Thay thế Lý do NaN thành "Nhập lý do"
                    # Thay thế giá trị NaN trong cột 'Lý do' bằng 'Nhập lý do'
                    if pd.isna(base_row['사유']):
                        base_row['사유'] = 'Nhập lý do'

                    merged_rows.append(base_row)  # Thêm dòng đã xử lý vào danh sách

                current_group = [dates[i]]  # Tạo một nhóm mới bắt đầu từ ngày hiện tại

        # Xử lý nhóm cuối cùng
        # Xử lý nhóm cuối cùng
        if current_group:
            start_date = current_group[0]
            end_date = current_group[-1]

            base_row = group_data[group_data['일자'] == start_date].iloc[0].copy()
            base_row['결석시작일'] = start_date.strftime('%Y.%m.%d')
            base_row['결석종료일'] = end_date.strftime('%Y.%m.%d')

            days_diff = (end_date - start_date).days + 1
            base_row['결석일수'] = days_diff

            if start_date != end_date:
                base_row['일자'] = f"{start_date.strftime('%Y.%m.%d')} ~ {end_date.strftime('%Y.%m.%d')}"
            else:
                base_row['일자'] = start_date.strftime('%Y.%m.%d')

            # Thay thế Lý do NaN thành "Nhập lý do"
            if pd.isna(base_row['사유']):
                base_row['사유'] = 'Nhập lý do'

            merged_rows.append(base_row)

    # Tạo DataFrame cuối cùng
    # Tạo DataFrame cuối cùng
    columns_order = ['번호', '성명', '일자', '출결구분', '사유', '결석시작일', '결석종료일', '결석일수']
    # Thứ tự các cột trong DataFrame

    if merged_rows:
        # Nếu có dữ liệu đã được xử lý
        processed_data = pd.DataFrame(merged_rows)
        # Tạo DataFrame từ danh sách các dòng đã xử lý
        processed_data = processed_data[columns_order]
        # Sắp xếp lại các cột theo thứ tự đã chỉ định
        print("7. Số lượng dòng dữ liệu đã xử lý:", len(processed_data))
        # In ra số lượng dòng dữ liệu đã xử lý
    else:
        # Nếu không có dữ liệu nào được xử lý
        print("7. Không có dữ liệu được xử lý")
        # In ra thông báo
        processed_data = pd.DataFrame(columns=columns_order)
        # Tạo một DataFrame rỗng với các cột đã chỉ định

    return processed_data  # Trả về DataFrame đã được xử lý