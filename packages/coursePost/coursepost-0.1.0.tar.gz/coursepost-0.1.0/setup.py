from setuptools import setup, find_packages

setup(
    name="coursePost",
    version="0.1.0",
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'coursePost=coursePost:main',
        ],
    },
    install_requires=[
        # 列出你的依赖包
    ],
    author="yuxi-ovo",
    author_email="2896402717@qq.com",
    description="Crawl the schedule",
    license="MIT",
    keywords="python course",
    url="https://github.com/CourseTool/course-post",
)
