from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


from scrapers.course import CourseParser

scraper = CourseParser()
scraper.scrape_deparment("csci")
