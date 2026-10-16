# Manual migration: align case_ui schema with current models.py
# Old data (pre-0005) was dumped to _case_ui_old_dump.json before applying;
# a follow-up script reads that dump and backfills Step / M2M / by / name.

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("case_ui", "0004_remove_caseui_allure_remove_caseui_element_and_more"),
    ]

    operations = [
        # 1. Create the new Step model (no M2M yet; added later).
        migrations.CreateModel(
            name="Step",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "order",
                    models.PositiveBigIntegerField(
                        verbose_name="页面操作执行顺序"
                    ),
                ),
                (
                    "action",
                    models.CharField(max_length=64, verbose_name="页面操作名称"),
                ),
                (
                    "keyword",
                    models.CharField(max_length=64, verbose_name="页面操作关键字"),
                ),
                (
                    "args",
                    models.JSONField(
                        blank=True, default=list, verbose_name="函数参数"
                    ),
                ),
            ],
            options={
                "ordering": ["order"],
            },
        ),
        # 2. Element: add `by` column (one-off default, then preserved=False).
        migrations.AddField(
            model_name="element",
            name="by",
            field=models.CharField(
                default="", max_length=32, verbose_name="定位方式"
            ),
            preserve_default=False,
        ),
        # 3. Element.locator: was TEXT (holding JSON {"by":..,"value":..});
        #    now a plain CharColumn holding the value string.
        migrations.AlterField(
            model_name="element",
            name="locator",
            field=models.CharField(max_length=255, verbose_name="定位路径"),
        ),
        # 4. CaseUI: add `name` column (one-off default).
        migrations.AddField(
            model_name="caseui",
            name="name",
            field=models.CharField(
                default="", max_length=64, verbose_name="UI测试用例名称"
            ),
            preserve_default=False,
        ),
        # 5. Drop old CaseUIInfo.step (JSON text column; data already dumped).
        migrations.RemoveField(
            model_name="caseuiinfo",
            name="step",
        ),
        # 6. Drop old CaseUIInfo.element M2M.
        migrations.RemoveField(
            model_name="caseuiinfo",
            name="element",
        ),
        # 7. Step.element M2M -> Element (Element table already exists).
        migrations.AddField(
            model_name="step",
            name="element",
            field=models.ManyToManyField(
                to="case_ui.element", verbose_name="页面元素id"
            ),
        ),
        # 8. CaseUIInfo.step M2M -> Step.
        migrations.AddField(
            model_name="caseuiinfo",
            name="step",
            field=models.ManyToManyField(
                to="case_ui.step", verbose_name="操作顺序"
            ),
        ),
        # 9. CaseUIInfo.name verbose_name tweak.
        migrations.AlterField(
            model_name="caseuiinfo",
            name="name",
            field=models.CharField(max_length=32, verbose_name="ui测试步骤名称"),
        ),
    ]
