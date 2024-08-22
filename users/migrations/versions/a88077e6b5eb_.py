"""empty message

Revision ID: a88077e6b5eb
Revises: 7998bfa0ba00
Create Date: 2024-08-22 16:28:19.034799

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a88077e6b5eb'
down_revision: Union[str, None] = '7998bfa0ba00'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('refresh_session',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('refresh_token', sa.UUID(), nullable=True),
    sa.Column('expires_in', sa.Integer(), nullable=True),
    sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.Column('user_id', sa.UUID(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_refresh_session_refresh_token'), 'refresh_session', ['refresh_token'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_refresh_session_refresh_token'), table_name='refresh_session')
    op.drop_table('refresh_session')
    # ### end Alembic commands ###
