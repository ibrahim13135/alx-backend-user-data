### Object Relational Tutorial

The SQLAlchemy Object Relational Mapper (ORM) allows for the association of user-defined Python classes with database tables and instances of those classes (objects) with rows in the corresponding tables. It includes systems for synchronizing changes between objects and their corresponding rows (unit of work) and for expressing database queries in terms of user-defined classes and their relationships.

### Version Check

First, ensure that we are using at least version 1.3 of SQLAlchemy.

```python
import sqlalchemy
print(sqlalchemy.__version__)
```

**Expected Output:**
```
1.3.0
```

### Connecting

For this tutorial, we use an in-memory SQLite database. We connect using `create_engine()`.

```python
from sqlalchemy import create_engine
engine = create_engine('sqlite:///:memory:', echo=True)
```

**Explanation:**
- `create_engine('sqlite:///:memory:')` creates an SQLite in-memory database.
- `echo=True` enables SQLAlchemy logging for debugging purposes.

### Declare a Mapping

We start by describing the database tables and defining classes mapped to those tables. We use the Declarative system to achieve this.

```python
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
```

**Explanation:**
- `declarative_base()` creates a base class for our classes mapped to database tables.

Next, we define a `User` class mapped to a `users` table.

```python
from sqlalchemy import Column, Integer, String

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    fullname = Column(String)
    nickname = Column(String)

    def __repr__(self):
        return f"<User(name='{self.name}', fullname='{self.fullname}', nickname='{self.nickname}')>"
```

**Explanation:**
- `__tablename__` specifies the table name.
- `Column` objects define the table's columns.
- `__repr__()` provides a string representation of the `User` objects for debugging.

### Creating the Table

To create the table in the database, we use the `Base.metadata.create_all()` method.

```python
Base.metadata.create_all(engine)
```

**Explanation:**
- This command creates the `users` table in the database defined by the `engine`.

### Creating a Session

We use a session to interact with the database. The session manages the persistence of objects.

```python
from sqlalchemy.orm import sessionmaker

Session = sessionmaker(bind=engine)
session = Session()
```

**Explanation:**
- `sessionmaker` creates a new session class.
- `Session()` instantiates a session object.

### Adding and Committing Objects

We can add new `User` objects to the session and commit them to the database.

```python
new_user = User(name='John', fullname='John Doe', nickname='johnny')
session.add(new_user)
session.commit()
```

**Explanation:**
- `session.add(new_user)` adds a new `User` object to the session.
- `session.commit()` commits the transaction, persisting the new `User` object to the database.

**Expected Output:**
```sql
INSERT INTO users (name, fullname, nickname) VALUES (?, ?, ?)
('John', 'John Doe', 'johnny')
```

### Querying

We can query the database for objects.

```python
for user in session.query(User).filter_by(name='John'):
    print(user)
```

**Expected Output:**
```
<User(name='John', fullname='John Doe', nickname='johnny')>
```

### Updating Objects

To update an object, modify its attributes and commit the session.

```python
user_to_update = session.query(User).filter_by(name='John').first()
user_to_update.nickname = 'john_doe'
session.commit()
```

**Explanation:**
- `filter_by(name='John').first()` fetches the first user with the name 'John'.
- `user_to_update.nickname = 'john_doe'` updates the nickname.
- `session.commit()` commits the changes.

**Expected Output:**
```sql
UPDATE users SET nickname=? WHERE users.id = ?
('john_doe', 1)
```

### Deleting Objects

To delete an object, remove it from the session and commit.

```python
user_to_delete = session.query(User).filter_by(name='John').first()
session.delete(user_to_delete)
session.commit()
```

**Explanation:**
- `session.delete(user_to_delete)` removes the user from the session.
- `session.commit()` commits the transaction, deleting the user from the database.

**Expected Output:**
```sql
DELETE FROM users WHERE users.id = ?
(1,)
```



### Create a Schema

With our `User` class constructed via the Declarative system, we have defined information about our table, known as table metadata. The object used by SQLAlchemy to represent this information for a specific table is called the `Table` object, and here Declarative has made one for us. We can see this object by inspecting the `__table__` attribute:

```python
User.__table__
```

**Expected Output:**
```
Table('users', MetaData(bind=None),
        Column('id', Integer(), table=<users>, primary_key=True, nullable=False),
        Column('name', String(), table=<users>),
        Column('fullname', String(), table=<users>),
        Column('nickname', String(), table=<users>), schema=None)
```

### Classical Mappings

The Declarative system is highly recommended but not required. Any plain Python class can be mapped to any `Table` using the `mapper()` function directly. When we declared our class, Declarative created a `Table` object according to our specifications and associated it with the class by constructing a `Mapper` object. This `Table` object is part of a larger collection known as `MetaData`, available using the `.metadata` attribute of our declarative base class.

We can use `MetaData` to issue `CREATE TABLE` statements to the database for all tables that don’t yet exist:

```python
Base.metadata.create_all(engine)
```

**Expected Output:**
```sql
SELECT ...
PRAGMA main.table_info("users")
()
PRAGMA temp.table_info("users")
()
CREATE TABLE users (
    id INTEGER NOT NULL, 
    name VARCHAR,
    fullname VARCHAR,
    nickname VARCHAR,
    PRIMARY KEY (id)
)
()
COMMIT
```

### Minimal Table Descriptions vs. Full Descriptions

For databases that require specific types or additional details, such as column lengths, we can modify our table definitions:

```python
from sqlalchemy import Sequence

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, Sequence('user_id_seq'), primary_key=True)
    name = Column(String(50))
    fullname = Column(String(50))
    nickname = Column(String(50))

    def __repr__(self):
        return "<User(name='%s', fullname='%s', nickname='%s')>" % (
                                self.name, self.fullname, self.nickname)
```

**Explanation:**
- `Sequence('user_id_seq')` ensures compatibility with databases like Firebird and Oracle that require sequences for primary key generation.

### Create an Instance of the Mapped Class

With mappings complete, let’s create and inspect a `User` object:

```python
ed_user = User(name='ed', fullname='Ed Jones', nickname='edsnickname')
print(ed_user.name)
print(ed_user.nickname)
print(str(ed_user.id))
```

**Expected Output:**
```
'ed'
'edsnickname'
'None'
```

**Explanation:**
- The `User` class automatically accepts keyword names that match the columns we’ve mapped.
- The `id` attribute produces a value of `None` when accessed, as it will be assigned by the database upon insertion.

### Creating a Session

We define a `Session` class which will serve as a factory for new `Session` objects:

```python
from sqlalchemy.orm import sessionmaker

Session = sessionmaker(bind=engine)
session = Session()
```

**Explanation:**
- `sessionmaker(bind=engine)` creates a new `Session` class bound to our database.
- `Session()` instantiates a session object.

### Adding and Committing Objects

Add new `User` objects to the session and commit them to the database:

```python
new_user = User(name='John', fullname='John Doe', nickname='johnny')
session.add(new_user)
session.commit()
```

**Expected Output:**
```sql
INSERT INTO users (name, fullname, nickname) VALUES (?, ?, ?)
('John', 'John Doe', 'johnny')
```

### Querying

Query the database for objects:

```python
for user in session.query(User).filter_by(name='John'):
    print(user)
```

**Expected Output:**
```
<User(name='John', fullname='John Doe', nickname='johnny')>
```

### Updating Objects

Modify object attributes and commit the session:

```python
user_to_update = session.query(User).filter_by(name='John').first()
user_to_update.nickname = 'john_doe'
session.commit()
```

**Expected Output:**
```sql
UPDATE users SET nickname=? WHERE users.id = ?
('john_doe', 1)
```

### Deleting Objects

Remove objects from the session and commit:

```python
user_to_delete = session.query(User).filter_by(name='John').first()
session.delete(user_to_delete)
session.commit()
```

**Expected Output:**
```sql
DELETE FROM users WHERE users.id = ?
(1,)
```

### Conclusion

This tutorial provides an overview of the SQLAlchemy ORM, demonstrating how to map classes to database tables, create and manipulate database records, and query the database using Python classes. By following these steps, you can effectively interact with a database using SQLAlchemy's high-level ORM.




### Adding and Updating Objects

To persist our `User` object, we use `Session.add()` to add it to our `Session`:

```python
ed_user = User(name='ed', fullname='Ed Jones', nickname='edsnickname')
session.add(ed_user)
```

At this point, the instance is pending; no SQL has yet been issued, and the object is not yet represented by a row in the database. The `Session` will issue the SQL to persist Ed Jones as soon as needed, using a process known as a flush. If we query the database for Ed Jones, all pending information will first be flushed, and the query is issued immediately thereafter.

For example, below we create a new `Query` object which loads instances of `User`. We “filter by” the `name` attribute of `ed`, and indicate that we’d like only the first result in the full list of rows. A `User` instance is returned which is equivalent to that which we’ve added:

```python
our_user = session.query(User).filter_by(name='ed').first()
```

**Expected Output:**
```sql
BEGIN (implicit)
INSERT INTO users (name, fullname, nickname) VALUES (?, ?, ?)
('ed', 'Ed Jones', 'edsnickname')
SELECT users.id AS users_id,
        users.name AS users_name,
        users.fullname AS users_fullname,
        users.nickname AS users_nickname
FROM users
WHERE users.name = ?
LIMIT ? OFFSET ?
('ed', 1, 0)
```

```python
our_user
# <User(name='ed', fullname='Ed Jones', nickname='edsnickname')>
```

In fact, the `Session` has identified that the row returned is the same row as one already represented within its internal map of objects, so we actually got back the identical instance as that which we just added:

```python
ed_user is our_user
# True
```

