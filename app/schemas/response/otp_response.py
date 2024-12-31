from pydantic import BaseModel


class RequiredOtp(BaseModel):
    trans_id: str


class OtpResponse(RequiredOtp):
    pass


class OtpVerifyResponse(RequiredOtp):
    email: str


class TransIdVerifyResponse(BaseModel):
    trans_id: str
