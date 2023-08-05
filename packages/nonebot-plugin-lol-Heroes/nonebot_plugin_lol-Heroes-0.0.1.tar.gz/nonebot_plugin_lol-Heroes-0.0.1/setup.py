import setuptools

with open("README.md", "r", encoding='utf-8') as fh:
    long_description = fh.read()

setuptools.setup(
    name="nonebot_plugin_lol-Heroes",
    version="0.0.1",
    author="Torres-圣君",
    author_email="2653644677@qq.com",
    description="基于NoneBot2实现，获取LOL英雄的背景故事和图片",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/cjladmin/lolheroes",
    license='MIT',
    install_requires=[
        "requests>=2.26.0",
        "nonebot2",
        "nonebot-adapter-onebot"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: MIT License"
    ]
)