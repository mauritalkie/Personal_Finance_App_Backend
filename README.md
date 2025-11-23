Local Development Setup

Follow these steps to run the project locally on a fresh machine:

1. Install Dependencies

Install PostgreSQL

Install Python

2. Database Setup

Create a PostgreSQL database with any name.
The important part is to match the name in your connection string inside the .env file.

3. Clone the Repository
git clone https://github.com/mauritalkie/Personal_Finance_App_Backend.git
cd Personal_Finance_App_Backend

4. Create and Activate a Virtual Environment
python -m venv venv
venv\Scripts\activate     # Windows

5. Install Python Requirements
pip install -r requirements.txt

Possible installation issues

Some packages may fail to build wheels.

You can fix this in two ways:

Install Rust, which allows those packages to compile from source.

Remove pinned versions in requirements.txt, allowing pip to install the latest wheels that don’t require compilation.

6. Environment Variables

Create a .env file based on .env.example and fill your credentials.

To generate a SECRET_KEY, you can run:

openssl rand -hex 32


If this command doesn’t work in Windows CMD, try using Git Bash.

7. Apply Database Migrations
alembic upgrade head

8. Run the Development Server

Navigate to the app directory:

cd app
fastapi dev main.py


The server will start at:

http://127.0.0.1:8000


For interactive API documentation (Swagger UI):

http://127.0.0.1:8000/docs