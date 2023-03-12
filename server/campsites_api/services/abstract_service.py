from typing import List, Generic, Optional, Type, TypeVar
from fastapi import HTTPException
from pydantic import UUID4, BaseModel

from sqlalchemy.orm import Session

from campsites_db.models import Base


ModelType = TypeVar("ModelType", bound=Base)
ModelTypeDTO = TypeVar("ModelTypeDTO", bound=BaseModel)


class AbstractService(Generic[ModelType, ModelTypeDTO]):
    def __init__(self, model: Type[ModelType], session: Session):
        self.model = model
        self.session = session

    def get(self, id: UUID4) -> Optional[ModelType]:
        result: Optional[ModelType] = (
            self.session.query(self.model).filter_by(id=id).first()
        )
        if result is None:
            raise HTTPException(status_code=404, detail=f"Item with id {id} not found")
        return result

    def list(
        self, limit: Optional[int] = 25, offset: Optional[int] = 0
    ) -> List[ModelType]:
        query = self.session.query(self.model)
        query = query.limit(limit)
        query = query.offset(offset)
        result: List[ModelType] = query.all()
        return result

    def create(self, item: ModelTypeDTO) -> ModelType:
        item: ModelType = self.model(**item.dict())
        self.session.add(item)
        try:
            self.session.commit()
        except:
            self.session.rollback()
            raise HTTPException(status_code=422, detail="Item could not be created.")
        return item

    # we are not going to return the list of objects, as it could be quite large
    def bulk_create(self, items: List[ModelTypeDTO]) -> None:
        items: List[ModelType] = [self.model(**item.dict()) for item in items]
        self.session.add_all(items)
        try:
            self.session.commit()
        except:
            self.session.rollback()
            raise HTTPException(status_code=422, detail="Items could not be created.")

    def update(self, id: UUID4, item: ModelTypeDTO) -> ModelTypeDTO:
        db_item = self.get(id)
        if db_item is None:
            raise HTTPException(status_code=404, detail=f"Item with id {id} not found")
        for key, value in item.dict().items():
            # we want to ensure we are not overwriting the ID
            if key != "id":
                setattr(db_item, key, value)
        self.session.commit()
        return db_item

    def delete(self, id: UUID4) -> None:
        item = self.session.query(self.model).filter_by(id=id).first()
        if item is None:
            raise HTTPException(status_code=404, detail=f"Item with id {id} not found")
        self.session.delete(item)
        self.session.commit()
