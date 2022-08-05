import setuptools
import sys
import os

# versionedModule = {}
# versionedModule['urllib'] = 'urllib'
# if sys.version_info.major < 3:
#     versionedModule['urllib'] = 'urllib2'
# long_description = ""

if os.path.isfile("readme.md"):
    with open("readme.md", "r") as fh:
        long_description = fh.read()

install_requires = []

if os.path.isfile("requirements.txt"):
    with open("requirements.txt", "r") as ins:
        for rawL in ins:
            line = rawL.strip()
            if len(line) < 1:
                continue
            install_requires.append(line)

description = (
    "With other multi-timezone clocks you can see where"
    " has what time, but with world_clock you can see who! You can add a"
    " person's name or any custom note to any clock, and even add more than"
    " one with the same timezone. Save to the cloud if you have a working"
    " Nextcloud/profile/ or ownCloud/profile/ directory in your user"
    " profile!"
)

setuptools.setup(
    name='world_clock',
    version='1.0.0',
    description=description,
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Programming Language :: Python :: 3',
        ('License :: OSI Approved ::'
         ' GNU General Public License v3 or later (GPLv3+)'),
        'Operating System :: POSIX :: Linux',
        'Topic :: Office/Business :: Scheduling',
    ],
    keywords='python world clocks timezones time zone calculator',
    url="https://github.com/poikilos/world_clock",
    author="Jake Gustafson",
    author_email='7557867+poikilos@users.noreply.github.com',
    license='GPLv3+',
    # packages=setuptools.find_packages(),
    packages=['worldclocktk'],
    include_package_data=True,  # look for MANIFEST.in
    # scripts=['example'] ,
    # See <https://stackoverflow.com/questions/27784271/
    # how-can-i-use-setuptools-to-generate-a-console-scripts-entry-
    # point-which-calls>
    entry_points={
        'console_scripts': ['world_clock=worldclocktk:main'],
    },
    install_requires=install_requires,
    #     versionedModule['urllib'],
    # ^ "ERROR: Could not find a version that satisfies the requirement urllib (from nopackage) (from versions: none)
    # ERROR: No matching distribution found for urllib"
    test_suite='nose.collector',
    tests_require=['nose', 'nose-cover3'],
    zip_safe=False, # It can't run zipped due to needing data files.
 )
