from Config import email_service
from Config import register_service
from Config import vote_counts_service

def get_email_service():
    return email_service

def get_register_service():
    return register_service

def get_vote_counts_service():
    return vote_counts_service



# def get_auth_service():
#     return AuthService(user_db_op, redis_session_op)

# def get_debate_service():
#     return DebateService