import os
from flask import Flask

def load_config():
    import xml.etree.ElementTree as ET
    tree = ET.parse('p17data/config.html')
    articles = tree.findall('body/article')
    config = {}
    for article in articles:
        sections = article.findall('section')
        for section in sections:
            configName = section.find('header/hgroup/h1').text
            paragraph = section.find('section/p')
            definitions = section.findall('section/dl/*')
            if paragraph is not None:
                config[configName] = paragraph.text
            elif definitions:
                config[configName] = {}
                for definition in definitions:
                    if definition.tag == 'dt':
                        definitionName = definition.text
                    elif definition.tag == 'dd':
                        config[configName][definitionName] = definition.text
    return config

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    
    app.config.update(load_config())

#    app.config.from_pyfile('p17data/config.py', silent=True)
#            SECRET_KEY='dev',
#            DATABASE=os.path.join(app.instance_path, 'blog.sqlite'),
#    )

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route('/hello')
    def hello():
        return 'Hello, World'

    from . import db
    db.init_app(app)

    from . import blog
    app.register_blueprint(blog.bp)
    app.add_url_rule('/', endpoint='index')

    return app
