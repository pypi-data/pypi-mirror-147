import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="maintain-website-tool",
    version="0.0.2",
    author="CSDUMMI",
    author_email="csdummi.misquality@simplelogin.co",
    description="Maintain a Website. Includes link checker.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://codeberg.org/developers/maintain-website-tool",
    project_urls={
        "Bug Tracker": "https://codeberg.org/developers/maintain-website-tool/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)",
        "Operating System :: OS Independent",
        "Development Status :: 3 - Alpha",
    ],
    package_dir={"":"src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
    entry_points={
        "console_scripts": [
            "maintain-website-tool=src.maintain_website_tool.main:main",
        ]
    }
)
