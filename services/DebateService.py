class DebateService:
    def __init__(self, postgresql_engine, redis_session_op):
        '''
        postgresql 永久儲存留言及粉絲數
        redis 快速索取查看目前的比數
        '''