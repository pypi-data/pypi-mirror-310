from datetime import date
from dataclasses import dataclass
from getinstance import InstanceManager

@dataclass
class Meta():
    id: str
    refresh_date: date


class Country:
    instances = InstanceManager()

    def __init__(self, name: str, metadata: Meta):
        self.name = name
        self.meta = metadata

    def hello(self, username):
        print(f'hello, {username} from {self.name}')


def test_countries(mocker):
    spy = mocker.spy(Country, 'hello')

    au = Country('Australia', Meta('AU', date.today()))
    ru = Country('Russia', Meta('RU', date.today()))

    assert set(Country.instances.all()) == set([au, ru])
    assert Country.instances.get(name='Australia') == au

    Country.instances.filter(name='Russia').hello(username='Alice')

    assert ru.hello.call_count == 1

    Country.instances.filter(name='Russia').name = 'Russian Federation'

    assert ru.name == 'Russian Federation'

    Country.instances.filter(name='Russian Federation').hello(username='Alisa')

    assert ru.hello.call_count == 2

    assert set(Country.instances.filter(meta__id='AU')) == set([au])
