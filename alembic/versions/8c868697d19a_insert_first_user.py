"""Insert First User

Revision ID: 8c868697d19a
Revises: 24d52159f910
Create Date: 2025-08-05 01:38:36.578967-03:00

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision: str = '8c868697d19a'
down_revision: Union[str, Sequence[str], None] = '24d52159f910'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Insert initial admin user
    from datetime import datetime
    from zoneinfo import ZoneInfo
    import bcrypt
    
    # Hash the admin password
    admin_password = 'admin123'
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(admin_password.encode('utf-8'), salt).decode('utf-8')
    
    members_table = sa.table('members',
        sa.column('cpf', sa.String),
        sa.column('name', sa.String),
        sa.column('nickname', sa.String),
        sa.column('email', sa.String),
        sa.column('pix_key', sa.String),
        sa.column('phone', sa.String),
        sa.column('password', sa.String),
        sa.column('is_admin', sa.Boolean),
        sa.column('is_enabled', sa.Boolean),
        sa.column('created_at', sa.DateTime),
    )
    
    op.bulk_insert(members_table, [
        {
            'cpf': '59469390415',
            'name': 'Marcelo de Campos',
            'nickname': "That's Poker",
            'email': 'sr.marcelo.campos@gmail.com',
            'pix_key': 'sr.marcelo.campos@gmail.com',
            'phone': '61984017586',
            'password': hashed_password,
            'is_admin': True,
            'is_enabled': True,
            'created_at': datetime.now(ZoneInfo("America/Sao_Paulo")),
        }
    ])


def downgrade() -> None:
    """Downgrade schema."""
    # Truncate the entire members table
    op.execute("TRUNCATE TABLE members RESTART IDENTITY CASCADE")
