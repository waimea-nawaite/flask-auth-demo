#============================================================================
# Database schema and seed data configuration
#============================================================================


#----------------------------------------------------------------------------
# Table definitions
#----------------------------------------------------------------------------
# Define your tables with a name, a schema and optional seed/sample data,
# using this format, and then add the tables to the Table Registry below:
#
# class TableName:
#     NAME      = "name"
#     SCHEMA    = "CREATE TABLE name (...)"
#     SEED_DATA = "INSERT INTO name (...)" or None
#----------------------------------------------------------------------------

class UserTable:

    NAME = "users"

    SCHEMA = """
        CREATE TABLE users (
            id      INTEGER PRIMARY KEY AUTOINCREMENT,
            forename        TEXT NOT NULL,
            surname         TEXT NOT NULL,
            username        TEXT NOT NULL,
            password_hash   TEXT NOT NULL
        )
    """

    SEED_DATA = """
    """

# Add more table classes here...
class MessagesTable:

    NAME = "messages"

    SCHEMA = """
        CREATE TABLE messages (
            id              INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id         INTEGER NOT NULL,
            title           TEXT NOT NULL,
            body            TEXT NOT NULL,

            FOREIGN KEY(user_id) REFERENCES user(id)

        )
    """

    SEED_DATA = """
        INSERT INTO messages (user_id, title, body)
    """


#----------------------------------------------------------------------------
# Table registry
#----------------------------------------------------------------------------
# Register all of your tables by adding them to the TABLES list here:
#
# TABLES = [
#     Table1,
#     Table2,
#     etc.
# ]
#
# Note: The table order is important - Create the tables that have
#       foreign keys AFTER the tables they link to have been created
#----------------------------------------------------------------------------

TABLES = [
    UserTable,
    # Add more tables here...
]

