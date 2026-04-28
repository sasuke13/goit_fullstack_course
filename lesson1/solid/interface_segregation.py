from abc import ABC, abstractmethod


class CodeProducer(ABC):
    @abstractmethod
    def write_code(self):
        pass


class PizzaConsumer(ABC):
    @abstractmethod
    def eat_pizza(self, slice_count):
        pass


class OfficeProgrammer(CodeProducer, PizzaConsumer):
    def __init__(self, name):
        self.name = name

    def eat_pizza(self, slice_count):
        print(f'{self.name} eat {slice_count} slice pizza!')

    def write_code(self):
        print(f'{self.name} write code!')


class RemoteProgrammer(CodeProducer):
    def write_code(self):
        print(f'{self.name} write code!')

