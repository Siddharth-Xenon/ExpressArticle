from fastapi import FastAPI
# Import your route modules here (assuming you have user_routes and blog_routes)
from routes import user_routes, blog_routes, auth_routes

app = FastAPI(title="Blog API",
              description="A simple blog API", version="1.0.0")

# Include your routers here
app.include_router(auth_routes.router, tags=["auth"])
app.include_router(user_routes.router, prefix="/users", tags=["users"])
app.include_router(blog_routes.router, prefix="/blogs", tags=["blogs"])


@app.get("/")
async def root():
    return {"message": "Hello, World from Blog API!"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)


'''
NOTES:
1.Convert time into readable format before returning.
2.unique username
3. current user cant update other users
4. update only your own blogs
'''
