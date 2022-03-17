from experta import *

# Função auxiliar para fazer perguntas de S/N
def make_question(text):
    while True:
        ans = input(text + ' ').upper()
        if ans in {'S', 'SIM', 'Y', 'YES'}:
            return True
        if ans in {'N', 'NÃO', 'NAO', 'NO'}:
            return False
        print('Responda SIM ou NAO / YES or NO')   

# Tipos de fatos
class Feature(Fact):
    pass

class Creature(Fact):
    pass

# Engine de Conhecimento
class ClassifyAnimalia(KnowledgeEngine):
    @DefFacts()
    def begin(self):
        yield Fact(action='start')

    # Possui coluna vertebral?
    @Rule(Fact(action='start'), NOT(Feature(has_spine=W())))
    def ask_spine(self):
        self.declare(Feature(has_spine=make_question('Esse animal possui coluna vertebral?')))

    ################### INVERTEBRADOS #########################################################

    # Possui pernas?
    @Rule(AND(Feature(has_spine=False), NOT(Feature(has_legs=W()))))
    def ask_legs(self):
        self.declare(Feature(has_legs=make_question('Esse animal possui pernas?')))

    # Possui 6 pernas?
    @Rule(AND(Feature(has_legs=True), NOT(Feature(has_legs_6=W()))))
    def ask_leg_amount_6(self):
        self.declare(Feature(has_legs_6=make_question('Esse animal possui 6 pernas?')))

    # Possui 8 pernas?
    @Rule(AND(Feature(has_legs_6=False), NOT(Feature(has_legs_8=W()))))
    def ask_leg_amount_8(self):
        self.declare(Feature(has_legs_8=make_question('Esse animal possui 8 pernas?')))

    # Possui manto ou casco?
    @Rule(AND(Feature(has_legs=False), NOT(Feature(has_shell=W()))))
    def ask_shell(self):
        self.declare(Feature(has_shell=make_question('Esse animal possui manto (epiderme esclerotizada) ou casco?')))

    # Possui corpo gelatinoso?
    @Rule(AND(Feature(has_shell=False), NOT(Feature(has_jelly_body=W()))))
    def ask_jelly_body(self):
        self.declare(Feature(has_jelly_body=make_question('Esse animal possui corpo gelatinoso?')))

    # Possui pele espinhosa?
    @Rule(AND(Feature(has_jelly_body=False), NOT(Feature(has_spike_skin=W()))))
    def ask_spike_skin(self):
        self.declare(Feature(has_spike_skin=make_question('Esse animal possui pele espinhosa?')))

    # Possui corpo segmentado? 
    @Rule(AND(Feature(has_spike_skin=False), NOT(Feature(has_segmented_body=W()))))
    def ask_segmented_body(self):
        self.declare(Feature(has_segmented_body=make_question('Esse animal possui o corpo segmentado?')))

    # Resposta: É um inseto
    @Rule(AND(Feature(has_legs_6=True), NOT(Creature(name=W()))))
    def insect(self):
        self.declare(Creature(name='Inseto'))

    # Resposta: É um aracnídeo
    @Rule(AND(Feature(has_legs_8=True), NOT(Creature(name=W()))))
    def arachnid(self):
        self.declare(Creature(name='Aracnídeo'))

    # Resposta: É um miriápode
    @Rule(AND(Feature(has_legs_8=False), NOT(Creature(name=W()))))
    def myriapoda(self):
        self.declare(Creature(name='Miriápode (artrópode com muitas pernas)'))

    # Resposta: É um molusco
    @Rule(AND(Feature(has_shell=True), NOT(Creature(name=W()))))
    def mollusk(self):
        self.declare(Creature(name='Molusco'))

    # Resposta: É um celenterado
    @Rule(AND(Feature(has_jelly_body=True), NOT(Creature(name=W()))))
    def celenterate(self):
        self.declare(Creature(name='Celenterado (como águas-vivas)'))

    # Resposta: É um equinodermo
    @Rule(AND(Feature(has_spike_skin=True), NOT(Creature(name=W()))))
    def echinoderm(self):
        self.declare(Creature(name='Equinodermo (como estrelas do mar)'))

    # Resposta: É um anelídeo
    @Rule(AND(Feature(has_segmented_body=True), NOT(Creature(name=W()))))
    def annelid(self):
        self.declare(Creature(name='Anelídeo'))

    ################### VERTEBRADOS #########################################################

    # Possui asas?
    @Rule(AND(Feature(has_spine=True), NOT(Feature(has_wings=W()))))
    def ask_wings(self):
        self.declare(Feature(has_wings=make_question('Esse animal possui asas?')))

    # Vive só na água?
    @Rule(AND(Feature(has_wings=False), NOT(Feature(aquatic=W()))))
    def ask_aquatic(self):
        self.declare(Feature(aquatic=make_question('Esse animal vive somente na água?')))

    # Vive parcialmente na água?
    @Rule(AND(Feature(aquatic=False), NOT(Feature(partial_aquatic=W()))))
    def ask_partial_aquatic(self):
        self.declare(Feature(partial_aquatic=make_question('Esse animal pode viver na água por algum tempo?')))

    # Possui escamas?
    @Rule(AND(Feature(partial_aquatic=False), NOT(Feature(has_scales=W()))))
    def ask_scales(self):
        self.declare(Feature(has_scales=make_question('Esse animal tem escamas?')))

    # Possui pelos?
    @Rule(AND(Feature(has_scales=False), NOT(Feature(has_fur=W()))))
    def ask_fur(self):
        self.declare(Feature(has_fur=make_question('Esse animal tem pelos?')))

    # Resposta: É uma ave
    @Rule(AND(Feature(has_wings=True), NOT(Creature(name=W()))))
    def bird(self):
        self.declare(Creature(name='Ave'))

    # Resposta: É um peixe ósseo (vertebrado)
    @Rule(AND(Feature(aquatic=True), NOT(Creature(name=W()))))
    def fish(self):
        self.declare(Creature(name='Peixe Ósseo'))

    # Resposta: É um anfíbio
    @Rule(AND(Feature(partial_aquatic=True), NOT(Creature(name=W()))))
    def amphibian(self):
        self.declare(Creature(name='Anfíbio'))

    # Resposta: É um réptil
    @Rule(AND(Feature(has_scales=True), NOT(Creature(name=W()))))
    def reptile(self):
        self.declare(Creature(name='Réptil'))

    # Reposta: É um mamífero
    @Rule(AND(Feature(has_fur=True), NOT(Creature(name=W()))))
    def mammal(self):
        self.declare(Creature(name='Mamífero'))

    ################### REGRAS DO SISTEMA #########################################################

    # Casos não classificados
    # Poderia, caso houvesse tempo, ser utilizado para extensões em tempo de execução
    @Rule(OR(Feature(has_fur=False), Feature(has_segmented_body=False)))
    def tell_unknown(self):
        print('Não conheço essa criatura.')
        self.declare(Fact(end=True))

    # Retorna nome da criatura
    @Rule(Creature(name=MATCH.name))
    def tell_creature(self, name):
        print("Sua criatura é um(a) %s!" % (name))
        self.declare(Fact(end=True))

    # Sugere jogar novamente
    @Rule(Fact(end=True))
    def ask_retry(self):
        self.declare(Fact(retry=make_question('Isso foi divertido. Quer jogar de novo?')))

    # Reseta sistema para o estado incial
    @Rule(Fact(retry=True))
    def restart(self):
        engine.reset()
        engine.run()

engine = ClassifyAnimalia()
engine.reset()  # Prepare the engine for the execution.
engine.run()  # Run it!

