from abc import ABC, abstractmethod

class UserOperation(ABC):
    @abstractmethod
    async def save_user(self, user):
        pass

    @abstractmethod
    async def find_user(self, identifier):
        pass