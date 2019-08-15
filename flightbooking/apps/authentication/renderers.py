import json

from rest_framework.renderers import JSONRenderer


class UserJSONRenderer(JSONRenderer):
    charset = 'utf-8'

    def render(self, data, media_type=None, render_context=None):
        errors = data.get('errors', None)

        if errors is not None:
            return super().render(data)

        return json.dumps({
            'user': data
        })