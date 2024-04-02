from db import Users_db
async def get_all_user(skip: int = 0, limit: int = 10):
    cursor = Users_db.find().skip(skip).limit(limit)
    
    # Tạo danh sách để lưu trữ các tài liệu
    users = []
    
    # Duyệt qua từng tài liệu trong Cursor và thêm vào danh sách
    async for user in cursor:
        users.append(user)
    
    return users

