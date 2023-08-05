from setuptools import find_packages, setup

setup(
    name="musma_ray",
    packages=find_packages(where=".", include="ray_release"),
    version="1.0.0.1",
    author="moey920",
    author_email='moey920@musma.net',
    description="for rllib tf2 export_policy_model, fix fcnet version",
    url="https://velog.io/@moey920",
    install_requires=["ray>=1.9", "click", "anyscale", "boto3", "freezegun"],
)
