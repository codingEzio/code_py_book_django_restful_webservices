
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