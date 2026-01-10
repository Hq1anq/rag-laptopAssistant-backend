import os
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, OperationFailure
from dotenv import load_dotenv

class DataNotFoundError(Exception):
    def __init__(self):
        super().__init__(f"Please make sure you have valid CSV file")

def csv_exists(file_name: str) -> bool:
    """
    Check if a CSV file exists.

    Args:
        filename (str): Absolute path of the file (e.g., "C:/Users/products.csv")

    Returns:
        bool: True if file exists, False otherwise
    """
    if not file_name.endswith(".csv"):
        raise ValueError("Filename must end with .csv")
    
    return os.path.isfile(file_name)

# Load biến môi trường từ file .env
load_dotenv()

def check_mongodb_connection():
    """
    Kiểm tra kết nối đến MongoDB Atlas dựa trên cấu hình trong file .env
    """
    uri = os.getenv("MONGODB_URI")
    db_name = os.getenv("MONGODB_NAME")
    
    if not uri:
        print("❌ Lỗi: Chưa cấu hình MONGODB_URI trong file .env")
        return False

    try:
        # Khởi tạo client với timeout ngắn để check nhanh
        client = MongoClient(uri, serverSelectionTimeoutMS=5000)
        
        # Lệnh 'ping' là cách nhanh nhất để kiểm tra xem server có phản hồi không
        client.admin.command('ping')
        
        print(f"✅ Kết nối MongoDB thành công!")
        print(f"- Database {db_name}")
        
        # Kiểm tra xem Database và Collection có tồn tại không (tùy chọn)
        collection_name = os.getenv("MONGODB_COLLECTION")
        db = client[db_name]

        if collection_name in db.list_collection_names():
            print(f"- Collection {collection_name}")
        else:
            print(f"- Lưu ý: Collection '{collection_name}' chưa tồn tại.")
            
        return True

    except ConnectionFailure:
        print("❌ Lỗi: Không thể kết nối tới Server (Sai URI hoặc lỗi mạng).")
    except OperationFailure:
        print("❌ Lỗi: Xác thực thất bại (Sai username hoặc password).")
    except Exception as e:
        print(f"❌ Đã xảy ra lỗi không xác định: {e}")
    
    return False