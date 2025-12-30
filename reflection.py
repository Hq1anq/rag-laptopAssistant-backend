import os
from dotenv import load_dotenv
from llms.llms import LLMs
from utils.style import getColorText, display_chat_history
from reflection import Reflection

def test_demo_reflection():
    load_dotenv()
    
    # 1. Khởi tạo LLM Gemini
    llm = LLMs(
        type="online",
        model_name="gemini",
        model_version="gemini-2.5-flash-lite",
        api_key=os.getenv("GEMINI_API_KEY")
    )

    reflection = Reflection(llm)

    test_scenarios = [
        {
            "name": "Sử dụng đại từ thay thế",
            "history": [
                {"role": "user", "content": "Tôi muốn tìm hiểu về laptop HP Victus 15."},
                {"role": "assistant", "content": "HP Victus 15 là dòng laptop gaming có card đồ họa AMD Radeon RX 6500M."},
                {"role": "user", "content": "Nó có giá bao nhiêu?"} # Câu hỏi cần Reflection
            ]
        },
        {
            "name": "Hỏi về cấu hình tiếp nối",
            "history": [
                {"role": "user", "content": "Acer One 14 dùng chip gì?"},
                {"role": "assistant", "content": "Acer One 14 sử dụng chip Intel Core i3 thế hệ 11."},
                {"role": "user", "content": "Thế còn Ram thì sao?"} # Câu hỏi cần Reflection
            ]
        },
        {
            "name": "Hội thoại dài + So sánh ngầm định",
            "history": [
                {"role": "user", "content": "Mình đang xem con HP Victus 15 giá 15 triệu."},
                {"role": "assistant", "content": "Đó là một lựa chọn tốt trong tầm giá với card đồ họa RX 6500M."},
                {"role": "user", "content": "Thế còn Asus TUF A15 thì sao?"},
                {"role": "assistant", "content": "Asus TUF A15 mạnh hơn với RTX 3060 nhưng giá cao hơn, khoảng 33 triệu VNĐ."},
                {"role": "user", "content": "Con nào chơi game nặng tốt hơn và đáng tiền hơn?"} # Câu hỏi cần Reflection
            ]
        },
        {
            "name": "Thay đổi thuộc tính liên tục (Context Switching)",
            "history": [
                {"role": "user", "content": "Laptop Acer One 14 có mấy GB Ram?"},
                {"role": "assistant", "content": "Dòng Acer One 14 bạn đang xem có 8GB RAM."},
                {"role": "user", "content": "Nâng cấp lên 16GB được không?"},
                {"role": "assistant", "content": "Có, máy này hỗ trợ nâng cấp thêm thanh RAM nữa."},
                {"role": "user", "content": "Vậy tổng giá sau khi nâng là bao nhiêu?"} # Câu hỏi cần Reflection
            ]
        },
        {
            "name": "Sử dụng từ lóng và viết tắt",
            "history": [
                {"role": "user", "content": "Shop có bán Dell XPS không?"},
                {"role": "assistant", "content": "Hiện tại shop mình chỉ tập trung các dòng HP, Asus và Acer thôi ạ."},
                {"role": "user", "content": "Vậy lấy cho mình thông tin con Vivobook 15X."},
                {"role": "assistant", "content": "Asus Vivobook 15X dùng chip i3 thế hệ 13, giá khoảng 13.5 triệu VNĐ."},
                {"role": "user", "content": "Chip đấy có yếu quá không?"} # Câu hỏi cần Reflection
            ]
        },
        {
            "name": "Câu hỏi lửng lơ (Ellipsis)",
            "history": [
                {"role": "user", "content": "Mình cần tìm laptop cho đồ họa."},
                {"role": "assistant", "content": "Bạn nên chọn Asus TUF A15 với màn hình 144Hz và card RTX 3060."},
                {"role": "user", "content": "Còn bảo hành?"} # Câu hỏi cực ngắn
            ]
        }
    ]

    terminal_width = 125
    for scenario in test_scenarios:
        print(f"--- KỊCH BẢN {getColorText(scenario['name'], 'cyan')} ---")
        display_chat_history(chat_history=scenario['history'], terminal_width=terminal_width)

        reflected_query = reflection(scenario['history'])
        padding1 = " " * (terminal_width - len(reflected_query) - 3)
        print(f"{padding1}-> {getColorText(reflected_query, "green")}")

if __name__ == "__main__":
    test_demo_reflection()