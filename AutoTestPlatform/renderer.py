from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer

class CodeResultMessageRenderer(JSONRenderer):
    def render(self, data, accepted_media_type=None, renderer_context=None):
        response: Response = renderer_context.get("response")

        response_dict = {
            "code": response.status_code,
            "message": "ok",
            "result": data
        }

        if 200<=response.status_code<=300:
            pass
        elif response.status_code >= 400:
            if "detail" in data:
                response_dict["message"] = data["detail"]
            elif isinstance(data,dict):
                response_dict["message"] = list(data.values())[0][0]
            elif isinstance(data,list):
                response_dict["message"] = str(data[0])
        return super().render(response_dict, accepted_media_type, renderer_context)