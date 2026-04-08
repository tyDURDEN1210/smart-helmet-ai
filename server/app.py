from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Smart Helmet AI is running 🚀"}


# 👇 REQUIRED by OpenEnv
def main():
    return app


# 👇 REQUIRED entrypoint
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("server.app:app", host="0.0.0.0", port=7860)