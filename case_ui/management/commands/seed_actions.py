from django.core.management.base import BaseCommand
from project.models import Project
from case_ui.models import Action, Element, KeyWord

KEYWORDS = [
    ("send_keys", "输入"),
    ("click", "点击"),
    ("clear", "清空"),
    ("text", "获取文本"),
    ("save_code_img", "保存验证码图片"),
    ("send_code", "输入验证码"),
]

ELEMENTS = [
    ("用户名输入框", "XPATH", '//input[@placeholder="用户名"]'),
    ("密码输入框", "XPATH", '//input[@placeholder="密码"]'),
    ("登录按钮", "XPATH", '//button[contains(text(),"登录")]'),
    ("记住我复选框", "XPATH", '//input[@name="remember"]'),
    ("登录错误提示", "XPATH", '//div[@class="login-error"]'),
    ("用户列表表格", "XPATH", '//table[@id="userTable"]'),
    ("新增用户按钮", "XPATH", '//button[@id="addUserBtn"]'),
    ("手机号输入框", "XPATH", '//input[@placeholder="手机号"]'),
    ("提交按钮", "XPATH", '//button[@type="submit"]'),
    ("编辑按钮", "XPATH", '//button[contains(text(),"编辑")]'),
    ("验证码图片", "XPATH", '//img[@id="captchaImg"]'),
    ("验证码输入框", "XPATH", '//input[@placeholder="验证码"]'),
]

ACTIONS = [
    {
        "name": "登录成功-正确账号密码",
        "allure": {
            "feature": "登录模块",
            "story": "账号登录",
            "title": "登录成功-正确账号密码",
            "description": "输入正确的账号密码并点击登录，验证成功进入首页",
        },
        "step": [
            {"sort": 1, "keyword_id": 1, "element_id": 1, "params": ["admin"]},
            {"sort": 2, "keyword_id": 1, "element_id": 2, "params": ["123456"]},
            {"sort": 3, "keyword_id": 2, "element_id": 3, "params": []},
        ],
        "parametrize": {
            "username": ["admin", "test01"],
            "password": ["123456", "123456"],
        },
        "validate": {
            "equals": [
                {
                    "expect_result": "admin",
                    "actual_result": {"keyword_id": 4, "element_id": 6, "params": []},
                }
            ]
        },
    },
    {
        "name": "登录失败-错误密码提示",
        "allure": {
            "feature": "登录模块",
            "story": "账号登录",
            "title": "登录失败-错误密码提示",
            "description": "输入错误密码点击登录，验证提示文案",
        },
        "step": [
            {"sort": 1, "keyword_id": 1, "element_id": 1, "params": ["admin"]},
            {"sort": 2, "keyword_id": 1, "element_id": 2, "params": ["wrong123"]},
            {"sort": 3, "keyword_id": 2, "element_id": 3, "params": []},
            {"sort": 4, "keyword_id": 4, "element_id": 5, "params": []},
        ],
        "parametrize": {},
        "validate": {
            "equals": [
                {
                    "expect_result": "用户名或密码错误",
                    "actual_result": {"keyword_id": 4, "element_id": 5, "params": []},
                }
            ]
        },
    },
    {
        "name": "新增用户-填写信息并提交",
        "allure": {
            "feature": "用户管理",
            "story": "新增用户",
            "title": "新增用户-填写信息并提交",
            "description": "点击新增按钮填写用户名和手机号并提交，验证新增成功",
        },
        "step": [
            {"sort": 1, "keyword_id": 2, "element_id": 7, "params": []},
            {"sort": 2, "keyword_id": 1, "element_id": 1, "params": ["zhangsan01"]},
            {"sort": 3, "keyword_id": 1, "element_id": 8, "params": ["13800000000"]},
            {"sort": 4, "keyword_id": 2, "element_id": 9, "params": []},
        ],
        "parametrize": {
            "username": ["zhangsan01", "lisi02"],
            "phone": ["13800000000", "13900000000"],
        },
        "validate": {
            "equals": [
                {
                    "expect_result": "zhangsan01",
                    "actual_result": {"keyword_id": 4, "element_id": 6, "params": []},
                }
            ]
        },
    },
    {
        "name": "修改用户信息-清空后重填",
        "allure": {
            "feature": "用户管理",
            "story": "修改用户",
            "title": "修改用户信息-清空后重填",
            "description": "编辑用户信息前清空用户名输入框并重新填写，提交后验证修改成功",
        },
        "step": [
            {"sort": 1, "keyword_id": 2, "element_id": 10, "params": []},
            {"sort": 2, "keyword_id": 3, "element_id": 1, "params": []},
            {"sort": 3, "keyword_id": 1, "element_id": 1, "params": ["zhangsan02"]},
            {"sort": 4, "keyword_id": 2, "element_id": 9, "params": []},
        ],
        "parametrize": {},
        "validate": {
            "equals": [
                {
                    "expect_result": "zhangsan02",
                    "actual_result": {"keyword_id": 4, "element_id": 6, "params": []},
                }
            ]
        },
    },
    {
        "name": "验证码登录-识别并填充验证码",
        "allure": {
            "feature": "登录模块",
            "story": "验证码登录",
            "title": "验证码登录-识别并填充验证码",
            "description": "输入账号密码后保存验证码图片并自动输入验证码，点击登录成功",
        },
        "step": [
            {"sort": 1, "keyword_id": 1, "element_id": 1, "params": ["admin"]},
            {"sort": 2, "keyword_id": 1, "element_id": 2, "params": ["123456"]},
            {"sort": 3, "keyword_id": 5, "element_id": 11, "params": []},
            {"sort": 4, "keyword_id": 6, "element_id": 12, "params": []},
            {"sort": 5, "keyword_id": 2, "element_id": 3, "params": []},
        ],
        "parametrize": {},
        "validate": {
            "equals": [
                {
                    "expect_result": "admin",
                    "actual_result": {"keyword_id": 4, "element_id": 6, "params": []},
                }
            ]
        },
    },
]


class Command(BaseCommand):
    help = "为 case_ui 造示例数据：6 个关键字、12 个元素、5 条 Action（前端新格式）"

    def add_arguments(self, parser):
        parser.add_argument("--project_id", type=int, default=1, help="项目 id，默认 1")

    def handle(self, *args, **options):
        project = Project.objects.get(id=options["project_id"])

        if not KeyWord.objects.exists():
            KeyWord.objects.bulk_create(
                [KeyWord(keyword_name=n, description=d) for n, d in KEYWORDS]
            )
            self.stdout.write(f"created keywords: {len(KEYWORDS)}")
        else:
            self.stdout.write("keywords already exist, skip")

        if not Element.objects.filter(project_id=project).exists():
            Element.objects.bulk_create(
                [
                    Element(name=n, by=b, path=p, project_id=project)
                    for n, b, p in ELEMENTS
                ]
            )
            self.stdout.write(f"created elements: {len(ELEMENTS)}")
        else:
            self.stdout.write("elements already exist, skip")

        if not Action.objects.filter(project_id=project).exists():
            Action.objects.bulk_create(
                [
                    Action(
                        name=a["name"],
                        allure=a["allure"],
                        step=a["step"],
                        parametrize=a["parametrize"],
                        validate=a["validate"],
                        project_id=project,
                    )
                    for a in ACTIONS
                ]
            )
            self.stdout.write(f"created actions: {len(ACTIONS)}")
        else:
            self.stdout.write("actions already exist, skip")
