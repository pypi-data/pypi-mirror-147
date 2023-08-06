import os
import sys
import threading
from . import objeto

class Terminal (objeto.Objeto):
  def __init__(self, **atributos):
    super().__init__(**atributos)

    if self.get('log') == None:
      self.set('log', 'log')

    if self.get('cnf') == None:
      self.set('cnf', 'cnf')

  def iniciar(self):
    pass