from firebase_admin import firestore
import firebase_admin

class Firestore:
   def __init__(self):
      self.app = firebase_admin.initialize_app() if not firebase_admin._apps else firebase_admin.get_app()
      self.db = firestore.client()
   
   def upsert(self, 
              collection: str, 
              document: str, 
              data: str) -> bool:
      
      self.db.collection(collection).document(document).set(data)
      return True