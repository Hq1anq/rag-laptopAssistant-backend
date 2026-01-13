class Reflection():
    def __init__(self, llm):
        self.llm = llm

    def _concat_and_format_texts(self, data):
        concatenatedTexts = []
        for entry in data:
            role = entry.get('role', '')
            content = entry.get('content', '') or entry.get('text', '')
            concatenatedTexts.append(f"{role}: {content} \n")
        return ''.join(concatenatedTexts)

    def __call__(self, chatHistory):
        history_string = self._concat_and_format_texts(chatHistory)

        prompt = f"""Bạn là một chuyên gia phân tích ngữ cảnh hội thoại. 
        Nhiệm vụ của bạn là kiểm tra xem câu hỏi mới nhất có liên quan đến các đối tượng Laptop đã thảo luận trong lịch sử hay không.

        LỊCH SỬ CHAT:
        {history_string}

        QUY TẮC XỬ LÝ:
        1. Nếu câu hỏi mới sử dụng đại từ (nó, con này, cái đấy, giá, màu sắc...) liên quan đến Laptop trong lịch sử -> Hãy tạo lại một câu hỏi độc lập bằng tiếng Việt sao cho người đọc có thể hiểu được nội dung mà không cần xem lại lịch sử. 
        2. Nếu câu hỏi mới là một câu tán gẫu, chào hỏi hoặc hoàn toàn KHÔNG liên quan đến Laptop (ví dụ: "Bạn tên gì?", "Ăn cơm chưa?", "Thời tiết sao rồi?") -> Bạn phải TRẢ VỀ NGUYÊN VĂN câu hỏi mới, không được thêm thắt thông tin laptop vào.

        CHỈ TRẢ VỀ CÂU HỎI CUỐI CÙNG, KHÔNG GIẢI THÍCH.
        """

        higherLevelSummariesPrompt = {
            "role": "user",
            "content": prompt
        }

        # Gọi LLM
        completion = self.llm.generate_content([higherLevelSummariesPrompt])
        
        # Trích xuất text từ response
        if hasattr(completion, 'text'):
            return completion.text
        return completion