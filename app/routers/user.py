from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from .. import  models, schemas, utils
from ..database import engine, SessionLocal, get_db
from sqlalchemy.orm import Session

router = APIRouter(
   prefix="/users",
    tags=['Users']
)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOUt)
def create_user(users: schemas.UserCreate, db: Session = Depends(get_db)):
    
    # hash the password - user.parssword
    hashed_password = utils.hash(users.password)
    users.password = hashed_password

    new_user= models.Users(**users.dict())
    db.add(new_user)
    db.commit() 
    db.refresh(new_user)

    return new_user 
 
@router.get('/{id}', response_model=schemas.UserOUt)
def get_user(id: int, db: Session = Depends(get_db)):

    user = db.query(models.Users).filter(models.Users.id == id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id: {id} does not exist")

    return user