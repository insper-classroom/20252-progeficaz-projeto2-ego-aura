from datetime import datetime

class Imovel:
    def __init__(self, id=None, logradouro=None, tipo_logradouro=None, bairro=None,
                 cidade=None, cep=None, tipo=None, valor=None, data_aquisicao=None):
        self.id = id
        self.logradouro = logradouro
        self.tipo_logradouro = tipo_logradouro
        self.bairro = bairro
        self.cidade = cidade
        self.cep = cep
        self.tipo = tipo
        self.valor = valor
        self.data_aquisicao = data_aquisicao or datetime.now().strftime('%Y-%m-%d')
    
    def to_dict(self):
        return {
            'id': self.id,
            'logradouro': self.logradouro,
            'tipo_logradouro': self.tipo_logradouro,
            'bairro': self.bairro,
            'cidade': self.cidade,
            'cep': self.cep,
            'tipo': self.tipo,
            'valor': self.valor,
            'data_aquisicao': self.data_aquisicao
        }
