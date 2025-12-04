from sqlalchemy import event
from src.utils import get_checksum
from src.db.models import Complaint


def set_checksum(mapper, connection, target):
    target.checksum = get_checksum(target.message)


event.listen(Complaint, "before_insert", set_checksum)
event.listen(Complaint, "before_update", set_checksum)
