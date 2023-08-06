import json
from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union

from sqlalchemy import inspection
from sqlmodel import Session, select
from sqlmodel.sql.expression import Select, SelectOfScalar

ModelType = TypeVar("ModelType")
CreateSchemaType = TypeVar("CreateSchemaType")
UpdateSchemaType = TypeVar("UpdateSchemaType")


class CrudBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    primaryKey = None
    SelectOfScalar.inherit_cache = True
    Select.inherit_cache = True

    def __init__(
        self,
        model: Type[ModelType],
        engine,
        primaryKey: Optional[Any] = None,
    ):
        self._model = model
        self._engine = engine
        self.setPrimaryKey(primaryKey)

    def setPrimaryKey(self, primaryKey: Optional[Any] = None):
        if primaryKey is None:
            try:
                self._primaryKey = self._model.id
            except AttributeError:
                self._primaryKey = inspection.inspect(self._model).primary_key[0]
        else:
            self._primaryKey = primaryKey

    def all(self) -> Optional[List[ModelType]]:
        with Session(self._engine) as session:
            statement = select(self._model)
            data = session.exec(statement).all()
        return data

    def create(self, model: CreateSchemaType) -> ModelType:
        if isinstance(model, dict):
            obj_in_data = json.dumps(model)
        else:
            obj_in_data = model.dict()
        with Session(self._engine) as session:
            db_obj = self._model(**obj_in_data)
            session.add(db_obj)
            session.commit()
            session.refresh(db_obj)
        return db_obj

    def find(self, primaryKey) -> Optional[ModelType]:
        with Session(self._engine) as session:
            data = session.exec(
                select(self._model).where(self._primaryKey == primaryKey)
            ).first()
        return data

    def findBy(self, column: str, value, get_many: bool = False) -> Optional[ModelType]:
        statement = select(self._model).where(getattr(self._model, column) == value)
        with Session(self._engine) as session:
            if get_many:
                result = session.exec(statement).all()
            else:
                result = session.exec(statement).first()
        return result

    def update(
        self, model: ModelType, data: Union[UpdateSchemaType, Dict[str, Any]]
    ) -> ModelType:
        model_data = model.dict()
        if isinstance(data, dict):
            update_data = data
        else:
            update_data = data.dict(exclude_unset=True)
        for field in model_data:
            if field in update_data:
                setattr(model, field, update_data[field])
        with Session(self._engine) as session:
            session.add(model)
            session.commit()
            session.refresh(model)
        return model

    def delete(self, model: ModelType) -> ModelType:
        with Session(self._engine) as session:
            session.delete(model)
            session.commit()
        return model

    def deleteMany(self, models: List[ModelType]) -> List[ModelType]:
        for model in models:
            self.delete(model)
        return models
