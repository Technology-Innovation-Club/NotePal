
# Notepal

This tool provides an easy way for users to interact with and source through their notes.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT) [![LangChain Applications](https://img.shields.io/badge/LangChain%20Applications-0.0.238-black)](https://example.com/langchain-applications/) [![OpenAI Requests](https://img.shields.io/badge/OpenAI%20-0.27.8-yellow)](https://example.com/openai-requests/) [![Django](https://img.shields.io/badge/Django-4.1.7-purple)](https://www.djangoproject.com/) [![Tailwind CSS](https://img.shields.io/badge/Tailwind%20CSS-3.6.0-blue)](https://tailwindcss.com/)


## Installation steps

### Prerequisites
- Docker: [Install Docker](https://docs.docker.com/get-docker/)
- Docker Compose: [Install Docker Compose](https://docs.docker.com/compose/install/)

Pull the docker [pgvector](https://github.com/pgvector/pgvector#docker) image:
```bash
docker pull ankane/pgvector
```

### Local Setup

**Clone the Repository:**
   
Clone the Notepal project repository from the source:

   ```bash
   git clone https://github.com/Technology-Innovation-Club/NotePal.git
   cd NotePal/notepal
```

**Create a virtual environment:**

```bash
python3 -m venv env
```
Create a Postgres database in the pgvector docker container

**Adding the Postgres database details to your `env/bin/activate` file**:
```code
export TIC_DB_NAME=[your local db name]
export TIC_DB_USER=[your local db user]
export TIC_DB_PASSWORD=[your local db password]
export TIC_DB_HOST=localhost
export TIC_DB_PORT=5433
export DEPLOYMENT_TIER=dev
```

**Install of the requirements**
```bash
pip install -r requirements.txt
```

**Migrate all the tables**:

```bash
python manage.py migrate
```

**Run the application**:

```bash
python manage.py runserver
```

## Running tailwind
### Prerequisites
NPM: [Nodejs](https://nodejs.org/en)

### Local Setup
Go to settings an specify the path npm on your machine or run `which npm` in your console.

Specify the path in `settings.py`

```code
NPM_BIN_PATH = <path-to-npm>
```
Run
```bash
python manage.py tailwind start
```
