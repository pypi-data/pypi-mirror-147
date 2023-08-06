from distutils.core import setup

setup(
    name="fakerDemo",  # 设置包名，pip install fakerDemo
    version="0.0.10",    # 版本号
    description="faker demo module", # 包的描述信息
    author="moluo",     # 作者
    py_modules = [        # 设置发布的包的文件列表，只要是要发布上线的都要把路径填上
        'faker_demo.person.mobile',
        'faker_demo.person.nickname',
        'faker_demo.company.name',
        'faker_demo.company.job'
    ]
)