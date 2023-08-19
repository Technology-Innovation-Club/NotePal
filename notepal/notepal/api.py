from ninja import NinjaAPI
from note.api import note_router
from chat.api import chat_router
from users.api import notepal_router

api = NinjaAPI()

api.add_router("/", notepal_router)
api.add_router("/note", note_router)
api.add_router("/chat", chat_router)
