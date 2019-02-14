
### Getting Started 
- Note
    - I'll explain what those aliases are later.
- Base
    1. ```pip3 install Django==1.11.5```
    2. ```pip3 install djangorestframework==3.6.4```
- Init 
    - ```djproj our_project && cd our_project```
    - ```djapp toys```
- Base & Init
    - Add these to ```INSTALLED_APPS```
        - ```rest_framework```
        - ```toys.apps.ToysConfig```
- Migrate 
    - ```djmakemig toys && djmig```
- Other terminal apps

    ```bash
    # 1.curl
    brew install curl

    # 2. httpie
    pip3 install httpie

    # 3. Postman
    # https://www.getpostman.com/downloads/

    # 4. Stoplight
    # https://stoplight.io (resiger needed, what the hell?)
    ```
    
### Checking Databases
- The 1st option is to use the ```sqlite3``` command utility.
    - Like this 
        
        ```bash
        # Tables | SQL script | SQL command
        
        sqlite3 db.sqlite3 ".tables"
        sqlite3 db.sqlite3 ".schema toys_toy"
        sqlite3 db.sqlite3 "SELECT * FROM toys_toy ORDER BY name;"
        ```
    
- Or, you could use a GUI tool.
    - Paid: [Navicat Premium](https://www.navicat.com/en/products/navicat-premium)
    - Free: [DB Browser for SQLite](https://sqlitebrowser.org/)