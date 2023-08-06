# SQL Crud

This package is build on top [SQLModel](https://sqlmodel.tiangolo.com/) and holds basics crud operations.<br>
The idea with this package is that i got tired of write basics crud operations over and over agin.

## Exempel usage

You need to bring your own engine and schemas

```python
from sqlmodel import Field, SQLModel, create_engine
from pydantic import BaseModel
import sqlcrud

#Base user model
class UserBase(SQLModel):
    name: str

#Sql table schema
class User(UserBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    password: str

#Create user schema
class UserCreate(UserBase):
    password: str

#Update user schema
class UserUpdate(BaseModel):
    name: Optional[str]
    password: Optional[str]

# Create a engine instans
engine = create_engine("sqlite:///database.db", echo=True)
```

Create your crud opetions class and pass in the CrudBase class a parent with your create and update schema definitions

```python
class UserCrud(sqlcrud.BaseCrud[User, UserCreate, UserUpdate]):
    def __init__(self):
        sqlcrud.BaseCrud.__init__(self, model=User, engine=engine)

user_crud = UserCrud()
```

## Available operations

### Create

Save a new model in the database

```python
newUser = UserCreate(name="Johan", password="mysupersecurepassword")
user_crud.create(model=newUser)
```

### All

Retrieve all models from database.

```python
users = user_crud.all()
```

### Find

Retrieve a model by its primary key

```python
myuser = user_crud.find(primaryKey=1)
```

### Find by

Retrieve one or many models by a matching value in a column

```python
get_one = user_crud.findby(column="name", value="Johan")
get_many = user_crud.findby(column="name", value="Johan", get_many=True)
```

### Update

Update a model that already exist in the database.

```python
me = user_crud.find(1)
updateUser=UserUpdate(password="mynewevenmoresupresecurepassword")
user_crud.update(model=me, data=updateuser)
```

### Delete

Delete one model from database.

```python
me = user_crud.find(1)
user_crud.delete(model=me)
```

Delete many models from database.

```python
users = user_crud.all()
user_crud.deleteMany(models=users)
```
