from sqlalchemy import ForeignKey, Table, Column, Integer, String, Float, create_engine
from sqlalchemy.orm import relationship, sessionmaker, DeclarativeBase, Mapped, mapped_column
import requests


class Base(DeclarativeBase):
    pass


# Association table for many-to-many relationship between Carts and Products
cart_product_association = Table(
    'cart_product', Base.metadata,
    Column('cart_id', Integer, ForeignKey('carts.id'), primary_key=True),
    Column('product_id', Integer, ForeignKey('products.id'), primary_key=True),
    Column('quantity', Integer, nullable=False, default=1)
)


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    id_api: Mapped[int] = mapped_column(Integer, unique=True, nullable=False)  # API ID
    email: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    username: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String, nullable=False)
    name: Mapped[str] = mapped_column(String, nullable=False)
    phone: Mapped[str] = mapped_column(String, nullable=True)

    carts: Mapped[list['Cart']] = relationship(back_populates='user')


class Product(Base):
    __tablename__ = 'products'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    id_api: Mapped[int] = mapped_column(Integer, unique=True, nullable=False)  # API ID
    title: Mapped[str] = mapped_column(String, nullable=False)
    price: Mapped[float] = mapped_column(Float, nullable=False)
    description: Mapped[str] = mapped_column(String, nullable=True)
    category: Mapped[str] = mapped_column(String, nullable=True)
    image: Mapped[str] = mapped_column(String, nullable=True)

    carts: Mapped[list['Cart']] = relationship(secondary=cart_product_association, back_populates='products')


class Cart(Base):
    __tablename__ = 'carts'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    id_api: Mapped[int] = mapped_column(Integer, unique=True, nullable=False)  # API ID
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'), nullable=False)

    user: Mapped['User'] = relationship(back_populates='carts')
    products: Mapped[list['Product']] = relationship(secondary=cart_product_association, back_populates='carts')


# Database setup
DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(DATABASE_URL, echo=True)
Session = sessionmaker(bind=engine)
session = Session()

# Create tables
Base.metadata.create_all(engine)


# Populate database with Fake Store API data
def fetch_and_populate():
    product_response = requests.get("https://fakestoreapi.com/products")
    if product_response.status_code == 200:
        products = product_response.json()
        for prod in products:
            product = Product(
                id_api=prod['id'],
                title=prod['title'],
                price=prod['price'],
                description=prod['description'],
                category=prod['category'],
                image=prod['image']
            )
            session.add(product)
    session.commit()
    user_response = requests.get("https://fakestoreapi.com/users")
    if user_response.status_code == 200:
        users = user_response.json()
        for usr in users:
            user = User(
                id_api=usr['id'],
                email=usr['email'],
                username=usr['username'],
                password=usr['password'],
                name=f"{usr['name']['firstname']} {usr['name']['lastname']}",
                phone=usr['phone']
            )
            session.add(user)

    cart_response = requests.get("https://fakestoreapi.com/carts")
    if cart_response.status_code == 200:
        carts = cart_response.json()
        for cart in carts:
            user = session.query(User).filter_by(id_api=cart['userId']).first()
            if user:
                new_cart = Cart(
                    id_api=cart['id'],
                    user_id=user.id
                )
                session.add(new_cart)

                for item in cart['products']:
                    product = session.query(Product).filter_by(id_api=item['productId']).first()
                    if product:
                        session.execute(
                            cart_product_association.insert().values(
                                cart_id=new_cart.id,
                                product_id=product.id,
                                quantity=item['quantity']
                            )
                        )

    session.commit()


fetch_and_populate()
