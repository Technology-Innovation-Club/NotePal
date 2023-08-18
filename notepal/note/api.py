from ninja import Router, File, Schema, Form
from ninja.files import UploadedFile
from .load_file import store_file, store_file_embedding
from .metadata import get_file_name, get_metadata
from note.models import NoteFileembedding
import traceback

note_router = Router()

@note_router.post("/upload")
def upload(request, file: UploadedFile = File(...)):
    try:
        file_name = get_file_name(file.name)
        metadata = get_metadata(file)
        note_file = store_file(file.read(), file_name, metadata)

        try:
            # store note chunks and embeddings
            store_file_embedding(note_file)
        except Exception as e:
            NoteFileembedding.objects.filter(id=note_file.id).delete()
            return e
        
        return note_file.id
    except Exception:
        print(traceback.format_exc())
        return Exception