The ORM concept at work here is known as an identity map and ensures that all operations upon a particular row within a `Session` operate upon the same set of data. Once an object with a particular primary key is present in the `Session`, all SQL queries on that `Session` will always return the same Python object for that particular primary key; it also will raise an error if an attempt is made to place a second, already-persisted object with the same primary key within the session.

We can add more `User` objects at once using `add_all()`:

```python
session.add_all([
    User(name='wendy', fullname='Wendy Williams', nickname='windy'),
    User(name='mary', fullname='Mary Contrary', nickname='mary'),
    User(name='fred', fullname='Fred Flintstone', nickname='freddy')
])
```

Also, we’ve decided Ed’s nickname isn’t that great, so let's change it:

```python
ed_user.nickname = 'eddie'
```

The `Session` is paying attention. It knows, for example, that Ed Jones has been modified:

```python
session.dirty
# IdentitySet([<User(name='ed', fullname='Ed Jones', nickname='eddie')>])
```

and that three new `User` objects are pending:

```python
session.new
# IdentitySet([
#   <User(name='wendy', fullname='Wendy Williams', nickname='windy')>,
#   <User(name='mary', fullname='Mary Contrary', nickname='mary')>,
#   <User(name='fred', fullname='Fred Flintstone', nickname='freddy')>
# ])
```

We tell the `Session` that we’d like to issue all remaining changes to the database and commit the transaction, which has been in progress throughout. We do this via `Session.commit()`. The `Session` emits the `UPDATE` statement for the nickname change on “ed”, as well as `INSERT` statements for the three new `User` objects we’ve added:

```python
session.commit()
```

**Expected Output:**
```sql
UPDATE users SET nickname=? WHERE users.id = ?
('eddie', 1)
INSERT INTO users (name, fullname, nickname) VALUES (?, ?, ?)
('wendy', 'Wendy Williams', 'windy')
INSERT INTO users (name, fullname, nickname) VALUES (?, ?, ?)
('mary', 'Mary Contrary', 'mary')
INSERT INTO users (name, fullname, nickname) VALUES (?, ?, ?)
('fred', 'Fred Flintstone', 'freddy')
COMMIT
```

`Session.commit()` flushes the remaining changes to the database and commits the transaction. The connection resources referenced by the session are now returned to the connection pool. Subsequent operations with this session will occur in a new transaction, which will again re-acquire connection resources when first needed.

If we look at Ed’s `id` attribute, which earlier was `None`, it now has a value:

```python
ed_user.id
```

**Expected Output:**
```sql
BEGIN (implicit)
SELECT users.id AS users_id,
        users.name AS users_name,
        users.fullname AS users_fullname,
        users.nickname AS users_nickname
FROM users
WHERE users.id = ?
(1,)
1
```

After the `Session` inserts new rows in the database, all newly generated identifiers and database-generated defaults become available on the instance, either immediately or via load-on-first-access. In this case, the entire row was re-loaded on access because a new transaction was begun after we issued `Session.commit()`. SQLAlchemy by default refreshes data from a previous transaction the first time it’s accessed within a new transaction, so that the most recent state is available.

### Session Object States

As our `User` object moved from being outside the `Session`, to inside the `Session` without a primary key, to actually being inserted, it moved between three out of five available “object states” - transient, pending, and persistent. Being aware of these states and what they mean is always a good idea.

### Rolling Back

Since the `Session` works within a transaction, we can roll back changes made too. Let’s make two changes that we’ll revert; ed_user’s name gets set to Edwardo:

```python
ed_user.name = 'Edwardo'
```

and we’ll add another erroneous user, fake_user:

```python
fake_user = User(name='fakeuser', fullname='Invalid', nickname='12345')
session.add(fake_user)
```

Querying the session, we can see that they’re flushed into the current transaction:

```python
session.query(User).filter(User.name.in_(['Edwardo', 'fakeuser'])).all()
```

**Expected Output:**
```sql
UPDATE users SET name=? WHERE users.id = ?
('Edwardo', 1)
INSERT INTO users (name, fullname, nickname) VALUES (?, ?, ?)
('fakeuser', 'Invalid', '12345')
SELECT users.id AS users_id,
        users.name AS users_name,
        users.fullname AS users_fullname,
        users.nickname AS users_nickname
FROM users
WHERE users.name IN (?, ?)
('Edwardo', 'fakeuser')
```

```python
# [<User(name='Edwardo', fullname='Ed Jones', nickname='eddie')>, <User(name='fakeuser', fullname='Invalid', nickname='12345')>]
```

Rolling back, we can see that ed_user’s name is back to ed, and fake_user has been kicked out of the session:

```python
session.rollback()
```

**Expected Output:**
```sql
ROLLBACK
```

```python
ed_user.name
# BEGIN (implicit)
# SELECT users.id AS users_id,
#        users.name AS users_name,
#        users.fullname AS users_fullname,
#        users.nickname AS users_nickname
# FROM users
# WHERE users.id = ?
# (1,)
# 'ed'

fake_user in session
# False
```

Issuing a `SELECT` illustrates the changes made to the database:

```python
session.query(User).filter(User.name.in_(['ed', 'fakeuser'])).all()
```

**Expected Output:**
```sql
SELECT users.id AS users_id,
        users.name AS users_name,
        users.fullname AS users_fullname,
        users.nickname AS users_nickname
FROM users
WHERE users.name IN (?, ?)
('ed', 'fakeuser')
```

```python
# [<User(name='ed', fullname='Ed Jones', nickname='eddie')>]
```


### Deleting Objects

To delete an object from the database, use the `Session.delete()` method. This marks the object for deletion, and the deletion occurs upon committing the transaction.

Let's delete one of the users we've added:

```python
session.delete(ed_user)
```

At this point, the object is marked for deletion, but no SQL is issued yet. The SQL statement will be issued upon the next flush, which can occur explicitly via `Session.flush()` or implicitly via `Session.commit()`.

```python
session.commit()
```

**Expected Output:**
```sql
DELETE FROM users WHERE users.id = ?
(1,)
COMMIT
```

Now, if we query for Ed, he should no longer be in the database:

```python
session.query(User).filter_by(name='ed').first()
```

**Expected Output:**
```sql
SELECT users.id AS users_id,
        users.name AS users_name,
        users.fullname AS users_fullname,
        users.nickname AS users_nickname
FROM users
WHERE users.name = ?
LIMIT ? OFFSET ?
('ed', 1, 0)
```

```python
# None
```

### Using Transactions

Transactions are critical for maintaining the integrity of your database operations. With SQLAlchemy, transactions are implicitly managed by the `Session` object. 

A `Session` begins a new transaction upon the first database operation and continues until `Session.commit()` or `Session.rollback()` is called. 

Here is a summary of how transactions work with `Session`:

1. **Begin a Transaction**: Automatically begins when a new `Session` is used for a database operation.
2. **Flush Changes**: `Session.flush()` sends pending changes to the database but does not commit the transaction.
3. **Commit a Transaction**: `Session.commit()` sends all changes to the database and ends the transaction.
4. **Rollback a Transaction**: `Session.rollback()` reverts all changes in the current transaction and ends the transaction.

### Example of a Transaction Workflow

Here’s an example workflow demonstrating these concepts:

```python
from sqlalchemy import create_engine, Column, Integer, String, Sequence
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Set up the engine and base
engine = create_engine('sqlite:///:memory:')
Base = declarative_base()

# Define the User class
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, Sequence('user_id_seq'), primary_key=True)
    name = Column(String(50))
    fullname = Column(String(50))
    nickname = Column(String(50))

    def __repr__(self):
        return "<User(name='%s', fullname='%s', nickname='%s')>" % (
            self.name, self.fullname, self.nickname)

# Create the table
Base.metadata.create_all(engine)

# Set up the session
Session = sessionmaker(bind=engine)
session = Session()

# Adding new users
ed_user = User(name='ed', fullname='Ed Jones', nickname='edsnickname')
session.add(ed_user)
session.commit()  # Commits the transaction

# Querying the user
our_user = session.query(User).filter_by(name='ed').first()
print(our_user)  # <User(name='ed', fullname='Ed Jones', nickname='edsnickname')>

# Updating the user
our_user.nickname = 'eddie'
session.commit()  # Commits the transaction

# Adding multiple users
session.add_all([
    User(name='wendy', fullname='Wendy Williams', nickname='windy'),
    User(name='mary', fullname='Mary Contrary', nickname='mary'),
    User(name='fred', fullname='Fred Flintstone', nickname='freddy')
])
session.commit()  # Commits the transaction

# Rolling back a transaction
our_user.name = 'Edwardo'
fake_user = User(name='fakeuser', fullname='Invalid', nickname='12345')
session.add(fake_user)
session.rollback()  # Rolls back the transaction

# Check the rollback
print(session.query(User).filter_by(name='Edwardo').first())  # None
print(session.query(User).filter_by(name='fakeuser').first())  # None

# Deleting a user
session.delete(our_user)
session.commit()  # Commits the transaction

# Check the deletion
print(session.query(User).filter_by(name='ed').first())  # None
```

### Explanation:

1. **Adding new users**: Adds and commits a user to the database.
2. **Querying the user**: Queries the user just added to verify.
3. **Updating the user**: Updates the user's nickname and commits the change.
4. **Adding multiple users**: Adds multiple users and commits the transaction.
5. **Rolling back a transaction**: Attempts to update a user and add a new user, but then rolls back the transaction, effectively undoing these changes.
6. **Deleting a user**: Deletes a user and commits the change, verifying the user has been removed from the database.

By following these steps, you can effectively manage your database operations using SQLAlchemy's ORM with transactions, ensuring data integrity and consistency.


### Querying

A `Query` object is created using the `query()` method on `Session`. This function takes a variable number of arguments, which can be any combination of classes and class-instrumented descriptors. Below, we indicate a `Query` which loads `User` instances. When evaluated in an iterative context, the list of `User` objects present is returned:

