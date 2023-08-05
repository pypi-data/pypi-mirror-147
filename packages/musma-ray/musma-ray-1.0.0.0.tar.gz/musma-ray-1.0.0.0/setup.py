from setuptools import setup, find_packages

setup(
    name='musma-ray', # 패키지 명

    version='1.0.0.0',

    description='Test Package',

    author='moey920',

    author_email='moey920@musma.net',

    url='https://velog.io/@moey920',

    license='Apache License',

    python_requires='>=3',

    install_requires=[], # 패키지 사용을 위해 필요한 추가 설치 패키지

    packages=find_packages(), # 패키지가 들어있는 폴더들
)