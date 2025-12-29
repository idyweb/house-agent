import pytest
from sqlalchemy.orm import Session, Mapped, mapped_column
from sqlalchemy import String
from api.db.base_model import BaseModel, Base

# Create a concrete model for testing the abstract BaseModel
class TestModel(BaseModel):
    __tablename__ = "test_model"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50))

def test_base_model_insert(db_session: Session):
    # Ensure table exists (it should be created by setup_database fixture if added to Base.metadata)
    # TestModel.__table__.create(db_session.bind)
    
    obj = TestModel(name="test_item")
    obj.insert(db_session)
    
    fetched = TestModel.fetch_one(db_session, name="test_item")
    assert fetched is not None
    assert fetched.name == "test_item"
    assert fetched.created_at is not None
    assert fetched.updated_at is not None
    assert obj.id == fetched.id
    assert obj.id is not None
def test_base_model_update(db_session: Session):
    TestModel.__table__.create(db_session.bind, checkfirst=True)
    obj = TestModel(name="initial")
    obj.insert(db_session)
    
    obj.name = "updated"
    obj.update(db_session)
    
    fetched = TestModel.fetch_one(db_session, id=obj.id)
    assert fetched.name == "updated"
    assert fetched.updated_at >= fetched.created_at

def test_base_model_delete(db_session: Session):
    TestModel.__table__.create(db_session.bind, checkfirst=True)
    obj = TestModel(name="to_delete")
    obj.insert(db_session)
    
    obj.delete(db_session)
    
    fetched = TestModel.fetch_one(db_session, name="to_delete")
    assert fetched is None
