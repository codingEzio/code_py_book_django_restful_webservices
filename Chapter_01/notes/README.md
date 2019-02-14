
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