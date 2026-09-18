from pathlib import Path

from rest_framework import serializers

from suite.models import Suite, RunResult


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

    def get_report_url(self,obj):
        dir_name = Path(obj.path)
        return  f"http://127.0.0.1:8000/api/suite/static/{dir_name.name}/report/index.html"

    def get_log_url(self,obj):
        dir_name = Path(obj.path)
        log_file = dir_name.glob("log/*.log")
        log_url_list = []
        for log in log_file:
            log_url_list.append(f"http://127.0.0.1:8000/api/suite/static/{dir_name.name}/log/{log.name}")
        return log_url_list

    def get_yaml_url(self,obj):
        dir_name = Path(obj.path).parent
        yaml_file = dir_name.glob("testcases/*.yaml")
        yaml_url_list = []
        for yaml in yaml_file:
            yaml_url_list.append(f"http://127.0.0.1:8000/api/suite/static/{dir_name.name}/testcases/{yaml.name}")
        return yaml_url_list