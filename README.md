# team_generator

TKinter is a 2 step process

1) Create the object
2) Display the object

```python

Button(root, text="text", state=DISABLED, padx=50)


# Input Field

e = Entry(root, width="50")
e.pack()
e.get()
e.insert(0, "placeholder") # Placeholder for input field


# Frame

frame = LabelFrame(root, padx=5, pady=5) # padding inside frame
frame.pack(padx=10, pady=10  ) # padding outside frame
```