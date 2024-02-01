## EXPRESS Article RESTAPi with FastAPi

Express Article is a Backend for Blog app with various endpoints including user management, Blog and User Dashboard powered by Mongodb as the database
### Deployement 
The API is deployed on Render and can be accessed at [https://expressarticle.onrender.com](https://expressarticle.onrender.com).
### SETUP
- **Set Up a Virtual Environment**
   - For Windows:
     ```
     python -m venv my_venv
     .\my_venv\Scripts\activate
     ```
   - For Unix or MacOS:
     ```
     python3 -m venv venv
     source venv/bin/activate
     ```
- **Install the necessary dependencies**
```bash
pip install -r requirements.txt  
``` 
- Create an .env file  
```bash 
MONGO_USER=sidsolanki920
MONGO_PASS=8493
```
  
- Run the server  
```bash
cd ./app
uvicorn src:main:app --reload
```
- If everything went fine, Success message will be logged and server will listen on port 8000  


### Usage

#### Endpoints
##### 1. Authentication
- **Path:** `/login`
- **Methods:** `POST` (Login)
- **Authorization:** None    
- **Description:** User login     
&nbsp;
- **Path:** `/register`
- **Method:** `POST`
- **Authorization:** None
- **Description:** Register a new user  

##### 2. User

- **Path:** `/user/update`
- **Method:** `PUT`
- **Authorization:** Requires a valid JWT token.   
- **Description:**
&nbsp;
- **Path:** `/user/profile`
- **Method:** `GET`
- **Authorization:** Requires a valid JWT token.   

##### 3. Blogs
- **Path:** `blog/dashboard`
- **Method:** `GET`
- **Authorization:** Requires a valid JWT token.  
&nbsp;  
- **Path:** `/blogs?page=..&limit=..`            Page and limit are intergers for pagination
- **Methods:** `GET` 
- **Authorization:** None    
&nbsp;  
- **Path:** `/blogs/retrieve/{blog_id}`           blog_id corresponds to unique id of the blog 
- **Method:** `GET`
- **Authorization:** None    
&nbsp;  
- **Path:** `/blogs/create`
- **Method:** `POST`
- **Authorization:** Requires a valid JWT token.  
&nbsp;  
- **Path:** `/blogs/update/{blog_id}`            blog_id corresponds to unique id of the blog    
- **Method:** `PUT`
- **Authorization:** Requires a valid JWT token and should be the author  
&nbsp;  
- **Path:** `/blogs/remove/{blog_id}`            blog_id corresponds to unique id of the blog    
- **Method:** `DELETE`
- **Authorization:** Requires a valid JWT token and should be the author

**Authorization and Access Permissions are done with FastApi Dependencies**

### Docker

To run it as a container, Simply Run   
```bash
docker-compose up
```
If current user is in docker group, Following is enough  
```bash
docker-compose up
```

 
