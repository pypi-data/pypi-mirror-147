import sys
import os
import threading
import datetime
import time
import traceback
from ..core import objeto

class Operacao(objeto.Objeto):
  def __init__(self, **atributos):
    super().__init__(**atributos)
    
    self.set('trabalhadores', {})
    self.set('id', 0)

    if 'processos' not in atributos:
      self.set('processos', 2)

    if 'itensPorProcessos' not in atributos:
      self.set('itensPorProcessos', 100)

  def _iniciar(self, **atributos):
    return self.mensagemErro(mensagem = 'Metodo iniciar nao implementado.', codigo = 'OPE-0001')

  def _processar(self, **atributos):
    return self.mensagemErro(mensagem = 'Metodo coletar nao implementado.', codigo = 'OPE-0001')

  def __informarFinalizacao(self):
    ativos = 0

    for i in self.get('trabalhadores'):
      if self.get('trabalhadores').get(i).get('thread').is_alive():
        ativos += 1

    if ativos == 0:
      self.set('situacao', {'mensagem' : 'Concluido.'})

  def __processar(self, id):
    termino = None
    trabalhador = self.get('trabalhadores').get(id)
    trabalhador['mensagem'] = 'Iniciando...'
    trabalhador.get('tempo')['inicio'] = datetime.datetime.now()
   
    try:
      continuar = True
      ret = None

      while continuar:
        ret = self.__retornarListaParaProcessamento()
        continuar = ret.get('sucesso')

        if continuar:
          lista = ret.get('objeto')
          itens = len(lista)
          continuar = itens > 0

          if continuar:
            trabalhador.get('lista')['emProcessamento'] = itens
            retorno = self._processar(lista = lista, id = id)

            if retorno.get('sucesso') == False:
              trabalhador['mensagem'] = retorno.get('mensagem')
              trabalhador['detalhe'] = retorno.get('detalhe')
              trabalhador['sucesso'] = False
              continuar = False

            trabalhador.get('lista')['processadas'] = trabalhador.get('lista').get('processadas') + itens
            trabalhador.get('lista')['emProcessamento'] = 0
          else:
            trabalhador['sucesso'] = True
        else:
          trabalhador['mensagem'] = ret.get('mensagem')
          trabalhador['detalhe'] = ret.get('detalhe')
    except Exception as e:
      trabalhador['mensagem'] = 'Erro durante a operacao.'
      trabalhador['detalhe'] = traceback.format_exc()

    trabalhador.get('tempo')['termino'] = datetime.datetime.now()

    self.__informarFinalizacao()

  def __retornarListaParaProcessamento(self):
    retorno = None
    lock = threading.Lock()

    try:
      lock.acquire()
      quantidade = self.get('itensPorProcessos')
      lista = self.get('lista')
      retorno = self.mensagemSucesso(objeto = lista[0:quantidade])
      self.set('lista', lista[quantidade:])
    except Exception as e:
      retorno = self.mensagemErro(mensagem = 'Falha ao retornar a lista para processamento.', detalhe = traceback.format_exc(), codigo = 'OPE-0005')
    finally:
      if lock.locked():
        lock.release()

    return retorno

  def incrementarContador(self):
    return self.__contador(1)

  def decrementarContador(self):
    return self.__contador(-1)

  def __contador(self, valor):
    retorno = None
    l = threading.Lock()

    try:
      l.acquire()
      self.set('ativos', self.get('ativos') + valor)
      retorno = self.mensagemSucesso()
    except Exception as e:
      retorno = self.mensagemErro(mensagem = 'Falha ao processar o contador.', detalhe = traceback.format_exc(), codigo = 'OPE-0004')
    finally:
      if l.locked():
        l.release()

    return retorno

  def situacao(self):
    situacao = {'situacao' : self.get('situacao'), 'trabalhadores' : {}}
    processados = 0
    emProcessamento = 0
    total = self.get('totalParaProcessar', 0)

    for i in self.get('trabalhadores'):
      c = self.get('trabalhadores').get(i)
      t = {}
      t['ativo'] = c.get('thread').is_alive()
      t['lista'] = c.get('lista')
      t['tempo'] = c.get('tempo')
      t['mensagem'] = {'mensagem' : c.get('mensagem'), 'detalhe' : c.get('detalhe')}
      situacao.get('trabalhadores')[i] = t
      processados += c.get('lista').get('processadas')
      emProcessamento += c.get('lista').get('emProcessamento')

    percentual = 0

    if total > 0:
      percentual = (processados / total) * 100

    situacao['processamento'] = {'total' : total, 'processados' : processados, 'emProcessamento' : emProcessamento, 'percentualConcluido' : percentual}

    return situacao

  def __preparar(self, **atributos):
    self.get('trabalhadores').clear()

  def executar(self, **atributos):
    try:
      self.__preparar(**atributos)
      retorno = self._iniciar(**atributos)

      if retorno.get('sucesso'):
        lista = retorno.get('objeto')

        if lista == None:
          self.set('situacao', {'mensagem' : 'Atributo "lista" nao encontrado apos a inicializacao.', 'detalhe' : ''})
        else:
          self.set('lista', lista)
          self.set('totalParaProcessar', len(lista))
          processos = self.get('processos')
          trabalhadores = self.get('trabalhadores')
          trabalhadores.clear()
          trabalhadoresId = 0

          while trabalhadoresId < processos:
            trabalhadores[trabalhadoresId] = {'id' : trabalhadoresId, 'sucesso' : False, 'mensagem' : '', 'detalhe' : '', 'lista' : {'processadas' : 0, 'emProcessamento' : 0}, 'tempo' : {'inicio' : None, 'termino' : None}, 'thread' : threading.Thread(target = self.__processar, args = (trabalhadoresId, ))}
            trabalhadores.get(trabalhadoresId).get('thread').start()
            trabalhadoresId += 1

          if atributos.get('executarEmSegundoPlano', True) == False:
            for i in trabalhadores:
              trabalhadores.get(i).get('thread').join()
          else:
            self.set('situacao', {'mensagem' : 'Atividades iniciadas.', 'detalhe' : ''})
      else:
        self.set('situacao', {'mensagem' : retorno.get('mensagem'), 'detalhe' : retorno.get('detalhe')})
    except Exception as e:
      self.set('situacao', {'mensagem' : 'Erro durante a execucao.', 'detalhe' : traceback.format_exc()})

