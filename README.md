## BLOG RESTAPi with FastAPi

Backend for Blog App with various endpoints including user management, Blogs and User Dashboard powered by mongodb as the database

### SETUP

- Clone this repository  
- Create a Virtual environment and Activate it  (Optional)
```bash
python -m venv .venv  
. .venv/bin/activate  
```
- Install the necessary dependencies 
```bash
pip install -r requirements.txt  
``` 
- Create an .env file  
```bash 
MONGODB_URL=mongodb://localhost:27017
SECRET= <Your secret for JWT>
```
- Optionally rename the db name and collections name in src/database.py as per your wish (Optional)

**Make sure you have mongodb installed locally**  
  
- Run the server  
```bash
uvicorn src:main:app --reload
```
- If everything went fine, Success message will be logged and server will listen on port 8000  


### Usage

#### Endpoints

All routes are mounted over /api/v1  
Hit up /api/v1/docs to see the swagger documentaion of the project  

##### 1. Dashboard

- **Path:** `/dashboard`
- **Method:** `GET`
- **Authorization:** Requires a valid JWT token.

##### 2. Accounts

- **Path:** `/accounts/login`
- **Methods:** `POST` (Login)
- **Authorization:** None    
&nbsp;
- **Path:** `/accounts/register`
- **Method:** `POST`
- **Authorization:** None    
&nbsp;  
- **Path:** `/accounts/logout`
- **Method:** `GET`
- **Authorization:** Requires a valid JWT token.    
&nbsp;
- **Path:** `/accounts/update`
- **Method:** `PUT`
- **Authorization:** Requires a valid JWT token.    
&nbsp;
- **Path:** `/accounts/profile`
- **Method:** `GET`
- **Authorization:** Requires a valid JWT token.   

##### 3. Blogs

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
sudo docker compose up
```
If current user is in docker group, Following is enough  
```bash
docker compose up
```

 