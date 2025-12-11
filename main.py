from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from database import Base, engine
from routers.studenten import router as studenten_router
from routers.gruppen import router as gruppen_router
from routers.veranstaltungen import router as veranstaltungen_router

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(studenten_router, prefix="/students", tags=["Students"])
app.include_router(gruppen_router, prefix="/groups", tags=["Groups"])
app.include_router(veranstaltungen_router, prefix="/events", tags=["Events"])

# Static frontend
app.mount("/", StaticFiles(directory="static", html=True), name="static")
