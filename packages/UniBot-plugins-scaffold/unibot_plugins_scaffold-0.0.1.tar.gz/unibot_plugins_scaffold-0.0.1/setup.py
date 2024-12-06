from setuptools import setup, find_packages

setup(
    name='UniBot-plugins-scaffold',
    version='0.0.1',
    author='PYmili',
    author_email='mc2005wj@163.com',
    description='UniBot的插件脚手架',
    long_description=open('README.md', encoding="utf-8").read(),
    long_description_content_type='text/markdown',
    url='https://github.com/PYmili/UniBot-plugins-scaffold',
    packages=find_packages(),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Programming Language :: Python :: 3.13',
    ],
    keywords='UniBot plugins',
    install_requires=[
        "art==6.3",
        "colorama==0.4.6",
        "loguru==0.7.2",
        "setuptools==75.6.0",
        "win32-setctime==1.1.0"
    ],  # 这里可以添加项目依赖
    entry_points={
        'console_scripts': [
            'unibot-ps=command:access',  # 这里的'unibot-ps'是命令行工具的名称，指定了入口函数
        ],
    },
    python_requires='>=3.9',  # 指定支持的Python版本
)
