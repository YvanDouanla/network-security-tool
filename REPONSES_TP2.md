# Réponses au TP 2 - GitHub Actions

Auteur : Douanla Yvan

## Question 1 : Pourquoi les tests ne dépendent-ils pas de l'ouverture réelle du port 443 ?

Les tests vérifient la validation des numéros de port. Ils ne tentent pas de connexion au port 443. Le seul appel à check_port utilise un port invalide, rejeté avant la création de la socket.

## Question 2 : Quelle différence entre push et pull_request ?

push déclenche le workflow lorsque des commits sont envoyés sur une branche configurée. pull_request le déclenche notamment lors de l'ouverture ou de la mise à jour d'une Pull Request visant main, afin de vérifier les changements proposés avant leur fusion.

## Question 3 : Que se passe-t-il si pytest renvoie un code d'erreur ?

L'étape des tests échoue et le job est marqué en échec. Par défaut, les étapes suivantes comme Bandit sont ignorées, tandis que certaines étapes de nettoyage peuvent encore s'exécuter.

## Question 4 : Pourquoi bloquer l'intégration d'une Pull Request lorsque les tests échouent ?

Cela évite d'intégrer dans main une modification qui ne respecte pas les comportements vérifiés par les tests. Pour rendre ce blocage obligatoire sur GitHub, il faut configurer les contrôles requis dans les règles de protection de branche ou un ruleset.

## Question 5 : Quelle différence entre le contrôle SAST et les tests fonctionnels pytest ?

Bandit réalise une analyse statique du code pour rechercher des motifs potentiellement dangereux, sans exécuter le programme. pytest exécute des tests pour vérifier les comportements attendus. Ces contrôles sont complémentaires.

## Échec volontaire observé

Test : test_valid_port
Assertion incorrecte : assert is_valid_port(443) is False
Erreur : assert True is False
Localisation : tests/test_network_check.py:6: AssertionError
Résultat : 1 failed, 2 passed.

Après correction de l'assertion en is True, le pipeline est revenu au vert.
