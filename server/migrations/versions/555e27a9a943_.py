"""empty message

Revision ID: 555e27a9a943
Revises: 
Create Date: 2023-06-15 15:08:01.743357

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '555e27a9a943'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('promotions',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('regions', sa.String(), nullable=True),
    sa.Column('weight', sa.String(), nullable=False),
    sa.Column('phone', sa.String(), nullable=True),
    sa.Column('email', sa.String(), nullable=False),
    sa.Column('instagram', sa.String(), nullable=True),
    sa.Column('payment', sa.String(), nullable=True),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('proposed_matches',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('storyline', sa.String(), nullable=True),
    sa.Column('type', sa.String(), nullable=False),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('promotion_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['promotion_id'], ['promotions.id'], name=op.f('fk_proposed_matches_promotion_id_promotions')),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('shows',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('venue', sa.String(), nullable=False),
    sa.Column('address', sa.String(), nullable=True),
    sa.Column('city', sa.String(), nullable=False),
    sa.Column('state', sa.String(), nullable=False),
    sa.Column('date', sa.DateTime(), nullable=True),
    sa.Column('where_to_view', sa.String(), nullable=True),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('promotion_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['promotion_id'], ['promotions.id'], name=op.f('fk_shows_promotion_id_promotions')),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user_promotions',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('promotion_id', sa.Integer(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['promotion_id'], ['promotions.id'], name=op.f('fk_user_promotions_promotion_id_promotions')),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], name=op.f('fk_user_promotions_user_id_users')),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('matches',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('type', sa.String(), nullable=True),
    sa.Column('storyline', sa.String(), nullable=True),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('show_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['show_id'], ['shows.id'], name=op.f('fk_matches_show_id_shows')),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('proposed_match_wrestlers',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('proposed_match_id', sa.Integer(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['proposed_match_id'], ['proposed_matches.id'], name=op.f('fk_proposed_match_wrestlers_proposed_match_id_proposed_matches')),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], name=op.f('fk_proposed_match_wrestlers_user_id_users')),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user_shows',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('show_id', sa.Integer(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['show_id'], ['shows.id'], name=op.f('fk_user_shows_show_id_shows')),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], name=op.f('fk_user_shows_user_id_users')),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('match_wrestlers',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('match_id', sa.Integer(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['match_id'], ['matches.id'], name=op.f('fk_match_wrestlers_match_id_matches')),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], name=op.f('fk_match_wrestlers_user_id_users')),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('match_wrestlers')
    op.drop_table('user_shows')
    op.drop_table('proposed_match_wrestlers')
    op.drop_table('matches')
    op.drop_table('user_promotions')
    op.drop_table('shows')
    op.drop_table('proposed_matches')
    op.drop_table('users')
    op.drop_table('promotions')
    # ### end Alembic commands ###
