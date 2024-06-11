from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


from app.scrapers.course import CourseParser
from app.database.postgres_client import PostgresClient

scraper = CourseParser()
scraper.scrape_deparment("csci")

client = PostgresClient()
client.delete_from_watchlist("12345")
