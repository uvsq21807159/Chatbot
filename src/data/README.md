Vous trouverez ci-dessous les manipulations à effectuer afin de faire fonctionner la partie traitement
de données de notre projet, qui utilise quelques services Microsoft Azure.

De plus, vous pourrez trouver la présentation des services choisis dans notre rapport final.
A noter que pour ceci, un abonnement gratuit (normal et étudiant) est totalement suffisant pour 
utiliser les services choisis par nous-mêmes. De plus, cela vous permettra de créer un groupe de 
ressources qui sera commun à tous les services utilisés. 

Enfin, si certains critères ne sont pas précisésci-dessous, cela signifie qu'il n'est pas nécessaire
d'y toucher.

# Azure Event Hubs

## L'espace de noms
- Dans la barre de recherches, saisir "Event Hubs"
- Créer espace de noms event hubs
- Sélectionner ou créer votre groupe de ressources
- Donner le nom 'uvsqterpollution' à votre espace
- Sélectionner un niveau tarifiaire "de base" (car suffisant)
- Créer et accéder à la ressource une fois la création terminée
- Dans l'onglet des paramètres, cliquer sur 'Stratégie d'accès partagé'
- Sélectionner la RootManageSharedAccessKey puis copier la clé primaire de la chaîne de connexion
- Ouvrer le fichier azure_composants.py et coller la valeur pour la constante CONN_STR

## Le hub d'évènements
- Retourner sur l'onglet "vue d'ensemble" et cliquer sur 'Créer hub d'évènements'
- Donner le nom 'dataHub' à votre hub
- Créer le hub

# Azure SQL Database
- Dans la barre de recherches, saisir "Azure SQL Database"
- Sélectionner 'Bases de données SQL' puis créer 'Base de données SQL'
- Donner le nom 'pollution_db' à votre base de données
- Créer un nouveau serveur (correspondant à l'étape ci-dessous)
- Utiliser l'option 'Configurer la base de données' dans l'onglet 'Calcul + stockage'
- Sélectionner 'De base' pour le niveau de service puis 'Appliquer'
- Créer la base de données et accéder à la ressource
- Sélectionner 'Editeur de requêtes' et se connecter (1)
- Copier le contenu de ./queries/create_table.sql et le coller dand 'Requête 1' pour l'exécuter

## Serveur SQL Database
- Donner le nom 'uvsq-pollution-server' à votre serveur
- Saisir 'user' pour la connexion d'administrateur du serveur
- Renseigner '4Za6PLL4qRCnnBx!' pour le mot de passe

# Azure Stream Analytics
- Dans la barre de recherches, saisir "Stream Analytics" et sélectionner "Travaux Stream Analytics"
- Créer "Tâche Stream Analytics"
- Nommer le travail en "insert_db" puis créer le travail
- Copier le contenu de ./queries/insert_db et sélectionner 'Modifier la requête' dans la vue d'ensemble
- Coller le contenu, sauvegarder la requête puis revenir à l'onglet précedent
- Dans l'onglet 'Identité Managée', ajouter une identité puis enregistrer
- Dans l'onglet 'Topologie de la tâche', sélectionner 'Entrées'
- Cliquer sur 'Ajouter une entrée de flux' puis 'Hub d'évènements'
- Renseigner 'datahub' dans l'alias de l'entrée puis vérifier l'event hub existant utilisé est bien celui créer auparavant avant d'enregistrer
- Dans l'onglet 'Topologie de la tâche', sélectionner 'Sorties'
- De même, cliquer sur "Ajouter' puis 'SQL Database'
- Renseigner 'pollutiondb' dans l'alias de sortie et 'Pollution' pour la table, tout en vérifiant si la base de données utilisée est celle créée auparavant avant d'enregistrer.

## Configuration du serveur
- Sélectionner le service 'pollutionserver' sur la page d'accueil d'Azure
- Dans l'onglet des paramètres, sélectionner 'Azure Active Directory' puis 'Définir l'adminisatrateur'
- Rechercher et sélectionner 'insert_db' puis enregistrer
- Dans l'onglet 'Sécurité', selectionner 'Mise en réseau' 
- Autoriser les services et les ressources Azure à accéder à ce serveur dans 'Exceptions'
- Ajouter une adresse IP cliente (si ce n'était pas encore réalisé à (1)) puis enregistrer

Enfin, retourner sur le service Stream Analytics 'insert_db' puis démarrer votre travail.
Vous n'aurez nul besoin de l'arrêter à présent.

