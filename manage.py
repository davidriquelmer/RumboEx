from flask_script import Manager, Server
from RumboEx import app

manager = Manager(app)

manager.add_command("runserver", Server(
    use_debugger=True,
    use_reloader=True,
    host="localhost"
))

if __name__ == '__main__':
    manager.run()
