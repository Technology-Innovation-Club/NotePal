# NotePal
NotePal is a web app that helps students take and organize their notes. It uses the OpenAI CHATGPT API to power a chatbot that can answer questions, generate text and quizzes.
### Prerequisites

Before you begin, make sure you have the following installed on your system:

- Docker: [Install Docker](https://docs.docker.com/get-docker/)
- Docker Compose: [Install Docker Compose](https://docs.docker.com/compose/install/)

### Getting Started

1. **Clone the Repository:**
   
   Clone the Notepal project repository from the source:

   ```bash
   git clone https://github.com/Technology-Innovation-Club/NotePal.git
   cd notepal
2. **Run docker**
    ```bash
    docker-compose up
    ```
  after the initial running of docker-compose, you can run 
   ```bash
    docker-compose up -d
   ```
You can access the Notepal application in your browser with
```bash
127.0.0.1:9000
```
To shutdown docker container
```bash
docker-compose down
```
