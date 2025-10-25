from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey, DateTime, select, func
from sqlalchemy.orm import declarative_base, sessionmaker, relationship, Session, selectinload
import random
from datetime import datetime, timedelta


# ----------------- Модели -----------------
Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    orders = relationship("Order", back_populates="user")

class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    order_items = relationship("OrderItem", back_populates="product")

class Order(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    user = relationship("User", back_populates="orders")
    items = relationship("OrderItem", back_populates="order")

class OrderItem(Base):
    __tablename__ = "order_items"
    id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey("orders.id"))
    product_id = Column(Integer, ForeignKey("products.id"))
    quantity = Column(Integer, default=1)
    order = relationship("Order", back_populates="items")
    product = relationship("Product", back_populates="order_items")

# ----------------- Подключение к БД -----------------
engine = create_engine("sqlite:///shop.db", echo=False)
Base.metadata.create_all(engine)
session = sessionmaker(bind=engine)

# написание запросов 
# with session() as ses:
#     ses:Session

#     users = ses.execute(query)

#     print(users.all())

# ----------------- Генерация данных -----------------
# session = session()
# # 1. Пользователи
# users = [User(name=f"User{i}", email=f"user{i}@mail.com") for i in range(1, 11)]
# session.add_all(users)

# # 2. Продукты
# products = [Product(name=f"Product{i}", price=round(random.uniform(5, 100), 2)) for i in range(1, 21)]
# session.add_all(products)

# session.commit()

# # 3. Заказы и элементы заказа
# for _ in range(30):  # создаем 30 заказов
#     user = random.choice(users)
#     order = Order(user=user, created_at=datetime.utcnow() - timedelta(days=random.randint(0, 30)))
#     session.add(order)

#     for _ in range(random.randint(1, 5)):  # 1-5 товаров в заказе
#         product = random.choice(products)
#         quantity = random.randint(1, 3)
#         order_item = OrderItem(order=order, product=product, quantity=quantity)
#         session.add(order_item)

# session.commit()

# print("Данные сгенерированы успешно!")
