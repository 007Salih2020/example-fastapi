from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List, Optional
from sqlalchemy import func
from .. import  models, schemas, oauth2
from ..database import get_db




router = APIRouter(
    prefix="/posts" ,     # annotation da ki - post lari kaldiriyoruz !
    tags=['Posts']
)


@router.get("/", response_model=List[schemas.PostOut])
def get_post( db: Session = Depends(get_db), current_user: int= Depends(oauth2.get_current_user)):
    # cursor.execute(""" SELECT  * from posts WHERE id = %s """, (str(id),))
    # post = find_post(id)
    # posts = db.query(models.Post).filter(
    #     models.Post.ownner_id == current_user.id).all()
    
    posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).all()


    return posts


@router.post("/{id}", status_code=status.HTTP_201_CREATED)
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int= Depends(oauth2.get_current_user) ):
    # cursor.execute(""" INSERT INTO post (title, content, published) VALUES /%s, %s, %s) RETURNING * """, 
    # (post.title, post.content, post.published)}  
    # conn.commit()
    print(current_user.id)
    print(current_user.email)
    new_post = models.Post(owner_id=current_user.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
  
    return  new_post


@router.get("/{id}", response_model=schemas.PostOut)
def get_post(id: int, db: Session = Depends(get_db), current_user: int= Depends(oauth2.get_current_user)):
    # cursor.execute(""" SELECT FROM posts WHERE id = %s  RETURNING * """, (str(id),))
    # post = cursor.fetchone()
    # conn.commit()
   # post= db.query(models.Post).filter(models.Post.id == id).first()

    posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()
    
    if not posts:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"post with id: {id} does not exist")

    return posts

 
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: int= Depends(oauth2.get_current_user)):

    # cursor.execute(""" DELETE FROM posts  WHERE id = %s RETURNING  """, 
    #                (post.title, post.content, post.published, str(id),))
    # deleted_post = cursor.fetchone ()
    # conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id == id)
    
    post = post_query.first()

    if post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"post with id: {id} does not exist")

    if post.owner_id != oauth2.current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                            detail="Not Authorized to perform requested action")
    
    post_query.delete(synchronize_session=False)
    # post_query.update( {"title": "this is my updated title",     "content": "this is the updated content"}, synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model=schemas.Post)
def update_post(id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int= Depends(oauth2.get_current_user)):
    
    post_query = db.query(models.Post).filter(models.Post.id == id)
    
    post = post_query.first()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"post with id: {id} does not exist")

    if post.owner_id != oauth2.current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                            detail="Not Authorized to perform requested action")
    post_query.update(updated_post.dict(), synchronize_session=False)
    # post_query.update( {"title": "this is my updated title",     "content": "this is the updated content"}, synchronize_session=False)
    db.commit()
    return post_query.first()
# Response(status_code=status.HTTP_204_NO_CONTENT)
 
 
