"""update

Revision ID: 2c50efc8be34
Revises: 2a2152286d9c
Create Date: 2025-03-16 16:27:35.311984

"""
from typing import Sequence, Union

from alembic import op
import fastapi_users_db_sqlalchemy
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2c50efc8be34'
down_revision: Union[str, None] = '2a2152286d9c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('todos', sa.Column('user_id', fastapi_users_db_sqlalchemy.generics.GUID(), nullable=False))
    op.create_foreign_key(None, 'todos', 'users', ['user_id'], ['id'], ondelete='CASCADE')
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'todos', type_='foreignkey')
    op.drop_column('todos', 'user_id')
    # ### end Alembic commands ###
