import firebase_admin
from firebase_admin import credentials, firestore, storage

class FirebaseDB:
    # Firebase Authentication
    def init(self) -> None:
        if not firebase_admin._apps:
            self.credential = credentials.Certificate("credentials.json")
            firebase_admin.initialize_app(self.credential, {"storageBucket": "revolutioning-recruitment.appspot.com"})

        # Initialize Firestore
        self.db = firestore.client()

    # Insert dict data into Firebase
    def add_dict_data(self, collection_name, document_id, data):
        ref = self.db.collection(collection_name).document(document_id)
        ref.set(data)

    # Remove dict data from Firebase
    def remove_dict_data(self, collection_name, document_id):
        ref = self.db.collection(collection_name).document(document_id)
        ref.delete()
        
    # Update dict data in Firebase
    def update_dict_data(self, collection_name, document_id, updated_data):
        ref = self.db.collection(collection_name).document(document_id)
        ref.update(updated_data)
        
    # Retrieve a specific data from Firebase
    def read_specific_dict_data(self, collection_name, document_id):
        ref = self.db.collection(collection_name).document(document_id)
        data = ref.get()
        
        if data.exists:
            return data.to_dict()
        
        else:
            return None

    # Retrieve all data from Firebase
    def read_all_dict_data(self, collection_name):
        ref = self.db.collection(collection_name)
        data = ref.get()
        
        collection = []
        
        for item in data:
            collection.append(item.to_dict())
            
        return collection

    # Sort the data in Firebase
    def sort_dict_data(self, collection_name, field_name):
        ref = self.db.collection(collection_name)
        data = ref.order_by(field_name).limit(6).get()
        
        for i in data:
            print(i.to_dict())
        
    # Insert PDF file into Firebase
    def add_pdf_file(self, filename):
        bucket = storage.bucket()
        
        blob = bucket.blob(filename.name)
        blob.upload_from_string(filename.read(), content_type=filename.type)
        
    # Retrieve PDF file from Firebase
    def get_pdf_file(self, remote_file, local_file):
        bucket = storage.bucket()
        
        blob = bucket.get_blob(remote_file)
        blob.download_to_filename(local_file)
        
    # Retrieve all PDF files from Firebase
    def get_all_pdf_files(self):
        bucket = storage.bucket()
        
        blobs = bucket.list_blobs()
        
        for blob in blobs:
            remote_path = blob.name
            
            ref = bucket.get_blob(remote_path)
            ref.download_to_filename(f"./downloaded_file/{remote_path[6:]}")
    
if __name__ == "__main__":
    # add_pdf_file("resume/ChaiWaiJinResume.pdf")
    # add_pdf_file("resume/Chan Yanhan - Resume.pdf")
    # add_pdf_file("resume/LeeYiMei_Resume.pdf")
    # get_pdf_file("resume/ChaiWaiJinResume.pdf", "./downloaded_file/ChaiWaiJinResume.pdf")
    
    # get_all_pdf_files()
    # sort_dict_data("users", "name")
    pass
    
    
    