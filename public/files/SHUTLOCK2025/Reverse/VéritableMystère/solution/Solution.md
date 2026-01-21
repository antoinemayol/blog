# VéritableMystère - Writeup
## Étape 1 - Décompression
Après analyse du script python on se rend compte que la compression **bzip2** est utilisée. \
Ainsi avec un script (unzip.py) on peut décompresser le bytecode. (cf: step1.py)
### step1.py
```python
PhBoc=False
PhBol=print
PhBoq=True
PhBof=None
PhBoz=len
PhBoC=ord
PhBoE=input
class PhBoO:
 def __init__(PhBoD,thBzPYif):
  PhBoD.thBzPYif=thBzPYif
  PhBoD.SIWITnmd=[]
  PhBoD.gxVNoOdD=[0]*8
...
```
## Étape 2 - Déobfuscation
Le scritp précédemment obtenu est illisible car le nom des variables a été obfuscé, pour mieux comprendre le comportement du script il est essentiel de renommer les variables autant que possible. On peut commencer par les variables présentes en haut du script et aussi remettre la variable **self** dans la class. On peut également indentifier que la variable **thBzPYif** est le bytecode injecté tout à la fin du script.\
\
Ensuite, il faut comprendre que ce script est enfaite une VM et que le bytecode injecté est le code à reverse. On peut identifier l'instruction set de la VM asser rapidement.
```python
self.XsptuCKp={34:PsehBoO.PhBoe,145:PhBoO.PhBov,216:PhBoO.PhBod,205:PhBoO.PhBop,195:PhBoO.PhBoK,16:PhBoO.PhBoG,65:PhBoO.PhBoA,30:PhBoO.PhBoM,126:PhBoO.PhBoV,194:PhBoO.PhBoi,115:PhBoO.PhBoa,120:PhBoO.PhBou,166:PhBoO.PhBoQ}
```

## Étape 3 - Fonctions de la VM
Cette étape est la plus importante car elle va permettre au joueur de comprendre le fonctionnement de la VM. \
Voici les fonctions les plus importantes à identifier:
### execBytecode
C'est la fonction principale qui exécute le bytecode instruction par instruction.
```python
  def execBytecode(self):
    self.isRunning = True
    while self.isRunning:
      try:
        opCode = self.eatBytecode()
      except:
        return 1
      if(self.parseOpcode(opCode)):
        return 1

    return self.getRegister(0)
```
### eatBytecode
Cette fonction permet de récupérer le byte pointé par le pointeur d'instruction.
```python
  def eatBytecode(self):
    res = self.bytecode[self.InstructionPointer]
    self.InstructionPointer += 1
    return res
```
### getRegister
Cette fonction permet de récupérer la valeur d'un registre.
```python
  def getRegister(self, i):
    return self.registers[i]
```
### setRegister
Cette fonction permet de changer la valeur d'un registre.
```python
  def setRegister(self, i, val):
    self.registers[i] = val
```
## Étape 4 - Reconstitution de l'IS

À présent le sait que la VM récupérère des bytecodes et éxecute la fonction associée, le nombre d'argument peut être défini à l'intérieur de la fonction.
### PhBoV

La fonction suivante utilise 2 fois eatBytecode, il y a donc 2 paramètres. La valeur du registre numéro **a** et mis à la valeur **b**. \
On peut donc identifier cette fonction comme étant une fonction **MOVE**. L'opcode associé à cette fonction dans l'instruciton set est **126** (0x7e).
```python
 def PhBoV(self):
  a=self.eatBytecode()
  b=self.eatBytecode()
  self.setRegister(a,b)
```

Regardons les apparitions de cette fonctions dans le bytecode de la VM.

> d8 01 <mark>7e</mark> 00 00 41 02 01 <mark>7e</mark> 03 75 a6 02 ...

Ici on voit que la valeur **0** est mise dans le registre numéro **0** puis un peu plus loin la valeur **75** est mise dans le registre numéro **3**.
On peut donc commencer à écrire le pseudo code suivant:
```
...
MOVE r0, 0
...
MOVE r3, 75
...
```

## Étape 5 - Pseudo-code final
Après avoir trouver toute les instructions utilisées dans le bytecode on trouve un pseudo-code ressemblant au code suivant:
```
INPUT 1
MOVVAL 0 0

LODSB 2 1
MOVVAL 3 117
TEST 2 3
JZNTH 2
MOVVAL 0 1

...

LODSB 2 1
MOVVAL 3 52
TEST 2 3
JZNTH 2
MOVVAL 0 1

LODSB 2 1
MOVVAL 3 0
TEST 2 3
JZNTH 2
MOVVAL 0 1

RET

```
Le mot de passe étant vérifié caractère par caractère on peut donc récupérer les 32 caractères du mot de passe et obtenir le flag.
