from django.db import migrations, models


def strip_step_args(apps, schema_editor):
    """把 Action.step 中每个步骤的 args 键去掉（用户要求的数据变更）"""
    Action = apps.get_model("case_ui", "Action")
    for action in Action.objects.all():
        steps = action.step or []
        new_steps = []
        changed = False
        for step in steps:
            if "args" in step:
                step = {k: v for k, v in step.items() if k != "args"}
                changed = True
            new_steps.append(step)
        if changed:
            action.step = new_steps
            action.save(update_fields=["step"])


def build_action_list(apps, schema_editor):
    """删除 CaseUIAction 之前，按 sort 顺序把它记录的关系展开成 CaseUI.action_list"""
    CaseUI = apps.get_model("case_ui", "CaseUI")
    CaseUIAction = apps.get_model("case_ui", "CaseUIAction")
    KeyWord = apps.get_model("case_ui", "KeyWord")
    Element = apps.get_model("case_ui", "Element")

    keywords = {k.id: k.keyword_name for k in KeyWord.objects.all()}
    elements = {e.id: (str(e.by), e.path) for e in Element.objects.all()}

    for caseui in CaseUI.objects.all():
        cases = []
        rows = (
            CaseUIAction.objects.filter(caseui_id=caseui.id)
            .select_related("action_id")
            .order_by("sort")
        )
        for row in rows:
            action = row.action_id
            case = dict(action.allure or {})
            steps = []
            for step in action.step or []:
                step_dict = {"action": step.get("action")}
                step_dict["keyword"] = keywords.get(step.get("keyword_id"))
                if "element_id" in step:
                    locator = elements.get(step["element_id"])
                    if locator:
                        step_dict["locator"] = [locator[0], locator[1]]
                steps.append(step_dict)
            case["step"] = steps
            cases.append(case)
        caseui.action_list = cases
        caseui.save(update_fields=["action_list"])


class Migration(migrations.Migration):

    dependencies = [
        ("case_ui", "0022_alter_element_by"),
    ]

    operations = [
        migrations.AddField(
            model_name="caseui",
            name="action_list",
            field=models.JSONField(default=list, verbose_name="测试步骤"),
            preserve_default=False,
        ),
        migrations.RunPython(strip_step_args, migrations.RunPython.noop),
        migrations.RunPython(build_action_list, migrations.RunPython.noop),
        migrations.RemoveField(
            model_name="action",
            name="parametrize",
        ),
        migrations.RemoveField(
            model_name="action",
            name="validate",
        ),
        migrations.DeleteModel(
            name="CaseUIAction",
        ),
    ]
