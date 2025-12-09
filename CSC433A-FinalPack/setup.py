from setuptools import setup, find_packages

setup(
    name="cyber-defense-suite-optionA",
    version="0.1.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "watchdog",
        "cryptography"
    ],
    entry_points={
        "console_scripts": [
            "fim-daemon=fim_daemon.main:main"
        ]
    },
)
