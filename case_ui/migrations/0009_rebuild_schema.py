"""Rebuild case_ui models: state-wise replace old models, database-wise only create new tables."""
import django.db.models.deletion
from django.db import migrations, models


# ---- State-only operations: replace old model state with new model state ----
state_ops = [
    # Delete old models from migration state (DB tables already dropped manually)
    migrations.DeleteModel(name='Step'),
    migrations.DeleteModel(name='CaseUIInfo'),
    migrations.DeleteModel(name='Element'),
    migrations.DeleteModel(name='CaseUI'),
]

# ---- Operations that run both in state AND in database (create new tables) ----
create_ops = [
    migrations.CreateModel(
        name='KeyWord',
        fields=[
            ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ('keyword_name', models.CharField(max_length=64, verbose_name='关键字名')),
        ],
        options={'verbose_name': 'keyword'},
    ),
    migrations.CreateModel(
        name='Allure',
        fields=[
            ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ('feature', models.CharField(blank=True, default='', max_length=64, verbose_name='所属模块')),
            ('story', models.CharField(blank=True, default='', max_length=64, verbose_name='功能名')),
            ('title', models.CharField(blank=True, default='', max_length=64, verbose_name='用例标题')),
            ('description', models.CharField(blank=True, default='', max_length=64, verbose_name='用例描述')),
        ],
        options={'verbose_name': 'allure'},
    ),
    migrations.CreateModel(
        name='Parametrize',
        fields=[
            ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ('param_key', models.CharField(max_length=64, verbose_name='参数化键名')),
            ('param_value', models.JSONField(verbose_name='参数化键值')),
        ],
        options={'verbose_name': 'parametrize'},
    ),
    migrations.CreateModel(
        name='Validate',
        fields=[
            ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ('validate_type', models.CharField(
                choices=[('equals', 'Equals'), ('contains', 'Contains'), ('db_equals', 'Db Equals'), ('db_contains', 'Db Contains')],
                max_length=32,
                verbose_name='断言类型',
            )),
            ('validate_params', models.JSONField(verbose_name='断言参数')),
        ],
        options={'verbose_name': 'validate'},
    ),
    migrations.CreateModel(
        name='Element',
        fields=[
            ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ('name', models.CharField(max_length=32, verbose_name='元素名称')),
            ('by', models.CharField(max_length=32, verbose_name='定位方式')),
            ('path', models.CharField(max_length=255, verbose_name='定位路径')),
            ('project_id', models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to='project.project',
                verbose_name='项目id',
            )),
        ],
        options={'verbose_name': 'element'},
    ),
    migrations.CreateModel(
        name='Action',
        fields=[
            ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ('sort', models.PositiveIntegerField(verbose_name='执行顺序')),
            ('allure_id', models.OneToOneField(
                on_delete=django.db.models.deletion.CASCADE,
                to='case_ui.allure',
                verbose_name='allure参数id',
            )),
            ('parametrize_id', models.OneToOneField(
                blank=True, null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to='case_ui.parametrize',
                verbose_name='parametrize参数id',
            )),
            ('Validate_id', models.OneToOneField(
                blank=True, null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to='case_ui.validate',
                verbose_name='validate参数id',
            )),
        ],
        options={'ordering': ['sort'], 'verbose_name': 'action'},
    ),
    migrations.CreateModel(
        name='Step',
        fields=[
            ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ('action', models.CharField(max_length=64, verbose_name='操作')),
            ('params', models.JSONField(blank=True, null=True, verbose_name='参数值')),
            ('action_id', models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to='case_ui.action',
                verbose_name='测试步骤id',
            )),
            ('element_id', models.ForeignKey(
                blank=True, null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to='case_ui.element',
                verbose_name='页面元素id',
            )),
            ('keyword_id', models.ForeignKey(
                blank=True, null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to='case_ui.keyword',
                verbose_name='关键字id',
            )),
        ],
        options={'verbose_name': 'step'},
    ),
    migrations.CreateModel(
        name='CaseUI',
        fields=[
            ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ('name', models.CharField(max_length=64, verbose_name='UI测试用例名称')),
            ('project_id', models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to='project.project',
                verbose_name='项目id',
            )),
        ],
        options={'verbose_name': 'caseui'},
    ),
    migrations.CreateModel(
        name='CaseUIStep',
        fields=[
            ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ('sort', models.PositiveIntegerField(verbose_name='执行顺序')),
            ('caseui_id', models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to='case_ui.caseui',
                verbose_name='UI测试用例id',
            )),
            ('step_id', models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to='case_ui.step',
                verbose_name='测试步骤id',
            )),
        ],
        options={
            'ordering': ['caseui_id', 'sort'],
            'unique_together': [('caseui_id', 'sort')],
            'verbose_name': 'caseuistep',
        },
    ),
    migrations.AddField(
        model_name='caseui',
        name='step_id',
        field=models.ManyToManyField(
            through='case_ui.CaseUIStep',
            to='case_ui.Step',
            verbose_name='步骤id',
        ),
    ),
]


class Migration(migrations.Migration):

    dependencies = [
        ('case_ui', '0008_alter_caseui_caseuiinfo'),
        ('project', '0001_initial'),
    ]

    operations = [
        # State-only: remove old models from migration graph (no SQL executed)
        migrations.SeparateDatabaseAndState(
            database_operations=[],
            state_operations=state_ops,
        ),
        # Both state + DB: create all new tables
        *create_ops,
    ]
