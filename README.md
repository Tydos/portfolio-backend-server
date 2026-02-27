# Portfolio Backend Server

This backend is built using **FastAPI** and provides REST APIs to fetch portfolio data from local files and a PostgreSQL cloud database hosted on **Databricks**. **Pydantic** is used for schema validation of API requests.

## API Routes

- **GET `/api/data`** – Returns general portfolio data.  
- **GET `/api/projects`** – Returns a list of portfolio projects.  
- **GET `/api/skills`** – Returns a list of skills.  
- **GET `/api/photographs`** – Returns all photographs.  
- **POST `/uploadphotos`** – Uploads a new photo to the database.  
- **GET `/getphotographs`** – Fetches paginated photographs using `limit` and `offset`.  
- **GET `/`** – Returns a welcome message for the API gateway.  

## Future Work

- Add API routes for uploading images to **Cloudinary** (image storage).  
- Store image embeddings in a **PostgreSQL pgvector** database for semantic search.
- Batch upload images to cloud