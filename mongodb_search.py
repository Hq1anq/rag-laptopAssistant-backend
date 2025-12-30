import os, logging
from dotenv import load_dotenv
from rag.core import RAG
from utils.style import getColorText

logging.getLogger("transformers").setLevel(logging.ERROR)

# 1. Load cấu hình từ .env
load_dotenv()

def test_closest_laptop():
    print("--- KIỂM TRA TRUY XUẤT LAPTOP SÁT NHẤT TỪ MONGODB ---")

    # 3. Khởi tạo đối tượng RAG với kết nối MongoDB
    rag_system = RAG(
        type='mongodb',
        mongodbUri=os.getenv("MONGODB_URI"),
        dbName=os.getenv("MONGODB_NAME"),
        dbCollection=os.getenv("MONGODB_COLLECTION"),
        embeddingName='./gte-multilingual-base',
        llm=None
    )

    # 4. Các câu truy vấn thử nghiệm
    queries = [
        "Tôi cần laptop gaming HP Victus",
        "Laptop Acer nào rẻ nhất?",
        "Tìm máy văn phòng có CPU Intel Core i3"
    ]

    for query in queries:
        print(getColorText(query, "green"))
        
        # Gọi hàm tìm kiếm vector
        # limit=1 để lấy cái sát nhất
        results = rag_system.vector_search(user_query=query, limit=1)
        
        if results and len(results) > 0:
            top_result = results[0]
            print(f"Kết quả sát nhất tìm thấy:")
            # In ra các trường dựa trên cấu hình MongoDB của bạn
            print(f"- Tên máy: {getColorText(top_result.get('name'), "yellow")}")
            print(f"- Giá: {getColorText(top_result.get('price'), "yellow")}")
            print(f"- Score: {getColorText(top_result.get('score'), "yellow")}")
        else:
            print("❌ Không tìm thấy kết quả nào phù hợp.")
        print("-" * 50)

def top_4_closest_laptops(query: str):
    print("--- KIỂM TRA TRUY XUẤT TOP 4 LAPTOP SÁT NHẤT TỪ MONGODB ---")

    # 3. Khởi tạo đối tượng RAG với kết nối MongoDB
    rag_system = RAG(
        type='mongodb',
        mongodbUri=os.getenv("MONGODB_URI"),
        dbName=os.getenv("MONGODB_NAME"),
        dbCollection=os.getenv("MONGODB_COLLECTION"),
        embeddingName='./gte-multilingual-base',
        llm=None
    )

    print(getColorText(query, "green"))
    
    # Gọi hàm tìm kiếm vector
    # limit=4 để lấy top 4 kết quả sát nhất
    results = rag_system.vector_search(user_query=query, limit=4)
    
    if results and len(results) > 0:
        print(f"Top 4 kết quả sát nhất tìm thấy:")
        for idx, result in enumerate(results, start=1):
            print(f"{idx}. Tên máy: {getColorText(result.get('name'), "yellow")}, CPU: {getColorText(result.get('processor'), "yellow")}, Score: {getColorText(result.get('score'), "yellow")}")
    else:
        print("❌ Không tìm thấy kết quả nào phù hợp.")

if __name__ == "__main__":
    test_closest_laptop()
    # top_4_closest_laptops("Intel Core i3")
    # top_4_closest_laptops("AMD Ryzen 7")
    # top_4_closest_laptops("Cho tôi laptop văn phòng AMD Ryzen 7")