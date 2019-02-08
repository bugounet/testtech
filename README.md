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
 - choix d'une BDD (je vais utiliser un SQLITE pour commencer)
 - authentification (pour un premier pas, je laisse l'API sans auth)
 - soumission d'un algo python (je stocke le fichier python dans les MEDIA et
  les uploaderai avec django-admin)
 - soumission d'un docker file (pareil que pour l'algo)

# Lancé d'images

- Construire l'image à partir du docker-file
```bash
docker build -t image_<running_task_hash_or_id> -f Dockerfile.dms .
```
- Exécuter le programme
```bash
docker run -d -ti --name=container_<running_task_hash_or_id_as_container_name> image_<running_task_hash_or_id> "-V <output_volume> -T"
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

Lancer le serveur:
```
source env/bin/activate
python manage.py runserver
```

Se connecter à django-admin:

La base de données SQLite fournie par défaut contient un user qui s'appelle
"admin". Son mot de passe est "owkin".
