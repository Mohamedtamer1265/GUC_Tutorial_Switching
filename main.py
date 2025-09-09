from website import create_app # will consider the folder as package
app = create_app() 
if __name__ == '__main__':
    app.run(debug=True)# will automatically run


