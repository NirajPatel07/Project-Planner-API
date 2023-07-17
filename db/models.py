from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String(64), unique=True)
    display_name = Column(String(64))
    creation_time = Column(DateTime, default=datetime.utcnow)

    teams = relationship('Team', secondary='team_users')

class Team(Base):
    __tablename__ = 'teams'

    id = Column(Integer, primary_key=True)
    name = Column(String(64), unique=True)
    description = Column(String(128))
    creation_time = Column(DateTime, default=datetime.utcnow)
    admin_id = Column(Integer, ForeignKey('users.id'))

    admin = relationship('User', backref='admin_teams')
    members = relationship('User', secondary='team_users')

class TeamUser(Base):
    __tablename__ = 'team_users'

    team_id = Column(Integer, ForeignKey('teams.id'), primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), primary_key=True)

class ProjectBoard(Base):
    __tablename__ = 'project_boards'

    id = Column(Integer, primary_key=True)
    name = Column(String(64), unique=True)
    description = Column(String(128))
    team_id = Column(Integer, ForeignKey('teams.id'))
    creation_time = Column(DateTime, default=datetime.utcnow)
    closed = Column(Boolean, default=False)
    end_time = Column(DateTime)

    team = relationship('Team', backref='boards')
    tasks = relationship('Task', backref='board')

class Task(Base):
    __tablename__ = 'tasks'

    id = Column(Integer, primary_key=True)
    title = Column(String(64))
    description = Column(String(128))
    user_id = Column(Integer, ForeignKey('users.id'))
    board_id = Column(Integer, ForeignKey('project_boards.id'))
    creation_time = Column(DateTime, default=datetime.utcnow)
    status = Column(String(12))  # 'OPEN', 'IN_PROGRESS', 'COMPLETE'

    assigned_user = relationship('User', backref='assigned_tasks')

