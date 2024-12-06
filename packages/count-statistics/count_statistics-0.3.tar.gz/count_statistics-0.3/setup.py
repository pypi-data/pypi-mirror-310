from setuptools import setup, find_packages

setup(
    name='count_statistics',
    version='0.3',
    package=find_packages(),
    install_requires=[
        'django',
    ],
    description='A library for counting user bookings.',
    author='Jocelyn Chen',
    author_email='cjl1759648974@outlook.com',
    url='https://github.com/jocelyncjl/airline-booking.git',
)