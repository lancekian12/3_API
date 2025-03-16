from . import db
from sqlalchemy.sql import func


class Users(db.Model):
    __tablename__ = "users"  # Ensure this matches your actual table name
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)  # Change to lowercase
    last_name = db.Column(db.String(100), nullable=False)  # Change to lowercase
    password = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())

    funds = db.relationship("Funds", backref="user")  # Use "user" for clarity

    def __repr__(self):
        return f"<User  {self.first_name}>"


class Funds(db.Model):
    __tablename__ = "funds"  # Ensure this matches your actual table name
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Numeric(10, 2), nullable=False)
    userId = db.Column(
        db.Integer, db.ForeignKey("users.id"), nullable=False
    )  # Use lowercase "users"
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())

    @property
    def serialize(self):
        """Return object data in easily serializable format"""
        return {
            "id": self.id,
            "amount": self.amount,
            "created_at": self.created_at,
        }
