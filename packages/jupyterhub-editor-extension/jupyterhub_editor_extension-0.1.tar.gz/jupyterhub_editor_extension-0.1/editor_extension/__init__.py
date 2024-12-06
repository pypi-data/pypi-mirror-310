from jupyterhub.handlers import BaseHandler

class EditorExtensionHandler(BaseHandler):
    async def get(self):
        self.write(f'Hello, this is mya EditorExtensionHandler')

def load_jupyterhub_extension(app):
    app.log.info('loading... editor extension handler')
    app.web_app.add_handlers('.*$', [(r'/editor-extension', EditorExtensionHandler)])