```python
for instance in session.query(User).order_by(User.id):
    print(instance.name, instance.fullname)
```

**Expected Output:**
```sql
SELECT users.id AS users_id,
        users.name AS users_name,
        users.fullname AS users_fullname,
        users.nickname AS users_nickname
FROM users ORDER BY users.id
```

```plaintext
ed Ed Jones
wendy Wendy Williams
mary Mary Contrary
fred Fred Flintstone
```

The `Query` also accepts ORM-instrumented descriptors as arguments. Any time multiple class entities or column-based entities are expressed as arguments to the `query()` function, the return result is expressed as tuples:

```python
for name, fullname in session.query(User.name, User.fullname):
    print(name, fullname)
```

**Expected Output:**
```sql
SELECT users.name AS users_name,
        users.fullname AS users_fullname
FROM users
```

```plaintext
ed Ed Jones
wendy Wendy Williams
mary Mary Contrary
fred Fred Flintstone
```

The tuples returned by `Query` are named tuples, supplied by the `KeyedTuple` class, and can be treated much like an ordinary Python object. The names are the same as the attribute’s name for an attribute, and the class name for a class:

```python
for row in session.query(User, User.name).all():
    print(row.User, row.name)
```

**Expected Output:**
```sql
SELECT users.id AS users_id,
        users.name AS users_name,
        users.fullname AS users_fullname,
        users.nickname AS users_nickname
FROM users
```

```plaintext
<User(name='ed', fullname='Ed Jones', nickname='eddie')> ed
<User(name='wendy', fullname='Wendy Williams', nickname='windy')> wendy
<User(name='mary', fullname='Mary Contrary', nickname='mary')> mary
<User(name='fred', fullname='Fred Flintstone', nickname='freddy')> fred
```

You can control the names of individual column expressions using the `ColumnElement.label()` construct, which is available from any `ColumnElement`-derived object, as well as any class attribute which is mapped to one (such as `User.name`):

```python
for row in session.query(User.name.label('name_label')).all():
    print(row.name_label)
```

**Expected Output:**
```sql
SELECT users.name AS name_label
FROM users
```

```plaintext
ed
wendy
mary
fred
```

The name given to a full entity such as `User`, assuming that multiple entities are present in the call to `Session.query()`, can be controlled using `aliased()`:

```python
from sqlalchemy.orm import aliased
user_alias = aliased(User, name='user_alias')

for row in session.query(user_alias, user_alias.name).all():
    print(row.user_alias)
```

**Expected Output:**
```sql
SELECT user_alias.id AS user_alias_id,
        user_alias.name AS user_alias_name,
        user_alias.fullname AS user_alias_fullname,
        user_alias.nickname AS user_alias_nickname
FROM users AS user_alias
```

```plaintext
<User(name='ed', fullname='Ed Jones', nickname='eddie')>
<User(name='wendy', fullname='Wendy Williams', nickname='windy')>
<User(name='mary', fullname='Mary Contrary', nickname='mary')>
<User(name='fred', fullname='Fred Flintstone', nickname='freddy')>
```

Basic operations with `Query` include issuing `LIMIT` and `OFFSET`, most conveniently using Python array slices and typically in conjunction with `ORDER BY`:

```python
for u in session.query(User).order_by(User.id)[1:3]:
    print(u)
```

**Expected Output:**
```sql
SELECT users.id AS users_id,
        users.name AS users_name,
        users.fullname AS users_fullname,
        users.nickname AS users_nickname
FROM users ORDER BY users.id
LIMIT ? OFFSET ?
```

```plaintext
<User(name='wendy', fullname='Wendy Williams', nickname='windy')>
<User(name='mary', fullname='Mary Contrary', nickname='mary')>
```

Filtering results is accomplished either with `filter_by()`, which uses keyword arguments:

```python
for name, in session.query(User.name).filter_by(fullname='Ed Jones'):
    print(name)
```

**Expected Output:**
```sql
SELECT users.name AS users_name FROM users
WHERE users.fullname = ?
```

```plaintext
ed
```

…or `filter()`, which uses more flexible SQL expression language constructs. These allow you to use regular Python operators with the class-level attributes on your mapped class:

```python
for name, in session.query(User.name).filter(User.fullname == 'Ed Jones'):
    print(name)
```

**Expected Output:**
```sql
SELECT users.name AS users_name FROM users
WHERE users.fullname = ?
```

```plaintext
ed
```

The `Query` object is fully generative, meaning that most method calls return a new `Query` object upon which further criteria may be added. For example, to query for users named “ed” with a full name of “Ed Jones”, you can call `filter()` twice, which joins criteria using `AND`:

```python
for user in session.query(User).filter(User.name == 'ed').filter(User.fullname == 'Ed Jones'):
    print(user)
```

**Expected Output:**
```sql
SELECT users.id AS users_id,
        users.name AS users_name,
        users.fullname AS users_fullname,
        users.nickname AS users_nickname
FROM users
WHERE users.name = ? AND users.fullname = ?
```

```plaintext
<User(name='ed', fullname='Ed Jones', nickname='eddie')>
```

### Summary

With SQLAlchemy’s `Session` and `Query` objects, you can perform a variety of database operations including adding, updating, deleting, and querying data. Here's a summary of the operations:

- **Adding**: Use `Session.add()` to add single objects and `Session.add_all()` to add multiple objects.
- **Updating**: Simply modify the object's attributes and commit the session.
- **Deleting**: Use `Session.delete()` to mark an object for deletion and commit the session.
- **Querying**: Use `Session.query()` to create a `Query` object. Filter results with `filter_by()` and `filter()`, and use slicing to limit and offset results. Control column names with `label()` and use `aliased()` for multiple entities.


### Common Filter Operators

Here’s a rundown of some of the most common operators used in `filter()`:

#### ColumnOperators.__eq__()

```python
query.filter(User.name == 'ed')
```

#### ColumnOperators.__ne__()

```python
query.filter(User.name != 'ed')
```

#### ColumnOperators.like()

```python
query.filter(User.name.like('%ed%'))
```

**Note**: `ColumnOperators.like()` renders the `LIKE` operator, which is case insensitive on some backends, and case sensitive on others. For guaranteed case-insensitive comparisons, use `ColumnOperators.ilike()`.

#### ColumnOperators.ilike() (case-insensitive LIKE)

```python
query.filter(User.name.ilike('%ed%'))
```

**Note**: Most backends don’t support `ILIKE` directly. For those, the `ColumnOperators.ilike()` operator renders an expression combining `LIKE` with the `LOWER` SQL function applied to each operand.

#### ColumnOperators.in_()

```python
query.filter(User.name.in_(['ed', 'wendy', 'jack']))

# works with query objects too:
query.filter(User.name.in_(
    session.query(User.name).filter(User.name.like('%ed%'))
))

# use tuple_() for composite (multi-column) queries
from sqlalchemy import tuple_
query.filter(
    tuple_(User.name, User.nickname).\
    in_([('ed', 'edsnickname'), ('wendy', 'windy')])
)
```

#### ColumnOperators.notin_()

```python
query.filter(~User.name.in_(['ed', 'wendy', 'jack']))
```

#### ColumnOperators.is_()

```python
query.filter(User.name == None)

# alternatively, if pep8/linters are a concern
query.filter(User.name.is_(None))
```

#### ColumnOperators.isnot()

```python
query.filter(User.name != None)

# alternatively, if pep8/linters are a concern
query.filter(User.name.isnot(None))
```

#### AND

```python
# use and_()
from sqlalchemy import and_
query.filter(and_(User.name == 'ed', User.fullname == 'Ed Jones'))

# or send multiple expressions to .filter()
query.filter(User.name == 'ed', User.fullname == 'Ed Jones')

# or chain multiple filter()/filter_by() calls
query.filter(User.name == 'ed').filter(User.fullname == 'Ed Jones')
```

**Note**: Make sure you use `and_()` and not the Python `and` operator!

#### OR

```python
from sqlalchemy import or_
query.filter(or_(User.name == 'ed', User.name == 'wendy'))
```

**Note**: Make sure you use `or_()` and not the Python `or` operator!

#### ColumnOperators.match()

```python
query.filter(User.name.match('wendy'))
```

**Note**: `ColumnOperators.match()` uses a database-specific `MATCH` or `CONTAINS` function; its behavior will vary by backend and is not available on some backends such as SQLite.

### Returning Lists and Scalars

A number of methods on `Query` immediately issue SQL and return a value containing loaded database results. Here’s a brief tour:

#### Query.all() returns a list

```python
query = session.query(User).filter(User.name.like('%ed')).order_by(User.id)
query.all()
```

**Expected Output:**
```sql
SELECT users.id AS users_id,
        users.name AS users_name,
        users.fullname AS users_fullname,
        users.nickname AS users_nickname
FROM users
WHERE users.name LIKE ? ORDER BY users.id
```

```plaintext
('%ed',)
[<User(name='ed', fullname='Ed Jones', nickname='eddie')>,
      <User(name='fred', fullname='Fred Flintstone', nickname='freddy')>]
```

**Warning**: When the `Query` object returns lists of ORM-mapped objects such as the `User` object above, the entries are deduplicated based on primary key, as the results are interpreted from the SQL result set. That is, if SQL query returns a row with `id=7` twice, you would only get a single `User(id=7)` object back in the result list. This does not apply to the case when individual columns are queried.

**See also**: My Query does not return the same number of objects as `query.count()` tells me - why?

### Summary

With SQLAlchemy’s `Session` and `Query` objects, you can perform a variety of database operations including adding, updating, deleting, and querying data. Here's a summary of the operations:

