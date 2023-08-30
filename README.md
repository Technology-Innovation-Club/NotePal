# NotePal
NotePal is a web app that helps students take and organize their notes. It uses the OpenAI CHATGPT API to power a chatbot that can answer questions, generate text and quizzes.
### Prerequisites

Before you begin, make sure you have the following installed on your system:

- Docker: [Install Docker](https://docs.docker.com/get-docker/)
- Docker Compose: [Install Docker Compose](https://docs.docker.com/compose/install/)

Pull the docker image:
```bash
docker pull ankane/pgvector
```
for more information
- https://github.com/pgvector/pgvector#docker
## Local Setup
### Getting Started

**Clone the Repository:**
   
Clone the Notepal project repository from the source:

   ```bash
   git clone https://github.com/Technology-Innovation-Club/NotePal.git
   cd NotePal/notepal
```

**Create a virtual environment:**

```code
python3 -m venv env
```

Adding the folowing to your `env/bin/activate` file:
```bash
export TIC_DB_NAME=[your local db name]
export TIC_DB_USER=[your local db user]
export TIC_DB_PASSWORD=[your local db password]
export TIC_DB_HOST=localhost
export TIC_DB_PORT=5433
export DEPLOYMENT_TIER=dev
```

The Database name, user, and password should be the same as your local postgres database that you have created for the project.


Run a migration to create the tables:

```code
python manage.py migrate
```

Create an admin user:

```code
echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('admin', '', 'ticadmin101')" | python manage.py shell
```

Run the application:

```code
python manage.py runserver
```
