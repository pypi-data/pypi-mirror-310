"""
# File       : http_exception.py
# Time       ：2024/11/21 10:39
# Author     ：xuewei zhang
# Email      ：shuiheyangguang@gmail.com
# version    ：python 3.12
# Description：适配 VUE-ELEMENT-PLUS-ADMIN 的 HTTPException
"""
from fastapi import HTTPException


class HTTPException_VueElementPlusAdmin(HTTPException):
    """自定义异常类"""

    def __init__(
        self,
        error_code: int,
        detail: str,
        http_status_code: int = 404
    ):
        super().__init__(
            status_code=http_status_code,
            detail={
                "code": error_code,
                "data": detail
            }
        )