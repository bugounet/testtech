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
