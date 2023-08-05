from fastapi import Request
from fastapi import APIRouter
from fastapi import status
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router = APIRouter()

templates = Jinja2Templates(directory="./templates")

# Path Operations

## Home
@router.get(
    path="/",
    response_class=HTMLResponse,
    status_code=status.HTTP_200_OK,
    summary="Shows home",
    tags=["Home"]
)
def home(request: Request):
    """
        Home.

        This shows the home.

        Returns a HTMLResponse.

    """
    return templates.TemplateResponse(
        name="home.html",
        context={"request": request}
    )