Si votre système d"exploitation est Linux (Debian), effectuez ces commandes :
```sh
sudo apt-get install pkg-config
sudo apt-get install libhdf5-serial-dev
```

Afin d'avoir la majorité des librairies nécessaires pour exécuter les scripts :
```sh
pip3 requirements.txt
```

Pour lancer l'application, vous pouvez exécutez le script app.py
OU ouvrir deux terminaux et effectuez dans chacun les commandes suivantes :
```sh
python3 src/data/data_ingest
python3 src/chatbot/main.py
```
