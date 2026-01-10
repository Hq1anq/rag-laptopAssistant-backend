import pandas as pd
from pymongo import MongoClient
from sentence_transformers import SentenceTransformer
import os, logging
from dotenv import load_dotenv
from utils.data import csv_exists, DataNotFoundError

load_dotenv()
logging.getLogger("transformers").setLevel(logging.ERROR)

# Tỷ giá chuyển đổi Indian Rupee -> VNĐ
INR_TO_VND = 291.15
MODEL_PATH = "./gte-multilingual-base"

# Khởi tạo model giống như trong dự án
model = SentenceTransformer(MODEL_PATH, trust_remote_code=True)

def upload_laptop_data(csv_path: str):
    if csv_exists(file_name=csv_path):
        df = pd.read_csv(csv_path)
    else:
        raise DataNotFoundError
    
    # Đổi tên cột đầu tiên thành _id
    if df.columns[0] == 'Unnamed: 0':
        df.rename(columns={df.columns[0]: '_id'}, inplace=True)
    
    # Chuyển đổi cột price sang VNĐ
    df['price'] = df['price'] * INR_TO_VND

    # Tạo combined_information từ các cột (giống logic build_chromadb.py)
    cols = [c for c in df.columns if c not in ['_id', 'image', 'embedding']]
    df['combined_information'] = df.apply(lambda row: ', '.join(f"{col}: {row[col]}" for col in cols), axis=1)

    # Tạo vector embedding
    embeddings = model.encode(df['combined_information'].tolist())

    # Kết nối và đẩy dữ liệu lên MongoDB
    client = MongoClient(os.getenv("MONGODB_URI"))
    collection = client[os.getenv("MONGODB_NAME")][os.getenv("MONGODB_COLLECTION")]
    collection.delete_many({}) # Xóa toàn bộ document hiện có
    
    documents = []
    for i, row in df.iterrows():
        doc = row.to_dict()
        doc['embedding'] = embeddings[i].tolist() # Trường này phải khớp với Vector Index trên Atlas
        documents.append(doc)

    collection.insert_many(documents)
    print(f"Đã đẩy thành công {len(documents)} laptop lên MongoDB Atlas.")

if __name__ == "__main__":
    upload_laptop_data('data/laptop.csv')