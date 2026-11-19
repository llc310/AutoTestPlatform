from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("suite", "0005_suite_hook_alter_suite_run_type"),
    ]

    operations = [
        migrations.RenameField(
            model_name="suite",
            old_name="project",
            new_name="project_id",
        ),
    ]
