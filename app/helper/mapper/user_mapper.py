from app.model.models import User
from app.schemas.request.authentication_request import RegisterRequest


class userMapper:
    @staticmethod
    def map_to_user(user_data: RegisterRequest):
        return User(
            name=user_data.name,
            hash_password=user_data.password,
            email=user_data.email,
            gender=user_data.gender.value,
            birth_year=user_data.birth_year,

        )