- **Adding**: Use `Session.add()` to add single objects and `Session.add_all()` to add multiple objects.
- **Updating**: Simply modify the object's attributes and commit the session.
- **Deleting**: Use `Session.delete()` to mark an object for deletion and commit the session.
- **Querying**: Use `Session.query()` to create a `Query` object. Filter results with `filter_by()` and `filter()`, and use slicing to limit and offset results. Control column names with `label()` and use `aliased()` for multiple entities. Common filter operators include `==`, `!=`, `like`, `ilike`, `in_`, `notin_`, `is_`, `isnot`, `and_`, `or_`, and `match`.



### Querying with SQLAlchemy

#### Querying Basics

Creating a Query object:
```python
query = session.query(User)
```
#### Using Query.all()

`Query.all()` returns a list of all results:
```python
query = session.query(User).filter(User.name.like('%ed')).order_by(User.id)
results = query.all()
```

#### Using Query.first()

`Query.first()` applies a limit of one and returns the first result:
```python
first_result = query.first()
```

**Example:**
```python
query = session.query(User).filter(User.name.like('%ed')).order_by(User.id)
first_user = query.first()
```
SQL:
```sql
SELECT users.id AS users_id,
       users.name AS users_name,
       users.fullname AS users_fullname,
       users.nickname AS users_nickname
FROM users
WHERE users.name LIKE ?
ORDER BY users.id
LIMIT 1 OFFSET 0
```
Output:
```plaintext
<User(name='ed', fullname='Ed Jones', nickname='eddie')>
```

#### Using Query.one()

`Query.one()` fetches all rows and raises an error if not exactly one result is found:
```python
try:
    user = query.one()
except MultipleResultsFound:
    # handle multiple results found
except NoResultFound:
    # handle no results found
```

**Example with multiple rows found:**
```python
user = query.one()
```
Error:
```plaintext
MultipleResultsFound: Multiple rows were found for one()
```

**Example with no rows found:**
```python
user = session.query(User).filter(User.id == 99).one()
```
Error:
```plaintext
NoResultFound: No row was found for one()
```

#### Using Query.one_or_none()

`Query.one_or_none()` returns None if no results are found, but raises an error if multiple results are found:
```python
user = query.one_or_none()
```

#### Using Query.scalar()

`Query.scalar()` invokes `Query.one()` and returns the first column of the row:
```python
user_id = session.query(User.id).filter(User.name == 'ed').order_by(User.id).scalar()
```
SQL:
```sql
SELECT users.id AS users_id
FROM users
WHERE users.name = ?
ORDER BY users.id
```
Output:
```plaintext
1
```

### Using Textual SQL

#### Using text() construct

You can use literal strings with the `text()` construct:
```python
from sqlalchemy import text
query = session.query(User).filter(text("id < 224")).order_by(text("id"))
users = query.all()
```

**Example:**
```python
for user in session.query(User).filter(text("id<224")).order_by(text("id")).all():
    print(user.name)
```
SQL:
```sql
SELECT users.id AS users_id,
       users.name AS users_name,
       users.fullname AS users_fullname,
       users.nickname AS users_nickname
FROM users
WHERE id<224
ORDER BY id
```
Output:
```plaintext
ed
wendy
mary
fred
```

#### Using Bind Parameters

You can specify bind parameters in the string-based SQL:
```python
query = session.query(User).filter(text("id < :value and name = :name")).params(value=224, name='fred')
user = query.one()
```

**Example:**
```python
session.query(User).filter(text("id<:value and name=:name")).params(value=224, name='fred').order_by(User.id).one()
```
SQL:
```sql
SELECT users.id AS users_id,
       users.name AS users_name,
       users.fullname AS users_fullname,
       users.nickname AS users_nickname
FROM users
WHERE id<:value and name=:name
ORDER BY users.id
```
Output:
```plaintext
<User(name='fred', fullname='Fred Flintstone', nickname='freddy')>
```

#### Using text() for Complete Statements

Use `text()` for complete statements:
```python
stmt = text("SELECT * FROM users WHERE name=:name")
users = session.query(User).from_statement(stmt).params(name='ed').all()
```

**Example:**
```python
session.query(User).from_statement(
    text("SELECT * FROM users where name=:name")
).params(name='ed').all()
```
SQL:
```sql
SELECT * FROM users where name=:name
```
Output:
```plaintext
[<User(name='ed', fullname='Ed Jones', nickname='eddie')>]
```

#### Using Column Expressions with text()

Link textual SQL to column expressions positionally:
```python
stmt = text("SELECT name, id, fullname, nickname FROM users where name=:name")
stmt = stmt.columns(User.name, User.id, User.fullname, User.nickname)
users = session.query(User).from_statement(stmt).params(name='ed').all()
```

**Example:**
```python
stmt = text("SELECT name, id, fullname, nickname FROM users where name=:name")
stmt = stmt.columns(User.name, User.id, User.fullname, User.nickname)
session.query(User).from_statement(stmt).params(name='ed').all()
```
SQL:
```sql
SELECT name, id, fullname, nickname FROM users where name=:name
```
Output:
```plaintext
[<User(name='ed', fullname='Ed Jones', nickname='eddie')>]
```

#### Using Specific Columns with text()

Specify columns to return:
```python
stmt = text("SELECT name, id FROM users where name=:name")
stmt = stmt.columns(User.name, User.id)
results = session.query(User.id, User.name).from_statement(stmt).params(name='ed').all()
```

**Example:**
```python
stmt = text("SELECT name, id FROM users where name=:name")
stmt = stmt.columns(User.name, User.id)
session.query(User.id, User.name).from_statement(stmt).params(name='ed').all()
```
SQL:
```sql
SELECT name, id FROM users where name=:name
```
Output:
```plaintext
[(1, 'ed')]
```

### Counting

#### Using Query.count()

`Query.count()` counts the number of rows:
```python
count = session.query(User).filter(User.name.like('%ed')).count()
```

**Example:**
```python
session.query(User).filter(User.name.like('%ed')).count()
```
SQL:
```sql
SELECT count(*) AS count_1
FROM (
    SELECT users.id AS users_id,
           users.name AS users_name,
           users.fullname AS users_fullname,
           users.nickname AS users_nickname
    FROM users
    WHERE users.name LIKE ?
) AS anon_1
```
Output:
```plaintext
2
```

#### Using func.count()

For specific counts:
```python
from sqlalchemy import func
count = session.query(func.count(User.name), User.name).group_by(User.name).all()
```

**Example:**
```python
session.query(func.count(User.name), User.name).group_by(User.name).all()
```
SQL:
```sql
SELECT count(users.name) AS count_1, users.name AS users_name
FROM users
GROUP BY users.name
```
Output:
```plaintext
[(1, 'ed'), (1, 'fred'), (1, 'mary'), (1, 'wendy')]
```

For `SELECT count(*) FROM table`:
```python
count = session.query(func.count('*')).select_from(User).scalar()
```

**Example:**
```python
session.query(func.count('*')).select_from(User).scalar()
```
SQL:
```sql
SELECT count(*) AS count_1
FROM users
```
Output:
```plaintext
4
```

Or using the primary key:
```python
count = session.query(func.count(User.id)).scalar()
```

**Example:**
```python
session.query(func.count(User.id)).scalar()
```
SQL:
```sql
SELECT count(users.id) AS count_1
FROM users
```
Output:
```plaintext
4
```

### Summary

With SQLAlchemy’s `Session` and `Query` objects, you can perform a variety of database operations including adding, updating, deleting, and querying data. Here's a summary of the operations:

- **Adding**: Use `Session.add()` to add single objects and `Session.add_all()` to add multiple objects.
- **Updating**: Simply modify the object's attributes and commit the session.
- **Deleting**: Use `Session.delete()` to mark an object for deletion and commit the session.
- **Querying**: Use `Session.query()` to create a `Query` object. Filter results with `filter_by()` and `filter()`, and use slicing to limit and offset results. Control column names with `label()` and use `aliased()` for multiple entities. Common filter operators include `==`, `!=`, `like`, `ilike`, `in_`, `notin_`, `is_`, `isnot`, `and_`, `or_`, and `match`.



## Building a Relationship

### Creating and Mapping a Related Table

To introduce a second table related to `User`, such as storing multiple email addresses for each user, we can use the `Address` table. This is a basic one-to-many relationship from users to addresses. Here’s how you can define this table along with its mapped class using SQLAlchemy's declarative system:

```python
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

class Address(Base):
    __tablename__ = 'addresses'
    id = Column(Integer, primary_key=True)
    email_address = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'))

    user = relationship("User", back_populates="addresses")

    def __repr__(self):
        return "<Address(email_address='%s')>" % self.email_address

User.addresses = relationship(
    "Address", order_by=Address.id, back_populates="user")
```

### Explanation

1. **ForeignKey**: This directive is applied to a column to constrain its values to those present in the specified remote column, creating a relationship between the tables.
2. **relationship()**: This ORM directive links the `Address` class to the `User` class via the `user` attribute and vice versa with the `addresses` attribute on the `User` class.
3. **back_populates**: This parameter allows the two classes to refer to each other, making it a bidirectional relationship.

### Creating the Addresses Table

After defining the relationship, you need to create the `addresses` table in the database. This is done using the `create_all` method:

```python
Base.metadata.create_all(engine)
```

### Working with Related Objects

When a `User` object is created, an empty `addresses` collection is automatically available. You can add `Address` objects to this collection as follows:

```python
jack = User(name='jack', fullname='Jack Bean', nickname='gjffdd')
jack.addresses = [
    Address(email_address='jack@google.com'),
    Address(email_address='j25@yahoo.com')
]
```

Committing the `User` and `Address` objects to the database:

```python
session.add(jack)
session.commit()
```

### Querying with Relationships

To fetch a `User` and their associated `Address` objects, you can perform queries using joins.

#### Simple Join

