from app.database import SessionLocal
from app.models import Ticket
db = SessionLocal()
t = Ticket(alert_id=1, title='Test 3')
db.add(t)
db.commit()
db.refresh(t)
print(t.created_at)
