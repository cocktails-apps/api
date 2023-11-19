import uvicorn

if __name__ == "__main__":
    uvicorn.run("coctails_api.app:app", port=8000, reload=True)
