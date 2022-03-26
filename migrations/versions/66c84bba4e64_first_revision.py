"""first revision

Revision ID: 66c84bba4e64
Revises: 
Create Date: 2022-03-26 13:23:10.525373

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "66c84bba4e64"
down_revision = None
branch_labels = None
depends_on = None


old_options = ("approved", "pending")
new_options = sorted(old_options + ("rejected",))

old_type = sa.Enum(*old_options, name="state")
new_type = sa.Enum(*new_options, name="state")
tmp_type = sa.Enum(*new_options, name="_state")

tcr = sa.sql.table("complaints", sa.Column("status", new_type, nullable=False))


def upgrade():
    # Create a tempoary "_status" type, convert and drop the "old" type
    tmp_type.create(op.get_bind(), checkfirst=False)
    op.execute(
        "ALTER TABLE complaints ALTER COLUMN status TYPE _state"
        " USING status::text::_state"
    )
    old_type.drop(op.get_bind(), checkfirst=False)
    # Create and convert to the "new" status type
    new_type.create(op.get_bind(), checkfirst=False)
    op.execute(
        "ALTER TABLE complaints ALTER COLUMN status TYPE state"
        " USING status::text::state"
    )
    tmp_type.drop(op.get_bind(), checkfirst=False)


def downgrade():
    # Convert 'output_limit_exceeded' status into 'timed_out'
    op.execute(
        tcr.update()
        .where(tcr.c.status == "output_limit_exceeded")
        .values(status="timed_out")
    )
    # Create a tempoary "_status" type, convert and drop the "new" type
    tmp_type.create(op.get_bind(), checkfirst=False)
    op.execute(
        "ALTER TABLE complaints ALTER COLUMN status TYPE _state"
        " USING status::text::_state"
    )
    new_type.drop(op.get_bind(), checkfirst=False)
    # Create and convert to the "old" status type
    old_type.create(op.get_bind(), checkfirst=False)
    op.execute(
        "ALTER TABLE complaints ALTER COLUMN status TYPE state"
        " USING status::text::state"
    )
    tmp_type.drop(op.get_bind(), checkfirst=False)
