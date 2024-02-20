import uuid
import hashlib
from fastapi import HTTPException

class AuthService:
     def __init__(self, user_db_op, session_db_op):
         self.user_db_op = user_db_op
         self.session_db_op = session_db_op

     def login(self, username, password):
         # Hash the password for comparison
         hashed_password = hashlib.sha256(password.encode()).hexdigest()
        
         # Find the user in the database
         user = self.user_db_op.find_user(username)
         if not user:
             raise HTTPException(status_code=404, detail="User not found")
        
         # Check if the hashed password matches the one stored in the database
         if user.password != hashed_password:
             raise HTTPException(status_code=401, detail="Incorrect password")
        
         # Generate a session token for the user
         session_token = self._generate_session_token(username)
        
         # Return the session token
         return {"token": session_token}

     def logout(self, session_token):
         # Delete the session token from Redis
         self.session_db_op.delete_session(session_token)
         return {"message": "Logged out successfully"}

     def _generate_session_token(self, username):
         # Create a unique session token
         session_token = hashlib.sha256(f"{username}{uuid.uuid4()}".encode()).hexdigest()
        
         # Store the session token in Redis with an expiration time (e.g., 3600 seconds)
         self.session_db_op.set_value_with_expiration(session_token, username, 3600)
        
         return session_token