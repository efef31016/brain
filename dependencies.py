from Config import email_service
from Config import register_service
from Config import login_service
from Config import logout_service
from Config import vote_counts_service
from Config import myaccount_service

def get_email_service():
    return email_service

def get_register_service():
    return register_service

def get_login_service():
    return login_service

def get_logout_service():
    return logout_service

def get_vote_counts_service():
    return vote_counts_service

def get_myaccount_service():
    return myaccount_service