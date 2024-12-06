<a name="readme-top"></a>

<br />
<h1 align="center">RR Connection Manager</h1>

  <p align="center">
    A package to help you connect to all Registry databases
    <br />
    <br />
    ·
    <a href="https://github.com/github_username/repo_name/issues">Report Bug</a>
    ·
    <a href="https://github.com/github_username/repo_name/issues">Request Feature</a>
  </p>
<br/>

## About The Project

This package wraps pykeepass and sshtunnel along with various connection tools including SQLAlchemy, to allow an all in one solution for connecting via SSH to our servers without the need to store connection details locally  
<br/>

## Getting Started

```
poetry add rr-connection-manager
```
or

```
pip install rr-connection-manager
```

### Prerequisites

You will need to ensure make sure you meet all the expected requirements for using <strong><a href="https://www.psycopg.org/docs/install.html#psycopg-vs-psycopg-binary">pyscopg2</a></strong>

## Connection Variables

The primary use case is for the connection variables to be taken from a keepass file. This will require some setup which includes running the <strong><a href="https://github.com/renalreg/rr-key-manager">RR Key Manager</a></strong>. Once you have done that connection manager should work out of the box.

Adding a conf.json file at the root of your project will override any attempt to connect to keepass. This is useful if you can't access the keepass file or you want use this on one of the servers. You can add connection details for as many servers as you like but the app_name field in the conf file must match the app_name variable past to the function to create your connection. 

```json
[
  {
    "app_name": "app_name",
    "app_host": "app_host",
    "db_host": "db_host",
    "database": "database_name",
    "db_user": "database_username",
    "db_password": "db_user_password",
    "db_port": "database_port",
    "tunnel_user": "tunnel_user",
    "tunnel_port": "tunnel_port"
  },
]
```
Not all of these are required for each connection. SQL Server connections for example only require DB_HOST and DATABASE.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## SQL Server Connection

To create a SQL Server connection object 

``` python
conn = SQLServerConnection(app="app_name")
```

From this you can choose to open a pyodbc cursor and use that to query the database

``` python
conn = SQLServerConnection(app="app_name")
cur = conn.cursor()
cur.execute("SELECT @@version")
info = cur.fetchone()
cur.close()
print(info)
```

You can pass in any extra config arguments you like when creating a cursor

``` python
conn = SQLServerConnection(app="app_name")
cur = conn.cursor(timeout=30, autocommit=True)
```

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Postgres Connection

To create a Postgres connection object 

``` python
conn = PostgresConnection(app="app_name")
```

From this you can choose to open a pyscopg2 cursor and use that to query the database

``` python
conn = PostgresConnection(app="app_name")
cur = conn.cursor()
cur.execute("SELECT version()")
info = cur.fetchone()
cur.close()
print(info)
```

You can pass in any extra config arguments you like when creating a cursor

``` python
conn = PostgresConnection(app="app_name")
cur = conn.cursor(connect_timeout=30, autocommit=True)
```

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## SQLite Connection

⚠️ Currently unsupported 

## SQL Alchemy

All connection types also wrap sqlalchemy so you are able to access a session. This uses the standard set of arguments when creating the engine.

``` python
conn = PostgresConnection(app="app_name")
session = conn.session()
```

You can build the engine yourself which you allows you to pass arguments

``` python
conn = PostgresConnection(app="app_name")
eng = conn.engine(echo=True)
session = conn.session(eng)
```

A session maker is also accessible and allows you to pass arguments

``` python
conn = PostgresConnection(app="app_name")
Session = conn.session_maker(expire_on_commit=True)
session = Session()
```

You can combine both

``` python
conn = PostgresConnection(app="app_name")
eng = conn.engine(echo=True)
Session = conn.session_maker(eng, expire_on_commit=True)
session = Session()
check_message = session.execute(text("""select version()""")).first()
session.close()
conn.close()
print(check_message)
```

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Connection check

To make testing the connection simple each class has a connection_check function that checks the version of the database it is connecting to. This uses the base packages not SQLAlchemy but it is assumed if they work so should SQLAlchemy.

```python
from rr_connection_manager import PostgresConnection
from rr_connection_manager import SQLServerConnection

conn = PostgresConnection(app="app_name")
conn.connection_check()

conn = SQLServerConnection(app="app_name")
conn.connection_check()
```

## Using a Tunnel

To connect to a database over SSH you need to add the tunnel argument.

```python
conn = PostgresConnection(app="app_name", tunnel=True)
```

In cases where you want to tunnel through an app server to the database server you can add the via_app argument

```python
conn = PostgresConnection(app="app_name", tunnel=True, via_app=True)
```

## Using a Specific Local Port
To use a specific local port with your connection you can pass the local_port argument.

```python
conn = PostgresConnection(app="app_name", tunnel=True, local_port=6100)
```

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE.txt` for more information.


# Contact

Renal Registry - [@UKKidney](https://twitter.com/@UKKidney) - rrsystems@renalregistry.nhs.uk

Project Link: [https://github.com/renalreg/rr-connection-manager](https://github.com/renalreg/rr-connection-manager)

<br />


# Acknowledgments

- [Best-README-Template](https://github.com/othneildrew/Best-README-Template)
- [Psycopg2](https://www.psycopg.org/)
- [Pyodbc](https://github.com/mkleehammer/pyodbc/wiki)
- [SQLAlchemy](https://www.sqlalchemy.org/)
- [Pykeepass](https://github.com/libkeepass/pykeepass)
- [sshtunnel](https://github.com/pahaz/sshtunnel)

<p align="right">(<a href="#readme-top">back to top</a>)</p>


[issues-shield]: https://img.shields.io/github/issues/renalreg/rr-connection-manager.svg?style=for-the-badge
[issues-url]: https://github.com/renalreg/rr-connection-manager/issues
[license-shield]: https://img.shields.io/github/license/renalreg/rr-connection-manager.svg?style=for-the-badge
[license-url]: https://github.com/renalreg/rr-connection-manager/blob/main/LICENSE

