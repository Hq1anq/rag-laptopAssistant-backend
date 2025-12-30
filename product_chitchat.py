from dotenv import load_dotenv
from embeddings import SentenceTransformerEmbedding, EmbeddingConfig
from semantic_router import SemanticRouter, Route
from utils.style import getColorText
from semantic_router.samples import laptopProductsSample, chitchatSample

import logging
logging.getLogger("transformers").setLevel(logging.ERROR)

# Load môi trường (để lấy cấu hình nếu cần)
load_dotenv()

MODEL_PATH = "./gte-multilingual-base"

def test_semantic_router():
    # Khởi tạo model Embedding
    embedding = SentenceTransformerEmbedding(
        config=EmbeddingConfig(name=MODEL_PATH)
    )

    product_route = Route(name="products", samples=laptopProductsSample)
    chitchat_route = Route(name="chitchat", samples=chitchatSample)

    router = SemanticRouter(embedding, routes=[product_route, chitchat_route])

    test_queries = [
        "Chào bạn, bạn tên là gì?",
        "Tôi muốn mua laptop chơi game",
        "Giá của máy HP Victus là bao nhiêu?",
        "Thời tiết hôm nay thế nào?",
        "Cấu hình máy Acer One 14 ra sao?",
        "Chính sách bảo hành của cửa hàng mình thế nào?",
        "Cho xem ảnh con máy Asus Vivobook với",
        "Thời tiết này đi mua laptop thì hết nước chấm",

        "Bạn có thích ăn táo (apple) không?",
        # Có thể nhầm Apple là thương hiệu laptop
        "Máy tính của tôi đang bị hỏng màn hình, phải làm sao?",
        # Đây là câu hỏi sửa chữa, không phải mua hàng
        "Lương của nhân viên bán laptop thường là bao nhiêu?"
        # Có từ laptop nhưng hỏi về nghề nghiệp
    ]

    print("\n--- Bắt đầu kiểm tra phân loại ---")
    for query in test_queries:
        # Hàm guide trả về (tên_route, confidence_score)
        # Ở đây serve.py lấy phần tử index [1] làm kết quả định hướng router.guide -> (score, route_name)
        guided_result = router.guide(query)[1]
        
        print(query)
        if guided_result == "products":
            print(getColorText("PRODUCT", "green"))
        else: print(getColorText("CHITCHAT", "yellow"))
        print("-" * 40)

if __name__ == "__main__":
    test_queries = test_semantic_router()