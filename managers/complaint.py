from models import complaint, RoleType, State
from db.config import database


class ComplaintManager:
    @staticmethod
    async def get_complaints(user):

        query = complaint.select()

        if user["role"] == RoleType.complainer:
            query = query.where(complaint.c.complainer_id == user["id"])

        elif user["role"] == RoleType.approver:
            query = query.where(complaint.c.state == State.pending)

        return await database.fetch_all(query)

    @staticmethod
    async def create_complaint(complaint_data, user):
        complaint_data["complainer_id"] = user["id"]
        id_ = await database.execute(complaint.insert().values(complaint_data))
        return await database.fetch_one(complaint.select().where(complaint.c.id == id_))

    @staticmethod
    async def delete_complaint(complaint_id):
        await database.execute(complaint.delete().where(complaint.c.id == complaint_id))

    @staticmethod
    async def approve_complaint(complaint_id):
        await database.execute(
            complaint.update()
            .where(complaint.c.id == complaint_id)
            .values(status=State.approved)
        )

    @staticmethod
    async def reject_complaint(complaint_id):
        await database.execute(
            complaint.update()
            .where(complaint.c.id == complaint_id)
            .values(status=State.rejected)
        )