To perform a simple implicit join:

```python
for u, a in session.query(User, Address).\
        filter(User.id == Address.user_id).\
        filter(Address.email_address == 'jack@google.com').\
        all():
    print(u)
    print(a)
```

#### Using `join()`

To explicitly use the `join()` method:

```python
session.query(User).join(Address).\
        filter(Address.email_address == 'jack@google.com').\
        all()
```

### Advanced Joins

For more complex joins or when multiple foreign keys are involved, specify the join conditions explicitly:

```python
query.join(Address, User.id == Address.user_id)    # explicit condition
query.join(User.addresses)                         # specify relationship from left to right
query.join(Address, User.addresses)                # explicit target
```

To perform an outer join:

```python
query.outerjoin(User.addresses)   # LEFT OUTER JOIN
```

### Controlling the SELECT Source

To control which entity is selected from in the list of joins, use `select_from()`:

```python
query = session.query(User, Address).select_from(Address).join(User)
```


### Using Aliases

When querying across multiple tables, you might need to reference the same table more than once. In SQL, this is typically handled using aliases. SQLAlchemy supports this using the `aliased()` construct. When joining to relationships using `aliased()`, the special attribute method `PropComparator.of_type()` can be used to alter the target of a relationship join to refer to a given `aliased()` object.

Here’s an example where we join to the `Address` entity twice to locate a user who has two distinct email addresses at the same time:

```python
from sqlalchemy.orm import aliased

adalias1 = aliased(Address)
adalias2 = aliased(Address)

for username, email1, email2 in session.query(User.name, adalias1.email_address, adalias2.email_address).\
    join(User.addresses.of_type(adalias1)).\
    join(User.addresses.of_type(adalias2)).\
    filter(adalias1.email_address == 'jack@google.com').\
    filter(adalias2.email_address == 'j25@yahoo.com'):
    print(username, email1, email2)
```

### Explanation

1. **aliased()**: Creates an alias for the `Address` table to reference it multiple times.
2. **PropComparator.of_type()**: Alters the target of the relationship join to refer to the aliased `Address` object.

### Output

```sql
SELECT users.name AS users_name,
        addresses_1.email_address AS addresses_1_email_address,
        addresses_2.email_address AS addresses_2_email_address
FROM users
JOIN addresses AS addresses_1 ON users.id = addresses_1.user_id
JOIN addresses AS addresses_2 ON users.id = addresses_2.user_id
WHERE addresses_1.email_address = 'jack@google.com'
    AND addresses_2.email_address = 'j25@yahoo.com';
```

```python
# Output in Python
jack jack@google.com j25@yahoo.com
```

### Using Subqueries

The `Query` object can generate statements suitable for subqueries. For example, to load `User` objects along with a count of how many `Address` records each user has, you can use a subquery. 

First, create a subquery that counts addresses grouped by user IDs:

```python
from sqlalchemy.sql import func

stmt = session.query(Address.user_id, func.count('*').label('address_count')).\
    group_by(Address.user_id).subquery()
```

Next, use this subquery in a main query to join it with the `User` table:

```python
for u, count in session.query(User, stmt.c.address_count).\
    outerjoin(stmt, User.id == stmt.c.user_id).order_by(User.id):
    print(u, count)
```

### Explanation

1. **func**: Generates SQL functions like `COUNT`.
2. **subquery()**: Converts the query into a subquery that can be used as a table in another query.
3. **outerjoin()**: Performs a LEFT OUTER JOIN, ensuring all users are included even if they have no addresses.

### Output

```sql
SELECT users.id AS users_id,
        users.name AS users_name,
        users.fullname AS users_fullname,
        users.nickname AS users_nickname,
        anon_1.address_count AS anon_1_address_count
FROM users
LEFT OUTER JOIN (SELECT addresses.user_id AS user_id, count(*) AS address_count
                 FROM addresses
                 GROUP BY addresses.user_id) AS anon_1
ON users.id = anon_1.user_id
ORDER BY users.id;
```

```python
# Output in Python
<User(name='ed', fullname='Ed Jones', nickname='eddie')> None
<User(name='wendy', fullname='Wendy Williams', nickname='windy')> None
<User(name='mary', fullname='Mary Contrary', nickname='mary')> None
<User(name='fred', fullname='Fred Flintstone', nickname='freddy')> None
<User(name='jack', fullname='Jack Bean', nickname='gjffdd')> 2
```

### Selecting Entities from Subqueries

To map a subquery to an entity, use `aliased()` to associate an alias of a mapped class with a subquery:

```python
stmt = session.query(Address).\
    filter(Address.email_address != 'j25@yahoo.com').\
    subquery()

adalias = aliased(Address, stmt)

for user, address in session.query(User, adalias).\
    join(adalias, User.addresses):
    print(user)
    print(address)
```

### Explanation

1. **aliased()**: Creates an alias for the `Address` subquery.
2. **join()**: Joins the aliased subquery with the `User` table.

### Output

```sql
SELECT users.id AS users_id,
        users.name AS users_name,
        users.fullname AS users_fullname,
        users.nickname AS users_nickname,
        anon_1.id AS anon_1_id,
        anon_1.email_address AS anon_1_email_address,
        anon_1.user_id AS anon_1_user_id
FROM users
JOIN (SELECT addresses.id AS id,
             addresses.email_address AS email_address,
             addresses.user_id AS user_id
      FROM addresses
      WHERE addresses.email_address != 'j25@yahoo.com') AS anon_1
ON users.id = anon_1.user_id;
```

```python
# Output in Python
<User(name='jack', fullname='Jack Bean', nickname='gjffdd')>
<Address(email_address='jack@google.com')>
```

### Using EXISTS

The `EXISTS` keyword in SQL checks if the given expression contains any rows. This can be useful for locating rows that do not have a corresponding row in a related table.

#### Explicit EXISTS

```python
from sqlalchemy.sql import exists

stmt = exists().where(Address.user_id == User.id)

for name, in session.query(User.name).filter(stmt):
    print(name)
```

### Explanation

1. **exists()**: Constructs an `EXISTS` clause.
2. **filter()**: Filters the query based on the `EXISTS` clause.

### Output

```sql
SELECT users.name AS users_name
FROM users
WHERE EXISTS (SELECT 1
              FROM addresses
              WHERE addresses.user_id = users.id);
```

```python
# Output in Python
jack
```

#### Using Comparator.any()

```python
for name, in session.query(User.name).filter(User.addresses.any()):
    print(name)
```

### Explanation

1. **any()**: Checks if there are any related rows in the `Address` table.

### Output

```sql
SELECT users.name AS users_name
FROM users
WHERE EXISTS (SELECT 1
              FROM addresses
              WHERE users.id = addresses.user_id);
```

```python
# Output in Python
jack
```

#### Using Comparator.any() with Criteria

```python
for name, in session.query(User.name).filter(User.addresses.any(Address.email_address.like('%google%'))):
    print(name)
```

### Explanation

1. **like()**: Adds a criterion to the `EXISTS` clause.

### Output

```sql
SELECT users.name AS users_name
FROM users
WHERE EXISTS (SELECT 1
              FROM addresses
              WHERE users.id = addresses.user_id
                AND addresses.email_address LIKE '%google%');
```

```python
# Output in Python
jack
```

#### Using Comparator.has()

For many-to-one relationships, `Comparator.has()` is the equivalent of `Comparator.any()`. The `~` operator negates the condition:

```python
session.query(Address).filter(~Address.user.has(User.name == 'jack')).all()
```

### Explanation

1. **has()**: Checks if there is a related row in the `User` table.
2. **~**: Negates the condition.

### Output

```sql
SELECT addresses.id AS addresses_id,
        addresses.email_address AS addresses_email_address,
        addresses.user_id AS addresses_user_id
FROM addresses
WHERE NOT EXISTS (SELECT 1
                  FROM users
                  WHERE users.id = addresses.user_id
                    AND users.name = 'jack');
```

```python
# Output in Python
[]
```

### Common Relationship Operators

SQLAlchemy provides several operators to handle relationships in queries. Here’s a detailed explanation with examples and outputs:

#### `Comparator.__eq__()` (many-to-one “equals” comparison)

```python
query.filter(Address.user == someuser)
```

### Explanation
- **`__eq__()`**: Checks if the `Address.user` is equal to `someuser`.

### Output

```sql
SELECT * FROM addresses WHERE addresses.user_id = :user_id;
```

#### `Comparator.__ne__()` (many-to-one “not equals” comparison)

```python
query.filter(Address.user != someuser)
```

### Explanation
- **`__ne__()`**: Checks if the `Address.user` is not equal to `someuser`.

### Output

```sql
SELECT * FROM addresses WHERE addresses.user_id != :user_id;
```

#### IS NULL (many-to-one comparison, also uses `Comparator.__eq__()`)

```python
query.filter(Address.user == None)
```

### Explanation
- **IS NULL**: Checks if the `Address.user` is `NULL`.

### Output

```sql
SELECT * FROM addresses WHERE addresses.user_id IS NULL;
```

#### `Comparator.contains()` (used for one-to-many collections)

```python
query.filter(User.addresses.contains(someaddress))
```

### Explanation
- **`contains()`**: Checks if the `User.addresses` collection contains `someaddress`.

### Output

```sql
SELECT * FROM users WHERE :someaddress_id IN (SELECT addresses.user_id FROM addresses WHERE addresses.user_id = users.id);
```

#### `Comparator.any()` (used for collections)

```python
query.filter(User.addresses.any(Address.email_address == 'bar'))
```

### Explanation
- **`any()`**: Checks if any `Address` in the `User.addresses` collection has `email_address` equal to 'bar'.

### Output

```sql
SELECT * FROM users WHERE EXISTS (SELECT 1 FROM addresses WHERE addresses.user_id = users.id AND addresses.email_address = 'bar');
```

