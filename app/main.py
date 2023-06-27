from fastapi import FastAPI 
from . import models
from .database import engine
from .routers import post, user, auth, vote
from .config import settings
from fastapi.middleware.cors import CORSMiddleware


print(settings.database_password)

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

client = TestClient(app)

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)

# while True:    
try:
    conn = psycopg2.connect(host='localhost', database='fastapi', user='postgres', 
                                password='Eo002621!', cursor_factory=RealDictCursor)
    cursor = conn.cursor()
    print("Database connection was succesful !")
except Exception as error:
    print("Database connection failed !")
    print("the Error was ", error)
    time.sleep(2)



my_posts = [{"title": "title of post1", "content": "content of post 1", "id": 1},
            {"title": "favorite foods", "content": "I like pizza", "id":2}]


def find_post(id):
    for p in my_posts:
        if p["id"] == id:
            return p
def find_index_post(id):
    for i, p in enumerate(my_posts):
        if p['id'] == id:      
            return i



@app.get("/")
def root():
  return {"message": "hello World !"}

 