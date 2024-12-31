import logging

import bcrypt

from app.schemas.request.authentication_request import RegisterRequest, AuthenticationRequest
from app.schemas.response.authentication_response import AuthenticationResponse
from app.repository.user_repository import UserRepository
from sqlalchemy.orm import session
from app.core.JWT_security import create_jwt_token
from app.service.otp_service import OtpService


class AuthenticationService(object):

    def __init__(self, db_session: session) -> None:
        self.db_session = db_session
        self.user_repository = UserRepository(db_session)
        self.otp_service = OtpService()

    def register(self, request: RegisterRequest) -> None:
        try:
            # check email exist
            user = self.user_repository.get_user_by_email(request.email)
            if user:
                raise Exception("Email already exists")

            # Kiểm tra trans_id
            verify = self.otp_service.verify_trans_id(request.email, request.trans_id)
            if not verify:
                raise Exception("TransId is invalid")

            # Mã hóa mật khẩu trước khi lưu vào cơ sở dữ liệu
            hashed_password = bcrypt.hashpw(request.password.encode('utf-8'), bcrypt.gensalt())
            request.password = hashed_password.decode('utf-8')

            # create user
            self.user_repository.create_user(request)
        except Exception as e:
            logging.error(e)
            raise e

    def authentication(self, request: AuthenticationRequest) -> AuthenticationResponse:
        try:
            user = self.user_repository.get_user_by_email(request.email)
            if not user:
                raise Exception("Email not found")

            # Kiểm tra mật khẩu
            check_password = bcrypt.checkpw(request.password.encode('utf-8'), user.hash_password.encode('utf-8'))
            if not check_password:
                raise Exception("Password is incorrect")

            # Tạo Firebase Custom Token
            id_token = create_jwt_token(user.id, user.email)

            return AuthenticationResponse(token=id_token)
        except Exception as e:
            logging.error(e)
            raise e
