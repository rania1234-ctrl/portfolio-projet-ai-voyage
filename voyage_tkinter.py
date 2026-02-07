import tkinter as tk
from PIL import Image, ImageTk
from sklearn import tree
import numpy as np

# === Données d'entraînement ===
X = [
    [1, 1, 1, 1, 0, 0],  # Bali
    [0, 0, 0, 0, 1, 0],  # Paris
    [0, 1, 0, 1, 0, 0],  # Islande
    [1, 0, 1, 0, 1, 1],  # Marrakech
    [1, 0, 0, 1, 1, 1],  # Tokyo
    [0, 1, 0, 0, 0, 0],  # Les Alpes
]
Y = [0, 1, 2, 3, 4, 5]
destinations = ["bali", "paris", "islande", "marrakech", "tokyo", "les alpes"]
labels_affichables = ["Bali 🇮🇩", "Paris 🇫🇷", "Islande 🇮🇸", "Marrakech 🇲🇦", "Tokyo 🇯🇵", "Les Alpes 🇫🇷"]

clf = tree.DecisionTreeClassifier()
clf = clf.fit(X, Y)

# === Questions ===
questions = [
    "🌡️ Préfères-tu un climat chaud ?",
    "🌿 Aimes-tu la nature ?",
    "💰 Souhaites-tu une destination pas chère ?",
    "🌍 Veux-tu sortir de l'Europe ?",
    "🏛️ Tu recherches une richesse culturelle ?",
    "🎉 Veux-tu faire la fête ?"
]

# === Interface principale ===
root = tk.Tk()
root.title("Système Expert de Voyage 🌍")
root.geometry("900x600")
root.resizable(False, False)

# === Arrière-plan ===
bg_image = Image.open("background.jpg").resize((900, 600))
bg_photo = ImageTk.PhotoImage(bg_image)
canvas = tk.Canvas(root, width=900, height=600)
canvas.pack(fill="both", expand=True)
canvas.create_image(0, 0, image=bg_photo, anchor="nw")

# === Titre ===
titre = tk.Label(root, text="Bienvenue dans le système expert de voyage",
                 font=("Helvetica", 18, "bold"), bg="white", fg="black")
canvas.create_window(450, 40, window=titre)

# === Composants dynamiques ===
label_question = tk.Label(root, text="", font=("Helvetica", 16), bg="white", fg="black")
canvas.create_window(450, 140, window=label_question)

image_label = tk.Label(root, bg="white")
canvas.create_window(450, 320, window=image_label)

# === Variables globales ===
reponses = []
index_question = 0
bouton_oui = bouton_non = None

# === Fonctions ===
def afficher_question():
    if index_question < len(questions):
        label_question.config(text=questions[index_question])
    else:
        faire_prediction()

def repondre(valeur):
    global index_question
    reponses.append(1 if valeur == "oui" else 0)
    index_question += 1
    afficher_question()

def faire_prediction():
    global bouton_oui, bouton_non

    entree = np.array([reponses])
    prediction = clf.predict(entree)[0]
    destination_nom = labels_affichables[prediction]
    image_file = f"{destinations[prediction]}.jpg"

    # Afficher la photo
    img = Image.open(image_file).resize((500, 300))
    photo = ImageTk.PhotoImage(img)
    image_label.config(image=photo)
    image_label.image = photo  # Garder la référence

    label_question.config(text=f"🌟 Destination recommandée : {destination_nom}")

    # Masquer les boutons
    bouton_oui.place_forget()
    bouton_non.place_forget()

    # Montrer le bouton recommencer
    bouton_restart.place(x=390, y=550)

def recommencer():
    global index_question, reponses
    reponses = []
    index_question = 0
    image_label.config(image=None)
    bouton_restart.place_forget()
    afficher_question()
    bouton_oui.place(x=320, y=220)
    bouton_non.place(x=500, y=220)

# === Boutons ===
bouton_oui = tk.Button(root, text="Oui", font=("Helvetica", 14), width=10, bg="#4CAF50", fg="white",
                       command=lambda: repondre("oui"))
bouton_non = tk.Button(root, text="Non", font=("Helvetica", 14), width=10, bg="#F44336", fg="white",
                       command=lambda: repondre("non"))

bouton_oui.place(x=320, y=220)
bouton_non.place(x=500, y=220)

bouton_restart = tk.Button(root, text="🔁 Recommencer", font=("Helvetica", 12, "bold"),
                           command=recommencer, bg="blue", fg="white")

# === Démarrage ===
afficher_question()
from sklearn.tree import plot_tree
import matplotlib.pyplot as plt

# === Fonction pour afficher l'arbre de décision ===
def afficher_arbre():
    plt.figure(figsize=(14, 8))
    plot_tree(clf,
              feature_names=["Chaud", "Nature", "PasCher", "HorsEurope", "Culture", "Fete"],
              class_names=labels_affichables,
              filled=True)
    plt.title("🧠 Arbre de Décision - Recommandation de Voyage")
    plt.show()

# === Bouton pour afficher l'arbre ===
bouton_arbre = tk.Button(root, text="🧠 Voir l'arbre de décision", font=("Helvetica", 12),
                         command=afficher_arbre, bg="#FFC107", fg="black")
bouton_arbre.place(x=20, y=550)

root.mainloop()