class Montagem(objeto.Objeto):
  def __init__(self, **atributos):
    super().__init__(**atributos)
    self.set('operacoes', {'itens' : {}, 'ordem' : []})
    self.set('situacao', self.__templateSituacao())

  def __templateSituacao(self):
    return {'mensagem' : '', 'ativo' : False, 'sucesso' : False, 'operacoes' : {'itens' : [], 'corrente' : '', 'concluido' : [], 'progresso' : ''}}

  def adicionar(self, **atributos):
    retorno = None

    nome = atributos.get('nome', None)
    operacao = atributos.get('operacao', None)

    if operacao == None:
      retorno = self.mensagemErro(mensagem = 'Operacao nao informado.', codigo = 'OPE-0006')
    else:
      if nome == None:
        retorno = self.mensagemErro(mensagem = 'Nome nao informado.', codigo = 'OPE-0007')
      else:
        if isinstance(operacao, Operacao):
          self.get('operacoes').get('itens')[nome] = operacao
          self.get('operacoes').get('ordem').append(nome)
          retorno = self.mensagemSucesso(mensagem = 'Operacao {0} adicionada com sucesso.'.format(nome))
        else:
          retorno = self.mensagemErro(mensagem = 'Operacao informada nao e um objeto da classe Operacao.', codigo = 'OPE-0008')

    return retorno

  def remover(self, **atributos):
    nome = atributos.get('nome')
    ordem = atributos.get('ordem')
    retorno = None

    if nome == None and posicao == None:
      retorno = self.mensagemErro(mensagem = 'Informar nome ou posicao da operacao para ser removida.', codigo = 'OPE-0009')
    else:
      operacoes = self.get('operacoes')

      if nome:
        if nome in operacoes.get('itens'):
          del operacoes.get('itens')[nome]

          if nome in operacoes.get('ordem'):
            operacoes.get('ordem').remove(nome)

          
          retorno = self.mensagemSucesso(mensagem = 'Operacao {0} removida com sucesso.'.format(nome))
        else:
          retorno = self.mensagemErro(mensagem = 'Operacao {0} removida com sucesso.'.format(nome), codigo = 'OPE-0010')
      else:
        if posicao >= 0 and posicao < len(operacoes.get('ordem')):
          nome = operacoes.get('ordem').pop(posicao)

          if nome in operacoes.get('itens'):
            del operacoes.get('itens')[nome]
          retorno = self.mensagemSucesso(mensagem = 'Operacao {0} removida com sucesso.'.format(nome))
        else:
          retorno = self.mensagemErro(mensagem = 'Operacao {0} removida com sucesso.'.format(nome), codigo = 'OPE-0010')

    return retorno

  def __iniciar(self, **atributos):
    operacoes = self.get('operacoes')
    situacao = self.get('situacao')

    if len(operacoes.get('ordem')) == 0:
      situacao['mensagem'] = 'Nao existe opereacoes para serem executadas.'
    else:
      self.set('situacao', self.__templateSituacao())
      situacao = self.get('situacao')
      situacao['mensagem'] = 'Preparando...'
      progressoTotal = 0
      progressoCorrente = 0

      for nome in operacoes.get('ordem'):
        situacao.get('operacoes').get('itens').append(nome)
        progressoTotal += 1

      situacao.get('operacoes')['progresso'] = '{0}/{1}'.format(progressoCorrente, progressoTotal)
      situacao['ativo'] = True

      for nome in situacao.get('operacoes').get('itens'):
        situacao['mensagem'] = 'Operacao corrente {0}'.format(nome)
        situacao.get('operacoes')['corrente'] = nome
        operacao = operacoes.get('itens').get(nome)

        if operacao != None:
          atributos['executarEmSegundoPlano'] = False
          operacao.executar(**atributos)
          sucesso = True

          for trabalhadorId in operacao.get('trabalhadores'):
            if operacao.get('trabalhadores').get(trabalhadorId).get('sucesso') == False:
              situacao['mensagem'] = 'Falha na operacao {0}, atividade encerrada. Erro: {1}.'.format(nome, operacao.get('trabalhadores').get(trabalhadorId).get('mensagem'))
              sucesso = False
              break

          if sucesso:
            progressoCorrente += 1
            situacao.get('operacoes').get('concluido').append(nome)
            situacao.get('operacoes')['progresso'] = '{0}/{1}'.format(progressoCorrente, progressoTotal)
          else:
            break
        else:
          situacao['mensagem'] = 'Atividade abortada, operacao {0} nao encontrada.'.format(nome)
          break

      situacao['ativo'] = False
      situacao['sucesso'] = progressoCorrente == progressoTotal
      situacao.get('operacoes')['corrente'] = ''

      if progressoCorrente == progressoTotal:
        situacao['mensagem'] = 'Operacoes concluidas com sucesso.'
      else:
        situacao['mensagem'] = 'Falha na operacao.'

  def executar(self, **atributos):
    retorno = None

    try:
      executarEmSegundoPlano = atributos.get('executarEmSegundoPlano', True)
      t = threading.Thread(target = self.__iniciar, kwargs = atributos)
      t.start()

      if executarEmSegundoPlano == False:
        t.join()
        retorno = self.mensagemSucesso(mensagem = 'Processo concluido.')
      else:
        retorno = self.mensagemSucesso(mensagem = 'Processo iniciado.')
    except Exception as e:
      retorno = self.mensagemErro(mensagem = 'Falha ao iniciar o processo.', detalhe = traceback.format_exc(), codigo = 'OPE-0012')

    return retorno