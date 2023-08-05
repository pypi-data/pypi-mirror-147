import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="spider_monitor_flow",  # 模块名称
    version="1.5",  # 当前版本
    author="simi",  # 作者
    author_email="1820407818@qq.com",  # 作者邮箱
    description="spider monitor！",  # 简短介绍
    long_description=long_description,  # 模块详细介绍
    long_description_content_type="text/markdown",  # 模块详细介绍格式
    packages=setuptools.find_packages(),  # 自动找到项目中导入的模块
    # 模块相关的元数据(更多描述信息)
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    # 依赖模块
    install_requires=[
        "pymongo",
        "similib",
        # "random_user_agent"
    ],
    python_requires=">=3",

)
