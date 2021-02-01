from dotenv import load_dotenv
from src.app import create_app
import os

load_dotenv()

env_name = os.getenv('FLASK_ENV')
app = create_app(env_name)

if __name__ == '__main__':
    port = os.getenv('PORT')
    host = os.getenv('HOST')
    app.run(host=host, port=port)
