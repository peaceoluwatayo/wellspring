"""Initial migration.

Revision ID: 68e8fe179369
Revises: 
Create Date: 2025-01-21 14:18:45.771516

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '68e8fe179369'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('student_behavior',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('teacher', sa.String(length=255), nullable=False),
    sa.Column('class_name', sa.String(length=255), nullable=False),
    sa.Column('section', sa.String(length=255), nullable=False),
    sa.Column('behavior', sa.String(length=255), nullable=False),
    sa.Column('students', sa.Text(), nullable=True),
    sa.Column('subject', sa.String(length=255), nullable=False),
    sa.Column('date', sa.Date(), nullable=False),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.Column('feedback', sa.Text(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('student_behaviour')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('student_behaviour',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('teacher', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('class', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('section', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('behavior', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('students', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('subject', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('date', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('timestamp', postgresql.TIMESTAMP(), autoincrement=False, nullable=False),
    sa.Column('feedback', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='student_behaviour_pkey')
    )
    op.drop_table('student_behavior')
    # ### end Alembic commands ###
