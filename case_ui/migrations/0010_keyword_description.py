"""Add description field to KeyWord and populate existing rows."""
from django.db import migrations, models


def populate_description(apps, schema_editor):
    KeyWord = apps.get_model('case_ui', 'KeyWord')
    desc_map = {
        'find_element': '查找单个元素',
        'find_elements': '查找多个元素',
        'clear': '清空输入框',
        'send_keys': '输入文本',
        'click': '点击元素',
        'text': '获取元素文本',
        'save_code_img': '保存验证码图片',
        'send_code': '发送验证码',
        'switch_to_alert': '切换到弹窗',
        'alert_text': '获取弹窗文本',
        'alert_accept': '接受弹窗',
        'alert_dismiss': '关闭弹窗',
        'alert_send_keys': '弹窗输入文本',
        'select_by_index': '下拉框按索引选择',
        'select_by_value': '下拉框按值选择',
        'select_by_visible_text': '下拉框按可见文本选择',
    }
    for kw in KeyWord.objects.all():
        kw.description = desc_map.get(kw.keyword_name, '')
        kw.save()


def reverse_populate(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('case_ui', '0009_rebuild_schema'),
    ]

    operations = [
        migrations.AddField(
            model_name='keyword',
            name='description',
            field=models.CharField(default='', max_length=64, verbose_name='操作描述'),
        ),
        migrations.RunPython(populate_description, reverse_populate),
    ]