#### `Comparator.any()` with keyword arguments

```python
query.filter(User.addresses.any(email_address='bar'))
```

### Explanation
- **`any()`**: Checks if any `Address` in the `User.addresses` collection has `email_address` equal to 'bar' using keyword arguments.

### Output

```sql
SELECT * FROM users WHERE EXISTS (SELECT 1 FROM addresses WHERE addresses.user_id = users.id AND addresses.email_address = 'bar');
```

#### `Comparator.has()` (used for scalar references)

```python
query.filter(Address.user.has(name='ed'))
```

### Explanation
- **`has()`**: Checks if the `User` related to the `Address` has the name 'ed'.

### Output

```sql
SELECT * FROM addresses WHERE EXISTS (SELECT 1 FROM users WHERE users.id = addresses.user_id AND users.name = 'ed');
```

#### `Query.with_parent()` (used for any relationship)

```python
session.query(Address).with_parent(someuser, 'addresses')
```

### Explanation
- **`with_parent()`**: Filters `Address` based on the relationship with `someuser` via the `addresses` attribute.

### Output

```sql
SELECT * FROM addresses WHERE addresses.user_id = :someuser_id;
```

### Eager Loading

Eager loading can significantly reduce the number of queries needed by loading related objects simultaneously.

#### `selectinload()`

This option loads collections using a secondary `SELECT` statement.

```python
from sqlalchemy.orm import selectinload

jack = session.query(User).options(selectinload(User.addresses)).filter_by(name='jack').one()
```

### Explanation
- **`selectinload()`**: Emits a secondary `SELECT` statement to load the `User.addresses` collection.

### Output

```sql
SELECT users.id AS users_id, users.name AS users_name, users.fullname AS users_fullname, users.nickname AS users_nickname
FROM users
WHERE users.name = 'jack';

SELECT addresses.user_id AS addresses_user_id, addresses.id AS addresses_id, addresses.email_address AS addresses_email_address
FROM addresses
WHERE addresses.user_id IN (:user_id);
```

```python
# Output in Python
<User(name='jack', fullname='Jack Bean', nickname='gjffdd')>
[<Address(email_address='jack@google.com')>, <Address(email_address='j25@yahoo.com')>]
```

#### `joinedload()`

This option loads related objects using a `JOIN`.

```python
from sqlalchemy.orm import joinedload

jack = session.query(User).options(joinedload(User.addresses)).filter_by(name='jack').one()
```

### Explanation
- **`joinedload()`**: Uses a `JOIN` to load the `User` and `Address` in one step.

### Output

```sql
SELECT users.id AS users_id, users.name AS users_name, users.fullname AS users_fullname, users.nickname AS users_nickname,
       addresses_1.id AS addresses_1_id, addresses_1.email_address AS addresses_1_email_address, addresses_1.user_id AS addresses_1_user_id
FROM users
LEFT OUTER JOIN addresses AS addresses_1 ON users.id = addresses_1.user_id
WHERE users.name = 'jack';

# Python Output
<User(name='jack', fullname='Jack Bean', nickname='gjffdd')>
[<Address(email_address='jack@google.com')>, <Address(email_address='j25@yahoo.com')>]
```

### Note

Even though the `OUTER JOIN` resulted in two rows, we still only got one instance of `User` back. SQLAlchemy applies a "uniquing" strategy based on object identity.

### Summary

- **`selectinload()`**: Suitable for loading collections.
- **`joinedload()`**: Better for many-to-one relationships.
- **`subqueryload()`**: Can be used as an alternative to `selectinload()` in some cases.

These eager loading techniques allow you to optimize the way related objects are loaded, reducing the number of queries and improving performance.


### Explicit Join + Eagerload

A third style of eager loading is to construct a `JOIN` explicitly and apply the extra table to a related object or collection on the primary object. This is useful for pre-loading the many-to-one object when filtering on that same object. The `contains_eager()` function allows this.

#### Example

Loading an `Address` row and the related `User` object, filtering on the `User` named “jack”, and using `contains_eager()` to apply the “user” columns to the `Address.user` attribute.

```python
from sqlalchemy.orm import contains_eager

jacks_addresses = session.query(Address).\
                        join(Address.user).\
                        filter(User.name == 'jack').\
                        options(contains_eager(Address.user)).\
                        all()
```

### SQL Output

```sql
SELECT users.id AS users_id,
       users.name AS users_name,
       users.fullname AS users_fullname,
       users.nickname AS users_nickname,
       addresses.id AS addresses_id,
       addresses.email_address AS addresses_email_address,
       addresses.user_id AS addresses_user_id
FROM addresses JOIN users ON users.id = addresses.user_id
WHERE users.name = 'jack';
```

### Python Output

```python
>>> jacks_addresses
[<Address(email_address='jack@google.com')>, <Address(email_address='j25@yahoo.com')>]

>>> jacks_addresses[0].user
<User(name='jack', fullname='Jack Bean', nickname='gjffdd')>
```

For more information on eager loading, including how to configure various forms of loading by default, see the section **Relationship Loading Techniques**.

### Deleting

Deleting a user and checking the cascade behavior for their related address objects.

#### Example

Marking the `User` object `jack` as deleted:

```python
session.delete(jack)
session.query(User).filter_by(name='jack').count()
```

### SQL Output

```sql
UPDATE addresses SET user_id=NULL WHERE addresses.id = ?;
((None, 1), (None, 2))

DELETE FROM users WHERE users.id = ?;
(5,)

SELECT count(*) AS count_1
FROM (SELECT users.id AS users_id,
      users.name AS users_name,
      users.fullname AS users_fullname,
      users.nickname AS users_nickname
      FROM users
      WHERE users.name = 'jack') AS anon_1;
('jack',)
```

### Python Output

```python
0
```

Checking if Jack’s `Address` objects are still present:

```python
session.query(Address).filter(
    Address.email_address.in_(['jack@google.com', 'j25@yahoo.com'])
).count()
```

### SQL Output

```sql
SELECT count(*) AS count_1
FROM (SELECT addresses.id AS addresses_id,
             addresses.email_address AS addresses_email_address,
             addresses.user_id AS addresses_user_id
      FROM addresses
      WHERE addresses.email_address IN ('jack@google.com', 'j25@yahoo.com')) AS anon_1;
```

### Python Output

```python
2
```

### Configuring `delete`/`delete-orphan` Cascade

To ensure related `Address` objects are deleted when the `User` is deleted, configure cascade options on the `User.addresses` relationship.

#### Example

1. **Close the Session:**

```python
session.close()
```

2. **Create a New `declarative_base()`:**

```python
Base = declarative_base()
```

3. **Declare the `User` class with cascade configuration:**

```python
class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    name = Column(String)
    fullname = Column(String)
    nickname = Column(String)
    
    addresses = relationship("Address", back_populates='user',
                             cascade="all, delete, delete-orphan")
    
    def __repr__(self):
        return "<User(name='%s', fullname='%s', nickname='%s')>" % (
            self.name, self.fullname, self.nickname)
```

4. **Declare the `Address` class:**

```python
class Address(Base):
    __tablename__ = 'addresses'
    
    id = Column(Integer, primary_key=True)
    email_address = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship("User", back_populates="addresses")
    
    def __repr__(self):
        return "<Address(email_address='%s')>" % self.email_address
```

5. **Load and modify data:**

```python
jack = session.query(User).get(5)
del jack.addresses[1]

session.query(Address).filter(
    Address.email_address.in_(['jack@google.com', 'j25@yahoo.com'])
).count()
```

### SQL Output

```sql
DELETE FROM addresses WHERE addresses.id = ?;
(2,)

SELECT count(*) AS count_1
FROM (SELECT addresses.id AS addresses_id,
             addresses.email_address AS addresses_email_address,
             addresses.user_id AS addresses_user_id
      FROM addresses
      WHERE addresses.email_address IN ('jack@google.com', 'j25@yahoo.com')) AS anon_1;
```

### Python Output

```python
1
```

By configuring the `cascade` option, the related `Address` objects are deleted when the `User` is deleted. This ensures that orphaned records are not left in the database.


I'm happy to help! Here’s a comprehensive breakdown of your content, complete with explanations and outputs.

---

### Deleting a User and Associated Addresses

When deleting a user, both the user and any associated addresses will be removed if cascading deletes are configured.

#### Example

```python
session.delete(jack)
```

### SQL Operations

Executing the deletion of Jack results in the following SQL statements being emitted:

```sql
DELETE FROM addresses WHERE addresses.id = ?;
(1,)

DELETE FROM users WHERE users.id = ?;
(5,)
```

These statements indicate that one address associated with Jack is deleted, followed by the deletion of Jack himself.

### Verifying Deletion of User

After the deletion, you can check if Jack still exists in the database:

```python
session.query(User).filter_by(name='jack').count()
```

#### SQL Output

```sql
SELECT count(*) AS count_1
FROM (SELECT users.id AS users_id,
             users.name AS users_name,
             users.fullname AS users_fullname,
             users.nickname AS users_nickname
      FROM users
      WHERE users.name = ?) AS anon_1;
('jack',)
```

### Result

```python
0
```

This confirms that Jack has been successfully deleted from the database.

### Verifying Deletion of Addresses

You can also check if any addresses associated with Jack remain:

```python
session.query(Address).filter(
    Address.email_address.in_(['jack@google.com', 'j25@yahoo.com'])
).count()
```

#### SQL Output

```sql
SELECT count(*) AS count_1
FROM (SELECT addresses.id AS addresses_id,
             addresses.email_address AS addresses_email_address,
             addresses.user_id AS addresses_user_id
      FROM addresses
      WHERE addresses.email_address IN (?, ?)) AS anon_1;
('jack@google.com', 'j25@yahoo.com')
```

