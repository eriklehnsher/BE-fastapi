async def get_all_user(skip: int = 0, limit: int = 10):
    # Sử dụng skip và limit để phân trang nếu cần
    cursor = Users_db.find().skip(skip).limit(limit)
    users = await cursor.to_list(length=limit)  # <-- Dòng gây lỗi
    
    # Chuyển đổi Cursor thành danh sách bằng hàm list()
    users = list(cursor)
    
    return users
