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

        prompt = """Hệ thống đang hỗ trợ tư vấn laptop. Dựa trên lịch sử trò chuyện và câu hỏi mới nhất của người dùng (có thể chứa các từ thay thế như 'nó', 'con này', 'máy đó'), hãy tạo lại một câu hỏi độc lập bằng tiếng Việt sao cho người đọc có thể hiểu được nội dung mà không cần xem lại lịch sử. 
        LƯU Ý: CHỈ TRẢ VỀ CÂU HỎI ĐÃ ĐƯỢC TỐI ƯU, KHÔNG GIẢI THÍCH GÌ THÊM.

        Lịch sử trò chuyện:
        {historyString}
        """.format(historyString=history_string)

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