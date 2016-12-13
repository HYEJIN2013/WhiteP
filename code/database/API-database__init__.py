from football_data.football_api_parser import FootballAPIWrapper

faw = FootballAPIWrapper()
faw.api_key = 'my_key'


def create_app(config_name):
    app = Flask(__name__)

    #loading configurations into the app
    app.config.from_object(config[config_name])

    #initialise the application
    config[config_name].init_app(app)

    faw.init_app(app)
    return app
