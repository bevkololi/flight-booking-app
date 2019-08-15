import json

from rest_framework.renderers import JSONRenderer


class ProfileJSONRenderer(JSONRenderer):
    """
    Describe how JSON is rendered by the profile app.
    """
    charset = 'utf-8'

    def render(self, data, media_type=None, renderer_context=None):
        # Attempt to get errors from the data object.

        errors = data.get('errors', None)

        if errors is not None:
            # Let the JSONRenderer handle any arising errors.
            return super().render(data)

        # namespace all profile responses with profiles
        return json.dumps(data)
