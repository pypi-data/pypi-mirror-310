from fastapi import FastAPI, APIRouter, Request, Response

router = APIRouter()

@router.get("/check")
async def login():
    return {"name": "Tester"}

### Plugable API ########################################################################
from danbi import plugable
class Test(plugable.IPlugin):
    def plug(self, **kwargs) -> bool:
        app: FastAPI = kwargs["app"]
        app.include_router(router, prefix="/api_v1/test", tags=["TEST"])
 
        return True
    
    def unplug(self, **kwargs) -> bool:
        return True
