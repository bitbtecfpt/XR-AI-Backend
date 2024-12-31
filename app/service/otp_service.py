import logging
import threading
from typing import Dict
from random import randint

from app.helper.send_email import send_email_otp
from app.schemas.request.otp_request import OtpSendRequest, OtpVerifyRequest
from app.schemas.response.otp_response import TransIdVerifyResponse


class OtpService(object):
    # Bộ nhớ tạm để lưu OTP
    otp_storage: Dict[str, str] = {}

    def __init__(self) -> None:
        pass

    @staticmethod
    def generate_otp(length=6) -> str:
        """
        Tạo mã OTP ngẫu nhiên.
        :param length: Độ dài mã OTP (mặc định là 6).
        :return: Chuỗi mã OTP.
        """
        try:
            # Tạo mã OTP ngẫu nhiên gồm các chữ số
            return ''.join([str(randint(0, 9)) for _ in range(length)])
        except Exception as e:
            # Ghi log lỗi
            logging.error(f"Error during OTP generation: {e}")
            raise Exception(f"Error during OTP generation: {e}")

    @staticmethod
    def generate_trans_id() -> str:
        """
        Tạo transId ngẫu nhiên.
        :return: Chuỗi transId.
        """
        try:
            return f"TRANS{randint(100000, 999999)}"
        except Exception as e:
            logging.error(f"Error during transId generation: {e}")
            raise Exception(f"Error during transId generation: {e}")

    @classmethod
    def save_otp(cls, email: str, otp: str, ttl: int = 300):
        """
        Lưu OTP vào bộ nhớ tạm với thời gian tồn tại (TTL).
        :param email: Địa chỉ email nhận OTP.
        :param otp: Mã OTP.
        :param ttl: Thời gian tồn tại của OTP (mặc định là 300 giây).
        """
        try:
            cls.otp_storage[email] = otp
            # Tự động xóa sau khi hết TTL
            timer = threading.Timer(ttl, lambda: cls.otp_storage.pop(email, None))
            timer.start()
        except Exception as e:
            logging.error(f"Error saving OTP: {e}")
            raise Exception(f"Error saving OTP: {e}")

    @classmethod
    def verify_otp(cls, request: OtpVerifyRequest):
        """
        Kiểm tra mã OTP có hợp lệ hay không.
        :param request: Dữ liệu yêu cầu xác minh OTP.
        :return: True nếu hợp lệ, ngược lại False.
        """
        try:
            email = request.email
            input_otp = request.otp

            # Lấy OTP và transId từ bộ nhớ
            stored_otp = cls.otp_storage.get(email)
            if stored_otp == input_otp:
                # Xóa OTP sau khi xác thực thành công
                trans_id = cls.generate_trans_id()
                cls.otp_storage.pop(email, None)
                cls.otp_storage[email] = trans_id
                return TransIdVerifyResponse(trans_id=trans_id)
            raise Exception("Invalid OTP")
        except Exception as e:
            # Ghi log lỗi
            logging.error(f"Error during OTP validation: {e}")
            raise Exception(f"Error during OTP validation: {e}")

    @classmethod
    def send_email_otp(cls, request: OtpSendRequest):
        """
              Gửi mã OTP qua email.
              :param request: Dữ liệu yêu cầu gửi OTP.
              """
        try:
            # Tạo mã OTP và transId
            otp = cls.generate_otp()

            # Lưu OTP và transId vào bộ nhớ tạm
            cls.save_otp(request.email, otp, ttl=300)

            send_email_otp(request.email, otp)

        except Exception as e:
            print(f"Failed to send email: {str(e)}")
            raise Exception(f"Failed to send email: {str(e)}")

    @classmethod
    def verify_trans_id(cls, email: str, trans_id: str) -> bool:
        """
        Kiểm tra transId có hợp lệ hay không.
        :param email: Địa chỉ email nhận OTP.
        :param trans_id: Mã transId.
        :return: True nếu hợp lệ, ngược lại False.
        """
        try:
            stored_trans_id = cls.otp_storage.get(email)
            if trans_id == stored_trans_id:
                return True
            return False
        except Exception as e:
            logging.error(f"Error during transId validation: {e}")
            raise Exception(f"Error during transId validation: {e}")
