
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError, SQLAlchemyError  

from utils.exception import general_exception_handler, http_exception_handler, integrity_error_handler, sqlalchemy_error_handler


def register_exception_handlers(app):
    """
    注册全局异常处理器，子类在前，父类在后。具体的前，抽象的在后。
    """
    app.add_exception_handler(HTTPException, http_exception_handler)    # 业务层面的报错
    app.add_exception_handler(IntegrityError, integrity_error_handler)  # 数据库完整性约束错误
    app.add_exception_handler(SQLAlchemyError, sqlalchemy_error_handler)  # SQLAlchemy数据库
    app.add_exception_handler(Exception, general_exception_handler)  # 捕获所有未处理的异常