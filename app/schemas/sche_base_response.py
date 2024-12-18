# Import các kiểu dữ liệu cần thiết từ thư viện typing
from typing import Optional, TypeVar, Generic


# Import BaseModel từ pydantic để tạo model
from pydantic import BaseModel

# Định nghĩa TypeVar "T" để sử dụng trong GenericModel
T = TypeVar("T")


class ResponseSchemaBase(BaseModel):
    code: str = "unknown"  # Mã code mặc định
    message: str = "Unknown error"  # Thông báo mặc định

    def custom_response(self, code: str, message: str) -> "ResponseSchemaBase":
        """
        Tạo custom response với code và message.

        Args:
            code (str): Mã code của response.
            message (str): Thông báo của response.

        Returns:
            ResponseSchemaBase: Instance mới với các giá trị đã được gán.
        """
        return ResponseSchemaBase(code=code, message=message)


class DataResponse(ResponseSchemaBase, BaseModel, Generic[T]):
    """
    Response schema chứa dữ liệu.

    Kế thừa từ ResponseSchemaBase và GenericModel.
    Cho phép chỉ định kiểu dữ liệu cho trường data.
    """
    # Dữ liệu của response, kiểu dữ liệu được xác định bởi TypeVar T
    data: Optional[T] = None

    class Config:
        arbitrary_types_allowed = True

    def create_response(self, code: str, message: str, **data: T) -> "DataResponse[T]":
        """
        Tạo custom response với code, message và data.

        Args:
            code (str): Mã code của response.
            message (str): Thông báo của response.
            **data (T): Dữ liệu của response. (**..: thể hiện tham số bổ sung)

        Returns:
            DataResponse: Instance mới với các giá trị đã được gán.
        """
        return DataResponse(code=code, message=message, data=data)

    def success_response(self, data: T):
        self.code = '000'
        self.message = 'Success'
        self.data = data
        return self


class MetadataSchema(BaseModel):
    """
    Schema cho metadata của phân trang.
    """
    # Trang hiện tại
    current_page: int
    # Số lượng items trên mỗi trang
    page_size: int
    # Tổng số items
    total_items: int


class PaginatedResponse(DataResponse[T]):
    """
    Response schema dành cho dữ liệu phân trang.
    """
    metadata: Optional[MetadataSchema] = None

    def create_paginated_response(
            self,
            code: str,
            message: str,
            data: T,
            current_page: int,
            page_size: int,
            total_items: int
    ) -> "PaginatedResponse[T]":
        """
        Tạo response phân trang với code, message, data, và metadata.

        Args:
            code (str): Mã code của response.
            message (str): Thông báo của response.
            data (T): Dữ liệu của response.
            current_page (int): Trang hiện tại.
            page_size (int): Số lượng items trên mỗi trang.
            total_items (int): Tổng số items.

        Returns:
            PaginatedResponse[T]: Instance của response phân trang.
        """
        self.code = code
        self.message = message
        self.data = data
        self.metadata = MetadataSchema(
            current_page=current_page,
            page_size=page_size,
            total_items=total_items
        )
        return self

    def success_paginated_response(
            self,
            data: T,
            current_page: int,
            page_size: int,
            total_items: int
    ) -> "PaginatedResponse[T]":
        """
        Tạo success response với code '000', message 'Success', data và metadata.

        Args:
            data (T): Dữ liệu của response.
            current_page (int): Trang hiện tại.
            page_size (int): Số lượng items trên mỗi trang.
            total_items (int): Tổng số items.

        Returns:
            PaginatedResponse[T]: Instance của response phân trang.
        """
        return self.create_paginated_response(
            code="000",
            message="Success",
            data=data,
            current_page=current_page,
            page_size=page_size,
            total_items=total_items
        )
