import json  # Thư viện dùng để làm việc với dữ liệu JSON (đọc, ghi).
from datetime import datetime  # Thư viện để làm việc với thời gian, dùng để lấy thời gian hiện tại.


class ChatHistoryFile:
    # Phương thức khởi tạo (constructor) cho lớp ChatHistoryFile
    # Tham số file_name là tên tệp JSON lưu trữ lịch sử chat, mặc định là 'chat_history.json'
    def __init__(self, file_name="chat_history.json"):
        self.file_name = file_name  # Lưu tên tệp vào thuộc tính của đối tượng

    # Phương thức lưu trữ một thông điệp vào tệp JSON
    def save_message(self, session_id, role, message):
        try:
            # Cố gắng mở tệp JSON và đọc dữ liệu vào biến 'data'
            with open(self.file_name, "r") as file:
                data = json.load(file)  # Đọc toàn bộ dữ liệu JSON vào biến 'data'
        except FileNotFoundError:
            # Nếu tệp không tồn tại, tạo một dictionary rỗng
            data = {}

        # Lấy thời gian UTC hiện tại và chuyển thành chuỗi ISO 8601
        timestamp = datetime.utcnow().isoformat()

        # Kiểm tra nếu session_id chưa có trong dữ liệu, nếu chưa thì tạo một danh sách trống
        if session_id not in data:
            data[session_id] = []

        # Thêm thông điệp mới vào lịch sử của session_id
        data[session_id].append({
            "role": role,  # Vai trò của người gửi (ví dụ: 'user' hoặc 'assistant')
            "message": message,  # Nội dung thông điệp
            "timestamp": timestamp  # Thời gian gửi thông điệp
        })

        # Ghi lại toàn bộ dữ liệu vào tệp JSON với định dạng đẹp (indent=4 để dễ đọc)
        with open(self.file_name, "w") as file:
            json.dump(data, file, indent=4)

    # Phương thức lấy lịch sử chat cho một session_id
    def get_history(self, session_id):
        try:
            # Cố gắng mở tệp JSON và đọc dữ liệu vào biến 'data'
            with open(self.file_name, "r") as file:
                data = json.load(file)  # Đọc toàn bộ dữ liệu JSON vào biến 'data'

            # Trả về lịch sử chat của session_id nếu có, nếu không trả về danh sách rỗng
            return data.get(session_id, [])
        except FileNotFoundError:
            # Nếu tệp không tồn tại, trả về danh sách rỗng
            return []


# một số chế độ mở rộng:
# Mở tệp để đọc (chế độ văn bản)
# Sử dụng chế độ 'r' để đọc tệp văn bản. Nếu tệp không tồn tại, sẽ ném ra lỗi FileNotFoundError.

# Mở tệp để ghi (chế độ văn bản)
# Sử dụng chế độ 'w' để ghi tệp. Nếu tệp tồn tại, nó sẽ bị ghi đè hoàn toàn.

# Mở tệp để ghi nhị phân (chế độ nhị phân)
# Sử dụng chế độ 'wb' để ghi tệp nhị phân. Nếu tệp không tồn tại, nó sẽ được tạo mới.

# Mở tệp để thêm vào (chế độ văn bản)
# Sử dụng chế độ 'a' để thêm dữ liệu vào cuối tệp. Nếu tệp không tồn tại, nó sẽ được tạo mới.

# Mở tệp để tạo mới (chế độ nhị phân)
# Sử dụng chế độ 'xb' để tạo tệp mới trong chế độ nhị phân. Nếu tệp đã tồn tại, sẽ ném ra lỗi FileExistsError.

# Mở tệp để đọc nhị phân (chế độ nhị phân)
# Sử dụng chế độ 'rb' để đọc tệp nhị phân. Dữ liệu sẽ được xử lý dưới dạng byte, không phải chuỗi văn bản.

# Mở tệp để ghi (chế độ nhị phân)
# Sử dụng chế độ 'wb' để ghi dữ liệu nhị phân vào tệp. Nếu tệp không tồn tại, nó sẽ được tạo mới.

# Mở tệp để thêm vào nhị phân (chế độ nhị phân)
# Sử dụng chế độ 'ab' để thêm dữ liệu nhị phân vào cuối tệp. Nếu tệp không tồn tại, nó sẽ được tạo mới.
