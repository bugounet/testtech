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
