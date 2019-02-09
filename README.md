# Test Owkin

# Sujet
On se propose de créer une API capable de programmer des appentissages et d'en
suivre la progression et les résultats.

Pour ce faire, on va créer une API capable de recevoir un docker (format
reste à déterminer). Cette soumission retournera un ID correspondant à la tache
créée. Ensuite on aura un accès en lecture sur la tâche qui permettra de lire
des informations relatives à la sortie du script.

Le lancement du docker se fera en arrière plan. Probablement avec un task
runner style celery.

Je proposerai dans ce document des informations en français, en revanche
l'API que je produis restera en anglais.

Pour simplifier le sujet, je vais commencer par implémenter une API
qui déclenche un apprentisssage.
Je laisse donc de côté les notions suivantes que j'envisage de traiter plus
tard si le temps me le permet:
 - config de production (le serveur devra être lancé en debug)
 - choix d'une BDD (je vais utiliser un SQLITE pour commencer)
 - authentification (pour un premier pas, je laisse l'API sans auth)
 - soumission d'un algo python (je stocke le fichier python dans les MEDIA et
  les uploaderai avec django-admin)
 - soumission d'un docker file (pareil que pour l'algo)

# Lancé d'images

- Créer un volume pour stocker les données de sortie
```bash
docker volume create training_output
```
- Construire l'image à partir du docker-file
```bash
docker build -t image_<running_task_hash_or_id> -f Dockerfile.dms .
```
- Exécuter le programme
```bash
docker run -d -ti --name=container_<running_task_hash_or_id_as_container_name> image_<running_task_hash_or_id> "-V training_output"
```

__Note:__
J'ai testé l'image générée et je recois une tracback assez étrange parfois:
```Exception ignored in: <bound method BaseSession.__del__ of <tensorflow.python.client.session.Session object at 0x7fda98b1ae80>>
Traceback (most recent call last):
  File "/usr/local/lib/python3.5/dist-packages/tensorflow/python/client/session.py", line 702, in __del__
TypeError: 'NoneType' object is not callable
```

D'après (cette discussion)[https://github.com/tensorflow/cleverhans/issues/17]
il s'agit d'un soucis quand on utilise keras et tensorflow. Ça ne m'empêche
à priori pas de récupérer les données donc je le laisse faire.

- Récupérer les données de sortie

## API
D'après les quelques tests effectués via le shell et docker, j'aurai besoin
de stocker en BDD les Id de run et par conséquent les différents IDs docker.
J'ai donc en principe deux modèles:

 - un TrainingTask qui correspond à un run de l'algorithme d'apprentissage
 - un TrainingConfiguration Stockage de l'algo, dockerfile et autres
 paramètres utilisés pour lancer le run.

Je vais donc mocker ça et créer une API qui proposera donc les routes et
actions suivantes:
GET /api/trainings --> Retourne la liste des TrainingConfiguration
POST /api/training/:id/run --> Crée un TrainingTask et retourne son ID

GET /api/task/:id/ --> Retourne le TrainingTask demandé avec le statut, les
résultats et les potentielles erreurs
{
    "status": ["created", "building", "training", "complete", "failure"],
    "id": <int>,
    "created_on": "iso-datetime"
    "failure_message": "Error message encountered for error summary",
    "test_loss": <DecimalField>
    "test_accuracy": <DecimalField>
}

## Setup

Créer un virtual env, installer les requirements, et lancer les tests:

```
virtualenv -p python3 env
source env/bin/activate
python manage.py test
```

Installer redis pour permettre à celery de fonctionner
```
brew install redis
```

Créer le volume de sortie des donnés de docker
```
docker volume create training_output
```

Lancer le serveur:
```
source env/bin/activate
# Start celery worker & beeat in background
celery -A test_owkin -l info & celery -A test_owkin beat &
# Start django server in foreground
python manage.py runserver
```

Se connecter à django-admin:

La base de données SQLite fournie par défaut contient un user qui s'appelle
"admin". Son mot de passe est "owkin".

## Utilisation:

Créer un algorithme:
POST /api/trainings

Publier un fichier python
curl -X PUT "http://localhost:8000/api/training/:id/upload" -F "file=@algo.py" -H "Content-Disposition:attachment; filename=algo.py"

Publier un dockerfile:
curl -X PUT "http://localhost:8000/api/training/:id/upload" -F "file=@Dockerfile.dms" -H "Content-Disposition:attachment; filename=Dockerfile.dms"

Programmer l'exécution de l'algo
POST /v1/training/:id/run

Suivre l'avancée de la task
GET /v1/task/:task_id

Annuler une task
POST /v1/task/:task_id/abort

## La suite du plan
Le projet rendu est cpable de recevoir des fichiers de config pour faire 
fonctionner les algos en arrière plan. Ce n'est pas super safe car tout le 
monde peut y accéder. J'aurais donc attaqué la suite du projet en mettant en 
place un système d'authentification basé sur les Users django.

L'API proposée n'est pas super pertinente car j'ignorais quelles informations
 on peut vouloir stocker sur les différents algos et leurs tasks. Il n'est 
 pas non plus ici question de sqavoir se connecter à une autre instance 
 docker que localhost ce qui limite énormément la performance du système. 