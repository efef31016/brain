     create_trigger_funciton = """CREATE OR REPLACE FUNCTION update_updated_at_column()
     RETURNS TRIGGER AS $$
     BEGIN
          NEW.updated_at = NOW(); -- 設定updated_at為目前時間
          RETURN NEW; -- 傳回更新後的記錄
     END;
     $$ LANGUAGE plpgsql;"""

create_trigger_example = """CREATE TRIGGER update_users_updated_at
BEFORE UPDATE ON "user".users
FOR EACH ROW
EXECUTE FUNCTION update_updated_at_column();
"""