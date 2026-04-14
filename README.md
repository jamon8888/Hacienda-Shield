# Hacienda Shield

Hacienda Shield aide a anonymiser vos documents avant leur analyse dans Claude Desktop, tout en gardant les donnees sensibles sur votre ordinateur.

Le principe est simple :
- le document reste en local ;
- les informations sensibles sont remplacees par des reperes ;
- Claude travaille sur une version nettoyee ;
- le document final est reconstruit localement.

## Installation simple sur Windows

Cette methode est la plus simple pour un usage normal.

1. Installez Claude Desktop.
2. Ouvrez Claude Desktop.
3. Ouvrez les reglages, puis la section des extensions.
4. Cliquez sur le bouton d'installation d'une extension.
5. Choisissez le fichier [hacienda-shield-v1.0.0.dxt](C:/Users/NMarchitecte/Documents/Hacienda-Shield/.worktrees/hacienda-shield-rebrand/dist/hacienda-shield-v1.0.0.dxt).
6. Validez l'installation et attendez la fin de la preparation.

Verification :
- l'extension `Hacienda Shield` apparait dans la liste des extensions ;
- elle est marquee comme installee ou activee ;
- vous pouvez revenir a la conversation sans message d'erreur.

## Installation avancee depuis le code source

Cette methode est utile uniquement si vous travaillez directement dans le depot ou si vous voulez preparer les dependances avant la premiere utilisation.

Prerequis :
- Python 3.10 ou plus ;
- une connexion internet ;
- environ 1 Go d'espace libre pour les dependances et modeles.

Sur Windows, depuis la racine du projet, lancez :

```powershell
setup_hacienda_shield.bat
```

Si vous preferez passer par Python :

```powershell
python setup_hacienda_shield.py
```

La preparation est terminee quand le script affiche un message de fin d'installation sans erreur.

## Choisir le dossier de travail dans Claude Desktop

Pour que Hacienda Shield trouve vos documents, il faut lui indiquer le dossier qui les contient.

1. Ouvrez Claude Desktop.
2. Ouvrez les reglages de l'extension Hacienda Shield.
3. Reperez le champ `Working directory`.
4. Renseignez le chemin complet du dossier qui contient vos documents.
5. Verifiez que vous avez choisi le dossier parent, et non un fichier unique.

Ne joignez pas le document comme simple piece jointe si vous voulez garder le traitement local. Le bon reflexe est de definir le dossier contenant les fichiers, puis de travailler a partir de ce dossier.

## Premiere utilisation

1. Ouvrez une nouvelle conversation dans Claude Desktop.
2. Verifiez que le bon dossier de travail est bien configure.
3. Demandez votre action en langage simple.

Exemple :

> Analyse ce contrat et resume les points de risque importants.

## Actions possibles

Avec Hacienda Shield, vous pouvez :
- anonymiser un document avant analyse ;
- relire les entites detectees et corriger les oublis ;
- restaurer un document final avec les informations d'origine ;
- traiter plusieurs formats de fichiers courants.

## Formats pris en charge

Formats d'entree :
- `.pdf`
- `.docx`
- `.txt`
- `.md`
- `.csv`

Points utiles :
- les fichiers Word conservent leur mise en forme autant que possible ;
- les documents tres longs peuvent etre traites en plusieurs etapes ;
- la premiere preparation peut prendre quelques minutes, puis les lancements suivants sont plus rapides.

## En cas de probleme

- Si l'installation semble longue au premier lancement, attendez la fin de la preparation.
- Si Claude ne trouve pas votre document, verifiez d'abord le contenu du champ `Working directory`.
- Si le dossier choisi est complique a retrouver, deplacez vos fichiers dans un dossier simple comme `Documents`, puis recommencez.
- Si le script d'installation Windows ne se lance pas, verifiez d'abord que Python est bien installe avant de relancer le script.
