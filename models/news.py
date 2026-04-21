from datetime import datetime
from typing import Optional
from sqlalchemy import DateTime, ForeignKey, Index, Integer, Text, func, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

# 基类：创建时间、更新时间
class Base(DeclarativeBase):
    # Mapped[T] 是 SQLAlchemy 2.0 新语法，用于类型提示，表示该属性是一个映射到数据库列的字段
    created_at: Mapped[datetime] = mapped_column(
        DateTime, 
        default=datetime.now,
        comment="创建时间"
        )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, 
        default=datetime.now, 
        onupdate=datetime.now,  # 每次更新时自动设置为当前时间
        comment="更新时间"
        )
    
# 表对应的模型类：继承基类，定义表结构
class Category(Base):  # 继承 Base → 自动变成表
    __tablename__ = "news_category"  # 指定表名

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, comment="分类ID")
    name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False, comment="分类名称")
    sort_order: Mapped[int] = mapped_column(Integer, default=0, nullable=False, comment="排序")

    def __repr__(self):
        return f"<Category(id={self.id}, name='{self.name}', sort_order={self.sort_order})>"
    # __repr__ = 给程序员看的对象字符串
    # 没有它 → 打印出来是内存地址（看不懂）
    # 有它 → 打印出来是清晰数据（方便调试）

class News(Base):
    __tablename__ = "news"

    # 创建索引：提升查询速度 → 添加目录
    __table_args__ = (
        Index('fk_news_category_idx', 'category_id'),  # 高频查询场景
        Index('idx_publish_time', 'publish_time')  # 按发布时间排序
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, comment="新闻ID")
    title: Mapped[str] = mapped_column(String(255), nullable=False, comment="新闻标题")
    description: Mapped[Optional[str]] = mapped_column(String(500), comment="新闻简介")
    content: Mapped[str] = mapped_column(Text, nullable=False, comment="新闻内容")
    image: Mapped[Optional[str]] = mapped_column(String(255), comment="封面图片URL")  # Optional[str] → 可以是字符串，也可以是 None（空）
    author: Mapped[Optional[str]] = mapped_column(String(50), comment="作者")
    category_id: Mapped[int] = mapped_column(Integer, ForeignKey('news_category.id'), nullable=False, comment="分类ID")
    views: Mapped[int] = mapped_column(Integer, default=0, nullable=False, comment="浏览量")
    publish_time: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, comment="发布时间")

    def __repr__(self):
        return f"<News(id={self.id}, title='{self.title}', views={self.views})>"