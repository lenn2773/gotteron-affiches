from PIL import Image
import os

for filename in ["logos/fribourg.png", "logos/geneve.png"]:
    if not os.path.exists(filename):
        print("Fichier introuvable :", filename)
        continue

    try:
        with Image.open(filename) as img:
            img.verify()

        with Image.open(filename) as img:
            print(filename)
            print("Format :", img.format)
            print("Dimensions :", img.size)
            print("Image valide !")

    except Exception as error:
        print("Erreur :", error)

print("\nTEST TERMINÉ")
