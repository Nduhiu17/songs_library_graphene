from flask import Flask
from flask_graphql import GraphQLView
from models import db_session
from schema import schema


# Configs
# TO-DO
# Modules
# TO-DO
# Models
# TO-DO
# Schema Objects
# TO-DO
# Routes
# TO-DO

app = Flask(__name__)
app.debug = True

app.add_url_rule(
    '/graphql',
    view_func=GraphQLView.as_view(
        'graphql',
        schema=schema,
        graphiql=True
    )
)


@app.route('/')
def index():
    return "<p>Listen to your favorite songs for free</p>"


@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()


if __name__ == '__main__':
    app.run()
