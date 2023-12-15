# Welcome to my Password Manager!
**What can it do?** - Right now, you can create an account, login to your account, and create, edit, view, and delete passwords! There are also helpful commands which allow you to learn more about how the password manager works and tips for good internet security practices!

**What do I need to install**? - Install the latest version of PostgreSQL [here](https://www.postgresql.org/download/).
This password manager was created with Windows version 16 of PostgreSQL. There are also additional packages you might need to install in the **REQUIREMENTS.txt** file.

## Important steps
1. After installing PostgreSQL, ensure that you remember the password that they prompt you to enter and the name of the default database (the name of the default database should be 'postgres', but double check).
2. Next, in the **database.ini** file, change the name of the database paramater value to the default database 'postgres'.
    - Note that you may also have to change other parameter values such as password, host, and port according to how you installed PostgreSQL!
3. Then, run **initialize.py**. If this does not work, double-check database.ini.
4. After running **initialize.py**, change the name of the database in database.ini back to 'ekeys'.
5. Finally, run **main.py** and enjoy!

