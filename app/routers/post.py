from fastapi import FastAPI,Response,HTTPException,status,Depends,APIRouter
# Response used to show an errror if we find something out of range
# HTTPException is same as response it will raise exception but we have not to write detail in it
# status will show the list of all errors and we will choose it from there
from .. import models,schemas,oauth2
from typing import List,Optional
from ..database import get_db
from sqlalchemy.orm import Session
from sqlalchemy import func

router=APIRouter(
    prefix="/posts"  ,# anywhere we see /posts we can remove it
    tags=['posts'] # used for grouping it on browser rather than postman
)


@router.get("/",response_model=List[schemas.PostOut]) 
# Here list bcoz we are trying to get all post and in schemas.post its not all
def test_posts(db: Session = Depends(get_db),current_user:int=Depends(oauth2.get_current_user)): #this is should be everytime for dependency
    #posts = db.query(models.Post).all()
    posts=db.query(models.Post,func.count(models.Vote.post_id).label("votes")).join(models.Vote,models.Vote.post_id==models.Post.id,isouter=True).group_by(models.Post.id).all()
    
    # posts = db.query(models.Post).filter(models.Post.owner_id==current_user.id).all()
    # the above hashtag will print the only post of which user we are logged in but fr social media
    # we want all the post so not using it
    return  posts
    #cursor.execute("SELECT * FROM posts")
    #posts=cursor.fetchall()
    #return {"data" : posts} # will give all data from database on postman
    #return {"message" : "Hello Kushwaha"}
    #return {"message" : my_posts} # to return data from memory upr saved wala


@router.post("/",status_code=status.HTTP_201_CREATED,response_model=schemas.Post)
# response model is for the data which only we want
 # we can also create our own status
def create_post(post: schemas.PostCreate,db: Session = Depends(get_db),current_user:int=Depends(oauth2.get_current_user)):
    #cursor.execute("INSERT INTO posts (title,content,published) values(%s,%s,%s) RETURNING *",
            #(post.title,post.content,post.published)) # %s is placeholders bcoz of it no weird data can be passed
    #new_post=cursor.fetchone()
    #conn.commit() # we commit it bcoz with these in database changes will be applied 
    # without commit op will be seen only on postman
    new_post=models.Post(owner_id=current_user.id,**post.dict())
    # ** will unpack the data and print all the data coloum in Post we dont need to write post. tiltle post
    #.content etc
    db.add(new_post) # this will add the new post to database
    db.commit() # this will show the newly added post on databse
    db.refresh(new_post) # this will print the data on database
    return new_post
    """
    post_dict=post.dict()
    post_dict['id']=randrange(0,10000000) # we are not using dbms so for id we are doing this bcoz unique id is mst
    # after this every post will have its new id automatically
    my_posts.append(post_dict)
    #print(post)
    #print(post.dict()) # it will show the op in dictionary
    #print(post.title)
    #return {"new posts" : " new post"} # it will show in the terminal
    #return {"new posts" : post} # it will show in the output and this is bydefault dict
    return {"new posts": post_dict}""" #we only retrieving post_dict and in fn Post mntnd h jo class me h wahi worked


# imp note / / double slash one for posts and one for latest if we write the latest wala logic after /posts/{id}
# it will show error bcoz fast api goes from top to bottom compiler it will fetch frst /posts/id and see id is in
# int bcoz we converted their and latest is str so it is necessary to find a correct orders
'''
@router.get("/posts/latest")
def get_latest_post():
    post=my_posts[len(my_posts)-1]
    return  post'''


# to get a particular post we search it by id
@router.get("/{id}",response_model=schemas.PostOut)
#def get_post(id):
def get_post(id : int ,response: Response,db: Session = Depends(get_db),current_user:int=Depends(oauth2.get_current_user)): # by default every id is str so necessary to be converted in int   
    #cursor.execute("SELECT * FROM posts where id=%s",(str(id))) 
    #post=cursor.fetchone()
    #post= find_post(id)
    #post=db.query(models.Post).filter(models.Post.id==id).first()
    post=db.query(models.Post,func.count(models.Vote.post_id).label("votes")).join(models.Vote,models.Vote.post_id==models.Post.id,isouter=True).group_by(models.Post.id).filter(models.Post.id==id).first()
    # filter is used to find one post with id first will print the the foirst id we searched for
    # db.query is used to for all posts here also from all post we have tone find one
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id :{id} not found")
        #httpexception we have to give 2 parameter status_code with status. and detail jo op me show hoga
        #response.status_code=404 # here we are writing the error number
        #response.status_code=status.HTTP_404_NOT_FOUND # with status it will show as the option of errors
        #return {"message" : f"post with id :{id} not found"} # f is necessary if curly braces ka ans int h to
    #return {"data" :post} # not necessary agr new if ya something hoga open in these exception me 
    # we provided the detail 
    return post


@router.delete("/{id}" , status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id : int,db: Session = Depends(get_db),current_user:int=Depends(oauth2.get_current_user)):
    #cursor.execute("DELETE FROM posts where id=%s RETURNING *",(str(id)))
    #deleted_post=cursor.fetchone()
    #conn.commit()
    print(current_user.email)
    post_query=db.query(models.Post).filter(models.Post.id==id)
    post =post_query.first()
    if post==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id :{id} does not exist")
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=f"Not authorized to perform requested action")
    post_query.delete(synchronize_session=False)
    db.commit()
    # deleting post
    # find the index in the array which has required id
    # my_posts.pop(index)
    #index = find_index_post(id)
    #my_posts.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT) # here we wrote response so terminal me error naa aaye  


# update 
@router.put("/{id}",response_model=schemas.Post)
def update_posts(id :int ,post: schemas.PostCreate,db: Session = Depends(get_db),current_user:int=Depends(oauth2.get_current_user)): # schemas.post bcoz we iported it from 
    # schemas.py
    #cursor.execute("UPDATE posts SET title=%s ,content=%s, published=%s WHERE id=%s RETURNING *",
                  # (post.title,post.content,post.published,str(id)))
    #updated_post=cursor.fetchone()
    #conn.commit()
    #index = find_index_post(id)
    post_query=db.query(models.Post).filter(models.Post.id==id)
    poste =post_query.first()
    if poste == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id :{id} not found")
    
    if poste.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=f"Not authorized to perform requested action")
    post_query.update(post.dict(),synchronize_session=False)
    db.commit()
    #post_dict=post.dict()
    #post_dict['id']= id
    #my_posts[index]= post_dict
    return post_query.first()