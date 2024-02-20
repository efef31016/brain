class VoteCountsService:
     def __init__(self, redis_operation):
         self.redis_operation = redis_operation

     def user_counts(self):
         keys = self.redis_operation.redis_config.get_keys("person:*")
         true_count = 0
         false_count = 0
         for key in keys:
             which_value = self.redis_operation.redis_config.hget(key, "which")
             if which_value == "true":
                 true_count += 1
             elif which_value == "false":
                 false_count += 1
         return {"trueCount": true_count, "falseCount": false_count}

     def vote_for_opinion(self, opinion_id, user_id):
         # 每人一票
         if self.redis_operation.redis_config.sismember(f"voted:{opinion_id}", user_id):
             return {"error": "User has already voted for this opinion."}
        
         # 記錄並更新得票數
         self.redis_operation.redis_config.sadd(f"voted:{opinion_id}", user_id)
         self.redis_operation.redis_config.hincrby("opinion_votes", opinion_id, 1)
        
         return {"success": "Vote recorded."}