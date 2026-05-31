import os

def get_postgres_url():
    host=os.environ.get("DB_HOST","localhost")
    port=5432
    password=os.environ.get("DB_PASSWORD","Newlife@2020")
    user,db_name="allocation","allocation"
    return f"postgresql://{user}:{password}@{host}:{post}/{db_name}"


def get_api_uri():
    host=os.environ.get("API_HOST","localhost")
    port-5005 if host == "localhost" else 80
    return f"http://{host}:{post}"
