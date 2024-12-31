from typing import List, Optional, Type
from sqlalchemy.orm import Session

from app.model.models import User
from app.helper.mapper.user_mapper import userMapper
from app.schemas.request.authentication_request import RegisterRequest


class UserRepository:
    """
    UserRepository sẽ xử lý các thao tác với bảng User trong cơ sở dữ liệu.
    """

    def __init__(self, db_session: Session):
        self.db_session = db_session

    def get_user_by_id(self, user_id: int) -> Optional[User]:
        """
        Lấy thông tin người dùng dựa trên user_id.

        Args:
            user_id (int): ID của người dùng.

        Returns:
            User: Đối tượng User nếu tìm thấy, None nếu không tìm thấy.
        """
        return self.db_session.query(User).filter(User.id == user_id).first()

    def get_user_by_email(self, email: str) -> Optional[User]:
        """
        Lấy thông tin người dùng dựa trên email.

        Args:
            email (str): Email của người dùng.

        Returns:
            User: Đối tượng User nếu tìm thấy, None nếu không tìm thấy.
        """

        return self.db_session.query(User).filter(User.email == email).first()

    def create_user(self, user_data: RegisterRequest) -> User:
        """
        Tạo một người dùng mới.

        Args:
            user_data (RegisterRequest): Dữ liệu người dùng từ yêu cầu API.

        Returns:
            User: Đối tượng User mới được tạo.
        """
        new_user = userMapper.map_to_user(user_data)

        self.db_session.add(new_user)
        self.db_session.commit()
        self.db_session.refresh(new_user)
        return new_user

    def get_all_users(self) -> list[Type[User]]:
        """
        Lấy tất cả người dùng.

        Returns:
            List[User]: Danh sách tất cả người dùng.
        """
        return self.db_session.query(User).all()

    def update_user(self, user_id: int, user_data: RegisterRequest) -> Optional[User]:
        """
        Cập nhật thông tin người dùng.

        Args:
            user_id (int): ID của người dùng cần cập nhật.
            user_data (RegisterRequest): Dữ liệu mới.

        Returns:
            User: Đối tượng User đã được cập nhật.
        """
        user = self.db_session.query(User).filter(User.id == user_id).first()
        if user:
            # Duyệt qua tất cả các trường trong User model
            for column in user.__table__.columns:
                current_value = getattr(user, column.name)
                new_value = getattr(user_data, column.name, None)  # Lấy giá trị mới từ user_data
                if new_value != current_value:
                    setattr(user, column.name, new_value)  # Cập nhật giá trị mới nếu có sự thay đổi

            self.db_session.commit()
            self.db_session.refresh(user)
            return user

        return None

    def delete_user(self, user_id: int) -> bool:
        """
        Xóa người dùng dựa trên user_id.

        Args:
            user_id (int): ID của người dùng cần xóa.

        Returns:
            bool: True nếu xóa thành công, False nếu không tìm thấy người dùng.
        """
        user = self.db_session.query(User).filter(User.id == user_id).first()
        if user:
            self.db_session.delete(user)
            self.db_session.commit()
            return True
        return False
