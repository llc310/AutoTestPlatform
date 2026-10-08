from pathlib import Path

from rest_framework import serializers

from suite.models import RunResult, Suite


class SuiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Suite
        fields = "__all__"


class RunResultSerializer(serializers.ModelSerializer):
    report_url = serializers.SerializerMethodField()
    log_url = serializers.SerializerMethodField()
    yaml_url = serializers.SerializerMethodField()

    class Meta:
        model = RunResult
        fields = "__all__"

    def get_report_url(self, obj):
        dir_name = Path(obj.path)
        return (
            f"http://127.0.0.1:8000/api/suite/static/{dir_name.as_posix()}/report/index.html"
        )

    def get_log_url(self, obj):
        dir_name = Path(obj.path)
        return (
            f"http://127.0.0.1:8000/api/suite/static/{dir_name.as_posix()}/frame.log"
        )

    def get_yaml_url(self, obj):
        dir_name = Path(obj.path)
        yaml_file = Path("upload_yaml" / dir_name).glob("yaml/*.yaml")
        yaml_url_list = []
        for yaml in yaml_file:
            yaml_url_list.append(
                f"http://127.0.0.1:8000/api/suite/static/{dir_name.as_posix()}/yaml/{yaml.name}"
            )
        return yaml_url_list
