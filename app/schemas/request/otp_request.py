from pydantic import BaseModel


class OtpSendRequest(BaseModel):
    email: str


class OtpVerifyRequest(BaseModel):
    email: str
    otp: str


class TransIdVerifyRequest(BaseModel):
    email: str
    transId: str
