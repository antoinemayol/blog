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
  PhBoD.mzcTzCFm=[0]*8
  PhBoD.WFeIUlGh=0
  PhBoD.IKaeEzxt=0
  PhBoD.XsptuCKp={34:PhBoO.PhBoe,145:PhBoO.PhBov,216:PhBoO.PhBod,205:PhBoO.PhBop,195:PhBoO.PhBoK,16:PhBoO.PhBoG,65:PhBoO.PhBoA,30:PhBoO.PhBoM,126:PhBoO.PhBoV,194:PhBoO.PhBoi,115:PhBoO.PhBoa,120:PhBoO.PhBou,166:PhBoO.PhBoQ}
  PhBoD.fufkLOmW=PhBoc
  if not PhBoD.PhBoW():
   PhBol("Mot de passe valide !")
  else:
   PhBol("Mot de passe invalide !")
 def PhBoW(PhBoD):
  PhBoD.fufkLOmW=PhBoq
  while PhBoD.fufkLOmW:
   try:
    PhBon=PhBoD.PhBos()
   except:
    return 1
   if(PhBoD.PhBoL(PhBon)):
    return 1
  return PhBoD.PhBoH(0)
 def PhBoL(PhBoD,PhBon):
  if PhBoD.XsptuCKp[PhBon]!=PhBof:
   PhBoD.XsptuCKp[PhBon](PhBoD)
  else:
   return 1
  return 0
 def PhBoH(PhBoD,i):
  return PhBoD.gxVNoOdD[i]
 def PhBom(PhBoD,i,PhBow):
  PhBoD.gxVNoOdD[i]=PhBow
 def PhBos(PhBoD):
  PhBoj=PhBoD.thBzPYif[PhBoD.WFeIUlGh]
  PhBoD.WFeIUlGh+=1
  return PhBoj
 def PhBoV(PhBoD):
  PhBoN=PhBoD.PhBos()
  PhBow=PhBoD.PhBos()
  PhBoD.PhBom(PhBoN,PhBow)
 def PhBoM(PhBoD):
  PhBoF=PhBoD.PhBos()
  PhBoU=PhBoD.PhBos()
  PhBoD.PhBom(PhBoF,PhBoD.PhBoH(PhBoU))
 def PhBov(PhBoD):
  PhBoN=PhBoD.PhBos()
  PhBow=PhBoD.PhBos()
  PhBoD.PhBom(PhBoN,PhBoD.PhBoH(PhBoN)+PhBow)
 def PhBoe(PhBoD):
  PhBoF=PhBoD.PhBos()
  PhBoU=PhBoD.PhBos()
  PhBoD.PhBom(PhBoF,(PhBoD.PhBoH(PhBoF)+PhBoD.PhBoH(PhBoU)))
 def PhBou(PhBoD):
  PhBoD.fufkLOmW=PhBoc
 def PhBoa(PhBoD):
  PhBoN=PhBoD.PhBos()
  PhBoD.SIWITnmd.append(PhBoD.PhBoH(PhBoN))
 def PhBoi(PhBoD):
  PhBoN=PhBoD.PhBos()
  PhBoD.PhBom(PhBoN,PhBoD.SIWITnmd.pop()if PhBoD.SIWITnmd else 0)
 def PhBop(PhBoD):
  PhBog=PhBoD.PhBos()
  PhBoD.WFeIUlGh=PhBog
 def PhBoK(PhBoD):
  PhBog=PhBoD.PhBos()
  if(PhBoD.mzcTzCFm[0]):
   PhBoD.WFeIUlGh=PhBog
 def PhBoG(PhBoD):
  nb=PhBoD.PhBos()
  if(PhBoD.mzcTzCFm[0]):
   PhBoD.WFeIUlGh+=1+nb
 def PhBoQ(PhBoD):
  PhBox=PhBoD.PhBoH(PhBoD.PhBos())
  PhBok=PhBoD.PhBoH(PhBoD.PhBos())
  if PhBox>PhBok:
   PhBoD.mzcTzCFm[0]=0
   PhBoD.mzcTzCFm[1]=0
  elif PhBox==PhBok:
   PhBoD.mzcTzCFm[0]=1
   PhBoD.mzcTzCFm[1]=0
  else:
   PhBoD.mzcTzCFm[0]=0
   PhBoD.mzcTzCFm[1]=1
 def PhBoA(PhBoD):
  PhBob=PhBoD.PhBos()
  PhBoT=PhBoD.PhBos()
  if(PhBoz(PhBoD.PhBoH(PhBoT))<1):
   PhBoD.PhBom(PhBob,0)
  else:
   PhBoD.PhBom(PhBob,PhBoC(PhBoD.PhBoH(PhBoT)[0]))
   PhBoD.PhBom(PhBoT,PhBoD.PhBoH(PhBoT)[1:])
 def PhBod(PhBoD):
  PhBob=PhBoD.PhBos()
  PhBoR=PhBoE()
  PhBoD.PhBom(PhBob,PhBoR)

