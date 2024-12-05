from setuptools import setup, find_packages

setup(
    name='bot-hokireceh',  # Nama pustaka Anda
    version='0.1.0',       # Versi awal
    description='Bot Telegram untuk komunitas Hoki Receh',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='HokiReceh',
    author_email='ads.hokireceh@gmail.com.com',
    url='https://codeberg.org/pemulungrupiah/bot-hokireceh',  # URL repositori GitHub Anda
    packages=find_packages(),
    install_requires=[
        'python-telegram-bot==20.0',
        'aiohttp==3.8.1',
        'python-dotenv==0.21.0',
        'requests==2.26.0',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