### Result

```python
0
```

This confirms that all addresses associated with Jack have also been deleted.

---

### More on Cascades

Cascades can be configured in SQLAlchemy to manage how operations like delete affect related objects. For more detailed configuration, refer to the section on **Cascades**. SQLAlchemy's cascade functionality can integrate with the `ON DELETE CASCADE` feature of the relational database, enabling consistent behavior across your application.

---

### Building a Many-to-Many Relationship

Now let’s explore how to set up a many-to-many relationship in SQLAlchemy by creating a blog application where users can write blog posts that have associated keywords.

#### Creating the Association Table

To create a many-to-many relationship, you need an association table. Here’s how you can define it:

```python
from sqlalchemy import Table, Text

# Association table
post_keywords = Table('post_keywords', Base.metadata,
    Column('post_id', ForeignKey('posts.id'), primary_key=True),
    Column('keyword_id', ForeignKey('keywords.id'), primary_key=True)
)
```

In this code:
- `post_keywords` is an un-mapped table that links `posts` and `keywords`.
- Each column in the table represents a foreign key to the `posts` and `keywords` tables.

---

### Defining BlogPost and Keyword Models

Next, define the `BlogPost` and `Keyword` classes, establishing their relationships using the `relationship()` construct.

#### BlogPost Class

```python
class BlogPost(Base):
    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    headline = Column(String(255), nullable=False)
    body = Column(Text)

    # Many-to-many relationship with Keyword
    keywords = relationship('Keyword',
                             secondary=post_keywords,
                             back_populates='posts')

    def __init__(self, headline, body, author):
        self.author = author
        self.headline = headline
        self.body = body

    def __repr__(self):
        return "BlogPost(%r, %r, %r)" % (self.headline, self.body, self.author)
```

In this class:
- Each `BlogPost` is linked to one or more `Keyword` entries via the `post_keywords` association table.

#### Keyword Class

```python
class Keyword(Base):
    __tablename__ = 'keywords'

    id = Column(Integer, primary_key=True)
    keyword = Column(String(50), nullable=False, unique=True)
    posts = relationship('BlogPost',
                          secondary=post_keywords,
                          back_populates='keywords')

    def __init__(self, keyword):
        self.keyword = keyword
```

In this class:
- Each `Keyword` can relate to multiple `BlogPost` entries through the same association table.

---

### Summary of Relationships

- **Cascading Deletes**: Ensure that related objects are deleted when a parent object is deleted.
- **Many-to-Many Relationships**: Use an association table to manage relationships between two entities.

This structure not only maintains referential integrity but also simplifies complex data interactions within your application.

---

### Deleting a User and Associated Addresses

When deleting a user, both the user and any associated addresses will be removed if cascading deletes are configured.

#### Example

```python
session.delete(jack)
```

### SQL Operations

Executing the deletion of Jack results in the following SQL statements being emitted:

```sql
DELETE FROM addresses WHERE addresses.id = ?;
(1,)

DELETE FROM users WHERE users.id = ?;
(5,)
```

These statements indicate that one address associated with Jack is deleted, followed by the deletion of Jack himself.

### Verifying Deletion of User

After the deletion, you can check if Jack still exists in the database:

```python
session.query(User).filter_by(name='jack').count()
```

#### SQL Output

```sql
SELECT count(*) AS count_1
FROM (SELECT users.id AS users_id,
             users.name AS users_name,
             users.fullname AS users_fullname,
             users.nickname AS users_nickname
      FROM users
      WHERE users.name = ?) AS anon_1;
('jack',)
```

### Result

```python
0
```

This confirms that Jack has been successfully deleted from the database.

### Verifying Deletion of Addresses

You can also check if any addresses associated with Jack remain:

```python
session.query(Address).filter(
    Address.email_address.in_(['jack@google.com', 'j25@yahoo.com'])
).count()
```

#### SQL Output

```sql
SELECT count(*) AS count_1
FROM (SELECT addresses.id AS addresses_id,
             addresses.email_address AS addresses_email_address,
             addresses.user_id AS addresses_user_id
      FROM addresses
      WHERE addresses.email_address IN (?, ?)) AS anon_1;
('jack@google.com', 'j25@yahoo.com')
```

### Result

```python
0
```

This confirms that all addresses associated with Jack have also been deleted.

---

### More on Cascades

Cascades can be configured in SQLAlchemy to manage how operations like delete affect related objects. For more detailed configuration, refer to the section on **Cascades**. SQLAlchemy's cascade functionality can integrate with the `ON DELETE CASCADE` feature of the relational database, enabling consistent behavior across your application.

---

### Building a Many-to-Many Relationship

Now let’s explore how to set up a many-to-many relationship in SQLAlchemy by creating a blog application where users can write blog posts that have associated keywords.

#### Creating the Association Table

To create a many-to-many relationship, you need an association table. Here’s how you can define it:

```python
from sqlalchemy import Table, Text

# Association table
post_keywords = Table('post_keywords', Base.metadata,
    Column('post_id', ForeignKey('posts.id'), primary_key=True),
    Column('keyword_id', ForeignKey('keywords.id'), primary_key=True)
)
```

In this code:
- `post_keywords` is an un-mapped table that links `posts` and `keywords`.
- Each column in the table represents a foreign key to the `posts` and `keywords` tables.

---

### Defining BlogPost and Keyword Models

Next, define the `BlogPost` and `Keyword` classes, establishing their relationships using the `relationship()` construct.

#### BlogPost Class

```python
class BlogPost(Base):
    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    headline = Column(String(255), nullable=False)
    body = Column(Text)

    # Many-to-many relationship with Keyword
    keywords = relationship('Keyword',
                             secondary=post_keywords,
                             back_populates='posts')

    def __init__(self, headline, body, author):
        self.author = author
        self.headline = headline
        self.body = body

    def __repr__(self):
        return "BlogPost(%r, %r, %r)" % (self.headline, self.body, self.author)
```

In this class:
- Each `BlogPost` is linked to one or more `Keyword` entries via the `post_keywords` association table.

#### Keyword Class

```python
class Keyword(Base):
    __tablename__ = 'keywords'

    id = Column(Integer, primary_key=True)
    keyword = Column(String(50), nullable=False, unique=True)
    posts = relationship('BlogPost',
                          secondary=post_keywords,
                          back_populates='keywords')

    def __init__(self, keyword):
        self.keyword = keyword
```

In this class:
- Each `Keyword` can relate to multiple `BlogPost` entries through the same association table.

---

### Summary of Relationships

- **Cascading Deletes**: Ensure that related objects are deleted when a parent object is deleted.
- **Many-to-Many Relationships**: Use an association table to manage relationships between two entities.

This structure not only maintains referential integrity but also simplifies complex data interactions within your application.


I'm glad to help you summarize and explain this content. Here’s a detailed breakdown of the many-to-many relationships and related concepts in SQLAlchemy, complete with example outputs.

---

### Notes on Class Declarations and Relationships

In SQLAlchemy’s declarative style, defining `__init__()` methods is optional. However, explicitly defining them can enhance clarity and functionality.

#### Many-to-Many Relationship

The `BlogPost.keywords` relationship showcases the defining feature of many-to-many relationships using the `secondary` keyword argument, which points to an association table (in this case, `post_keywords`). This table only contains columns that reference the two sides of the relationship.

### Adding Author to BlogPost

To implement the author relationship, we need to link `BlogPost` to `User`. Since a user can have multiple blog posts, we configure this relationship with `lazy='dynamic'` to prevent loading all posts at once.

#### Setting Up Relationships

```python
BlogPost.author = relationship(User, back_populates="posts")
User.posts = relationship(BlogPost, back_populates="author", lazy="dynamic")
```

### Creating the Database Tables

After defining the models and their relationships, you need to create the tables in the database:

```python
Base.metadata.create_all(engine)
```

### Resulting SQL Statements

The creation of tables will generate SQL commands like the following:

```sql
CREATE TABLE keywords (
    id INTEGER NOT NULL,
    keyword VARCHAR(50) NOT NULL,
    PRIMARY KEY (id),
    UNIQUE (keyword)
);
COMMIT;

CREATE TABLE posts (
    id INTEGER NOT NULL,
    user_id INTEGER,
    headline VARCHAR(255) NOT NULL,
    body TEXT,
    PRIMARY KEY (id),
    FOREIGN KEY(user_id) REFERENCES users (id)
);
COMMIT;

CREATE TABLE post_keywords (
    post_id INTEGER NOT NULL,
    keyword_id INTEGER NOT NULL,
    PRIMARY KEY (post_id, keyword_id),
    FOREIGN KEY(post_id) REFERENCES posts (id),
    FOREIGN KEY(keyword_id) REFERENCES keywords (id)
);
COMMIT;
```

### Adding Blog Posts for a User

Let’s add some blog posts for a user named Wendy:

#### Retrieving Wendy

```python
wendy = session.query(User).filter_by(name='wendy').one()
```

#### SQL Output

```sql
SELECT users.id AS users_id,
        users.name AS users_name,
        users.fullname AS users_fullname,
        users.nickname AS users_nickname
FROM users
WHERE users.name = ?;
('wendy',)
```

#### Creating a Blog Post

```python
post = BlogPost("Wendy's Blog Post", "This is a test", wendy)
session.add(post)
```

### Adding Keywords

Since keywords are unique in the database, we can add them as follows:

```python
post.keywords.append(Keyword('wendy'))
post.keywords.append(Keyword('firstpost'))
```

### Querying Blog Posts by Keyword

To find all blog posts with the keyword 'firstpost', we can use the `any` operator:

```python
session.query(BlogPost).filter(BlogPost.keywords.any(keyword='firstpost')).all()
```

#### SQL Output