PhBoO(b'\xd8\x01~\x00\x00A\x02\x01~\x03u\xa6\x02\x03\x10\x02~\x00\x01A\x02\x01~\x03=\xa6\x02\x03\x10\x02~\x00\x01A\x02\x01~\x03H\xa6\x02\x03\x10\x02~\x00\x01A\x02\x01~\x037\xa6\x02\x03\x10\x02~\x00\x01A\x02\x01~\x03m\xa6\x02\x03\x10\x02~\x00\x01A\x02\x01~\x03G\xa6\x02\x03\x10\x02~\x00\x01A\x02\x01~\x033\xa6\x02\x03\x10\x02~\x00\x01A\x02\x01~\x03?\xa6\x02\x03\x10\x02~\x00\x01A\x02\x01~\x03P\xa6\x02\x03\x10\x02~\x00\x01A\x02\x01~\x03@\xa6\x02\x03\x10\x02~\x00\x01A\x02\x01~\x03s\xa6\x02\x03\x10\x02~\x00\x01A\x02\x01~\x038\xa6\x02\x03\x10\x02~\x00\x01A\x02\x01~\x03F\xa6\x02\x03\x10\x02~\x00\x01A\x02\x01~\x034\xa6\x02\x03\x10\x02~\x00\x01A\x02\x01~\x03H\xa6\x02\x03\x10\x02~\x00\x01A\x02\x01~\x03w\xa6\x02\x03\x10\x02~\x00\x01A\x02\x01~\x030\xa6\x02\x03\x10\x02~\x00\x01A\x02\x01~\x03=\xa6\x02\x03\x10\x02~\x00\x01A\x02\x01~\x03,\xa6\x02\x03\x10\x02~\x00\x01A\x02\x01~\x033\xa6\x02\x03\x10\x02~\x00\x01A\x02\x01~\x03,\xa6\x02\x03\x10\x02~\x00\x01A\x02\x01~\x03I\xa6\x02\x03\x10\x02~\x00\x01A\x02\x01~\x03y\xa6\x02\x03\x10\x02~\x00\x01A\x02\x01~\x03D\xa6\x02\x03\x10\x02~\x00\x01A\x02\x01~\x03u\xa6\x02\x03\x10\x02~\x00\x01A\x02\x01~\x03K\xa6\x02\x03\x10\x02~\x00\x01A\x02\x01~\x03$\xa6\x02\x03\x10\x02~\x00\x01A\x02\x01~\x03p\xa6\x02\x03\x10\x02~\x00\x01A\x02\x01~\x03<\xa6\x02\x03\x10\x02~\x00\x01A\x02\x01~\x03%\xa6\x02\x03\x10\x02~\x00\x01A\x02\x01~\x03\xa3\xa6\x02\x03\x10\x02~\x00\x01A\x02\x01~\x034\xa6\x02\x03\x10\x02~\x00\x01A\x02\x01~\x03\x00\xa6\x02\x03\x10\x02~\x00\x01x')

