from django.core.management.base import BaseCommand

from case_ui.models import Action, CaseUI, CaseUIAction
from project.models import Project

CASES = [
    ("用户管理完整流程", [5, 6, 7, 8, 9]),
    ("登录与搜索用户", [5, 6]),
    ("新增用户并校验", [5, 7]),
    ("删除用户并校验", [5, 8]),
    ("登录退出流程", [5, 9]),
]


class Command(BaseCommand):
    help = "按已有 Action 造 CaseUI：5 条用例，用 CaseUIAction.sort 排序"

    def add_arguments(self, parser):
        parser.add_argument("--project_id", type=int, default=21)

    def handle(self, *args, **options):
        project = Project.objects.get(id=options["project_id"])
        for name, action_ids in CASES:
            case, created = CaseUI.objects.get_or_create(name=name, project_id=project)
            if not created:
                self.stdout.write(f"exists, skip: {name}")
                continue
            for sort, aid in enumerate(action_ids, 1):
                CaseUIAction.objects.create(
                    caseui_id=case,
                    sort=sort,
                    action_id=Action.objects.get(id=aid, project_id=project),
                )
            self.stdout.write(f"created: {name} ({len(action_ids)} actions)")
