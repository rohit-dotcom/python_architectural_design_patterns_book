from dataclasses import dataclass
from typing import NamedTuple
from collections import namedtuple
import pytest


@dataclass(frozen=True)
class student:
    name:str
    age:int

class airplane(NamedTuple):
    brand:str
    size:str

@dataclass(frozen=True)
class Money():
    currency:str
    value:int

    def __add__(self,other):
        if self.currency!=other.currency:
            raise ValueError("cannot add values of different currency")
        return Money(self.currency,self.value+other.value)

    def __sub__(self,other):
        if self.currency!=other.currency:
            raise ValueError("cannot subtract values of different currency")
        return Money(self.currency,self.value-other.value)
    
    def __mul__(self,other):
        if isinstance(other,Money):
            raise ValueError("cannot multiply currencies")
        elif isinstance(other,(int,float)):
            return Money(self.currency,self.value*other)
        else:
            raise ValueError('cannot multiply 2 differnet instances')

line=namedtuple('line',['sku','qty'])

fiver=Money('INR',5)
tenner=Money('INR',10)

def test_quality():
    assert student('rohit',33)==student('rohit',33)
    assert airplane('boeing','small')!=('airbus','large')
    assert line('small-chair','20')==line('small-chair','20')

def test_can_add_money_values_of_same_currency():
    assert fiver+fiver==tenner

def test_can_subtract_money_values_of_same_currency():
    assert tenner-fiver==fiver

def test_cannot_add_modey_of_different_currencies():
    five_inr=Money("INR",5)
    fine_dollar=Money("Dollar",5)

    with pytest.raises(ValueError):
        five_inr+fine_dollar

def test_cannot_multiply_money_values():
    with pytest.raises(ValueError):
        fiver*tenner

def test_can_multiply_money_with_scalar():
    assert fiver*5==Money('INR',25)

@dataclass(frozen=True)
class Name():
    first_name:str
    last_name:str


class Person():
    def __init__(self,name:Name):
        self.name=name

def test_harry_is_barry():
    rohit=Person(Name('Rohit','Sharma'))

    mohit=rohit

    mohit.name=Name('Mohit','Sharma')

    assert rohit==mohit