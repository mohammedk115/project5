from sqlalchemy import (
    create_engine,
    MetaData,
    Table,
    Column,
    Integer,
    String,
    Float,
    DateTime,
    ForeignKey,
    Text
)

from datetime import datetime


# SQLite database




#postgress
DATABASE_URL = "sqlite:///skills.db"

engine = create_engine(
    DATABASE_URL,
    echo=False
)

metadata = MetaData()


# Users table
users = Table(
    "users",
    metadata,

    Column(
        "id",
        Integer,
        primary_key=True
    ),

    Column(
        "name",
        String(100),
        nullable=False
    )
)


# Skills table
skills = Table(
    "skills",
    metadata,

    Column(
        "id",
        Integer,
        primary_key=True
    ),

    Column(
        "name",
        String(100),
        unique=True,
        nullable=False
    )
)


# Courses table
courses_table = Table(
    "courses",
    metadata,

    Column(
        "id",
        Integer,
        primary_key=True
    ),

    Column(
        "title",
        String(200),
        nullable=False
    ),

    Column(
        "description",
        Text,
        nullable=False
    )
)


# Many-to-many relationship
user_skills = Table(
    "user_skills",
    metadata,

    Column(
        "user_id",
        Integer,
        ForeignKey("users.id"),
        primary_key=True
    ),

    Column(
        "skill_id",
        Integer,
        ForeignKey("skills.id"),
        primary_key=True
    )
)


# Embeddings table
embeddings = Table(
    "embeddings",
    metadata,

    Column(
        "id",
        Integer,
        primary_key=True
    ),

    Column(
        "entity_type",
        String(50),
        nullable=False
    ),

    Column(
        "entity_id",
        Integer,
        nullable=False
    ),

    Column(
        "embedding",
        Text,
        nullable=False
    )
)


# Recommendation logs
recommendation_logs = Table(
    "recommendation_logs",
    metadata,

    Column(
        "id",
        Integer,
        primary_key=True
    ),

    Column(
        "user_id",
        Integer,
        ForeignKey("users.id")
    ),

    Column(
        "course_id",
        Integer,
        ForeignKey("courses.id")
    ),

    Column(
        "similarity_score",
        Float
    ),

    Column(
        "created_at",
        DateTime,
        default=datetime.utcnow
    )
)


# Create all tables
metadata.create_all(engine)


print("Database tables created successfully.")