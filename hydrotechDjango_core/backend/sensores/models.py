from django.db import models


class SensorComponente(models.Model):
    """
    Component (interface comum do padrão Composite).
    Nó folha (Sensor) e nó composto (SensorGroup) compartilham este contrato,
    permitindo tratar a árvore de sensores de forma uniforme.

    A estrutura é genérica: os sensores podem ser alocados em qualquer lugar
    (rio, estação, município, etc.), não apenas em rios.
    """

    nome = models.CharField(max_length=100)
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    # ---------- Métodos da interface Composite ----------

    def adicionar(self, componente):
        """Adiciona um filho. Por padrão, folhas lançam erro."""
        raise NotImplementedError(
            'Operação de composição não suportada por este componente.'
        )

    def remover(self, componente):
        """Remove um filho. Por padrão, folhas lançam erro."""
        raise NotImplementedError(
            'Operação de composição não suportada por este componente.'
        )

    def get_sensores(self):
        """
        Retorna a lista de sensores (folhas) alcançáveis a partir deste
        componente. Em uma folha retorna [self]; em um composite percorre
        toda a subárvore.
        """
        raise NotImplementedError(
            'Operação de travessia não implementada por este componente.'
        )

    def get_nome(self):
        return self.nome

    def get_tipo(self):
        """Tipo do componente: 'sensor' (folha) ou 'grupo' (composite)."""
        return 'componente'

    def __str__(self):
        return self.get_nome()


class Sensor(SensorComponente):
    """Leaf: um sensor individual, sem filhos."""

    TIPOS_CHOICES = [
        ('nivel_agua', 'Nível da Água'),
        ('vazao', 'Vazão'),
        ('velocidade', 'Velocidade da Corrente'),
        ('turbidez', 'Turbidez'),
        ('ph', 'pH'),
        ('temperatura', 'Temperatura'),
        ('pluviometria', 'Pluviometria'),
        ('outro', 'Outro'),
    ]

    STATUS_CHOICES = [
        ('ativo', 'Ativo'),
        ('inativo', 'Inativo'),
        ('manutencao', 'Manutenção'),
    ]

    tipo = models.CharField(max_length=50, choices=TIPOS_CHOICES)
    unidade = models.CharField(max_length=20)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='ativo')
    modelo = models.CharField(max_length=100, blank=True)

    # Localização genérica: sensor pode estar fora de um rio no futuro.
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    rio = models.ForeignKey(
        'rios.Rios',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='sensores',
    )

    # Vínculo com o composite pai (pode ser raiz caso vazio).
    grupo = models.ForeignKey(
        'SensorGroup',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='sensores',
    )

    # ----------------------------------------------------------
    # Interface Composite (nó folha)
    # ----------------------------------------------------------

    def adicionar(self, componente):
        raise TypeError('Sensor é um nó folha e não pode conter filhos.')

    def remover(self, componente):
        raise TypeError('Sensor é um nó folha e não possui filhos.')

    def get_sensores(self):
        return [self]

    def get_tipo(self):
        return 'sensor'

    def get_ultimo_valor(self):
        ultima = self.leituras.order_by('-criado_em').first()
        return ultima.valor if ultima else None


class SensorGroup(SensorComponente):
    """Composite: agrupa sensores e/ou outros grupos, formando uma árvore."""

    descricao = models.TextField(blank=True)

    # Endereço/localização genérica — o grupo pode representar qualquer lugar.
    endereco = models.CharField(max_length=200, blank=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)

    # Vínculo opcional com um rio. Fica em branco para locais fora de rio.
    rio = models.ForeignKey(
        'rios.Rios',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='grupos_sensores',
    )

    # Auto-referência para formar subárvores (Composite recursivo).
    parent = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='subgrupos',
    )

    # ----------------------------------------------------------
    # Interface Composite (nó composto)
    # ----------------------------------------------------------

    def adicionar(self, componente):
        if isinstance(componente, Sensor):
            componente.grupo = self
            componente.save()
        elif isinstance(componente, SensorGroup):
            componente.parent = self
            componente.save()
        else:
            raise TypeError(
                'Apenas Sensor (folha) ou SensorGroup (composite) podem ser adicionados.'
            )

    def remover(self, componente):
        if isinstance(componente, Sensor) and componente.grupo_id == self.pk:
            componente.grupo = None
            componente.save()
        elif isinstance(componente, SensorGroup) and componente.parent_id == self.pk:
            componente.parent = None
            componente.save()
        else:
            raise ValueError('Componente não pertence a este grupo.')

    def get_sensores(self):
        sensores = list(self.sensores.all())
        for subgrupo in self.subgrupos.all():
            sensores.extend(subgrupo.get_sensores())
        return sensores

    def get_tipo(self):
        return 'grupo'

    def get_total_sensores(self):
        return len(self.get_sensores())

    def get_leituras_agregadas(self, limite=None):
        """
        Agrega as leituras de todos os sensores da subárvore.
        Demonstra o uso uniforme da interface Composite.
        """
        leituras = []
        for sensor in self.get_sensores():
            leituras.extend(sensor.leituras.all())
        leituras.sort(key=lambda l: l.criado_em, reverse=True)
        return leituras[:limite] if limite else leituras


class Leitura(models.Model):
    """Registro de medição de um sensor (nó folha)."""

    sensor = models.ForeignKey(
        Sensor,
        on_delete=models.CASCADE,
        related_name='leituras',
    )
    valor = models.FloatField()
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-criado_em']

    def __str__(self):
        return f'{self.sensor.nome}: {self.valor} {self.sensor.unidade}'