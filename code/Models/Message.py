from datetime import datetime

class Message:
    def __init__(self, author_role: str, content: str):
        self.author_role = author_role  # 'client' or 'operator' or 'technician'
        self.content = content
        self.sent_at = datetime.now().isoformat()

    def to_dict(self) -> dict:
        return {
            "author_role": self.author_role,
            "content": self.content,
            "sent_at": self.sent_at,
        }