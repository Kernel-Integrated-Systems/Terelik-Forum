from fastapi import APIRouter, Request, Form
from starlette.responses import RedirectResponse, HTMLResponse
from starlette.templating import Jinja2Templates

from services.messages_services import get_message_by_id, create_message, get_user_contacts
from services.user_services import authenticate

messages_router = APIRouter(prefix='/messages', tags=['Messages'])


templates = Jinja2Templates(directory="templates")


@messages_router.get("/messages/{contact_id}", response_class=HTMLResponse)
def get_chat_history(contact_id: int, request: Request):
    user_info = authenticate(request)
    messages = get_message_by_id(user_info["user_id"], contact_id)
    users = get_user_contacts(user_info["user_id"])
    return templates.TemplateResponse("chat.html", {
        "request": request,
        "messages": messages,
        "users": users,
        "current_user_id": user_info["user_id"],
        "contact_id": contact_id
    })
@messages_router.post("/messages/send")
def send_message(request: Request, receiver_id: int = Form(...), content: str = Form(...)):
    user_info = authenticate(request)
    create_message(sender_id=user_info["user_id"], receiver_id=receiver_id, content=content)
    return RedirectResponse(url=f"/messages/{receiver_id}", status_code=302)
