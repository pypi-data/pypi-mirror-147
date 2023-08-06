import os
import sys
import io
import traceback
import threading

class Objeto():
  def __init__(self, **atributos):
    self.__atributos = {}

    for k in atributos:
      self.__atributos[k] = atributos.get(k)

    if os.name == 'nt':
      self.__atributos['separador'] = '\\'
    else:
      self.__atributos['separador'] = '/'

  def set(self, nome, valor):
    self.__atributos[nome] = valor

  def get(self, nome, valor = None):
    return self.__atributos.get(nome, valor)

  def mensagemErro(self, **atributos):
    atributos['tipo'] = 'erro'
    return self.__mensagem(**atributos)

  def mensagemSucesso(self, **atributos):
    atributos['tipo'] = 'informativo'
    return self.__mensagem(**atributos)

  def __mensagem(self, **atributos):
    return {'tipo' : atributos.get('tipo', 'informativo'), 'mensagem' : atributos.get('mensagem', 'Nao informado.'), 'detalhe' : atributos.get('detalhe', 'Nao informado.'), 'objeto' : atributos.get('objeto', None), 'sucesso' : atributos.get('tipo', 'info') != 'erro', 'codigo' : atributos.get('codigo', 'SCS-0000')}

  def criarDiretorios(self, **atributos):
    retorno = None
    diretorio = atributos.get('diretorio')

    if os.path.exists(diretorio) == False:
      try:
        os.makedirs(diretorio)
        retorno = self.mensagemSucesso(mensagem = 'Diretorio criado com sucesso.')
      except:
        retorno = self.mensagemErro(mensagem = 'Falha ao criar o diretorio {0}.'.format(diretorio), detalhe = traceback.format_exc(), codigo = 'ARQ-0005')
    else:
      retorno = self.mensagemSucesso(mensagem = 'Diretorio ja existe.')

    return retorno

  def abrirArquivo(self, **atributos):
    retorno = None
    nomeDoArquivo = atributos.get('arquivo', None)
    modoDeLeitura = atributos.get('modo', 'r')
    criarArquivoCasoNaoExista = atributos.get('criar', False)

    if nomeDoArquivo:
      if os.path.exists(nomeDoArquivo) or criarArquivoCasoNaoExista:
        if os.path.exists(nomeDoArquivo) == False:
          modoDeLeitura = 'a+'

        partes = nomeDoArquivo.split(self.get('separador'))

        if len(partes) > 1:
          partes = partes[:-1]
          diretorio = ''

          if partes[0] == '':
            diretorio = self.get('separador')
            diretorio.pop(0)

          limite = len(partes)
          idx = 0

          while idx < limite:
            diretorio += partes[idx]
            idx += 1

            if idx < limite:
              diretorio += self.get('separador')

          retorno = self.criarDiretorios(diretorio = diretorio)
        else:
          retorno = self.mensagemSucesso()

        if retorno.get('sucesso'):
          try:
            retorno = self.mensagemSucesso(mensagem = 'Arquivo aberto com sucesso.', objeto = open(nomeDoArquivo, modoDeLeitura))
          except Exception as e:
            retorno = self.mensagemErro(mensagem = 'Falha ao abrir o arquivo {0}.'.format(nomeDoArquivo), detalhe = traceback.format_exc(), codigo = 'ARQ-0666')
      else:
        retorno = self.mensagemErro(mensagem = 'Arquivo nao existe.', codigo = 'ARQ-0002')
    else:
      retorno = self.mensagemErro(mensagem = 'Nao informado o arquivo para abrir.', codigo = 'ARQ-0001')

    return retorno

  def fecharArquivo(self, **atributos):
    retorno = None
    arquivo = atributos.get('arquivo')

    if arquivo == None:
      retorno = self.mensagemErro(mensagem = 'Nao informado o arquivo para ser fechado.', codigo = 'ARQ-0003')
    else:
      if isinstance(arquivo, io.IOBase):
        try:
          arquivo.close()
          retorno = self.mensagemSucesso(mensagem = 'Arquivo fechado com sucesso.')
        except:
          retorno = self.mensagemErro(mensagem = 'Falha ao fechar o arquivo {0}.'.format(arquivo.name), detalhe = traceback.format_exc(), codigo = 'ARQ-0006')
      else:
        retorno = self.mensagemErro(mensagem = 'Atributo arquivo nao e da classe io.IOBase.', codigo = 'ARQ-0004')

    return retorno

  def gravarArquivo(self, **atributos):
    retorno = None

    if atributos.get('sincronizado', False):
      l = threading.Lock()

      try:
        l.acquire()
        retorno = self.abrirArquivo(arquivo = atributos.get('arquivo'), modo = 'a+', criar = True)

        if retorno.get('sucesso'):
          retorno.get('objeto').write(atributos.get('dados'))
          retorno = self.fecharArquivo(arquivo = retorno.get('objeto'))
      except Exception as e:
        retorno = self.mensagemErro(mensagem = 'Falha ao solicitar bloqueio do arquivo.', codigo = 'USR-0002')
      finally:
        if l.locked():
          l.release()
    else:
      retorno = self.abrirArquivo(arquivo = atributos.get('arquivo'), modo = 'a+', criar = True)

      if retorno.get('sucesso'):
        retorno.get('objeto').write(atributos.get('dados'))
        retorno = self.fecharArquivo(arquivo = retorno.get('objeto'))

    return retorno

  def versao(self):
    return "0.1.0"
