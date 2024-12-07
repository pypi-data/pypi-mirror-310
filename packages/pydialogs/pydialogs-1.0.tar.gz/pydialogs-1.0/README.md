# pydialogs
Python Library for making Dialogs
## Requirements
- Python 3.x
- `curses` and `textwrap` libraries
## Functions
### 1. `alert(title, message, width=50, height=10, button="OK")`
Displays a simple alert box in the console.
#### Parameters:
- `title` (str): The title of the box.
- `message` (str): The message to display in the box.
- `width` (int, optional): The width of the box. Default is 50.
- `height` (int, optional): The height of the box. Default is 10.
- `button` (str, optional): The label of the button. Default is "OK".
#### Example Usage:
```python
alert("Welcome", "Welcome to my script, press OK to continue.")
```
### 2. `select(title, message, width=50, height=10, options=None)` `(returns str)`
Displays a box in the console where the user can use the arrow keys to navigate through choices the user can select.
#### Parameters:
- `title` (str): The title of the selection box.
- `message` (str): The message to display in the box.
- `width` (int, optional): The width of the box. Default is 50.
- `height` (int, optional): The height of the box. Default is 10.
- `options` (list, optional): A list of options to choose from. Default is `["Yes", "No"]`.
#### Example Usage:
```python
selection = select("IMPORTANT", "All data will be erased on drive Z:\, do you want to continue?", options=["Yes", "No"])
alert(f"You selected: {selection}")
```