```sql
INSERT INTO keywords (keyword) VALUES (?)
('wendy',);

INSERT INTO keywords (keyword) VALUES (?)
('firstpost',);

INSERT INTO posts (user_id, headline, body) VALUES (?, ?, ?)
(2, "Wendy's Blog Post", 'This is a test');

INSERT INTO post_keywords (post_id, keyword_id) VALUES (?, ?);
...
```

#### Result

```python
[BlogPost("Wendy's Blog Post", 'This is a test', <User(name='wendy', fullname='Wendy Williams', nickname='windy')>)]
```

### Querying Posts Owned by Wendy with a Keyword Filter

To filter blog posts authored by Wendy and also containing a specific keyword:

```python
session.query(BlogPost).filter(BlogPost.author == wendy).filter(BlogPost.keywords.any(keyword='firstpost')).all()
```

#### SQL Output

```sql
SELECT posts.id AS posts_id,
        posts.user_id AS posts_user_id,
        posts.headline AS posts_headline,
        posts.body AS posts_body
FROM posts
WHERE ? = posts.user_id AND (EXISTS (SELECT 1
    FROM post_keywords, keywords
    WHERE posts.id = post_keywords.post_id
        AND keywords.id = post_keywords.keyword_id
        AND keywords.keyword = ?))
(2, 'firstpost')
```

#### Result

```python
[BlogPost("Wendy's Blog Post", 'This is a test', <User(name='wendy', fullname='Wendy Williams', nickname='windy')>)]
```

### Using Wendy’s Own Posts Relationship

You can directly access Wendy's posts using the `posts` relationship defined as dynamic:

```python
wendy.posts.filter(BlogPost.keywords.any(keyword='firstpost')).all()
```

#### SQL Output

```sql
SELECT posts.id AS posts_id,
        posts.user_id AS posts_user_id,
        posts.headline AS posts_headline,
        posts.body AS posts_body
FROM posts
WHERE ? = posts.user_id AND (EXISTS (SELECT 1
    FROM post_keywords, keywords
    WHERE posts.id = post_keywords.post_id
        AND keywords.id = post_keywords.keyword_id
        AND keywords.keyword = ?))
(2, 'firstpost')
```

#### Result

```python
[BlogPost("Wendy's Blog Post", 'This is a test', <User(name='wendy', fullname='Wendy Williams', nickname='windy')>)]
```

### Further References

For more detailed guidance, refer to the following:

- **Query Reference**: [Query API](https://docs.sqlalchemy.org/en/14/orm/query.html)
- **Mapper Reference**: [Mapper Configuration](https://docs.sqlalchemy.org/en/14/orm/mapping_styles.html)
- **Relationship Reference**: [Relationship Configuration](https://docs.sqlalchemy.org/en/14/orm/relationship_api.html)
- **Session Reference**: [Using the Session](https://docs.sqlalchemy.org/en/14/orm/session_api.html)

---



### SQLAlchemy Concepts

1. **Declarative Base**: Use `declarative_base()` to create models that automatically map to database tables.

2. **Model Declaration**:
   - Each model represents a table in the database.
   - Use `__tablename__` to define the table name.
   - Define columns with types, e.g., `INTEGER`, `VARCHAR`, etc.

3. **Relationships**:
   - Use `relationship()` to define relationships between models (e.g., one-to-many, many-to-many).
   - Bidirectional relationships are set using `back_populates`.

4. **Lazy Loading**: Use `lazy='dynamic'` for relationships that might return a large number of records, allowing for filtering.

5. **Creating Tables**: Use `Base.metadata.create_all(engine)` to create tables based on the defined models.

### Tasks Overview

#### 0. User Model
- Create a `User` model for the `users` table with the following attributes:
  - `id`: Integer primary key
  - `email`: Non-nullable string
  - `hashed_password`: Non-nullable string
  - `session_id`: Nullable string
  - `reset_token`: Nullable string

#### 1. Create User
- Implement `add_user` method in the `DB` class to add a new user to the database.

#### 2. Find User
- Implement `find_user_by` to retrieve users based on provided keyword arguments, raising appropriate exceptions.

#### 3. Update User
- Implement `update_user` to update user attributes using `find_user_by`, raising a `ValueError` for invalid attributes.

#### 4. Hash Password
- Define `_hash_password` method using `bcrypt` to return a salted hash of the input password.

#### 5. Register User
- Implement `Auth.register_user` to register a new user, checking for existing users and hashing the password.

#### 6. Basic Flask App
- Set up a Flask app with a single route (`/`) that returns a JSON message.

#### 7. User Registration Endpoint
- Create a POST `/users` route to register users and return appropriate JSON responses.

#### 8. Credentials Validation
- Implement `Auth.valid_login` to validate user credentials by checking email and hashed password.

### Key Code Snippets

1. **User Model Example**:
   ```python
   from sqlalchemy import Column, Integer, String
   from user import Base

   class User(Base):
       __tablename__ = 'users'
       id = Column(Integer, primary_key=True)
       email = Column(String(250), nullable=False)
       hashed_password = Column(String(250), nullable=False)
       session_id = Column(String(250), nullable=True)
       reset_token = Column(String(250), nullable=True)
   ```

2. **DB Class Structure**:
   ```python
   class DB:
       def __init__(self) -> None:
           self._engine = create_engine("sqlite:///a.db", echo=True)
           Base.metadata.create_all(self._engine)
           self.__session = None

       @property
       def _session(self) -> Session:
           if self.__session is None:
               DBSession = sessionmaker(bind=self._engine)
               self.__session = DBSession()
           return self.__session
   ```

3. **User Registration Example**:
   ```python
   try:
       user = auth.register_user(email, password)
   except ValueError as err:
       print("could not create a new user: {}".format(err))
   ```

### Exceptions Handling
- Handle `NoResultFound` and `InvalidRequestError` for database operations to manage queries effectively.

### Flask Integration
- Ensure to import the `Auth` class and handle requests properly to maintain the authentication flow.



Here’s how you can implement the specified functions in your `auth.py` and `app.py` files for the user authentication service. Each function is accompanied by a brief description and example.

### 9. Generate UUID

```python
import uuid

class Auth:
    def __init__(self):
        # Initialization code

    def _generate_uuid(self):
        """Generate a new UUID."""
        return str(uuid.uuid4())
```

### 10. Get session ID

```python
def create_session(self, email: str) -> str:
    """Create a session for a user."""
    user = self._db.find_user_by_email(email)
    if not user:
        return None
    session_id = self._generate_uuid()
    self._db.update_user(user.id, session_id=session_id)
    return session_id
```

**Example:**
```python
auth.create_session(email)  # Returns session ID or None
```

### 11. Log in

```python
from flask import abort, jsonify, request

@app.route('/sessions', methods=['POST'])
def login():
    email = request.form.get('email')
    password = request.form.get('password')
    if not auth.valid_login(email, password):
        abort(401)
    session_id = auth.create_session(email)
    response = jsonify(email=email, message="logged in")
    response.set_cookie('session_id', session_id)
    return response
```

**Example:**
```bash
curl -XPOST localhost:5000/sessions -d 'email=bob@bob.com' -d 'password=mySuperPwd'
```

### 12. Find user by session ID

```python
def get_user_from_session_id(self, session_id: str):
    """Get user by session ID."""
    if session_id is None:
        return None
    return self._db.find_user_by_session_id(session_id)
```

### 13. Destroy session

```python
def destroy_session(self, user_id: int):
    """Destroy user session."""
    self._db.update_user(user_id, session_id=None)
```

### 14. Log out

```python
@app.route('/sessions', methods=['DELETE'])
def logout():
    session_id = request.cookies.get('session_id')
    user = auth.get_user_from_session_id(session_id)
    if not user:
        abort(403)
    auth.destroy_session(user.id)
    return redirect('/')
```

### 15. User profile

```python
@app.route('/profile', methods=['GET'])
def profile():
    session_id = request.cookies.get('session_id')
    user = auth.get_user_from_session_id(session_id)
    if not user:
        abort(403)
    return jsonify(email=user.email)
```

### 16. Generate reset password token

```python
def get_reset_password_token(self, email: str) -> str:
    """Generate a reset password token."""
    user = self._db.find_user_by_email(email)
    if not user:
        raise ValueError("User not found")
    reset_token = self._generate_uuid()
    self._db.update_user(user.id, reset_token=reset_token)
    return reset_token
```

### 17. Get reset password token

```python
@app.route('/reset_password', methods=['POST'])
def reset_password():
    email = request.form.get('email')
    user = auth.get_user_by_email(email)
    if not user:
        abort(403)
    reset_token = auth.get_reset_password_token(email)
    return jsonify(email=email, reset_token=reset_token)
```

### 18. Update password

```python
def update_password(self, reset_token: str, password: str):
    """Update user password."""
    user = self._db.find_user_by_reset_token(reset_token)
    if not user:
        raise ValueError("Invalid token")
    hashed_password = hash_password(password)  # Assume hash_password is defined
    self._db.update_user(user.id, hashed_password=hashed_password, reset_token=None)
```

### 19. Update password endpoint

```python
@app.route('/reset_password', methods=['PUT'])
def update_password_endpoint():
    email = request.form.get('email')
    reset_token = request.form.get('reset_token')
    new_password = request.form.get('new_password')
    
    try:
        auth.update_password(reset_token, new_password)
        return jsonify(email=email, message="Password updated")
    except ValueError:
        abort(403)
```

### Summary of the Flow

1. **User Registration**: Register a new user.
2. **Login**: Create a session and respond with a session ID.
3. **Profile**: Retrieve user profile information using the session ID.
4. **Password Reset**: Generate and send a reset token via email, then allow password updates using the token.

Make sure to adapt these snippets based on your actual database methods and error handling conventions.
