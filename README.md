# VroomLegend

VroomLegend est un jeu de course de voiture dans un environnement en 2D avec des graphismes attractifs. Traversez une piste de course autour d'un lac, en évitant les nombreux obstacles qui se dresseront sur votre route.

## Guide d'installation

Tout d'abord, il faut cloner le projet :

`git clone https://github.com/Saditud/vroom-legend` 

Ensuite, on peut trouver dans les répertoires :
- vroom-legend/client/dist/vroom-legend.exe
- vroom-legend/back/dist/server-vroom-legend.exe

Il suffit de lancer d'abord le fichier server-vroom-legend.exe puis le fichier vroom-legend.exe pour jouer au jeu.

S'il y a des problèmes de lancement, désactiver votre l'antivirus
Si le multijoueur ne fonctionne pas, désactivez votre firewall 

## Guide environnement de développement

### Prérequis

Installer la dernière version de python https://www.python.org/downloads/
Télécharger les librairies avec PIL du front et du back:
```bash
pip install -r client/requirements.txt
pip install -r back/requirements.txt
```

Pour lancer le code:
- le back
```bash
python back/serverHTTP/serverHTTP.py
```
- le front
```bash
python client/src/main.py
```