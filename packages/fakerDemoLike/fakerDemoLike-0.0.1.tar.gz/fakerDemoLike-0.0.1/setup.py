from distutils.core import setup

setup(
    name="fakerDemoLike",  # 设置包名，pip install fakerDemoLike
    version="0.0.1",    # 版本号
    description="faker demo module", # 包的描述信息
    author="likeyog",     # 作者
    py_modules = [        # 设置发布的包的文件列表，只要是要发布上线的都要把路径填上
        'fakerDemoLike.person.mobile',
        'fakerDemoLike.person.nickname',
        'fakerDemoLike.company.name',
        'fakerDemoLike.company.job'
    ]
)