from flask import Flask, request, jsonify, send_file
import os
import sys
import platform
    

app = Flask(__name__)

# Chemin du dossier de stockage des fichiers
storage_path = "C:/Partage"

# if platform.system() == "Darwin":  # Vérifier si le système d'exploitation est macOS
    # storage_path = "/Users/Partage"
# else:
# Chemin par défaut pour les autres systèmes d'exploitation


# Utiliser storage_path pour vos opérations de stockage


# Créer une instance de l'application Flask
app = Flask(__name__)

# Définir le point d'extrémité pour télécharger un fichier
@app.route("/download/<filename>", methods=["GET"])
def download_file(filename):
    # Construire le chemin du fichier en joignant le chemin de stockage (storage_path) et le nom du fichier
    file_path = os.path.join(storage_path, filename)
    # Vérifier si le fichier existe
    if os.path.isfile(file_path):
        # Si le fichier existe, l'envoyer en tant que pièce jointe
        return send_file(file_path, as_attachment=True)
    else:
        # Si le fichier n'existe pas, renvoyer une réponse JSON indiquant que le fichier n'a pas été trouvé
        return jsonify({"message": "Fichier non trouvé"})

# Définir le point d'extrémité pour téléverser un fichier
@app.route("/upload", methods=["POST"])
def upload_file():
    # Vérifier si la clé "file" est présente dans les fichiers de la requête
    if "file" not in request.files:
        # Si aucun fichier n'est présent, renvoyer une réponse JSON indiquant qu'aucun fichier n'a été téléversé
        return jsonify({"message": "Aucun fichier téléversé"})

    # Récupérer le fichier à partir de la requête
    file = request.files["file"]

    # Vérifier si le fichier n'est pas vide et a un nom de fichier valide
    if file and file.filename != "":
        # Enregistrer le fichier dans le répertoire de stockage (storage_path) en utilisant le nom de fichier d'origine
        file.save(os.path.join(storage_path, file.filename))

        # Renvoyer une réponse JSON indiquant que le fichier a été téléversé avec succès
        return jsonify({"message": "Fichier téléversé avec succès"})
    else:
        # Renvoyer une réponse JSON indiquant une erreur lors du téléversement du fichier
        return jsonify({"message": "Erreur lors du téléversement du fichier"})
    
# Fonction pour afficher les fichiers dans le dossier du NAS
@app.route("/files", methods=["GET"])
def list_files():
    files = os.listdir(storage_path)
    return jsonify(files)

# Point d'extrémité pour supprimer un fichier
@app.route("/delete/<filename>", methods=["POST"])
def delete_file(filename):
    # Construire le chemin du fichier en joignant le chemin de stockage (storage_path) et le nom du fichier
    file_path = os.path.join(storage_path, filename)
    
    # Vérifier si le fichier existe avant de le supprimer
    if os.path.exists(file_path):
        # Supprimer le fichier
        os.remove(file_path)
        return "Fichier supprimé avec succès", 200
    else:
        return "Fichier non trouvé", 404
    

@app.route('/api/status', methods=['GET'])
def server_status():
    # Mettez ici toute logique pour vérifier l'état du serveur.
    # Par exemple, vous pouvez vérifier les connexions à la base de données,
    # les services externes, etc.

    # Si le serveur est en ligne, renvoyer un code d'état 200
    return jsonify(message="Le serveur est en ligne"), 200

    
if __name__ == "__main__":
    # Lancer l'application Flask sur l'adresse 0.0.0.0 (toutes les interfaces) et sur le port 8000
    app.run(host="0.0.0.0", port=8000)
