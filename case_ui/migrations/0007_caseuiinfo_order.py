# Add CaseUIInfo.order (not null) with a one-off default for existing rows.

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("case_ui", "0006_alter_element_locator"),
    ]

    operations = [
        migrations.AddField(
            model_name="caseuiinfo",
            name="order",
            field=models.PositiveBigIntegerField(
                default=1, verbose_name="测试步骤执行顺序"
            ),
            preserve_default=False,
        ),
        migrations.AlterModelOptions(
            name="caseuiinfo",
            options={"ordering": ["order"]},
        ),
    ]
