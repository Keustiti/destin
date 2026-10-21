import random
import json
import streamlit as st

st.set_page_config(page_title="Destins — simulation de vie", page_icon="✨", layout="wide")

WORLDS = {
    "Monde réel": {"icon": "🌍", "places": ["Lyon, France", "Montréal, Canada", "Dakar, Sénégal", "Tokyo, Japon"], "families": ["Martin", "Diallo", "Moreau", "Bernard", "Leroy"]},
    "Kuroko Basket": {"icon": "🏀", "places": ["Tokyo, Japon", "Kanagawa, Japon", "Kyoto, Japon"], "families": ["Kagami", "Kuroko", "Aomine", "Midorima", "Kise"]},
    "Naruto": {"icon": "🍥", "places": ["Konoha", "Suna", "Kiri", "Iwa", "Kumo"], "families": ["Uchiha", "Hyûga", "Nara", "Uzumaki", "Inuzuka", "Akimichi", "Aburame", "Inconnu"]},
    "Jujutsu Kaisen": {"icon": "🔮", "places": ["Tokyo, Japon", "Kyoto, Japon", "Sendai, Japon"], "families": ["Gojo", "Zenin", "Kamo", "Inconnu"]},
}
CHAKRA = {"Uchiha": "Feu", "Hyûga": "Foudre", "Nara": "Yin", "Uzumaki": "Vent", "Inuzuka": "Terre", "Akimichi": "Terre", "Aburame": "Terre", "Inconnu": "Vent"}
HAIR = ["Courts et bouclés", "Courts et lisses", "Mi-longs", "Longs", "Ébouriffés", "Tressés"]
BEARDS = ["Pas de barbe", "Barbe légère", "Barbe courte", "Barbe fournie"]
JOBS = ["Facteur", "Analyste", "Livreur", "Militaire", "Vendeur", "Infirmier", "Cuisinier", "Professeur", "Ingénieur", "Journaliste", "Footballeur professionnel", "Sportif professionnel"]
SEXUALITIES = ["Hétérosexuel·le", "Homosexuel·le", "Bisexuel·le", "Pansexuel·le", "Asexuel·le", "En questionnement", "Je préfère ne pas préciser"]
HERO_ASSOCIATIONS = ["Les Vigies d’Aurore", "L’Alliance Méridienne", "Le Pacte des Gardiens", "La Constellation Libre", "Les Sentinelles Civiques"]
OCCULT_TECHNIQUES = ["Fil d’énergie", "Écho spectral", "Sceau de retour", "Pas fulgurant", "Voile protecteur", "Aiguille d’ombre", "Onde de répulsion", "Marque du traqueur", "Peau de braise", "Prisme occulte", "Frappe résonnante", "Miroir des maléfices", "Ancre gravitationnelle", "Lame de silence", "Pollen soporifique", "Déviation vectorielle", "Cloche des esprits", "Nœud de contention", "Écran prismatique", "Pas du funambule", "Lueur purificatrice", "Main spectrale", "Fil à retardement", "Sceau de partage", "Vague de pression"]
KUROKO_ZONES = ["Zone de l’instinct", "Zone du tempo", "Zone de la vision totale", "Zone du tir sans hésitation", "Zone du contre-pied", "Zone du dernier quart-temps", "Zone du passeur invisible", "Zone du duel aérien", "Zone de la défense miroir", "Zone de l’éveil collectif", "Zone du sang-froid", "Zone du rythme brisé"]
HERO_ARMORS = {
    "Armure Aegis": (1400, "Protection équilibrée"), "Exo-armure Atlas": (2600, "Force et protection maximales"),
    "Armure furtive Spectre": (2200, "Infiltration et discrétion"), "Armure solaire Hélios": (3200, "Énergie et résistance"),
    "Armure modulaire Chimère": (3800, "Adaptation aux missions"), "Armure des abysses Nérée": (2900, "Résistance et mobilité")
}
MISSION_LEVELS = {"D": 20, "C": 35, "B": 50, "A": 65, "S": 80, "SS": 95}
CLAN_JUTSU = {
    "Uchiha": ["Katon : souffle de braise", "Sharingan naissant", "Katon : boule de feu", "Shurikenjutsu du clan", "Genjutsu : reflet écarlate", "Katon : dragon ardent", "Sharingan affiné", "Katon : mur de flammes", "Genjutsu : nuit inversée", "Katon : pluie de braises", "Lames de chakra écarlates", "Barrière de flammes"],
    "Hyûga": ["Poing souple", "Byakugan affiné", "Paume des 64 coups", "Rotation céleste", "Paume du Hakke", "Frappe des méridiens", "Pas du tourbillon", "Garde des 8 trigrammes", "Vision du réseau de chakra", "Paume jumelle du Hakke", "Poing souple : rupture", "Mur des 8 trigrammes"],
    "Nara": ["Contrôle de l’ombre", "Étreinte de l’ombre", "Possession des ombres", "Filet d’ombres", "Liaison à distance", "Clones d’ombre tactiques", "Piège crépusculaire", "Rassemblement des ombres", "Piqûre des ombres", "Paralysie en éventail", "Chasse nocturne", "Tissage des ombres"],
    "Uzumaki": ["Sceau simple", "Chaînes de chakra", "Barrière de scellement", "Sceau de protection", "Entrave des chaînes", "Marque de détection", "Barrière des quatre points", "Sceau de contention", "Chaînes de suppression", "Barrière des cinq directions", "Sceau de régénération", "Prison des chaînes tourbillonnantes"],
    "Inuzuka": ["Odorat développé", "Marquage bestial", "Crocs lacérants", "Bête humaine", "Poursuite en spirale", "Morsure tournoyante", "Pistage longue distance", "Défense en tandem", "Double croc traqueur", "Bond du loup", "Charge en meute", "Poursuite des trois crocs"],
    "Akimichi": ["Expansion partielle", "Roulade de la boulette", "Expansion du corps", "Poing géant", "Pas du boulet", "Expansion partielle des bras", "Charge tourbillonnante", "Contrôle du mode papillon", "Poing du papillon", "Roulade météore", "Expansion défensive", "Charge des montagnes"],
    "Aburame": ["Nuée défensive", "Repérage par insectes", "Essaim tactique", "Insectes de brouillage", "Cocon protecteur", "Balise d’insectes", "Nuée drainante", "Écran entomologique", "Insectes pisteurs", "Ruche de diversion", "Mur de coléoptères", "Essaim silencieux"],
    "Inconnu": ["Clone de base", "Substitution maîtrisée", "Technique de dissimulation", "Rafale de shuriken", "Pas silencieux", "Sceau de repérage", "Clone de diversion", "Barrière de chakra", "Technique de l’aiguille d’eau", "Prison de terre", "Pas éclair", "Sceau de protection mobile"],
}
PUPIL_TECHNIQUES = {
    "Sharingan": ["Lecture des mouvements", "Genjutsu du reflet", "Copie d’une technique observée", "Perception du chakra", "Mangekyō latent"],
    "Byakugan": ["Vision panoramique", "Repérage du réseau de chakra", "Frappe des méridiens", "Vision à longue portée", "Protection du Hakke"],
    "Rinnegan": ["Perception des flux", "Attraction gravitationnelle", "Répulsion gravitationnelle", "Barrière des six voies", "Maîtrise des six voies"],
}
NARUTO_GEAR = {
    "Étui de kunai renforcé": (380, "Arme · améliore légèrement la puissance des missions"),
    "Tanto de chakra": (1100, "Arme de mêlée · bonus de puissance en mission"),
    "Lot de fumigènes et de fils": (520, "Outils · aide aux choix d’infiltration"),
    "Gants de scellement": (900, "Outils · soutien aux jutsu de sceau"),
    "Parchemin de jutsu": (750, "Consommable · apprend le prochain jutsu de ton clan"),
    "Parchemin du mentor ermite": (1800, "Consommable · ouvre un entraînement spécial avec un mentor"),
    "Parchemin des pupilles": (4200, "Rare · permet de tenter l’éveil du Rinnegan après une mission de rang S"),
}
RARE_MENTOR_JUTSU = ["Rasengan", "Invocation des crapauds", "Technique du clone multiple", "Rasenshuriken", "Barrière des quatre flammes", "Sceau de contention avancé", "Pas éclair du maître", "Écran de chakra tournoyant"]
NPC_NAMES = ["Maya Sorel", "Noé Valen", "Inès Marot", "Yanis Kader", "Lina Solène", "Eli Navarro", "Sacha Delcourt", "Camille Oran", "Nour Belkacem", "Jules Ardent", "Ari Nishida", "Lou Vernet", "Milan Kuroda", "Tess Amani", "Romy Delaunay", "Naël Bensaïd", "Aiko Senda", "Théo Marchal", "Mina Kessler", "Ilyes Morel"]

st.markdown("""<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Space+Grotesk:wght@500;600;700&display=swap');
html,body,[class*="css"]{font-family:'DM Sans',sans-serif} .stApp{background:#f5f7fa;color:#1d2735}
.block-container{max-width:540px;padding:0 0 6rem;margin:0 auto}
.hero{background:#ed174c;border-radius:0;padding:14px 18px;color:white;margin:0 -1rem 12px;box-shadow:0 3px 10px #1c31431c}
.hero h1{font-family:'Space Grotesk';font-size:1.35rem;margin:0;text-align:center;letter-spacing:.03em}.hero p{display:none}
.card{background:#fff;border:1px solid #e6eaf0;border-radius:13px;padding:13px 15px;margin:8px 0;box-shadow:0 3px 12px #162a4009}
.event{border-left:4px solid #e4ad37}.muted{color:#718096;font-size:.9rem}.big{font-family:'Space Grotesk';font-size:1.35rem;font-weight:700}
.avatar{background:linear-gradient(145deg,#e7f2ff,#fff1dc);border-radius:16px;padding:10px;text-align:center;border:1px solid #e6eaf0}
.face{font-size:3.2rem;line-height:1.05}.stButton>button{border-radius:12px;font-weight:600;min-height:2.7rem}
.stProgress>div>div>div>div{background:#48a890}[data-testid="stMetric"]{background:white;border:1px solid #e6eaf0;padding:12px 16px;border-radius:14px}
[data-testid="stTabs"] [role="tablist"]{position:fixed;z-index:999;bottom:0;left:50%;transform:translateX(-50%);width:min(100vw,540px);box-sizing:border-box;background:#103c5b;padding:6px 5px max(6px,env(safe-area-inset-bottom));border-radius:0;margin:0;gap:0;display:grid;grid-template-columns:repeat(3,minmax(0,1fr)) 84px repeat(4,minmax(0,.75fr));box-shadow:0 -3px 14px #152b4c35}
[data-testid="stTabs"] button[role="tab"],.stTabs button[role="tab"]{min-width:0;color:#fff!important;-webkit-text-fill-color:#fff!important;background:#103c5b!important;border:0;border-radius:9px;padding:8px 3px;font-size:.70rem;font-weight:800;white-space:normal;line-height:1.15;display:flex;align-items:center;justify-content:center}
[data-testid="stTabs"] button[role="tab"] *,[data-testid="stTabs"] button[role="tab"] span,[data-testid="stTabs"] button[role="tab"] p,.stTabs button[role="tab"] *{color:#fff!important;-webkit-text-fill-color:#fff!important;fill:#fff!important;stroke:#fff!important}
[data-testid="stTabs"] button[role="tab"]:hover,.stTabs button[role="tab"]:hover{background:#225675!important}
[data-testid="stTabs"] button[role="tab"][aria-selected="true"],.stTabs button[role="tab"][aria-selected="true"]{background:#d71946!important;color:#fff!important;-webkit-text-fill-color:#fff!important;box-shadow:0 0 0 2px #ffbac9 inset}
[data-testid="stTabs"] button[role="tab"][aria-selected="true"] *,.stTabs button[role="tab"][aria-selected="true"] *{color:#fff!important;-webkit-text-fill-color:#fff!important;fill:#fff!important;stroke:#fff!important}
[data-testid="stTabs"] button[role="tab"]:nth-child(4){visibility:hidden;pointer-events:none}
[data-testid="stRadio"] [role="radiogroup"]{gap:5px}
.st-key-advance_year_fixed{position:fixed;z-index:1002;bottom:5px;left:50%;transform:translateX(-50%);width:92px}
.st-key-advance_year_fixed button{background:#159447!important;color:#fff!important;border:2px solid white;border-radius:24px;min-height:46px;padding:4px;font-size:.72rem;font-weight:800;box-shadow:0 2px 9px #102b3d75}
.st-key-advance_year_fixed button *{color:#fff!important;fill:#fff!important}
@media(max-width:600px){.block-container{padding-left:12px;padding-right:12px}.hero{margin-left:-12px;margin-right:-12px}.face{font-size:2.7rem}[data-testid="stTabs"] button[role="tab"]{font-size:.64rem;padding-left:2px;padding-right:2px}}
</style>""", unsafe_allow_html=True)

def init():
    defaults = {"started": False, "age": 0, "year": {"activities": [], "events": [], "close": [], "training_counts": {}}, "stats": {"Bonheur": 72, "Santé": 88, "Intelligence": 54, "Talent": 48, "Beauté": 55}, "family": [], "friends": [], "children": [], "clubs": [], "history": [], "story_paths": [], "mission_counts": {}, "jutsu_level": 0, "known_jutsu": [], "mentor_jutsu": [], "pupil_power": "", "pupil_stage": 0, "mentor_training": [], "mentor_progress": {}, "tailed_beast": "", "beast_mastery": 0, "orientation": "Je préfère ne pas préciser", "partner": None, "dating_candidate": None, "hero_affiliation": "", "npc_roster": [], "npc_memories": [], "career_skills": {}, "fatigue": 10, "technique_level": 1, "job_tasks": 0, "career_level": 0, "money": 1200, "coins": 0, "pending_coins": 0, "rank": "Civil", "career": "Aucune", "technique": "Aucune", "techniques": [], "zones": [], "challenges": [], "dead": False, "death_reason": "", "heir_count": 0, "current_page": "Année en cours", "honor": 0, "fame": 0, "inventory": [], "captured": False, "event_followups": [], "event_memory": [], "news_memory": []}
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value
    if st.session_state.started and st.session_state.technique != "Aucune" and st.session_state.technique not in st.session_state.techniques:
        st.session_state.techniques.append(st.session_state.technique)

def add_year_item(section, text):
    st.session_state.year[section].append(text)

def finish_challenge(key, label, reward):
    if key not in st.session_state.challenges:
        st.session_state.challenges.append(key)
        st.session_state.pending_coins += reward
        st.session_state.year["events"].append(f"🏆 Défi accompli : {label} · {reward} pièces Destin seront versées à la fin de ta vie.")

def advance_year():
    world = st.session_state.world
    age = st.session_state.age
    name = f"{st.session_state.first} {st.session_state.surname}"
    if age >= 65 and (age >= 90 or random.random() < .18):
        st.session_state.dead = True
        st.session_state.death_reason = f"à l’âge de {age} ans, après une longue vie"
        st.session_state.coins += st.session_state.pending_coins
        st.session_state.year["events"].append(f"Les défis de ta vie te rapportent {st.session_state.pending_coins} pièces Destin pour la dynastie.")
        st.session_state.pending_coins = 0
        st.session_state.year["events"].append(f"La famille se rassemble auprès de {name}. Son histoire prend fin à {age} ans.")
        st.rerun()
    st.session_state.age += 1
    new_age = st.session_state.age
    relative = random.choice(st.session_state.family) if st.session_state.family else "Un proche"
    relative_name = relative.split(" ·")[0]
    close_events = [f"{relative_name} commence une nouvelle année de sa vie.", f"{relative_name} t’annonce une décision qui va changer ses projets.", f"{relative_name} demande ton aide pour traverser une période compliquée.", f"{relative_name} célèbre une réussite et veut la fêter avec toi.", f"{relative_name} s’éloigne un peu et tu ne sais pas encore pourquoi.", f"{relative_name} reprend contact avec une personne importante de son passé.", f"{relative_name} te confie une inquiétude qu’il/elle cachait depuis longtemps.", f"{relative_name} te propose un voyage ou un projet à préparer ensemble.", f"{relative_name} fait une rencontre qui pourrait transformer sa vie.", f"{relative_name} a besoin d’un conseil pour une décision difficile."]
    close_event = random.choice(close_events)
    st.session_state.stats["Bonheur"] = max(0, min(100, st.session_state.stats["Bonheur"] + random.choice([-5, 0, 3, 6])))
    npc_updates = npc_year_update(world, new_age)
    st.session_state.year = {"activities": [], "events": [yearly_event(world, new_age)] + npc_updates, "close": [close_event], "training_counts": {}, "world_news": world_news(world), "event_resolved": False}
    if st.session_state.family and random.random() < .3:
        other = random.choice(st.session_state.family).split(" ·")[0]
        st.session_state.year["close"].append(random.choice([f"{other} t’envoie un message inattendu et attend ta réponse.", f"{other} organise une réunion de famille sans te prévenir du motif.", f"{other} traverse un changement important dans son travail.", f"{other} te présente une personne qui pourrait devenir un nouvel ami.", f"{other} se dispute avec un proche et te demande de ne pas prendre parti.", f"{other} te fait une surprise après avoir gardé un secret toute l’année."]))
    if 6 <= new_age <= 18 and world in ("Monde réel", "Kuroko Basket"):
        finish_challenge("school", "Fréquenter l’école", 100)
    if new_age in (18, 25, 40, 60): finish_challenge(f"age_{new_age}", f"Atteindre {new_age} ans", 100)
    st.rerun()

def age_stage(age):
    if age < 3: return "Petite enfance", "👶"
    if age < 6: return "Maternelle", "🧸"
    if age < 11: return "École primaire", "🎒"
    if age < 15: return "Collège", "📚"
    if age < 18: return "Lycée", "🏫"
    if age < 23: return "Études supérieures", "🎓"
    return "Vie adulte", "🌱"

def family_members(world, surname):
    roles = ["parent", "frère / sœur"]
    if world == "Naruto":
        jobs = ["chûnin au village", "ninja médecin", "jonin instructeur", "marchande d’armes", "responsable des archives"]
    elif world == "Kuroko Basket":
        jobs = ["entraîneur scolaire", "kinésithérapeute", "professeur", "journaliste sportif", "joueur professionnel"]
    elif world == "Jujutsu Kaisen":
        jobs = ["assistant d’exorciste", "professeur", "médecin", "employée de bureau", "exorciste de grade 2"]
    else:
        jobs = ["facteur", "infirmière", "analyste", "professeur", "livreur", "cuisinière", "militaire", "vendeuse"]
    names = random.sample(["Maya", "Noah", "Lina", "Eli", "Samir", "Lou", "Jules", "Inès"], 2)
    return [f"{person} {surname} · {role} · {random.choice(jobs)}" for person, role in zip(names, roles)]

def career_skill_profile(world, career="Aucune"):
    if world == "Naruto": names = ["Chakra", "Ninjutsu", "Genjutsu", "Taijutsu", "Furtivité"]
    elif world == "Jujutsu Kaisen": names = ["Énergie occulte", "Contrôle", "Barrières", "Combat", "Perception"]
    elif world == "Kuroko Basket": names = ["Tirs", "Dribble", "Vision du jeu", "Défense", "Endurance"]
    elif career == "Héros indépendant": names = ["Technologie", "Combat", "Réflexes", "Sauvetage", "Discrétion"]
    elif "Footballeur" in career: names = ["Tirs", "Passe", "Contrôle", "Tactique", "Endurance"]
    elif "Sportif professionnel" in career: names = ["Technique", "Puissance", "Réflexes", "Tactique", "Endurance"]
    else:
        profiles = {"Facteur": ["Endurance", "Orientation", "Fiabilité", "Relation client"], "Analyste": ["Technologies", "Analyse", "Communication", "Précision"], "Livreur": ["Conduite", "Orientation", "Endurance", "Fiabilité"], "Militaire": ["Discipline", "Tactique", "Condition", "Leadership"], "Vendeur": ["Négociation", "Écoute", "Connaissance produit", "Gestion"], "Infirmier": ["Soins", "Sang-froid", "Communication", "Endurance"], "Cuisinier": ["Technique", "Organisation", "Créativité", "Endurance"], "Professeur": ["Pédagogie", "Préparation", "Écoute", "Gestion de classe"], "Ingénieur": ["Technologies", "Conception", "Analyse", "Sécurité"], "Journaliste": ["Enquête", "Vérification", "Écriture", "Réseau"]}
        names = profiles.get(career.split(" ·")[0], ["Compétence", "Organisation", "Communication", "Endurance"])
    existing = st.session_state.get("career_skills", {})
    return {name: max(0, min(100, int(existing.get(name, 18 if name == "Endurance" else 22)))) for name in names}

def create_npc(world, age, role=None):
    active = {npc.get("name") for npc in st.session_state.get("npc_roster", [])}
    available = [name for name in NPC_NAMES if name not in active]
    if not available: return None
    if role is None:
        role_pool = ["Ami", "Rival", "Camarade"] if age < 12 else ["Ami", "Rival", "Mentor", "Collègue", "Allié"]
        role = random.choice(role_pool)
    jobs = {"Naruto": ["genin studieuse", "sensei de taijutsu", "ninja médecin", "archiviste du village", "rival de ton équipe"], "Kuroko Basket": ["meneur de jeu", "entraîneuse du club", "rival au tir", "arbitre bénévole", "recruteur régional"], "Jujutsu Kaisen": ["élève exorciste", "mentor de terrain", "gardienne des archives", "rival de Kyoto", "médecin de l’école"], "Monde réel": ["apprentie cuisinière", "mécanicien", "étudiant en arts", "soigneuse bénévole", "journaliste locale", "entraîneur de quartier"]}
    return {"id": f"npc-{random.randint(100000, 999999)}", "name": random.choice(available), "role": role, "job": random.choice(jobs[world]), "age": max(0, age + random.randint(-2, 3)), "trust": random.randint(35, 60), "rivalry": random.randint(15, 45) if role == "Rival" else 0, "status": "Présent·e", "memories": [], "last_seen": age, "interactions": 0}

def npc_year_update(world, age):
    roster = st.session_state.npc_roster
    for npc in roster:
        if npc.get("status") == "Présent·e": npc["age"] = min(110, npc.get("age", age) + 1)
    messages = []
    away = [npc for npc in roster if npc.get("status") == "Parti·e"]
    if away and random.random() < .10:
        returning = random.choice(away)
        returning["status"] = "Présent·e"
        memory = returning.get("memories", [])
        echo = f" après s’être rappelé(e) votre dernière conversation sur {memory[-1].get('choice', 'vos anciens projets')}" if memory else " après une longue absence"
        messages.append(f"{returning['name']} revient dans ton quotidien{echo}. Le lien n’a pas été effacé par le temps.")
    active = [npc for npc in roster if npc.get("status") == "Présent·e"]
    if age >= 5 and len(active) < 5 and random.random() < .72:
        role = "Mentor" if world == "Naruto" and age >= 11 and not any(n.get("role") == "Sensei" and n.get("status") == "Présent·e" for n in roster) else None
        newcomer = create_npc(world, age, role)
        if newcomer:
            if role == "Mentor": newcomer["role"] = "Sensei"
            roster.append(newcomer)
            messages.append(f"{newcomer['name']} entre dans ta vie comme {newcomer['job']}. Cette rencontre pourra compter pour la suite.")
    low_trust = [npc for npc in active if npc.get("trust", 50) < 38]
    if active and (low_trust and random.random() < .28 or random.random() < .045):
        npc = random.choice(low_trust or active)
        npc["status"] = "Parti·e"
        memory = npc.get("memories", [])
        echo = f" {npc['name']} se souvient encore de {memory[-1].get('choice', 'votre dernier échange')}" if memory else ""
        messages.append(f"{npc['name']} quitte ton quotidien : ses projets l’emmènent ailleurs.{echo}")
        st.session_state.npc_memories.append({"age": age, "npc": npc["name"], "event": "départ", "trust": npc.get("trust", 50)})
    familiar = [npc for npc in active if npc.get("memories")]
    if familiar and random.random() < .32:
        npc = random.choice(familiar)
        memory = random.choice(npc["memories"])
        messages.append(f"{npc['name']} reparle de l’année de tes {memory['age']} ans, quand tu as choisi de {memory['choice'].lower()}. Cette décision influence encore votre relation.")
        npc["trust"] = max(0, min(100, npc.get("trust", 50) + (2 if memory.get("tone") == "positif" else -2 if memory.get("tone") == "négatif" else 0)))
    if active and random.random() < .18:
        rival = next((npc for npc in active if npc.get("role") == "Rival"), None)
        if rival:
            messages.append(f"Ton rival {rival['name']} te lance un défi. Il/elle se rappelle votre dernier résultat et veut prendre sa revanche.")
    return messages

def record_npc_memory(npc, choice, age):
    positive = any(word in choice.lower() for word in ["aider", "aide", "encourager", "s’excuser", "protéger", "partager", "conseil", "entraîner"])
    negative = any(word in choice.lower() for word in ["défier", "refuser", "ignorer", "trahir", "humilier", "distance"])
    tone = "positif" if positive else "négatif" if negative else "neutre"
    delta = 10 if positive else -8 if negative else 3
    npc["trust"] = max(0, min(100, npc.get("trust", 50) + delta))
    npc["rivalry"] = max(0, min(100, npc.get("rivalry", 0) + (12 if negative and npc.get("role") == "Rival" else -3 if positive else 0)))
    npc["memories"].append({"age": age, "choice": choice, "tone": tone})
    npc["memories"] = npc["memories"][-12:]
    npc["last_seen"] = age
    npc["interactions"] = npc.get("interactions", 0) + 1
    st.session_state.npc_memories.append({"age": age, "npc": npc["name"], "event": choice, "tone": tone, "trust": npc["trust"]})
    st.session_state.npc_memories = st.session_state.npc_memories[-100:]

def update_career_skill(world, activity, career):
    skills = career_skill_profile(world, career)
    text = activity.lower()
    requested = next((key for key in skills if key.lower() in text), None)
    if requested:
        skills[requested] = min(100, skills[requested] + random.randint(2, 5))
        st.session_state.career_skills = skills
        return
    target = None
    if world == "Naruto":
        target = "Genjutsu" if "genjutsu" in text or "illusion" in text else "Chakra" if "chakra" in text or "ermite" in text or "rasengan" in text else "Taijutsu" if "taijutsu" in text or "combat" in text else "Ninjutsu" if "jutsu" in text or "parchemin" in text else "Furtivité" if "furtivité" in text or "éclaire" in text else None
    elif world == "Jujutsu Kaisen":
        target = "Barrières" if "barrière" in text or "voile" in text else "Contrôle" if "contrôle" in text or "sceau" in text else "Perception" if "analyser" in text or "trace" in text else "Combat" if "combat" in text or "exorc" in text else "Énergie occulte" if "occulte" in text or "fléau" in text else None
    elif world == "Kuroko Basket":
        target = "Tirs" if "tir" in text or "shoot" in text else "Dribble" if "dribble" in text else "Défense" if "défense" in text else "Vision du jeu" if "passe" in text or "collectif" in text else "Endurance" if "entraînement" in text or "match" in text else None
    elif career == "Héros indépendant":
        target = "Technologie" if "technologie" in text or "armure" in text else "Sauvetage" if "civil" in text or "sauvetage" in text else "Discrétion" if "discret" in text or "infiltr" in text else "Réflexes" if "réflex" in text else "Combat" if "combat" in text or "menace" in text else None
    elif "Footballeur" in career or "Sportif" in career:
        target = "Tirs" if "tir" in text else "Passe" if "passe" in text else "Tactique" if "tactique" in text else "Endurance" if "sport" in text or "match" in text or "entraînement" in text else "Technique" if "technique" in text or "entraînement" in text else None
    elif world == "Monde réel":
        role_skills = {"Facteur": ("Orientation", ["tournée", "adresse", "livraison"]), "Analyste": ("Analyse", ["données", "analyse", "rapport"]), "Livreur": ("Conduite", ["livraison", "route", "colis"]), "Militaire": ("Tactique", ["mission", "unité", "protocole"]), "Vendeur": ("Négociation", ["client", "vente", "négocier"]), "Infirmier": ("Soins", ["patient", "soin", "urgence"]), "Cuisinier": ("Technique", ["service", "recette", "cuisine"]), "Professeur": ("Pédagogie", ["élève", "classe", "cours"]), "Ingénieur": ("Technologies", ["prototype", "système", "sécurité"]), "Journaliste": ("Enquête", ["source", "témoin", "enquête"])}
        base_role = career.split(" ·")[0]
        if base_role in role_skills and any(token in text for token in role_skills[base_role][1]): target = role_skills[base_role][0]
    if target is None:
        target = next((key for key in skills if key.lower() in text), None)
    if target in skills: skills[target] = min(100, skills[target] + random.randint(2, 5))
    st.session_state.career_skills = skills

def world_news(world):
    headlines = {
        "Monde réel": ["Sciences : une équipe annonce une avancée dans le stockage d’énergie.", "Sports : plusieurs équipes nationales préparent leurs championnats.", "Culture : un festival itinérant fait étape dans la région.", "Économie : des formations professionnelles sont financées dans plusieurs villes.", "Environnement : des bénévoles restaurent les forêts locales.", "Technologie : un réseau de transport est testé dans plusieurs capitales.", "Santé : une campagne de dépistage gratuite ouvre dans les quartiers.", "Météo : une vague de chaleur conduit les écoles à adapter leurs horaires.", "Justice : une enquête sur une fraude financière connaît un nouveau rebondissement.", "Culture : un musée retrouve une œuvre disparue depuis des décennies.", "Solidarité : une collecte citoyenne dépasse son objectif en une journée.", "Transports : une ligne ferroviaire relie enfin plusieurs petites villes.", "Sports : un club amateur crée la surprise en coupe nationale.", "Éducation : une bourse ouvre l’accès aux études pour de nouveaux élèves.", "Environnement : une espèce rare est observée près de la ville.", "Numérique : une panne mondiale perturbe les services pendant plusieurs heures."],
        "Kuroko Basket": ["Ligue universitaire : Seirin annonce un changement de stratégie.", "NBA : plusieurs clubs négocient des transferts importants.", "Basket lycéen : un tournoi interrégional réunira les meilleures équipes.", "Infirmerie : des joueurs vedettes suivent un programme de récupération.", "Scouts : des recruteurs étrangers assistent aux matchs de jeunes talents.", "Classement : Tokyo et Kanagawa se disputent la première place.", "Une nouvelle règle expérimentale accélère les fins de match.", "Un ancien entraîneur reprend du service dans un lycée réputé.", "Une académie ouvre un centre de détection dans le Kansai.", "Une équipe outsider élimine le favori du tournoi préfectoral.", "La NBA annonce une tournée de pré-saison au Japon.", "Une polémique éclate autour d’un arbitrage en finale.", "Un joueur vedette fait une pause pour préserver sa santé.", "Les qualifications nationales dévoilent un tableau particulièrement difficile.", "Un tournoi trois contre trois attire des équipes de tout le pays.", "Une salle historique ferme, puis un ancien joueur propose de la sauver."],
        "Naruto": ["Les cinq grands villages discutent d’un accord de circulation.", "Des patrouilles signalent des déplacements près du Pays du Vent.", "Le bureau des missions publie de nouvelles affectations de rang C.", "Des membres de l’Akatsuki auraient été aperçus sur une route commerciale.", "Une rencontre exceptionnelle du conseil des Kage est évoquée à la radio.", "Suna demande de l’aide pour protéger une caravane.", "Un sommet diplomatique est déplacé après une menace anonyme.", "Des traces de chakra inconnues apparaissent près d’un ancien sanctuaire.", "Kiri renforce ses patrouilles maritimes après la disparition d’un navire.", "Un échange d’otages entre deux seigneurs féodaux est proposé.", "Une épidémie de fièvre touche un poste frontalier isolé.", "Un fragment de parchemin relance le débat sur les techniques interdites.", "Un village mineur demande officiellement la protection de Konoha.", "La radio intercepte un message codé attribué à l’Akatsuki.", "Un convoi de ravitaillement n’est jamais arrivé au Pays de la Terre.", "Le conseil des Kage annonce un exercice commun de secours."],
        "Jujutsu Kaisen": ["L’école de Kyoto prépare une rencontre inter-écoles.", "Plusieurs voiles sont apparus dans des régions éloignées.", "Les règles de classement des fléaux sont réexaminées.", "Une équipe de Tokyo est envoyée sur un site abandonné.", "Une nouvelle trace d’énergie occulte est repérée près d’un hôpital.", "Un exorciste de haut rang a disparu en mission.", "Des témoins signalent une rue qui change de longueur la nuit.", "Un outil maudit est retrouvé dans une vente aux enchères clandestine.", "Le conseil interdit l’accès à un tunnel après trois disparitions.", "Un fléau de grade 1 évite les affrontements et semble chercher quelqu’un.", "Un voile apparaît autour d’un festival sans toucher les visiteurs.", "Une ancienne école d’exorcisme est découverte sous un immeuble.", "Des rapports de Kyoto et Tokyo décrivent la même empreinte occulte.", "Un exorciste inconnu soigne des civils avant de disparaître.", "Le conseil convoque les mentors pour une réunion d’urgence.", "Une barrière protège un quartier entier d’un fléau invisible."]}
    recent = st.session_state.get("news_memory", [])
    pool = [item for item in headlines[world] if item not in recent]
    if len(pool) < 3:
        pool = headlines[world]
    selected = random.sample(pool, 3)
    st.session_state.news_memory = (recent + selected)[-12:]
    return selected

def mission_power(world):
    stats = st.session_state.stats
    fatigue_penalty = st.session_state.get("fatigue", 0) // 12
    if world == "Kuroko Basket": return stats.get("Basket", stats.get("Talent", 48)) + st.session_state.get("fame", 0) // 5 + min(15, len(st.session_state.zones) * 3) - fatigue_penalty
    if world == "Naruto":
        rank_bonus = {"Étudiant de l’académie": 0, "Genin": 6, "Chûnin": 12, "Jônin": 18, "Hokage": 25}.get(st.session_state.rank, 0)
        gear_bonus = 5 if "Tanto de chakra" in st.session_state.inventory else 2 if "Étui de kunai renforcé" in st.session_state.inventory else 0
        hereditary_bonus = min(12, st.session_state.get("pupil_stage", 0) * 2) + st.session_state.get("beast_mastery", 0) * 3
        return (stats.get("Talent", 48) + stats.get("Santé", 50)) // 2 + rank_bonus + gear_bonus + hereditary_bonus - fatigue_penalty
    if world == "Jujutsu Kaisen":
        rank_bonus = {"Grade 4": 0, "Grade 3": 5, "Grade 2": 10, "Grade 1": 16, "Grade spécial": 25}.get(st.session_state.rank, 0)
        return (stats.get("Talent", 48) + stats.get("Santé", 50)) // 2 + st.session_state.technique_level * 4 + rank_bonus - fatigue_penalty
    if st.session_state.career == "Héros indépendant": return sum(stats.get(x, 50) for x in ["Talent", "Santé", "Intelligence"]) // 3 + st.session_state.get("fame", 0) // 4 + (5 if any(armor in st.session_state.inventory for armor in HERO_ARMORS) else 0) - fatigue_penalty
    if "Footballeur professionnel" in st.session_state.career or st.session_state.career == "Sportif professionnel":
        return stats.get("Talent", 48) + stats.get("Santé", 50) // 4 + st.session_state.get("fame", 0) // 5 - fatigue_penalty
    return (stats.get("Talent", 48) + stats.get("Santé", 50) + stats.get("Intelligence", 50)) // 3 + st.session_state.career_level * 3 - fatigue_penalty

def mission_title(world, rank):
    if world == "Monde réel":
        if st.session_state.career == "Héros indépendant": return "Affrontement contre un super-vilain SS" if rank == "SS" else f"Intervention héroïque de rang {rank}"
        if "Footballeur professionnel" in st.session_state.career: return "Finale de Ligue des champions · rang SS" if rank == "SS" else "Match de championnat" if rank in ("D", "C", "B") else f"Match décisif de rang {rank}"
        career_missions = {
            "Facteur": ["Tournée prioritaire · colis médical", "Recherche d’un destinataire disparu", "Distribution sous intempéries", "Courrier confidentiel à protéger"],
            "Analyste": ["Audit d’une fraude complexe", "Crise de données à résoudre", "Prévision d’un risque majeur", "Rapport stratégique contesté"],
            "Livreur": ["Livraison urgente en zone difficile", "Colis perdu à retrouver", "Tournée de nuit sous pression", "Transport d’un équipement fragile"],
            "Militaire": ["Évacuation d’une équipe isolée", "Reconnaissance en terrain difficile", "Convoi de secours sous escorte", "Opération de sauvetage coordonnée"],
            "Vendeur": ["Ouverture d’un point de vente stratégique", "Client mystère à convaincre", "Négociation d’un contrat majeur", "Gestion d’une crise en magasin"],
            "Infirmier": ["Renfort aux urgences", "Évacuation sanitaire", "Soins en situation de crise", "Coordination d’une équipe de nuit"],
            "Cuisinier": ["Service d’un banquet sous pression", "Concours culinaire régional", "Cuisine de secours après une panne", "Menu de gala à sauver"],
            "Professeur": ["Sortie scolaire à sécuriser", "Projet de classe à défendre", "Élève à retrouver avant un examen", "Concours inter-établissements"],
            "Ingénieur": ["Prototype à stabiliser avant lancement", "Panne critique d’infrastructure", "Audit de sécurité d’un système", "Projet d’innovation à défendre"],
            "Journaliste": ["Enquête à source confidentielle", "Témoin à protéger", "Reportage en zone de crise", "Dossier de corruption à vérifier"],
            "Sportif professionnel": ["Finale internationale", "Retour après blessure", "Duel contre le champion en titre", "Sélection nationale décisive"]}
        career = st.session_state.career.split(" ·")[0]
        if career in career_missions:
            title_index = st.session_state.mission_counts.get(rank, 0) % len(career_missions[career])
            return f"{career_missions[career][title_index]} · rang {rank}"
        return f"Mission professionnelle de rang {rank} · {st.session_state.career}"
    if world == "Kuroko Basket":
        basket_missions = {
            "D": ["Défi de fondamentaux · tirs sous pression", "Match amical contre le club voisin", "Défi de défense en un contre un"],
            "C": ["Qualifications du district", "Match retour contre un rival scolaire", "Tournoi des clubs de la préfecture"],
            "B": ["Demi-finale régionale", "Rencontre contre un lycée tête de série", "Match de barrage pour les nationales"],
            "A": ["Tournoi national · premier tour", "Duel tactique contre une équipe d’élite", "Match de qualification à élimination directe"],
            "S": ["Demi-finale de la Winter Cup", "Match décisif contre un cinq majeur", "Finale préfectorale sous haute tension"],
            "SS": ["Finale du tournoi national · rivalité ultime", "Défi SS contre un rival de la Génération", "Finale de la Winter Cup · dernier tir"]}
        titles = basket_missions[rank]
        return titles[st.session_state.mission_counts.get(rank, 0) % len(titles)]
    if world == "Naruto":
        ninja_missions = {"D": ["Retrouver un messager disparu", "Protéger une ferme des bandits", "Livrer un remède au poste frontière"], "C": ["Escorter un convoi à travers le col", "Récupérer un rouleau volé", "Démasquer un espion près du village"], "B": ["Intercepter une équipe ennemie", "Sauver des civils dans une zone contestée", "Protéger une négociation entre clans"], "A": ["Opération secrète derrière les lignes", "Neutraliser une menace sur la frontière", "Extraire un allié d’un territoire hostile"], "S": ["Affrontement contre une unité d’élite", "Défense d’un village allié", "Poursuite d’un déserteur de rang supérieur"], "SS": ["Affrontement contre l’Akatsuki · rang SS", "Opération secrète des cinq villages", "Menace majeure contre le village · rang SS"]}
        titles = ninja_missions[rank]
        return f"{titles[st.session_state.mission_counts.get(rank, 0) % len(titles)]} · {st.session_state.rank}"
    if world == "Jujutsu Kaisen":
        occult_missions = {"D": ["Enquête sur un objet maudit", "Exorcisme dans une maison vide", "Protection d’un témoin"], "C": ["Voile occulte dans une station", "Fléau rôdeur près d’une école", "Sauvetage dans un immeuble condamné"], "B": ["Exorcisme d’un fléau intelligent", "Évacuation d’un quartier sous voile", "Enquête sur une série de disparitions"], "A": ["Duel contre un fléau de haut grade", "Barrière instable dans un hôpital", "Sauvetage d’une équipe isolée"], "S": ["Fléau spécial aperçu dans le métro", "Affrontement dans un domaine fermé", "Incident occulte de niveau national"], "SS": ["Fléau inédit · menace de grade spécial", "Domaine inconnu · mission SS", "Exorcisme critique sous voile total"]}
        titles = occult_missions[rank]
        return f"{titles[st.session_state.mission_counts.get(rank, 0) % len(titles)]} · {st.session_state.rank}"

def mission_approaches(world):
    if world == "Kuroko Basket": return ["Jouer collectif", "Prendre la responsabilité du tir", "Provoquer le rival" ]
    if world == "Naruto": return ["Protéger les civils", "Suivre les ordres", "Prendre le parchemin à tout prix"]
    if world == "Jujutsu Kaisen": return ["Protéger les civils", "Exorciser proprement", "Utiliser le fléau comme appât", "Analyser son énergie", "Sceller la zone avant d’attaquer"]
    if st.session_state.career == "Héros indépendant": return ["Sauver les civils d’abord", "Neutraliser la menace", "Faire passer la réputation avant tout"]
    if world == "Monde réel":
        choices = {
            "Facteur": ["Sécuriser les médicaments", "Vérifier chaque adresse", "Accélérer la tournée au risque d’une erreur"],
            "Analyste": ["Vérifier les données à la source", "Alerter l’équipe conformité", "Publier avant la validation"],
            "Livreur": ["Protéger le colis", "Prévenir le destinataire du retard", "Prendre un raccourci risqué"],
            "Militaire": ["Protéger les civils", "Suivre le protocole de l’unité", "Poursuivre seul la cible"],
            "Vendeur": ["Écouter le client", "Demander l’aide du responsable", "Forcer la vente pour atteindre l’objectif"],
            "Infirmier": ["Prioriser le patient le plus urgent", "Coordonner avec l’équipe", "Agir seul sans attendre le renfort"],
            "Cuisinier": ["Réorganiser le service avec l’équipe", "Adapter le menu aux réserves", "Servir malgré le contrôle incomplet"],
            "Professeur": ["Assurer la sécurité des élèves", "Écouter les familles", "Protéger la réputation de l’établissement"],
            "Ingénieur": ["Interrompre le test pour vérifier la sécurité", "Mobiliser l’équipe technique", "Lancer le prototype malgré les doutes"],
            "Journaliste": ["Protéger ta source", "Recouper les faits", "Publier l’information sans seconde vérification"],
            "Footballeur professionnel": ["Jouer collectif", "Tenter le tir décisif", "Provoquer le défenseur adverse"],
            "Sportif professionnel": ["Respecter le plan de récupération", "Prendre le risque du duel", "Protéger ta santé et déclarer forfait"],
        }
        return choices.get(st.session_state.career.split(" ·")[0], ["Respecter les consignes", "Aider une personne en difficulté", "Prendre un raccourci risqué"])
    return ["Respecter les consignes", "Aider une personne en difficulté", "Prendre un raccourci risqué"]

def resolve_mission(world, rank, approach):
    difficulty = MISSION_LEVELS[rank]
    power = mission_power(world)
    chance = max(5, min(95, round(58 + (power - difficulty) * 1.15)))
    risk_base = {"D": 1, "C": 2, "B": 4, "A": 7, "S": 12, "SS": 20}[rank]
    armor_protection = 12 if any(armor in st.session_state.inventory for armor in HERO_ARMORS) else 0
    protection = armor_protection or (6 if "Équipement de mission" in st.session_state.inventory else 0)
    risk = max(0.2, min(48, risk_base + max(0, difficulty - power) * .32 - protection))
    good = any(word in approach.lower() for word in ["protéger", "civils", "aider", "collectif", "consignes", "proprement"])
    evil = any(word in approach.lower() for word in ["à tout prix", "réputation avant", "fléau comme appât", "provoquer"])
    st.session_state.honor = max(-100, min(100, st.session_state.honor + (4 if good else -4 if evil else 1)))
    st.session_state.fatigue = min(100, st.session_state.fatigue + 4 + list(MISSION_LEVELS).index(rank) * 2)
    roll = random.random() * 100
    title = mission_title(world, rank)
    st.session_state.mission_counts[rank] = st.session_state.mission_counts.get(rank, 0) + 1
    if world == "Jujutsu Kaisen":
        current_grade = st.session_state.rank
        st.session_state.mission_counts[current_grade] = st.session_state.mission_counts.get(current_grade, 0) + 1
    if roll < risk:
        st.session_state.dead = True
        st.session_state.death_reason = f"est mort(e) pendant {title.lower()}"
        result = f"{title} tourne au drame. Tu as perdu la vie."
        st.session_state.coins += st.session_state.pending_coins
        st.session_state.pending_coins = 0
        followup = f"La nouvelle de ta disparition pendant {title.lower()} atteint tes proches. La communauté organise un hommage."
    elif roll < risk + chance:
        reward = {"D": 120, "C": 220, "B": 400, "A": 700, "S": 1200, "SS": 2200}[rank]
        st.session_state.money += reward
        st.session_state.fame += {"D": 1, "C": 2, "B": 4, "A": 7, "S": 12, "SS": 20}[rank]
        result = f"Réussite ! {title} est accompli. Tu gagnes {reward} crédits et ta renommée augmente."
        st.session_state.mission_counts[f"{rank}_success"] = st.session_state.mission_counts.get(f"{rank}_success", 0) + 1
        update_career_skill(world, f"{title} {approach}", st.session_state.career)
        if rank in ("A", "S", "SS"): st.balloons()
        else: st.toast("Mission réussie !", icon="✨")
        if world == "Monde réel" and st.session_state.career not in ("Aucune", "Héros indépendant"):
            st.session_state.job_tasks += 1
            if st.session_state.job_tasks >= 3:
                st.session_state.career_level += 1
                st.session_state.job_tasks = 0
                result += f" Tes missions débloquent une promotion : niveau professionnel {st.session_state.career_level}."
        if world == "Kuroko Basket" and rank == "SS":
            st.session_state.stats["Basket"] = min(100, st.session_state.stats.get("Basket", 48) + 8)
            new_zones = [zone for zone in KUROKO_ZONES if zone not in st.session_state.zones]
            if new_zones:
                awakened_zone = random.choice(new_zones)
                st.session_state.zones.append(awakened_zone)
                result += f" Tu éveilles {awakened_zone} et gagnes une nouvelle compétence."
            if "Rival de l’équipe nationale" not in st.session_state.friends: st.session_state.friends.append("Rival de l’équipe nationale · joueur élite")
            result += " Tu gagnes une compétence de rivalité et peux recruter ton rival dans ton équipe."
        if world == "Monde réel" and "Footballeur professionnel" in st.session_state.career and rank == "SS":
            st.session_state.career = random.choice(["Footballeur professionnel · titulaire en Ligue des champions", "Footballeur professionnel · transfert international"])
            result += " Ta performance déclenche une offre de transfert pour un grand club européen."
        if world == "Naruto" and rank in ("S", "SS") and st.session_state.rank == "Chûnin": st.session_state.rank = "Jônin"
        if world == "Naruto" and rank in ("A", "S", "SS") and random.random() < (.12 if rank == "A" else .3):
            jutsu_list = CLAN_JUTSU.get(st.session_state.clan, CLAN_JUTSU["Inconnu"])
            if st.session_state.jutsu_level < len(jutsu_list):
                reward_jutsu = jutsu_list[st.session_state.jutsu_level]
                st.session_state.jutsu_level += 1
                st.session_state.known_jutsu.append(reward_jutsu)
                result += f" Le parchemin récupéré t’apprend {reward_jutsu}."
        if world == "Jujutsu Kaisen" and rank in ("S", "SS") and st.session_state.rank == "Grade 1": st.session_state.rank = "Grade spécial"
        followup = random.choice([f"Après {title.lower()}, une nouvelle piste ouvre une mission de suivi.", f"La réussite de {title.lower()} attire l’attention d’un rival qui réclame un défi.", f"Un contact rencontré pendant {title.lower()} transmet une information confidentielle.", f"Une conséquence inattendue de {title.lower()} change les priorités de ton équipe.", f"Un témoin de {title.lower()} revient avec une demande urgente.", f"Un nouveau commanditaire propose une mission liée à {title.lower()}.", f"Une équipe rivale prépare une riposte après {title.lower()}."])
    else:
        outcome = random.choices(["échec", "fuite", "capture"], weights=[45, 35, 20])[0]
        if outcome == "capture":
            st.session_state.captured = True
            capture_detail = random.choice(["un adversaire te reconnaît et exige des informations", "un complice inconnu semble avoir organisé ta capture", "tu es séparé(e) de ton équipe dans une cachette", "tes affaires sont confisquées, mais tu gardes un objet dissimulé", "un gardien te révèle qu’un autre prisonnier connaît ton rival"])
            result = f"Tu es capturé(e) pendant {title.lower()} : {capture_detail}. Il faudra organiser ta fuite avant de reprendre les missions."
            followup = random.choice(["Tes proches apprennent ta capture. Un contact mystérieux propose de t’aider à t’évader.", "Un message codé arrive jusqu’à ta cellule : quelqu’un prépare une diversion.", "Ton rival apprend ta capture et doit choisir s’il vient te secourir.", "Un changement de garde crée une occasion de fuite, mais un autre prisonnier veut partir avec toi."])
        elif outcome == "fuite":
            result = f"{random.choice([f'La situation dégénère pendant {title.lower()}.', f'Un imprévu fait échouer le plan pendant {title.lower()}.', f'Ton équipe se retrouve encerclée pendant {title.lower()}.', f'Une alerte inattendue bouleverse {title.lower()}.'])} Tu choisis de fuir et rentres blessé(e), mais vivant(e)."
            st.session_state.stats["Santé"] = max(0, st.session_state.stats["Santé"] - 5)
            followup = random.choice(["Un soigneur t’aide à récupérer. Un témoin affirme avoir vu quelque chose d’important sur les lieux.", "Ton équipe te reproche ta fuite, mais une preuve confirme que tu as évité le pire.", "Un proche remarque ta blessure et découvre un détail troublant sur la mission.", "La fuite laisse derrière toi un objet qui attire l’attention d’un nouvel adversaire."])
        else:
            result = random.choice([f"Échec : tu n’atteins pas l’objectif de {title.lower()}. Un nouveau plan sera nécessaire.", f"L’objectif de {title.lower()} t’échappe de peu. Une décision prise sur le terrain devra être revue.", f"Tu dois interrompre {title.lower()} après une erreur de jugement. Le rapport déclenche un débat dans ton équipe.", f"L’adversaire anticipe ton approche pendant {title.lower()}. Tu rentres sans récompense, mais avec une piste."])
            followup = random.choice([f"Ton échec sur {title.lower()} révèle un indice qui permet de préparer une nouvelle tentative.", f"Un témoin de {title.lower()} te contacte et propose une autre approche.", f"Ton rival entend parler de l’échec et t’envoie un défi inattendu.", f"Un objet récupéré après {title.lower()} ouvre une piste vers une nouvelle mission."])
    st.session_state.year["events"].append(result)
    st.session_state.year["activities"].append(f"{title} · {approach} · {result}")
    st.session_state.history.append({"age": st.session_state.age, "mission": title, "rang": rank, "choix": approach, "résultat": result, "honneur": st.session_state.honor})
    st.session_state.event_followups.append(followup)
    return result, chance, risk

def avatar_art(hair, gender, beard="Pas de barbe"):
    hair_paths = {
        "Courts et bouclés": "M25 43 Q20 15 48 15 Q76 15 72 45 L65 39 Q61 27 52 31 Q42 20 32 36 Z",
        "Courts et lisses": "M25 44 Q22 15 49 15 Q76 15 73 43 L65 34 Q52 39 39 31 L31 44 Z",
        "Mi-longs": "M24 48 Q20 14 49 14 Q78 14 74 49 L68 62 L64 37 Q51 27 37 36 L32 62 Z",
        "Longs": "M24 50 Q19 13 49 13 Q79 13 74 50 L72 79 L63 64 L64 37 Q49 29 36 37 L34 78 L27 66 Z",
        "Ébouriffés": "M25 46 L20 28 L34 32 L37 15 L48 26 L59 14 L61 31 L77 25 L71 48 L65 39 Q50 28 36 39 Z",
        "Tressés": "M25 48 Q20 15 49 15 Q78 15 73 49 L70 78 L64 62 L65 37 Q50 29 36 37 L33 78 L27 65 Z",
    }
    hair_color = "#30221f" if gender == "Garçon" else "#38234f" if gender == "Fille" else "#244657"
    beard_shape = '<path d="M34 57 Q49 70 64 57 L61 68 Q49 78 37 68 Z" fill="#49332d"/>' if gender != "Fille" and beard != "Pas de barbe" else ""
    svg = f'''<svg viewBox="0 0 100 100" width="96" height="96" role="img" aria-label="Aperçu du personnage">
    <circle cx="50" cy="50" r="49" fill="#e7f2ff"/><path d="M20 100 Q22 73 50 72 Q78 73 80 100" fill="#4679a5"/>
    <ellipse cx="50" cy="49" rx="25" ry="31" fill="#e9b995"/>
    <path d="{hair_paths.get(hair, hair_paths['Courts et lisses'])}" fill="{hair_color}"/>
    <ellipse cx="40" cy="49" rx="2.1" ry="2.8" fill="#263546"/><ellipse cx="60" cy="49" rx="2.1" ry="2.8" fill="#263546"/>
    <path d="M44 62 Q50 66 56 62" fill="none" stroke="#a94f58" stroke-width="2" stroke-linecap="round"/>{beard_shape}</svg>'''
    return f'<div class="avatar">{svg}<br><b>{hair}</b><br><span class="muted">{beard if gender != "Fille" else ""}</span></div>'

def _yearly_event_candidate(world, age):
    paths = st.session_state.get("story_paths", [])
    active_npcs = [npc for npc in st.session_state.get("npc_roster", []) if npc.get("status") == "Présent·e"]
    if active_npcs and random.random() < .20:
        npc = random.choice(active_npcs)
        if npc.get("role") == "Rival": return f"Ton rival {npc['name']} te défie à nouveau après votre dernier face-à-face."
        if npc.get("role") in ("Mentor", "Sensei") and age >= 10: return f"{npc['name']}, ton sensei, t’invite à une séance spéciale et attend de voir si tu as retenu ses conseils."
        if npc.get("role") == "Ami": return f"{npc['name']} te demande de l’aide pour une décision importante et se souviendra de ta réponse."
    if world == "Monde réel" and age >= 16 and "superhero_origin" not in paths and random.random() < .025:
        return "Un insecte inconnu te mord lors d’une sortie. Des capacités inhabituelles apparaissent et une nouvelle histoire s’ouvre."
    if world == "Monde réel" and age >= 18 and st.session_state.career not in ("Aucune", "Héros indépendant") and random.random() < .48:
        career = st.session_state.career.split(" ·")[0]
        work_events = {
            "Facteur": ["Une tournée est interrompue par une tempête : des médicaments urgents doivent arriver avant la nuit.", "Un chien perdu t’accompagne pendant ta tournée et connaît un chemin que personne n’emprunte.", "Une lettre sans adresse complète porte un message important pour une famille isolée.", "Un quartier réclame un nouveau passage après plusieurs colis disparus."],
            "Analyste": ["Un indicateur incohérent dans ton rapport révèle une fraude qui menace un client.", "Une panne de données efface une partie des résultats avant une présentation décisive.", "Une collègue découvre que le modèle prévoit un risque que personne n’avait vu.", "La direction te demande d’expliquer publiquement une conclusion contestée."],
            "Livreur": ["Un colis fragile doit être livré avant la fermeture d’un hôpital, mais l’adresse est inaccessible.", "Une livraison disparaît du système et un client t’accuse à tort.", "Une route barrée te force à choisir entre retard et détour dangereux.", "Un client âgé ne répond pas et le colis contient un objet dont il a besoin."],
            "Militaire": ["Un exercice de secours devient réel après un accident sur une route isolée.", "Une équipe manque à l’appel pendant une patrouille et la radio grésille.", "Une décision rapide protège ton unité, mais pourrait enfreindre un ordre reçu.", "Une mission de logistique se transforme en évacuation sous pression."],
            "Vendeur": ["Une cliente revient avec un objet défectueux et une histoire qui change la priorité du magasin.", "Une erreur de caisse crée un manque important juste avant l’inventaire.", "Un client célèbre veut un article rare et le magasin n’en possède qu’un.", "Une nouvelle recrue panique pendant une journée de forte affluence."],
            "Infirmier": ["Un patient isolé refuse de rentrer chez lui malgré la fin des soins.", "Une panne électrique perturbe le service au moment d’une urgence.", "Un enfant te confie un détail qui aide l’équipe médicale à comprendre son état.", "Une famille demande une seconde explication avant une décision importante."],
            "Cuisinier": ["Une livraison de produits manque avant le service le plus chargé de la saison.", "Un critique culinaire arrive incognito pendant une soirée complète.", "Un jeune collègue se blesse et l’équipe doit réorganiser le service.", "Une recette familiale oubliée peut sauver le menu d’un événement."],
            "Professeur": ["Un élève brillant cesse soudainement de rendre ses devoirs et te demande de garder un secret.", "Une sortie scolaire est retardée et un élève manque à l’appel.", "Une dispute entre deux familles éclate à la sortie de l’école.", "Une classe prépare un projet qui pourrait sauver la bibliothèque locale."],
            "Ingénieur": ["Un prototype échoue lors de son premier essai public et l’équipe cherche la cause.", "Une panne menace un pont piétonnier quelques heures avant son ouverture.", "Une jeune inventrice demande ton aide pour protéger son idée.", "Un test révèle une faille de sécurité que le calendrier du projet avait ignorée."],
            "Journaliste": ["Une source anonyme te remet des documents et te demande de protéger son identité.", "Un témoin retire son témoignage juste avant la publication de ton enquête.", "Deux versions opposées circulent après un incident dans ta ville.", "Un article ancien que tu as écrit aide une famille à retrouver un proche."],
            "Footballeur professionnel": ["Un recruteur étranger assiste à l’entraînement sans annoncer le club qu’il représente.", "Ton capitaine se blesse avant un match décisif et le vestiaire attend ta réaction.", "Une séance sous la pluie révèle une faiblesse tactique de l’équipe.", "Un jeune joueur de l’académie te demande de l’aider à gérer la pression."],
            "Sportif professionnel": ["Un sponsor propose un contrat qui entre en conflit avec tes valeurs.", "Une blessure légère arrive avant une compétition importante.", "Un rival change de catégorie et réclame un duel officiel.", "Ton équipe médicale propose un programme qui pourrait transformer ta saison."]}
        options = work_events.get(career, work_events["Analyste"])
        return random.choice(options)
    if world == "Naruto" and st.session_state.get("rank") == "Jônin" and age >= 25 and random.random() < .18:
        return "Le Hokage annonce son retrait. Le conseil étudie les noms des successeurs et ton travail de jônin est cité."
    if world == "Naruto" and age >= 12 and st.session_state.get("rank") in ("Genin", "Chûnin", "Jônin") and "mentor_ermite" not in paths and random.random() < .08:
        return "Un mentor ermite itinérant a observé ton contrôle du chakra et propose un entraînement exigeant."
    if world == "Naruto" and age >= 8 and not st.session_state.get("tailed_beast") and "beast_seal" not in paths and random.random() < .025:
        return "Un sceau ancien s’active pendant une cérémonie : un démon à queue cherche un nouvel hôte."
    if world == "Naruto" and age >= 12 and st.session_state.get("rank") in ("Genin", "Chûnin", "Jônin") and random.random() < .25:
        return "Un jônin cherche un ninja fiable pour une mission spéciale de reconnaissance à la frontière."
    if world == "Jujutsu Kaisen" and age >= 15 and st.session_state.get("rank", "").startswith("Grade") and random.random() < .25:
        return "Ton mentor te propose de tenter ta chance pour consulter un dossier confidentiel sur un fléau inédit."
    if world == "Kuroko Basket" and "basket_recrutement" in paths and age >= 15 and random.random() < .45:
        return random.choice(["Après tes performances, un recruteur t’invite à un tournoi de jeunes espoirs.", "Une académie propose un essai privé à ton équipe.", "La presse sportive publie un portrait de ton club et de ses joueurs."])
    if world == "Kuroko Basket" and "camp_basket" in paths and age >= 13 and random.random() < .4:
        return random.choice(["Le camp d’été te rappelle : une place s’est libérée dans le groupe avancé.", "Un entraîneur du camp veut observer tes progrès lors d’un match.", "Tes amis du camp te proposent de former une équipe pour un tournoi."])
    if world == "Kuroko Basket" and age >= 15 and "Club de basket" in st.session_state.clubs and len(st.session_state.zones) < len(KUROKO_ZONES) and random.random() < .18:
        return "Dans un match serré, tu sens ta Zone s’éveiller. Ton entraîneur te propose un défi pour tenter de la maîtriser."
    if random.random() < .62:
        surprises = {
            "Monde réel": ["Un ancien camarade reprend contact et te propose une sortie.", "Une panne générale bouleverse les habitudes de la ville.", "Tu trouves un portefeuille et dois décider quoi en faire.", "Un animal perdu te suit jusque chez toi.", "Une personne de ton entourage t’annonce une grande nouvelle.", "Un voisin organise une collecte après un incendie dans son immeuble.", "Une vidéo tournée dans le métro te rend témoin d’un incident inattendu.", "Une grève des transports change tes plans au dernier moment.", "Un petit commerce du quartier risque de fermer et ses habitués s’organisent.", "Un concours local t’ouvre une porte que tu n’avais jamais envisagée.", "Un inconnu te remet un objet perdu qui semble appartenir à quelqu’un de ta famille.", "Une tempête coupe l’électricité et les voisins s’entraident.", "Un ancien professeur t’envoie une invitation à une cérémonie de retrouvailles.", "Tu découvres une erreur sur un document officiel qui pourrait coûter cher.", "Une association te propose de participer à une action solidaire.", "Un ami annule un voyage au dernier moment et te propose sa place.", "Une rumeur circule sur un nouveau projet qui va transformer ton quartier.", "Un concours de talents est organisé dans ta ville.", "Tu reçois par erreur un colis qui contient un indice sur son véritable destinataire.", "Un proche te demande de l’accompagner à un rendez-vous difficile."],
            "Kuroko Basket": ["Une blessure légère pendant l’échauffement te force à adapter ton jeu.", "Un rival te lance un défi inattendu après l’entraînement.", "Un ancien joueur partage avec toi un conseil décisif.", "Un coéquipier manque le match : il faut revoir la stratégie.", "Une vidéo de ton dernier match devient virale et attire un agent.", "Un gymnase ferme pour travaux à quelques jours d’un tournoi.", "Un coéquipier cache une douleur pour ne pas perdre sa place.", "Une équipe inconnue maîtrise une défense qui neutralise vos meilleurs joueurs.", "Un tournoi de rue propose un format trois contre trois avec une récompense rare.", "Un ancien rival te demande de t’entraîner avec lui en secret.", "Ton entraîneur confie le dernier tir à un joueur inattendu.", "Un recruteur compare ton jeu à celui d’un autre espoir.", "Une équipe perd son capitaine et te demande de mener l’échauffement.", "Une séance dans une salle vide te permet de travailler un geste signature.", "Le tableau du tournoi vous place face à une équipe que vous n’avez jamais battue."],
            "Naruto": ["Une alerte retentit : un messager n’est pas revenu de mission.", "Un marchand itinérant propose un parchemin dont l’origine est incertaine.", "Un rival t’aide à éviter un piège pendant l’entraînement.", "La radio annonce une rencontre diplomatique surprise.", "Un ancien rouleau de ton clan réagit à ton chakra.", "Une patrouille découvre des traces qui s’arrêtent au milieu d’une rivière.", "Un jeune ninja disparaît après avoir reçu une lettre anonyme.", "Un marchand demande une escorte, mais refuse de révéler sa destination.", "Un fragment de masque de l’Akatsuki est retrouvé près d’un relais.", "Une dispute éclate entre deux villages au sujet d’un pont frontalier.", "Un animal messager blessé transporte un code que ton équipe ne reconnaît pas.", "Un parchemin scellé porte le nom de ton clan et une date ancienne.", "Un rival te propose une alliance temporaire pour réussir un examen.", "La radio annonce une éclipse et des mouvements suspects dans les montagnes.", "Un ninja errant demande l’asile au village, mais le conseil hésite."],
            "Jujutsu Kaisen": ["Un rideau occulte se lève sans prévenir dans un quartier animé.", "Un fléau mineur s’attache à un objet trouvé sur ton chemin.", "Un autre élève te demande de l’aide pour une mission urgente.", "Une rumeur annonce l’arrivée d’un exorciste de renom.", "Un vieux cinéma rejoue le même film chaque nuit, même après sa fermeture.", "Une station de métro compte un quai de plus sur les plans que dans la réalité.", "Un fléau semble répéter les derniers mots de ses victimes.", "Un talisman inconnu apparaît dans le casier d’un élève absent.", "Un rideau se déplace avec les passagers d’un bus nocturne.", "Une trace occulte mène à un hôpital qui n’existe plus sur les cartes.", "Un exorciste vétéran te laisse un outil maudit sans explication.", "Un élève de Kyoto disparaît après un échange de messages codés.", "Un fléau protège une personne au lieu de l’attaquer.", "Une vieille photo change chaque fois qu’on la regarde.", "Un rapport classé révèle que deux incidents éloignés partagent la même signature."]}
        return random.choice(surprises[world])
    family = st.session_state.get("family", [])
    if family and random.random() < .24:
        person = random.choice(family).split(" ·")[0]
        personal_events = [f"{person} te demande de garder un secret qui pourrait changer votre relation.", f"{person} reçoit une nouvelle importante et veut être la première personne à t’en parler.", f"{person} traverse une période difficile et n’ose pas demander de l’aide.", f"{person} t’invite à une sortie qui réunit des proches que tu n’as pas vus depuis longtemps.", f"{person} fait un choix inattendu qui bouleverse les projets de la famille.", f"{person} te présente une nouvelle personne qui pourrait devenir un allié ou un rival.", f"{person} retrouve un objet de famille accompagné d’une histoire jusque-là inconnue.", f"{person} célèbre une réussite et te propose de partager son prochain projet."]
        return random.choice(personal_events)
    if age < 3: return random.choice(["Tu fais tes premiers pas sous les encouragements de ta famille.", "Une promenade avec un proche devient ton grand souvenir de l’année.", "Tu découvres un nouveau jeu et réclames une histoire avant de dormir."])
    if world == "Monde réel":
        if age < 6: return random.choice(["La rentrée en maternelle approche : tu découvres ta classe.", "Un proche t’emmène au parc et tu te fais un nouvel ami.", "Une sortie en famille marque les vacances."])
        if age < 11: return random.choice(["Une sortie scolaire te fait découvrir un nouvel endroit.", "Le club sportif local ouvre ses inscriptions.", "Tu réussis un projet à l’école et ta famille fête ça."])
        if age < 15: return random.choice(["Le collège organise une journée de découverte des métiers.", "Les inscriptions aux clubs et équipes sportives sont ouvertes.", "Un stage d’observation se prépare pour les élèves."])
        if age < 18: return random.choice(["Le lycée annonce ses options et ses équipes sportives.", "Une entreprise locale propose des stages de découverte.", "Les examens de fin d’année approchent."])
        if age < 23: return random.choice(["Les inscriptions à l’université et aux formations sont ouvertes.", "Un forum de stages et d’emplois se tient près de chez toi.", "Un choix d’orientation important se présente."])
        return random.choice(["Une offre d’emploi correspondant à ton profil est publiée.", "Un proche te demande conseil pour un choix important.", "Une nouvelle formation professionnelle ouvre dans ta ville."])
    if world == "Kuroko Basket":
        if age < 11: return random.choice(["Tu rejoins un atelier de mini-basket.", "Un match local t’inspire à t’entraîner.", "Tes proches remarquent ta précision au panier."])
        if age < 15: return random.choice(["Le club du collège organise ses sélections.", "Un tournoi régional approche : ton équipe s’entraîne dur.", "Ton entraîneur te propose un poste à travailler."])
        if age < 18: return random.choice(["Les sélections du lycée commencent. Les recruteurs observent les joueurs.", "Un match serré met ton esprit d’équipe à l’épreuve.", "Un tournoi inter-lycées attire plusieurs observateurs."])
        return random.choice(["Une équipe universitaire t’invite à un essai.", "Un recruteur suit les résultats de ton équipe.", "Une opportunité de camp d’entraînement se présente."])
    if world == "Naruto":
        if age < 6: return random.choice(["Ton chakra se manifeste pour la première fois.", "Ta famille partage une histoire sur ton clan.", "Le village célèbre une fête traditionnelle."])
        if age < 12: return random.choice(["À l’académie, tu apprends les bases du chakra.", "Une rumeur évoque une tension à la frontière.", "Un proche t’aide à maîtriser un nouvel exercice."])
        if age < 15: return random.choice(["L’examen genin approche : ton équipe révise les bases.", "Une mission de rang D est proposée aux jeunes ninjas.", "La radio annonce une rencontre diplomatique entre villages."])
        return random.choice(["Une mission adaptée à ton grade est publiée au bureau des ninjas.", "L’examen chûnin est annoncé pour les équipes qualifiées.", "La radio signale une tension à la frontière du pays."])
    if age < 15: return random.choice(["Une activité occulte est repérée près de ton école.", "Ton énergie occulte se manifeste pendant une sortie.", "Un mentor remarque un potentiel inhabituel."])
    return random.choice(["Une mission d’exorcisme adaptée à ton niveau est signalée.", "Une présence inquiétante est détectée près de la gare.", "L’école organise un entraînement entre élèves."])

def yearly_event(world, age):
    followups = st.session_state.event_followups
    memory = st.session_state.event_memory
    while followups and followups[0] in memory:
        followups.pop(0)
    if followups:
        event = followups.pop(0)
    else:
        event = _yearly_event_candidate(world, age)
        for _ in range(8):
            if event not in memory: break
            event = _yearly_event_candidate(world, age)
    st.session_state.event_memory.append(event)
    st.session_state.event_memory = st.session_state.event_memory[-30:]
    return event

init()
st.markdown('<div class="hero"><h1>✨ DESTINS</h1><p>Une vie, mille chemins. Chaque choix écrit la suite.</p></div>', unsafe_allow_html=True)

if not st.session_state.started:
    left, right = st.columns([1.1, .9], gap="large")
    with left:
        st.markdown('<div class="card"><div class="big">1 · Choisis ton univers</div><p class="muted">Sélectionne l’univers dans lequel tu veux vivre.</p></div>', unsafe_allow_html=True)
        world = st.radio("Univers", list(WORLDS), format_func=lambda item: f"{WORLDS[item]['icon']}  {item}", horizontal=True, label_visibility="collapsed")
        first = st.text_input("Prénom", "Rick")
        surname_choice = st.selectbox("Nom / clan", ["Attribution aléatoire"] + WORLDS[world]["families"])
        gender = st.selectbox("Personnage", ["Garçon", "Fille", "Non-binaire"])
        orientation = st.selectbox("Orientation romantique", SEXUALITIES, help="Ce choix définit les rencontres possibles de ton personnage.")
        hair = st.selectbox("Coupe de cheveux", HAIR)
        beard = st.selectbox("Barbe", BEARDS, index=0, disabled=(gender == "Fille"))
        st.caption(f"🪙 Pièces Destin disponibles : {st.session_state.coins}")
        available_traits = min(4, max(1, st.session_state.coins // 50))
        birth_traits = st.multiselect("Attributs de naissance · 50 pièces chacun", ["Beauté +10", "Talent +10", "Santé +10", "Intelligence +10"], max_selections=available_traits, disabled=st.session_state.coins < 50, help="Gagne ou conserve des pièces Destin pour acheter des attributs à la naissance.")
        if world == "Naruto": st.info("Le clan sélectionné détermine ton affinité chakra et tes techniques de départ.")
        st.markdown("#### Aperçu de ton personnage")
        avatar_col, start_col = st.columns([1, 1.4])
        with avatar_col:
            st.markdown(avatar_art(hair, gender, beard), unsafe_allow_html=True)
        with start_col:
            st.write("")
            if st.button("✨  Créer mon personnage", type="primary", use_container_width=True):
                family = random.choice(WORLDS[world]["families"]) if surname_choice == "Attribution aléatoire" else surname_choice
                place = random.choice(WORLDS[world]["places"])
                stats = {"Bonheur": 72, "Santé": 88, "Intelligence": 54, "Talent": 48, "Beauté": 55}
                if world == "Kuroko Basket": stats["Basket"] = 48
                for trait in birth_traits:
                    stat = trait.split(" +")[0]
                    stats[stat] = min(100, stats[stat] + 10)
                st.session_state.coins -= len(birth_traits) * 50
                clan = family if world == "Naruto" else ""
                pupil_power = "Sharingan" if clan == "Uchiha" else "Byakugan" if clan == "Hyûga" else ""
                st.session_state.update(started=True, world=world, first=first.strip() or "Alex", surname=family, gender=gender, orientation=orientation, hair=hair, beard=beard, avatar="", place=place, clan=clan, pupil_power=pupil_power, pupil_stage=0, known_jutsu=[], mentor_jutsu=[], mentor_training=[], mentor_progress={}, tailed_beast="", beast_mastery=0, partner=None, dating_candidate=None, hero_affiliation="", npc_roster=[], npc_memories=[], career_skills=career_skill_profile(world), fatigue=10, age=0, rank="Étudiant de l’académie" if world == "Naruto" else "Élève", career="Aucune", career_level=0, job_tasks=0, technique=random.choice(OCCULT_TECHNIQUES) if world == "Jujutsu Kaisen" else "Aucune", techniques=[], zones=[], technique_level=1, jutsu_level=0, mission_counts={}, year={"activities": [], "events": [f"{first or 'Alex'} {family} naît à {place}. Sa famille l’accueille dans ce nouvel univers."], "close": [], "training_counts": {}, "world_news": world_news(world), "event_resolved": False}, family=family_members(world, family), friends=[], children=[], clubs=[], history=[], story_paths=[], stats=stats, money=1200, dead=False, death_reason="", generation=1, honor=0, fame=0, inventory=[], captured=False, event_followups=[], event_memory=[])
                st.rerun()
    with right:
        st.markdown('<div class="card"><div class="big">2 · Prévisualise ton avatar</div><p>Ton personnage t’accompagnera dans sa chronologie. La coiffure et la barbe évolueront avec le temps.</p></div>', unsafe_allow_html=True)
        descriptions = {"Monde réel": "École, loisirs, orientation et métiers.", "Kuroko Basket": "Clubs, matchs, entraînement et recrutement.", "Naruto": "Clans, chakra, missions et examens ninja.", "Jujutsu Kaisen": "École d’exorcisme, fléaux et missions occultes."}
        for title, data in WORLDS.items(): st.markdown(f'<div class="card">{data["icon"]} <b>{title}</b><br><span class="muted">{descriptions[title]}</span></div>', unsafe_allow_html=True)
else:
    world, age = st.session_state.world, st.session_state.age
    if world == "Kuroko Basket": st.session_state.stats.setdefault("Basket", 48)
    if "world_news" not in st.session_state.year:
        st.session_state.year["world_news"] = world_news(world)
    name = f"{st.session_state.first} {st.session_state.surname}"
    stage, stage_icon = age_stage(age)
    col_avatar, col_info = st.columns([.55, 2.45], gap="small")
    with col_avatar: st.markdown(avatar_art(st.session_state.hair, st.session_state.gender, st.session_state.beard if age >= 16 else "Pas de barbe"), unsafe_allow_html=True)
    with col_info:
        st.markdown(f"### {WORLDS[world]['icon']} {name}")
        st.markdown(f"**{stage_icon} {stage} · {age} ans**　|　📍 {st.session_state.place}　|　🏷️ {st.session_state.rank}　|　💰 {st.session_state.money:,} crédits　|　⚖️ Honneur {st.session_state.honor:+d}")
        if world == "Monde réel" and st.session_state.career != "Aucune": st.caption(f"💼 {st.session_state.career} · niveau {st.session_state.career_level}")
        if world == "Jujutsu Kaisen": st.caption(f"🌀 Technique : {st.session_state.technique} · maîtrise {st.session_state.technique_level}/3 · découvertes {len(st.session_state.techniques)}/{len(OCCULT_TECHNIQUES)}")
        if world == "Kuroko Basket" and st.session_state.zones: st.caption("🏀 Zones éveillées : " + " · ".join(st.session_state.zones))
        if world == "Naruto": st.caption(f"🍥 Chakra {CHAKRA.get(st.session_state.clan, 'Vent')} · Missions de ce grade : {st.session_state.mission_counts.get(st.session_state.rank, st.session_state.mission_counts.get('D', 0))}")
        if world == "Jujutsu Kaisen" and st.session_state.rank.startswith("Grade"):
            st.caption(f"📋 Missions réussies à ce grade : {st.session_state.mission_counts.get(st.session_state.rank, 0)} · 2 missions ouvrent l’évaluation suivante")
        if world == "Naruto": st.caption(f"Clan {st.session_state.clan} · affinité chakra : {CHAKRA.get(st.session_state.clan, 'Vent')} · jutsu appris {st.session_state.jutsu_level}/{len(CLAN_JUTSU.get(st.session_state.clan, CLAN_JUTSU['Inconnu']))}")
        if world == "Naruto" and st.session_state.get("pupil_power"): st.caption(f"👁️ {st.session_state.pupil_power} · techniques héréditaires {st.session_state.pupil_stage}/{len(PUPIL_TECHNIQUES[st.session_state.pupil_power])}")
        if world == "Naruto" and st.session_state.get("tailed_beast"): st.caption(f"🌀 {st.session_state.tailed_beast} · maîtrise {st.session_state.beast_mastery}/3")
        if world == "Monde réel" and st.session_state.get("hero_affiliation"): st.caption(f"🦸 Association : {st.session_state.hero_affiliation}")
        if st.session_state.get("partner"): st.caption(f"💞 En couple avec {st.session_state.partner['name']}")
    if st.session_state.dead:
        st.error(f"Fin de vie : {name} est décédé(e) {st.session_state.death_reason}.")
        if st.session_state.children:
            heir = st.selectbox("Choisis l’enfant qui poursuivra la dynastie", st.session_state.children)
            if st.button("Continuer avec cet enfant", type="primary", use_container_width=True):
                st.session_state.generation = st.session_state.get("generation", 1) + 1
                st.session_state.first = heir.split()[0]
                st.session_state.age = 0
                st.session_state.dead = False
                st.session_state.death_reason = ""
                st.session_state.stats = {"Bonheur": 72, "Santé": 88, "Intelligence": 54, "Talent": 48, "Beauté": 55}
                st.session_state.gender = random.choice(["Garçon", "Fille", "Non-binaire"])
                st.session_state.hair = random.choice(HAIR)
                st.session_state.beard = "Pas de barbe"
                st.session_state.challenges = []
                st.session_state.pending_coins = 0
                st.session_state.clubs = []
                st.session_state.rank = "Élève" if world != "Naruto" else "Étudiant de l’académie"
                st.session_state.career = "Aucune"
                st.session_state.career_level = 0
                st.session_state.job_tasks = 0
                st.session_state.mission_counts = {}
                st.session_state.honor = 0
                st.session_state.fame = 0
                st.session_state.inventory = []
                st.session_state.captured = False
                st.session_state.event_followups = []
                st.session_state.event_memory = []
                st.session_state.technique = random.choice(OCCULT_TECHNIQUES) if world == "Jujutsu Kaisen" else "Aucune"
                st.session_state.techniques = []
                st.session_state.zones = []
                st.session_state.jutsu_level = 0
                st.session_state.known_jutsu = []
                st.session_state.mentor_jutsu = []
                st.session_state.pupil_power = "Sharingan" if world == "Naruto" and st.session_state.surname == "Uchiha" else "Byakugan" if world == "Naruto" and st.session_state.surname == "Hyûga" else ""
                st.session_state.pupil_stage = 0
                st.session_state.mentor_training = []
                st.session_state.mentor_progress = {}
                st.session_state.tailed_beast = ""
                st.session_state.beast_mastery = 0
                st.session_state.partner = None
                st.session_state.dating_candidate = None
                st.session_state.hero_affiliation = ""
                st.session_state.orientation = random.choice(SEXUALITIES)
                st.session_state.npc_roster = []
                st.session_state.npc_memories = []
                st.session_state.career_skills = career_skill_profile(world)
                st.session_state.fatigue = 10
                st.session_state.technique_level = 1
                st.session_state.year = {"activities": [], "events": [f"{heir} reprend le flambeau de la famille {st.session_state.surname}."], "close": [], "training_counts": {}, "world_news": world_news(world), "event_resolved": False}
                st.session_state.family = [f"{name} · parent décédé · {st.session_state.career}"] + family_members(world, st.session_state.surname)[:1]
                st.rerun()
        else:
            st.info("Tu n’as pas d’enfant pour reprendre la dynastie. Dans une prochaine partie, tu pourras fonder une famille.")
        st.stop()
    if st.button("⏭ Année +", key="advance_year_fixed", type="primary"):
        advance_year()
    tab_year, tab_actions, tab_rankings, tab_next, tab_career, tab_life, tab_shop, tab_save = st.tabs(["📖 Année", "🎯 Actions", "🏆 Classement", " ", "💼 Carrière", "👥 Proches", "🛍️ Boutique", "💾 Sauver"])

    with tab_year:
        st.markdown(f"#### {stage_icon} {stage} · année de tes {age} ans")
        ev_col, close_col = st.columns([1.15, .85], gap="large")
        with ev_col:
            st.markdown("**📖 Ton événement de l’année**")
            for event in st.session_state.year["events"]: st.markdown(f'<div class="card event">{event}</div>', unsafe_allow_html=True)
            event_text = " ".join(st.session_state.year["events"]).lower()
            work_event = world == "Monde réel" and age >= 18 and st.session_state.career != "Aucune" and any(word in event_text for word in ["tournée", "colis", "destinataire", "fraude", "données", "prototype", "infrastructure", "patient", "urgences", "service", "livraison", "client", "enquête", "témoin", "capitaine", "recruteur étranger", "contrat qui entre", "compétition importante", "sélection nationale", "élève brillant", "sortie scolaire", "rapport stratégique", "équipe isolée", "exercice de secours", "inventaire", "recette familiale", "témoignage"])
            opportunity = work_event or any(word in event_text for word in ["recruteurs", "recruteur", "camp", "essai", "sélections", "selection", "stage", "occasion", "invité", "invite", "recrutement", "hokage", "offre d’emploi", "emploi", "mission spéciale", "dossier confidentiel", "mission de suivi", "rival réclame", "information pour la suite", "tentative", "super-vilain", "défi d’équipe", "tournoi régional", "nouvelle affectation", "piste près de", "trace occulte", "affaire qui vient", "ta Zone s’éveiller", "dossier lié au métier", "mord", "capacités inhabituelles", "mentor ermite", "démon à queue"])
            if opportunity:
                reactions = ["Tenter ma chance", "Demander conseil à un proche", "Laisser passer cette occasion"]
            elif "ton rival" in event_text and "déf" in event_text:
                reactions = ["Relever le défi", "Lui parler franchement", "Demander conseil à un proche"]
            elif "sensei" in event_text or "mentor" in event_text:
                reactions = ["Accepter l’entraînement", "Poser des questions", "Décliner poliment"]
            elif "demande de l’aide" in event_text:
                reactions = ["L’aider", "L’écouter d’abord", "Refuser et expliquer pourquoi"]
            elif age < 3:
                reactions = ["Demander à un proche de t’aider", "Observer calmement", "Tendre la main"]
            elif world == "Naruto" and age >= 12:
                reactions = ["Accepter la mission", "Demander conseil à l’équipe", "Prévenir le responsable du village"]
            elif world == "Jujutsu Kaisen" and age >= 15:
                reactions = ["Partir avec le mentor", "Demander du renfort", "Examiner les lieux d’abord"]
            elif world == "Monde réel" and age >= 18 and st.session_state.career != "Aucune":
                reactions = ["Prendre les choses en main", "Demander conseil à un proche", "Suivre le protocole"]
            elif world == "Kuroko Basket" and age >= 11:
                reactions = ["Relever le défi", "En parler à l’entraîneur", "Encourager l’équipe"]
            elif age < 6:
                reactions = ["En parler à un parent", "Participer avec les autres", "Prendre le temps d’observer"]
            else:
                reactions = ["Saisir l’occasion", "Demander conseil à un proche", "Inviter un ami à participer"]
            response = st.selectbox("Comment réagis-tu à cet événement ?", reactions, key=f"event_choice_{age}")
            event_button = "🎲 Tenter ma chance" if opportunity and response == "Tenter ma chance" else "Réagir à l’événement"
            if st.button(event_button, disabled=st.session_state.year.get("event_resolved", False)):
                st.session_state.year["event_resolved"] = True
                if opportunity and response == "Tenter ma chance":
                    skill = st.session_state.stats.get("Basket", st.session_state.stats.get("Talent", 50)) if world == "Kuroko Basket" else (st.session_state.stats.get("Intelligence", 50) + st.session_state.stats.get("Talent", 50)) // 2 if work_event else st.session_state.stats.get("Intelligence", 50)
                    if world == "Kuroko Basket" and "Club de basket" in st.session_state.clubs: skill += 12
                    chance = min(85, max(20, 25 + skill // 2))
                    if random.randint(1, 100) <= chance:
                        if world == "Kuroko Basket" and "zone" in event_text:
                            path, title = "zone_eveil", "L’éveil de ta Zone"
                            new_zones = [zone for zone in KUROKO_ZONES if zone not in st.session_state.zones]
                            if new_zones:
                                awakened = random.choice(new_zones)
                                st.session_state.zones.append(awakened)
                                st.session_state.stats["Basket"] = min(100, st.session_state.stats.get("Basket", 48) + 6)
                                detail = f"Tu entres dans {awakened}. Cette concentration exceptionnelle révèle une nouvelle facette de ton jeu."
                            else: detail = "Ton niveau de concentration s’améliore encore. Tu as déjà éveillé toutes les Zones connues."
                        elif world == "Kuroko Basket" and ("camp" in event_text):
                            path, title = "camp_basket", "Le camp des espoirs"
                            detail = "Tu réussis la sélection ! Tu es invité(e) au camp d’été. Une nouvelle histoire s’ouvre : entraînements avancés, nouvelles amitiés et rivalités."
                        elif world == "Kuroko Basket":
                            path, title = "basket_recrutement", "Le regard des recruteurs"
                            detail = "Tu impressionnes les recruteurs ! Une nouvelle histoire s’ouvre autour des tournois d’espoirs et des essais d’académie."
                        elif world == "Monde réel" and ("mord" in event_text or "capacités inhabituelles" in event_text):
                            path, title = "superhero_origin", "Le pouvoir inattendu"
                            detail = "La morsure réveille des aptitudes extraordinaires. Tu deviens héros indépendant et une première intervention se prépare."
                        elif world == "Naruto" and "ermite" in event_text:
                            path, title = "mentor_ermite", "La voie du mentor ermite"
                            detail = "Le mentor accepte de t’entraîner. Il t’enseigne d’abord le Rasengan, puis peut t’aider à maîtriser le mode ermite si tu persévères."
                        elif world == "Naruto" and "démon à queue" in event_text:
                            path, title = "beast_seal", "Un sceau à protéger"
                            detail = "Tu acceptes le sceau protecteur et deviens l’hôte d’un démon à queue. Le contrôler demandera du temps, un mentor et des choix prudents."
                            st.session_state.tailed_beast = random.choice(["Démon à une queue", "Démon à trois queues", "Démon à neuf queues"])
                        elif world == "Monde réel" and work_event:
                            path, title = "career_mission", "Une mission professionnelle décisive"
                            detail = f"Ton initiative transforme l’incident en réussite pour ton équipe. Une nouvelle mission de {st.session_state.career.lower()} et un contact utile se débloquent."
                            st.session_state.job_tasks += 1
                            st.session_state.money += 300
                            if st.session_state.job_tasks >= 3:
                                st.session_state.career_level += 1
                                st.session_state.job_tasks = 0
                                detail += f" Tes réussites t’offrent une promotion au niveau {st.session_state.career_level}."
                            st.session_state.event_followups.append(f"Le suivi de ton intervention au travail révèle un nouveau dossier lié au métier de {st.session_state.career.lower()}.")
                        elif world == "Monde réel":
                            path, title = "opportunite_professionnelle", "Une porte s’ouvre"
                            detail = "Ta candidature retient l’attention. Une nouvelle histoire de stage et d’orientation professionnelle commence."
                        elif world == "Naruto" and "hokage" in event_text and st.session_state.rank == "Jônin":
                            path, title = "hokage_nomination", "La succession du Hokage"
                            detail = "Le conseil te choisit comme prochain Hokage. Tu deviens le protecteur du village et une nouvelle intrigue politique commence."
                        elif world == "Naruto":
                            path, title = "mission_speciale", "Mission spéciale"
                            detail = "Ton initiative est remarquée. Une mission spéciale et une nouvelle intrigue se débloquent."
                        else:
                            path, title = "mission_occulte", "Le dossier confidentiel"
                            detail = "Tu gagnes la confiance de ton mentor. Un dossier occulte confidentiel et une nouvelle mission se débloquent."
                        if path not in st.session_state.story_paths: st.session_state.story_paths.append(path)
                        if path == "basket_recrutement": st.session_state.career = "Espoir du basket"
                        if path == "hokage_nomination": st.session_state.rank = "Hokage"
                        if path == "superhero_origin": st.session_state.career = "Héros indépendant"
                        if path == "mentor_ermite" and path not in st.session_state.story_paths: st.session_state.story_paths.append(path)
                        if path == "beast_seal" and path not in st.session_state.story_paths: st.session_state.story_paths.append(path)
                        st.session_state.year["events"].append(f"🔓 Nouvelle histoire débloquée — {title} : {detail}")
                        st.session_state.history.append({"age": age, "choix": "Tenter ma chance", "résultat": "Réussite", "histoire": title})
                    else:
                        detail = "Tu n’es pas retenu(e) cette fois. Cette expérience te donne une piste pour retenter ta chance lors d’une prochaine occasion."
                        st.session_state.year["events"].append(f"🎲 Tu as tenté ta chance : {detail}")
                        st.session_state.history.append({"age": age, "choix": "Tenter ma chance", "résultat": "Échec"})
                else:
                    st.session_state.history.append({"age": age, "choix": f"Événement : {response}"})
                for npc in st.session_state.get("npc_roster", []):
                    if npc.get("status") == "Présent·e" and npc.get("name", "").lower() in event_text:
                        record_npc_memory(npc, response, age)
                followup_options = {
                    "Monde réel": ["Une association locale te sollicite après ta réaction. Une décision ouvre une nouvelle piste.", "Un contact de ta ville t’apporte une information qui pourrait changer tes projets.", "Une personne que tu as aidée revient avec une proposition inattendue."],
                    "Kuroko Basket": ["Un entraîneur analyse ta réaction et t’invite à un défi d’équipe.", "Ton rival prépare une nouvelle stratégie pour votre prochaine rencontre.", "Un coéquipier partage une piste vers un tournoi régional."],
                    "Naruto": ["Le bureau des missions reçoit un rapport lié à ton choix et ouvre une nouvelle affectation.", "Une rumeur à la radio révèle une piste près de la frontière.", "Un ninja de ton équipe te confie une information qui mènera à une mission."],
                    "Jujutsu Kaisen": ["Ton mentor repère une nouvelle trace occulte liée à ton enquête.", "Un rapport confidentiel révèle un fléau qui pourrait être lié à l’incident.", "Un autre élève demande ton aide pour une affaire qui vient d’émerger."]}
                st.session_state.event_followups.append(random.choice(followup_options[world]))
                add_year_item("activities", f"Face à l’événement, tu as choisi : {response.lower()}.")
                if any(word in response.lower() for word in ["protéger", "aider", "conseil", "renfort", "protocole", "équipe"]): st.session_state.honor = min(100, st.session_state.honor + 1)
                if any(word in response.lower() for word in ["à tout prix", "ignorer", "abandonner"]): st.session_state.honor = max(-100, st.session_state.honor - 2)
                stat = "Talent" if any(word in response.lower() for word in ["accepter", "défi", "participer", "saisir"]) else "Bonheur"
                st.session_state.stats[stat] = min(100, st.session_state.stats[stat] + 3)
                if "ami" in response.lower() or "équipe" in response.lower():
                    add_year_item("close", "Un proche ou un coéquipier a répondu à ton invitation et a partagé ce moment avec toi.")
                st.rerun()
            st.markdown("**📝 Tes activités cette année**")
            if st.session_state.year["activities"]:
                for item in st.session_state.year["activities"]: st.markdown(f'<div class="card">✅ {item}</div>', unsafe_allow_html=True)
            else: st.markdown('<div class="card muted">Tu n’as pas encore choisi d’activité pour cette année.</div>', unsafe_allow_html=True)
            st.markdown("**🌐 Pendant ce temps, dans le monde**")
            for headline in st.session_state.year.get("world_news", []):
                st.markdown(f'<div class="card">📡 {headline}</div>', unsafe_allow_html=True)
        with close_col:
            st.markdown("**👨‍👩‍👧 Actions de tes proches**")
            if st.session_state.year["close"]:
                for item in st.session_state.year["close"]: st.markdown(f'<div class="card">💛 {item}</div>', unsafe_allow_html=True)
            else: st.markdown('<div class="card muted">Ta famille vit aussi son année. Une nouvelle peut arriver à tout moment.</div>', unsafe_allow_html=True)
            st.markdown("**📊 Aptitudes**")
            for stat, value in st.session_state.stats.items(): st.write(f"{stat} · {value}%"); st.progress(value / 100)
    with tab_next:
        st.empty()

    with tab_rankings:
        st.markdown("#### 🏆 Classements de l’univers")
        st.caption("Compare ta progression à celle des équipes, des ninjas ou des figures qui façonnent ton monde.")
        if world == "Kuroko Basket":
            teams = [("Rakuzan", 94), ("Tōō", 90), ("Seirin", 86), ("Yōsen", 82), ("Kaijō", 78)]
            if "Club de basket" in st.session_state.clubs: teams.append((f"Club de {st.session_state.surname}", min(99, 40 + st.session_state.stats.get("Basket", 48) // 2 + st.session_state.fame // 3)))
            st.dataframe([{"Équipe": team, "Indice": score} for team, score in sorted(teams, key=lambda row: row[1], reverse=True)], hide_index=True, use_container_width=True)
        elif world == "Naruto":
            ninja_rows = [("Naruto Uzumaki", "Konoha", 98), ("Sasuke Uchiha", "Errant", 96), ("Sakura Haruno", "Konoha", 88), (name, st.session_state.place, min(99, st.session_state.stats["Talent"] + st.session_state.fame))]
            st.dataframe([{"Ninja": who, "Village / statut": where, "Indice": score} for who, where, score in sorted(ninja_rows, key=lambda row: row[2], reverse=True)], hide_index=True, use_container_width=True)
            st.markdown("**Villages · réputation**")
            village_scores = [("Konoha", 96), ("Kumo", 91), ("Suna", 87), ("Kiri", 82), ("Iwa", 79)]
            st.dataframe([{"Village": village, "Indice": score} for village, score in sorted(village_scores, key=lambda row: row[1], reverse=True)], hide_index=True, use_container_width=True)
        elif world == "Jujutsu Kaisen":
            rows = [("Satoru Gojo", "Tokyo", 100), ("Yuta Okkotsu", "Tokyo", 96), ("Maki Zenin", "Tokyo", 86), (name, st.session_state.rank, min(99, st.session_state.stats["Talent"] + st.session_state.fame))]
            st.dataframe([{"Exorciste": who, "Grade": grade, "Indice": score} for who, grade, score in sorted(rows, key=lambda row: row[2], reverse=True)], hide_index=True, use_container_width=True)
        elif "Footballeur professionnel" in st.session_state.career:
            rows = [("A. Moreau", "Olympique Lyonnais", 91), ("M. Diallo", "Paris FC", 88), (name, st.session_state.career, min(99, st.session_state.stats["Talent"] + st.session_state.fame))]
            st.dataframe([{"Joueur": who, "Club": club, "Indice": score} for who, club, score in sorted(rows, key=lambda row: row[2], reverse=True)], hide_index=True, use_container_width=True)
        elif "Basket" in world:
            rows = [("Équipe des Aigles", "Ligue nationale", 92), ("Club des Comètes", "Ligue nationale", 87), (name, st.session_state.career, min(99, st.session_state.stats["Talent"] + st.session_state.fame))]
            st.dataframe([{"Équipe / joueur": who, "Catégorie": category, "Indice": score} for who, category, score in sorted(rows, key=lambda row: row[2], reverse=True)], hide_index=True, use_container_width=True)
        elif world == "Monde réel" and "Héros" not in st.session_state.career:
            st.info("Les classements professionnels se débloquent lorsque tu rejoins une carrière sportive ou héroïque.")
        else:
            rows = [("Héros du Nord", "Ligue civile", 93), ("Sentinelle", "Ligue civile", 84), (name, st.session_state.career, min(99, st.session_state.stats["Talent"] + st.session_state.fame))]
            st.dataframe([{"Personne": who, "Rôle": role, "Indice": score} for who, role, score in sorted(rows, key=lambda row: row[2], reverse=True)], hide_index=True, use_container_width=True)

    with tab_actions:
        st.markdown(f"#### Actions accessibles · {stage}")
        actions = []
        if age < 3:
            actions = [("Jouer avec un jouet", "Talent", "Tu explores en jouant. Ta curiosité grandit."), ("Faire une promenade avec un proche", "Bonheur", "Un proche t’emmène prendre l’air."), ("Écouter une histoire", "Intelligence", "Une histoire partagée stimule ton imagination.")]
        elif age < 6:
            actions = [("Aller à la maternelle", "Intelligence", "Tu apprends et joues avec les enfants de ta classe."), ("Sortie au parc avec un parent", "Bonheur", "Une promenade au parc devient un bon souvenir."), ("Dessiner ou bricoler", "Talent", "Tu crées quelque chose avec tes mains.")]
        elif age < 11:
            actions = [("Étudier à l’école primaire", "Intelligence", "Tu travailles une nouvelle matière."), ("Rejoindre un club sportif", "Talent", "Tu découvres l’esprit d’équipe à l’entraînement."), ("Lire à la bibliothèque", "Intelligence", "Tu termines un livre qui t’apprend de nouvelles choses."), ("Sortie avec un proche", "Bonheur", "Tu passes un après-midi avec ta famille.")]
        elif age < 15:
            actions = [("Étudier pour le collège", "Intelligence", "Tu prépares tes cours et tes contrôles."), ("Rejoindre l’équipe sportive", "Talent", "Tu participes aux entraînements et aux sélections."), ("Faire un stage d’observation", "Intelligence", "Tu découvres un métier pendant une courte période."), ("Sortir avec tes amis", "Bonheur", "Tu retrouves tes amis après les cours.")]
        elif age < 18:
            actions = [("Préparer les examens du lycée", "Intelligence", "Tu avances dans tes révisions."), ("T’entraîner avec l’équipe", "Talent", "Tu renforces tes chances d’être repéré."), ("Faire un stage", "Intelligence", "Tu gagnes une première expérience professionnelle."), ("Passer du temps avec tes amis", "Bonheur", "Tu partages une sortie avec tes amis.")]
        elif age < 23:
            actions = [("Suivre des cours supérieurs", "Intelligence", "Tu avances dans tes études."), ("Faire un stage professionnel", "Talent", "Ton expérience attire l’attention d’un employeur."), ("T’entraîner", "Santé", "Tu gardes une bonne hygiène de vie."), ("Voir tes proches", "Bonheur", "Tu prends du temps pour ton entourage.")]
        else:
            actions = [("Suivre une formation", "Intelligence", "Tu développes une nouvelle compétence."), ("Faire du sport", "Santé", "Tu prends soin de ta forme."), ("Voir tes proches", "Bonheur", "Tu renforces tes liens."), ("Chercher une opportunité professionnelle", "Talent", "Tu avances dans ta carrière.")]
        if world == "Monde réel" and age >= 18:
            if st.session_state.career == "Aucune":
                actions.append(("Postuler à un métier", "Intelligence", "Tu prépares une candidature pour un emploi."))
            else:
                actions = [item for item in actions if item[0] != "Chercher une opportunité professionnelle"]
            if st.session_state.career != "Aucune" and not st.session_state.year.get("career_task_done", False):
                actions.append(("Effectuer une tâche au travail", "Talent", "Tu mènes une mission importante dans ton métier."))
        if world == "Monde réel" and st.session_state.career == "Héros indépendant":
            if not st.session_state.get("hero_affiliation"):
                actions.append(("Postuler à une association héroïque", "Talent", "Tu présentes tes valeurs et tes interventions à une équipe de héros indépendante."))
            else:
                actions.append(("Entraînement de l’association", "Talent", f"Tu suis un exercice de l’équipe {st.session_state.hero_affiliation}."))
        if 6 <= age < 18 and world == "Kuroko Basket":
            actions = [item for item in actions if item[0] != "Rejoindre un club sportif"]
            if "Club de basket" not in st.session_state.clubs:
                actions.append(("Rejoindre un club de basket", "Basket", "Tu réussis les sélections et rejoins ton club de basket. Les entraînements et matchs entre amis sont débloqués."))
            else:
                actions.append(("S’entraîner au basket avec tes amis", "Basket", "Tu répètes les passes et les tirs avec tes amis du club."))
                if age >= 11:
                    actions.append(("Jouer un match avec tes amis du club", "Basket", "Tu participes à un match amical avec tes amis."))
        if world == "Kuroko Basket" and "camp_basket" in st.session_state.story_paths and age >= 13:
            actions.append(("Participer au camp d’été des espoirs", "Basket", "Tu retrouves les jeunes sélectionnés et découvres un entraînement de haut niveau."))
        if world == "Kuroko Basket" and "basket_recrutement" in st.session_state.story_paths and age >= 15:
            actions.append(("Passer un essai dans une académie", "Basket", "Tu joues devant un entraîneur qui pourrait t’ouvrir la voie du basket professionnel."))
        if world == "Kuroko Basket" and age >= 6:
            if age < 15: actions.append(("Entraînement de basket", "Basket", "Tes fondamentaux progressent et tes chances d’intégrer une équipe augmentent."))
            else: actions.extend([( "Travailler les tirs", "Basket", "Tu répètes tes tirs sous pression."), ("Match d’entraînement", "Basket", "Un match intense te prépare aux sélections.")])
            if age >= 15 and "Club de basket" in st.session_state.clubs and len(st.session_state.zones) < len(KUROKO_ZONES):
                actions.append(("Éveiller une Zone", "Basket", "Sous la pression d’un défi intense, tu cherches l’état de concentration absolue."))
        elif world == "Naruto":
            actions.extend([("Exercice de chakra" if age < 12 else "Entraînement de chakra", "Talent", "Tu apprends à mieux contrôler ton chakra."), ("Étudier les bases ninja", "Intelligence", "Tu mémorises les règles et techniques de l’académie.")])
            rank = st.session_state.rank
            jutsu_list = CLAN_JUTSU.get(st.session_state.clan, CLAN_JUTSU["Inconnu"])
            next_jutsu = st.session_state.jutsu_level
            jutsu_unlocked = (next_jutsu == 0 and age >= 6) or (next_jutsu == 1 and rank in ("Genin", "Chûnin", "Jônin", "Hokage")) or (next_jutsu >= 2 and rank in ("Chûnin", "Jônin", "Hokage"))
            if next_jutsu < len(jutsu_list) and jutsu_unlocked:
                actions.append((f"Apprendre un jutsu : {jutsu_list[next_jutsu]}", "Talent", f"Tu travailles une technique de ton clan : {jutsu_list[next_jutsu]}."))
            pupil_list = PUPIL_TECHNIQUES.get(st.session_state.get("pupil_power", ""), [])
            pupil_stage = st.session_state.get("pupil_stage", 0)
            if pupil_list and pupil_stage < len(pupil_list) and age >= 10:
                actions.append((f"Apprendre une technique héréditaire : {pupil_list[pupil_stage]}", "Talent", f"Tu entraînes ton {st.session_state.pupil_power} sous la supervision du clan."))
            if age >= 12 and "mentor_ermite" in st.session_state.story_paths:
                actions.append(("S’entraîner avec le mentor ermite", "Talent", "Ton mentor te guide dans la maîtrise du Rasengan et du chakra naturel."))
            mentors = [npc for npc in st.session_state.get("npc_roster", []) if npc.get("status") == "Présent·e" and npc.get("role") in ("Mentor", "Sensei")]
            if age >= 10:
                for mentor in mentors:
                    actions.append((f"Séance de mentorat : {mentor['name']}", "Talent", f"Tu reprends avec {mentor['name']} une technique rare et non héréditaire."))
            if age >= 12 and st.session_state.get("tailed_beast"):
                actions.append(("Maîtriser le démon à queue", "Talent", "Tu travailles avec un mentor pour canaliser cette puissance sans perdre le contrôle."))
            if age >= 12 and rank == "Étudiant de l’académie":
                actions.append(("Passer l’examen genin", "Talent", "Tu affrontes l’épreuve qui peut faire de toi un genin."))
            elif rank == "Genin":
                if age >= 15 and st.session_state.mission_counts.get("D", 0) >= 2: actions.append(("Passer l’examen chûnin", "Talent", "Tu participes aux épreuves de sélection chûnin."))
            elif rank == "Chûnin":
                if age >= 18 and st.session_state.mission_counts.get("C", 0) >= 3: actions.append(("Passer la sélection jônin", "Talent", "Les responsables évaluent ton leadership et tes résultats."))
            elif rank in ("Jônin", "Hokage"):
                if rank == "Jônin": actions.append(("Conseiller le village", "Intelligence", "Tu aides les dirigeants à préparer une décision pour le village."))
        elif world == "Jujutsu Kaisen":
            actions.extend([("Contrôler ton énergie occulte", "Talent", f"Tu affines ta technique, {st.session_state.technique}."), ("Étudier les fléaux", "Intelligence", "Tu apprends à reconnaître leurs traces et leurs points faibles.")])
            if st.session_state.technique_level < 3:
                actions.append(("Développer ta technique occulte", "Talent", f"Tu pousses plus loin la maîtrise de {st.session_state.technique}."))
            if age >= 12 and len(st.session_state.techniques) < len(OCCULT_TECHNIQUES):
                actions.append(("Apprendre une nouvelle technique occulte", "Talent", "Tu explores une nouvelle application de ton énergie occulte."))
            rank = st.session_state.rank
            if age >= 15 and rank == "Élève":
                actions.append(("Intégrer l’école d’exorcisme", "Intelligence", "Un mentor évalue ton potentiel et t’accueille à l’école."))
            elif rank.startswith("Grade"):
                mission_grade = {"Grade 4": "4", "Grade 3": "3", "Grade 2": "2", "Grade 1": "1", "Grade spécial": "spécial"}.get(rank, "4")
                current_grade = int(mission_grade) if mission_grade.isdigit() else 0
                if current_grade > 1 and st.session_state.mission_counts.get(rank, 0) >= 2:
                    actions.append(("Évaluation de promotion", "Talent", "Tu présentes tes rapports et ton contrôle de l’énergie occulte aux responsables."))
        career_training_ready = (world == "Monde réel" and st.session_state.career != "Aucune" and age >= 18) or (world == "Kuroko Basket" and age >= 6) or (world == "Naruto" and age >= 6) or (world == "Jujutsu Kaisen" and age >= 12)
        if career_training_ready:
            for skill in career_skill_profile(world, st.session_state.career):
                actions.append((f"Entraînement ciblé : {skill}", "Talent", f"Tu consacres ta séance à développer {skill.lower()}."))
        if world == "Monde réel" and "opportunite_professionnelle" in st.session_state.story_paths and 14 <= age < 24:
            actions.append(("Commencer le stage débloqué", "Intelligence", "Tu commences le stage obtenu grâce à ta réussite et découvres un nouveau métier."))
        if world == "Naruto" and "mission_speciale" in st.session_state.story_paths and age >= 12:
            actions.append(("Accepter la mission spéciale", "Talent", "Tu pars en équipe sur une mission spéciale de reconnaissance."))
        if world == "Jujutsu Kaisen" and "mission_occulte" in st.session_state.story_paths and age >= 15 and st.session_state.rank.startswith("Grade"):
            actions.append(("Enquêter sur le dossier confidentiel", "Talent", "Avec ton mentor, tu suis la piste du dossier occulte et découvres un nouveau lieu d’enquête."))
        if age >= 8:
            actions.append(("Récupération et repos", "Santé", "Tu récupères avant les prochaines épreuves."))
        st.session_state.year.setdefault("training_counts", {})
        training_count = st.session_state.year["training_counts"].get("bonus", 0)
        st.caption(f"🏋️ Entraînements avec bonus cette année : {training_count}/3")
        training_terms = ["entraînement", "entraîner", "s’entraîner", "tirs", "musculation", "faire du sport", "match", "camp d’été", "essai dans une académie", "chakra", "énergie occulte", "jutsu", "technique occulte", "technique héréditaire", "zone", "ermite", "association", "mentorat", "sensei"]
        if training_count >= 3:
            actions = [item for item in actions if not any(term in item[0].lower() for term in training_terms)]
            st.caption("Tes trois entraînements bonus de l’année sont utilisés. Les activités d’entraînement reprendront l’année prochaine.")
        if world == "Kuroko Basket":
            club_status = "✅ Club de basket rejoint : entraînements et matchs entre amis débloqués." if "Club de basket" in st.session_state.clubs else "🔒 Rejoins un club de basket pour débloquer les entraînements avec tes amis et les matchs amicaux."
            st.info(club_status)
        elif world == "Monde réel":
            if age < 18: st.info(f"Parcours : {stage} · tes études, stages et loisirs développent les compétences utiles pour choisir un métier.")
            elif st.session_state.career == "Aucune": st.info("Parcours : choisis un métier et postule. Tes compétences influencent tes chances d’être recruté(e).")
            else: st.info(f"Parcours : {st.session_state.career} · effectue trois missions professionnelles pour gagner une promotion.")
        elif world == "Naruto":
            if st.session_state.rank == "Étudiant de l’académie": st.info("Parcours ninja : entraîne-toi à l’académie, puis passe l’examen genin à partir de 12 ans.")
            elif st.session_state.rank == "Genin": st.info(f"Parcours ninja : réussis des missions de rang D ({st.session_state.mission_counts.get('D', 0)}/2) pour pouvoir tenter l’examen chûnin dès 15 ans.")
            elif st.session_state.rank == "Chûnin": st.info(f"Parcours ninja : conduis des missions de rang C ({st.session_state.mission_counts.get('C', 0)}/3) avant la sélection jônin.")
            elif st.session_state.rank == "Jônin": st.info("Parcours ninja : dirige des missions de rang A et sers le village. Le Hokage et le conseil choisissent leur successeur.")
            else: st.info(f"Parcours ninja : {st.session_state.rank} · tes décisions influencent la sécurité et la diplomatie du village.")
        elif world == "Jujutsu Kaisen":
            if st.session_state.rank == "Élève": st.info("Parcours occulte : entraîne ta technique et rejoins l’école d’exorcisme à partir de 15 ans.")
            else: st.info(f"Parcours occulte : {st.session_state.rank} · réussis deux missions pour demander une évaluation de promotion.")
        selected = st.selectbox("Choisis une activité", [item[0] for item in actions])
        job_choice = st.selectbox("Métier visé", JOBS, key=f"job_choice_{age}") if selected == "Postuler à un métier" else None
        hero_choice = st.selectbox("Association visée", HERO_ASSOCIATIONS, key=f"hero_choice_{age}") if selected == "Postuler à une association héroïque" else None
        decision_choices = None
        if "match" in selected.lower():
            decision_choices = ["Tenter un tir décisif", "Faire une passe à un coéquipier", "Protéger l’avance en défendant"]
        elif world == "Naruto" and "Mission" in selected:
            decision_choices = ["Éclaire la zone d’abord", "Coordonne une attaque", "Protège ton équipe"]
        elif world == "Jujutsu Kaisen" and ("Mission" in selected or "Enquêter" in selected):
            decision_choices = ["Analyser les traces du fléau", "Protéger les civils", "L’attaquer de front"]
        field_decision = st.selectbox("Choix sur le terrain", decision_choices, key=f"field_choice_{age}_{selected}") if decision_choices else None
        if st.button("Faire cette activité", type="primary", use_container_width=True):
            action = next(item for item in actions if item[0] == selected)
            if world == "Kuroko Basket": st.session_state.stats.setdefault("Basket", 48)
            is_training = any(word in selected.lower() for word in ["entraînement", "entraîner", "s’entraîner", "tirs", "musculation", "faire du sport", "match", "camp d’été", "essai dans une académie", "chakra", "énergie occulte", "jutsu", "technique occulte", "technique héréditaire", "zone", "ermite", "association", "mentorat", "sensei"])
            special_activity = selected in ("Postuler à une association héroïque", "Entraînement de l’association", "Maîtriser le démon à queue", "S’entraîner avec le mentor ermite") or selected.startswith("Apprendre une technique héréditaire :") or selected.startswith("Séance de mentorat :")
            if selected == "Rejoindre un club de basket":
                if "Club de basket" not in st.session_state.clubs: st.session_state.clubs.append("Club de basket")
            if selected == "Postuler à une association héroïque":
                chance = min(90, 25 + st.session_state.stats["Talent"] // 2 + st.session_state.fame // 3 + st.session_state.honor // 5)
                if random.randint(1, 100) <= chance:
                    st.session_state.hero_affiliation = hero_choice
                    activity_text = f"{hero_choice} accepte ta candidature. Tu rejoins une équipe de héros et débloques ses entraînements et missions collectives."
                    st.balloons()
                else:
                    activity_text = f"{hero_choice} te remercie, mais attend davantage de maîtrise et de preuves de fiabilité. Tu pourras retenter ta chance."
            elif selected == "Entraînement de l’association":
                count = st.session_state.year["training_counts"].get("bonus", 0)
                activity_text = f"Avec {st.session_state.hero_affiliation}, tu répètes les exercices d’intervention." if count < 3 else f"Tu participes à l’exercice de {st.session_state.hero_affiliation}, mais tu as déjà obtenu tes trois bonus d’entraînement annuels."
            elif selected == "Maîtriser le démon à queue":
                chance = min(90, 25 + st.session_state.stats["Intelligence"] // 2 + st.session_state.stats["Santé"] // 4 + st.session_state.beast_mastery * 8)
                if random.randint(1, 100) <= chance:
                    st.session_state.beast_mastery = min(3, st.session_state.beast_mastery + 1)
                    if st.session_state.beast_mastery >= 2 and "Synchronisation du chakra" not in st.session_state.known_jutsu: st.session_state.known_jutsu.append("Synchronisation du chakra")
                    activity_text = f"Tu canalises mieux le chakra de {st.session_state.tailed_beast} (maîtrise {st.session_state.beast_mastery}/3)."
                else:
                    st.session_state.stats["Santé"] = max(0, st.session_state.stats["Santé"] - 5)
                    activity_text = "Le chakra échappe à ton contrôle. Ton mentor interrompt la séance. Santé −5."
            elif selected == "S’entraîner avec le mentor ermite":
                progress = st.session_state.mentor_progress.get("ermite", 0) + 1
                st.session_state.mentor_progress["ermite"] = progress
                rewards = []
                if progress >= 1 and "Rasengan" not in st.session_state.known_jutsu:
                    st.session_state.known_jutsu.append("Rasengan")
                    rewards.append("le Rasengan")
                if progress >= 3 and "Mode ermite" not in st.session_state.mentor_training:
                    st.session_state.mentor_training.append("Mode ermite")
                    st.session_state.known_jutsu.append("Mode ermite")
                    rewards.append("le mode ermite")
                activity_text = f"Le mentor te fait répéter les exercices de contrôle du chakra (séance {progress})." + (" Tu apprends " + " et ".join(rewards) + " !" if rewards else " Continue pour atteindre le mode ermite.")
            elif selected.startswith("Séance de mentorat :"):
                mentor_name = selected.split(": ", 1)[1]
                mentor = next(npc for npc in st.session_state.npc_roster if npc.get("name") == mentor_name and npc.get("status") == "Présent·e")
                progress = st.session_state.mentor_progress.get(mentor["id"], 0) + 1
                st.session_state.mentor_progress[mentor["id"]] = progress
                record_npc_memory(mentor, "S’entraîner avec mon sensei", age)
                activity_text = f"{mentor_name} corrige ton contrôle et te transmet une méthode personnelle (séance {progress}/2)."
                if progress % 2 == 0:
                    rare = [jutsu for jutsu in RARE_MENTOR_JUTSU if jutsu not in st.session_state.known_jutsu]
                    if rare:
                        learned = random.choice(rare)
                        st.session_state.known_jutsu.append(learned)
                        st.session_state.mentor_jutsu.append(learned)
                        activity_text += f" Ton sensei t’enseigne le jutsu rare {learned}, accessible par entraînement et non par hérédité."
                        st.session_state.event_followups.append(f"Ton sensei {mentor_name} te révèle une variante avancée de {learned} à travailler ensemble.")
            elif selected.startswith("Apprendre une technique héréditaire :"):
                pupil_list = PUPIL_TECHNIQUES.get(st.session_state.pupil_power, [])
                technique_name = pupil_list[st.session_state.pupil_stage]
                st.session_state.pupil_stage += 1
                if technique_name not in st.session_state.known_jutsu: st.session_state.known_jutsu.append(technique_name)
                activity_text = f"Ton {st.session_state.pupil_power} s’affine : tu maîtrises {technique_name}."
            if special_activity:
                pass
            elif selected == "Postuler à un métier":
                application_chance = min(90, 30 + st.session_state.stats["Intelligence"] // 2 + st.session_state.stats["Talent"] // 4)
                if random.randint(1, 100) <= application_chance:
                    st.session_state.career = job_choice
                    st.session_state.career_level = 1
                    activity_text = f"Ta candidature est acceptée : tu deviens {job_choice.lower()}. Ta carrière commence."
                else:
                    activity_text = f"Ta candidature pour le poste de {job_choice.lower()} n’est pas retenue cette fois."
            elif selected == "Effectuer une tâche au travail":
                st.session_state.year["career_task_done"] = True
                st.session_state.job_tasks += 1
                st.session_state.money += 450
                if st.session_state.job_tasks >= 3:
                    st.session_state.career_level += 1
                    st.session_state.job_tasks = 0
                    activity_text = f"Tu termines une mission importante dans ton métier de {st.session_state.career.lower()} et obtiens une promotion au niveau {st.session_state.career_level}. +450 crédits."
                else:
                    activity_text = f"Tu avances dans ton métier de {st.session_state.career.lower()}. +450 crédits. Encore {3 - st.session_state.job_tasks} mission(s) réussie(s) avant l’évaluation de promotion."
            elif selected == "Intégrer l’école d’exorcisme":
                st.session_state.rank = "Grade 4"
                activity_text = f"Tu es admis(e) à l’école d’exorcisme comme apprenti(e) de grade 4. Ta technique {st.session_state.technique} sera évaluée par un mentor."
            elif selected.startswith("Apprendre un jutsu :"):
                jutsu = CLAN_JUTSU.get(st.session_state.clan, CLAN_JUTSU["Inconnu"])[st.session_state.jutsu_level]
                st.session_state.jutsu_level += 1
                if jutsu not in st.session_state.known_jutsu: st.session_state.known_jutsu.append(jutsu)
                activity_text = f"Tu maîtrises {jutsu}, une technique transmise par ton clan."
            elif selected == "Développer ta technique occulte":
                st.session_state.technique_level = min(3, st.session_state.technique_level + 1)
                activity_text = f"Ta maîtrise de {st.session_state.technique} atteint le niveau {st.session_state.technique_level}/3."
            elif selected == "Apprendre une nouvelle technique occulte":
                undiscovered = [name for name in OCCULT_TECHNIQUES if name not in st.session_state.techniques]
                if undiscovered:
                    st.session_state.technique = random.choice(undiscovered)
                    st.session_state.techniques.append(st.session_state.technique)
                    st.session_state.technique_level = 1
                    activity_text = f"Tu découvres {st.session_state.technique}, une nouvelle technique occulte. Tu pourras la perfectionner et l’utiliser en mission."
                else:
                    activity_text = "Tu maîtrises déjà toutes les techniques occultes connues."
            elif selected == "Éveiller une Zone":
                chance = min(85, max(20, 25 + st.session_state.stats.get("Basket", 48) // 2 + st.session_state.stats["Santé"] // 5))
                if random.randint(1, 100) <= chance:
                    undiscovered = [zone for zone in KUROKO_ZONES if zone not in st.session_state.zones]
                    awakened = random.choice(undiscovered)
                    st.session_state.zones.append(awakened)
                    st.session_state.story_paths.append(f"zone_{len(st.session_state.zones)}")
                    st.session_state.year["events"].append(f"🏀 Éveil : tu entres dans {awakened}. Ton jeu atteint un nouveau palier.")
                    activity_text = f"Tu éveilles {awakened} et découvres une nouvelle dimension de ton jeu. L’état ne dure que si tu gardes une excellente condition physique."
                else:
                    activity_text = f"Tu frôles la Zone ({chance}% de chance), mais la concentration retombe. Ton entraînement prépare une prochaine tentative."
            elif selected.startswith("Passer l’examen") or selected == "Passer la sélection jônin":
                target_rank = {"Passer l’examen genin": "Genin", "Passer l’examen chûnin": "Chûnin", "Passer la sélection jônin": "Jônin"}[selected]
                exam_chance = min(92, 25 + st.session_state.stats["Talent"] // 2 + st.session_state.stats["Intelligence"] // 4)
                if random.randint(1, 100) <= exam_chance:
                    st.session_state.rank = target_rank
                    st.session_state.year["events"].append(f"🎖️ Réussite à l’examen : tu deviens {target_rank}.")
                    activity_text = f"Tu réussis les épreuves et obtiens le grade de {target_rank}."
                else:
                    activity_text = f"Tu ne réussis pas encore l’examen pour devenir {target_rank}. Tu peux continuer à t’entraîner et retenter ta chance."
            elif selected == "Évaluation de promotion":
                rank_up = {"Grade 4": "Grade 3", "Grade 3": "Grade 2", "Grade 2": "Grade 1", "Grade 1": "Grade spécial"}
                next_rank = rank_up.get(st.session_state.rank, "Grade 3")
                promotion_chance = 20 if next_rank == "Grade spécial" else min(90, 35 + st.session_state.stats["Talent"] // 2 + st.session_state.stats["Intelligence"] // 4)
                if random.randint(1, 100) <= promotion_chance:
                    st.session_state.rank = next_rank
                    st.session_state.mission_counts[next_rank] = 0
                    activity_text = f"Le conseil valide ta progression : tu passes {next_rank}."
                else:
                    activity_text = "Le conseil te demande davantage d’expérience avant de valider ta promotion."
            elif field_decision and world in ("Naruto", "Jujutsu Kaisen"):
                field_chance = min(90, 30 + st.session_state.stats["Talent"] // 2 + st.session_state.stats["Intelligence"] // 4)
                field_success = random.randint(1, 100) <= field_chance
                if world == "Naruto" and "Mission" in selected:
                    if selected.startswith("Mission de rang"):
                        mission_rank = selected[-1]
                    else:
                        mission_rank = {"Genin": "D", "Chûnin": "C", "Jônin": "A", "Hokage": "A"}.get(st.session_state.rank, "D")
                    if field_success:
                        st.session_state.mission_counts[mission_rank] = st.session_state.mission_counts.get(mission_rank, 0) + 1
                        activity_text = f"Tu as choisi de {field_decision.lower()}. Mission réussie : ton équipe revient avec les informations demandées."
                    else: activity_text = f"Tu as choisi de {field_decision.lower()}. La mission est interrompue et ton équipe rentre prudemment."
                elif world == "Jujutsu Kaisen":
                    mission_key = st.session_state.rank
                    if field_success:
                        st.session_state.mission_counts[mission_key] = st.session_state.mission_counts.get(mission_key, 0) + 1
                        activity_text = f"Tu as choisi de {field_decision.lower()}. Le fléau est maîtrisé et les civils sont en sécurité."
                    else: activity_text = f"Tu as choisi de {field_decision.lower()}. Le fléau s’échappe, mais ton rapport aide l’équipe à préparer la suite."
            elif field_decision and world == "Kuroko Basket":
                level = st.session_state.stats.get("Basket", st.session_state.stats.get("Talent", 48))
                success = random.randint(1, 100) <= min(90, 35 + level // 2)
                result = "L’action réussit et ton équipe prend l’avantage." if success else "L’adversaire lit ton jeu, mais tu apprends de cette action."
                activity_text = f"Pendant le match, tu as choisi de {field_decision.lower()}. {result}"
            else:
                activity_text = action[2]
            st.session_state.year["activities"].append(activity_text)
            st.session_state.history.append({"age": age, "choix": selected, "détail": activity_text})
            if is_training:
                count = st.session_state.year["training_counts"].get("bonus", 0)
                if count < 3:
                    st.session_state.stats[action[1]] = min(100, st.session_state.stats.get(action[1], 48) + random.randint(3, 7))
                    st.session_state.year["training_counts"]["bonus"] = count + 1
                    st.session_state.stats["Bonheur"] = min(100, st.session_state.stats["Bonheur"] + 2)
                else:
                    st.session_state.year["activities"][-1] += " Tu as déjà atteint la limite de trois entraînements avec bonus cette année."
            else:
                st.session_state.stats[action[1]] = min(100, st.session_state.stats.get(action[1], 48) + random.randint(3, 7))
                st.session_state.stats["Bonheur"] = min(100, st.session_state.stats["Bonheur"] + (2 if action[1] != "Bonheur" else 0))
            if selected == "Récupération et repos":
                st.session_state.fatigue = max(0, st.session_state.fatigue - 22)
                st.session_state.year["activities"][-1] += f" Fatigue −22 · niveau actuel {st.session_state.fatigue}%."
            elif is_training or selected == "Effectuer une tâche au travail":
                st.session_state.fatigue = min(100, st.session_state.fatigue + (8 if selected == "Effectuer une tâche au travail" else 6))
            update_career_skill(world, f"{selected} {activity_text}", st.session_state.career)
            if "stage" in selected.lower(): st.session_state.money += 100
            st.success("Activité ajoutée à l’année en cours.")
            st.rerun()

        st.markdown("#### 🎖️ Missions de rang · D → SS")
        if world == "Kuroko Basket" and "Rival de l’équipe nationale · joueur élite" in st.session_state.friends and "Rival recruté" not in st.session_state.clubs:
            if st.button("🤝 Recruter ton rival dans l’équipe", use_container_width=True):
                st.session_state.clubs.append("Rival recruté")
                st.session_state.year["events"].append("Ton rival accepte de rejoindre ton équipe après votre affrontement historique.")
                st.session_state.event_followups.append("Une équipe rivale lance un défi à votre nouveau duo. Un tournoi décisif se prépare.")
                st.rerun()
        if st.session_state.captured:
            st.warning("Tu es retenu(e) prisonnier(ère). Il faut d’abord préparer une évasion.")
            escape_chance = max(10, min(90, 25 + st.session_state.stats["Talent"] // 2 + st.session_state.stats["Intelligence"] // 4))
            if st.button(f"Tenter l’évasion · {escape_chance}% de réussite", use_container_width=True):
                if random.randint(1, 100) <= escape_chance:
                    st.session_state.captured = False
                    text = "Tu réussis à t’évader. Un témoin te remet une piste vers une nouvelle intrigue."
                    st.session_state.event_followups.append(text)
                    st.session_state.year["events"].append(text)
                else:
                    text = "L’évasion échoue. Tu restes captif(ve), mais tu repères une faiblesse dans la surveillance."
                    st.session_state.year["events"].append(text)
                    st.session_state.event_followups.append("Un changement de garde ouvre une nouvelle occasion de fuite.")
                st.rerun()
        else:
            max_rank = "SS"
            mission_ready = True
            if world == "Monde réel":
                mission_ready = age >= 18 and st.session_state.career != "Aucune"
                max_rank = "SS"
            elif world == "Kuroko Basket":
                mission_ready = age >= 11 and "Club de basket" in st.session_state.clubs
                max_rank = "SS" if age >= 15 else "B" if age >= 13 else "C"
            elif world == "Naruto":
                mission_ready = age >= 12 and st.session_state.rank in ("Genin", "Chûnin", "Jônin", "Hokage")
                max_rank = {"Genin": "C", "Chûnin": "A", "Jônin": "S", "Hokage": "SS"}.get(st.session_state.rank, "D")
            elif world == "Jujutsu Kaisen":
                mission_ready = age >= 15 and st.session_state.rank.startswith("Grade")
                max_rank = {"Grade 4": "C", "Grade 3": "B", "Grade 2": "A", "Grade 1": "S", "Grade spécial": "SS"}.get(st.session_state.rank, "D")
            if not mission_ready:
                st.caption("Les missions se débloquent avec l’âge, le métier, le club ou le grade requis.")
            else:
                rank_order = list(MISSION_LEVELS)
                available_ranks = rank_order[:rank_order.index(max_rank) + 1]
                rank = st.selectbox("Rang de mission", available_ranks, key=f"mission_rank_{age}")
                approach = st.selectbox("Approche", mission_approaches(world), key=f"mission_approach_{age}")
                power = mission_power(world)
                chance = max(5, min(95, round(58 + (power - MISSION_LEVELS[rank]) * 1.15)))
                armor_protection = 12 if any(armor in st.session_state.inventory for armor in HERO_ARMORS) else 0
                protection = armor_protection or (6 if "Équipement de mission" in st.session_state.inventory else 0)
                risk = max(.2, min(48, {"D": 1, "C": 2, "B": 4, "A": 7, "S": 12, "SS": 20}[rank] + max(0, MISSION_LEVELS[rank] - power) * .32 - protection))
                st.markdown(f'<div class="card event"><b>{mission_title(world, rank)}</b><br>Puissance {power} · réussite estimée {chance}% · risque critique {risk:.1f}%<br><span class="muted">En cas d’échec : fuite, capture ou blessure. Une mission peut aussi être fatale.</span></div>', unsafe_allow_html=True)
                if st.button("Partir en mission", type="primary", use_container_width=True):
                    resolve_mission(world, rank, approach)
                    if st.session_state.dead: st.rerun()
                    st.rerun()

    with tab_career:
        current_role = st.session_state.career if world == "Monde réel" and st.session_state.career != "Aucune" else world
        st.markdown(f"#### 💼 Parcours · {current_role}")
        st.caption(f"Niveau {st.session_state.career_level} · {st.session_state.rank} · {st.session_state.job_tasks} tâche(s) vers la prochaine évaluation")
        st.session_state.career_skills = career_skill_profile(world, st.session_state.career)
        st.markdown(f'<div class="card event"><b>Fatigue · {st.session_state.fatigue}%</b><br><span class="muted">Les missions et entraînements la font monter. La récupération la fait baisser.</span></div>', unsafe_allow_html=True)
        st.progress(st.session_state.fatigue / 100)
        skill_left, skill_right = st.columns(2, gap="medium")
        skill_items = list(st.session_state.career_skills.items())
        for index, (skill, value) in enumerate(skill_items):
            with (skill_left if index % 2 == 0 else skill_right):
                st.write(f"{skill} · {value}%")
                st.progress(value / 100)
        if world == "Naruto":
            st.markdown("#### 📜 Arsenal et apprentissages")
            st.write("Jutsu appris : " + (" · ".join(st.session_state.known_jutsu) if st.session_state.known_jutsu else "aucun pour le moment"))
            if st.session_state.mentor_jutsu: st.caption("Jutsu rares appris auprès d’un mentor : " + " · ".join(st.session_state.mentor_jutsu))
            if st.session_state.pupil_power: st.caption(f"Pouvoir héréditaire : {st.session_state.pupil_power} · maîtrise {st.session_state.pupil_stage}/{len(PUPIL_TECHNIQUES.get(st.session_state.pupil_power, []))}")
            if st.session_state.tailed_beast: st.caption(f"Démon scellé : {st.session_state.tailed_beast} · maîtrise {st.session_state.beast_mastery}/3")
        elif world == "Jujutsu Kaisen":
            st.markdown("#### 🌀 Techniques occultes")
            st.write(f"Technique principale : {st.session_state.technique} · maîtrise {st.session_state.technique_level}/3")
            st.caption("Techniques découvertes : " + (" · ".join(st.session_state.techniques) if st.session_state.techniques else "aucune"))
        elif world == "Kuroko Basket":
            st.markdown("#### 🏀 Profil de joueur")
            st.write(f"Club : {', '.join(st.session_state.clubs) if st.session_state.clubs else 'aucun club rejoint'}")
            st.caption("Zones maîtrisées : " + (" · ".join(st.session_state.zones) if st.session_state.zones else "aucune Zone éveillée"))
        elif world == "Monde réel" and st.session_state.career == "Héros indépendant":
            st.markdown("#### 🦸 Équipement et équipe")
            st.write(f"Association : {st.session_state.hero_affiliation or 'indépendant·e'}")
            st.caption("Armures : " + (" · ".join(item for item in st.session_state.inventory if item in HERO_ARMORS) or "aucune"))
        st.markdown("#### Évolution cette année")
        recent_career = [item for item in st.session_state.year.get("activities", []) if any(word in item.lower() for word in ["travail", "mission", "entraînement", "jutsu", "technique", "match", "carrière", "sensei"])]
        if recent_career:
            for item in recent_career: st.markdown(f'<div class="card">📈 {item}</div>', unsafe_allow_html=True)
        else: st.markdown('<div class="card muted">Tes aptitudes évolueront quand tu choisiras des actions de carrière, des missions ou des entraînements.</div>', unsafe_allow_html=True)

    with tab_life:
        relatives, radio = st.columns(2, gap="large")
        with relatives:
            st.markdown("#### Famille et amis")
            for person in st.session_state.family:
                details = person.split(" · ")
                relation = details[1] if len(details) > 1 else "proche"
                profession = details[2] if len(details) > 2 else "Profession inconnue"
                st.markdown(f'<div class="card">👤 <b>{details[0]}</b><br><span class="muted">{relation} · Métier : {profession}</span></div>', unsafe_allow_html=True)
            if st.session_state.friends:
                for friend in st.session_state.friends: st.markdown(f'<div class="card">🤝 {friend}</div>', unsafe_allow_html=True)
            st.markdown("#### Rencontres, rivaux et mentors")
            active_npcs = [npc for npc in st.session_state.npc_roster if npc.get("status") == "Présent·e"]
            if active_npcs:
                for npc in active_npcs:
                    st.markdown(f'<div class="card">{ "⚔️" if npc.get("role") == "Rival" else "🧭" if npc.get("role") in ("Sensei", "Mentor") else "👥"} <b>{npc["name"]}</b> · {npc.get("role", "connaissance")}<br><span class="muted">{npc.get("job", "") } · confiance {npc.get("trust", 50)} · rivalité {npc.get("rivalry", 0)}</span></div>', unsafe_allow_html=True)
                npc_name = st.selectbox("Personnage", [npc["name"] for npc in active_npcs], key="npc_interaction_target")
                npc_choice = st.selectbox("Interaction", ["Encourager et soutenir", "Demander de l’aide", "Partager un secret", "Proposer un projet commun", "Défier sur son terrain", "S’excuser après un désaccord", "Prendre mes distances"], key="npc_interaction_choice")
                if st.button("Agir avec ce personnage", key="npc_interaction_button"):
                    npc = next(item for item in active_npcs if item["name"] == npc_name)
                    record_npc_memory(npc, npc_choice, age)
                    if npc_choice == "Défier sur son terrain":
                        skill = max(st.session_state.career_skills.values(), default=st.session_state.stats["Talent"])
                        won = random.randint(1, 100) <= min(90, 28 + skill // 2)
                        if won:
                            npc["rivalry"] = max(0, npc["rivalry"] - 10)
                            result = f"Tu remportes le défi face à {npc_name}. Il/elle respecte ta progression, même si la rivalité reste vive."
                        else:
                            npc["rivalry"] = min(100, npc["rivalry"] + 12)
                            result = f"{npc_name} remporte le défi et prend l’avantage. Il/elle s’en souviendra à votre prochaine rencontre."
                    elif npc_choice == "Prendre mes distances":
                        npc["status"] = "Parti·e"
                        result = f"Tu prends tes distances avec {npc_name}. La relation reste dans tes souvenirs, et cette personne pourra réapparaître plus tard."
                    else:
                        result = random.choice([f"{npc_name} accueille ta proposition et se confie à toi.", f"{npc_name} hésite, puis accepte de faire un pas vers toi.", f"{npc_name} n’est pas disponible aujourd’hui, mais garde ton geste en mémoire.", f"{npc_name} te répond avec une proposition inattendue."])
                        if npc["trust"] >= 70 and f"{npc_name} · allié" not in st.session_state.friends:
                            st.session_state.friends.append(f"{npc_name} · allié")
                            result += " Vous devenez alliés."
                    st.session_state.year["close"].append(result)
                    st.session_state.history.append({"age": age, "npc": npc_name, "choix": npc_choice, "confiance": npc.get("trust"), "rivalité": npc.get("rivalry")})
                    st.rerun()
            else:
                st.markdown('<div class="card muted">Une nouvelle rencontre arrivera avec les événements. Tu peux aussi provoquer une rencontre ici.</div>', unsafe_allow_html=True)
            if age >= 6 and len(active_npcs) < 6:
                role_options = ["Ami", "Rival", "Mentor", "Collègue"] + (["Sensei"] if world == "Naruto" else [])
                encounter_role = st.selectbox("Type de rencontre souhaité", role_options, key="npc_new_role")
                if st.button("🌟 Organiser une nouvelle rencontre", key="npc_new_encounter"):
                    newcomer = create_npc(world, age, encounter_role)
                    if newcomer:
                        st.session_state.npc_roster.append(newcomer)
                        st.session_state.year["close"].append(f"Tu rencontres {newcomer['name']}, {newcomer['job']}. Un nouveau lien se crée et votre première impression comptera.")
                        st.session_state.history.append({"age": age, "npc": newcomer["name"], "événement": "rencontre"})
                    st.rerun()
            memories = st.session_state.npc_memories[-6:]
            if memories:
                with st.expander("🧠 Souvenirs et conséquences"):
                    for memory in reversed(memories):
                        st.caption(f"{memory.get('age', '?')} ans · {memory['npc']} : {memory['event']} · confiance {memory.get('trust', '—')}")
            if st.button("Appeler un proche"):
                person = random.choice(st.session_state.family)
                st.session_state.year["close"].append(f"Tu appelles {person.split(' ·')[0]} et prends de ses nouvelles.")
                st.session_state.stats["Bonheur"] = min(100, st.session_state.stats["Bonheur"] + 4)
                st.rerun()
            interact = st.selectbox("Interaction", ["Encourager un proche", "Demander conseil", "Proposer une sortie", "Aider pour une tâche", "Partager un secret", "Fêter une réussite", "S’excuser après une dispute", "Présenter un nouvel ami", "Lancer un projet ensemble", "Prendre des nouvelles après une absence"])
            if st.button("Interagir"):
                person = random.choice(st.session_state.family)
                response = random.choice(["accepte avec plaisir", "te remercie et te propose son aide en retour", "est occupé(e), mais promet de vous revoir bientôt", "se confie et vous rapproche", "hésite puis finit par accepter", "réagit mal sur le moment avant de revenir s’expliquer", "te surprend avec une proposition à son tour", "te demande de l’accompagner dans une décision importante", "garde le silence, mais te remercie quelques jours plus tard", "transforme ce moment en souvenir que vous reparlerez longtemps"])
                st.session_state.year["close"].append(f"Tu as choisi de {interact.lower()} avec {person.split(' ·')[0]}. Cette personne {response}.")
                st.session_state.history.append({"age": age, "choix": f"{interact} · {person.split(' ·')[0]}"})
                st.session_state.stats["Bonheur"] = min(100, st.session_state.stats["Bonheur"] + 3)
                st.rerun()
            if age >= 18 and st.button("Fonder une famille · avoir un enfant"):
                child = f"{random.choice(['Noa','Léa','Milo','Inaya','Sacha','Nina'])} {st.session_state.surname}"
                st.session_state.children.append(child)
                st.session_state.family.append(child + " · enfant")
                st.session_state.year["close"].append(f"Une nouvelle personne rejoint ta famille : {child}.")
                finish_challenge("child", "Avoir un enfant", 200)
                st.rerun()
            if age >= 16:
                st.markdown("#### 💞 Rencontres et relations")
                st.caption(f"Orientation romantique : {st.session_state.orientation} · chaque relation se construit par tes choix.")
                if st.session_state.partner:
                    partner = st.session_state.partner
                    st.markdown(f'<div class="card">💞 <b>{partner["name"]}</b><br><span class="muted">{partner["occupation"]} · {partner["status"]}</span></div>', unsafe_allow_html=True)
                    partner_action = st.selectbox("Avec ton/ta partenaire", ["Passer du temps ensemble", "Organiser une sortie", "Parler d’un projet commun", "Mettre fin à la relation"], key="partner_action")
                    if st.button("Confirmer l’interaction", key="partner_interaction"):
                        if partner_action == "Mettre fin à la relation":
                            st.session_state.year["close"].append(f"Tu mets fin à ta relation avec {partner['name']}. Cette décision marque une nouvelle étape.")
                            st.session_state.partner = None
                        else:
                            st.session_state.stats["Bonheur"] = min(100, st.session_state.stats["Bonheur"] + 4)
                            st.session_state.year["close"].append(f"Tu choisis de {partner_action.lower()} avec {partner['name']}. Cette personne te répond avec attention et propose un nouveau projet.")
                            st.session_state.event_followups.append(f"{partner['name']} revient vers toi avec une proposition qui pourrait changer votre relation.")
                        st.rerun()
                else:
                    if st.session_state.dating_candidate:
                        candidate = st.session_state.dating_candidate
                        st.markdown(f'<div class="card event">✨ Tu rencontres <b>{candidate["name"]}</b> · {candidate["occupation"]}<br><span class="muted">{candidate["trait"]}</span></div>', unsafe_allow_html=True)
                        choices = ["Proposer une sortie amicale", "Commencer par une amitié", "Décliner la rencontre"] if st.session_state.orientation == "Asexuel·le" else ["Proposer un rendez-vous", "Commencer par une amitié", "Décliner la rencontre"]
                        meeting_choice = st.radio("Que souhaites-tu faire ?", choices, key="meeting_choice", horizontal=True)
                        if st.button("Valider mon choix", key="meeting_decision"):
                            if meeting_choice in ("Proposer un rendez-vous", "Proposer une sortie amicale"):
                                chance = min(90, max(20, 35 + st.session_state.stats["Beauté"] // 4 + st.session_state.stats["Bonheur"] // 5))
                                if random.randint(1, 100) <= chance:
                                    candidate["status"] = "Lien de confiance" if st.session_state.orientation == "Asexuel·le" else "Relation naissante"
                                    st.session_state.partner = candidate
                                    st.session_state.year["close"].append(f"Ton rendez-vous avec {candidate['name']} se passe bien. Vous décidez de vous revoir.")
                                    st.session_state.event_followups.append(f"{candidate['name']} te propose une sortie qui pourrait faire évoluer votre relation.")
                                    st.balloons()
                                else:
                                    st.session_state.year["close"].append(f"Le courant ne passe pas vraiment avec {candidate['name']}, mais vous vous quittez en bons termes.")
                            elif meeting_choice == "Commencer par une amitié":
                                st.session_state.friends.append(f"{candidate['name']} · nouvel ami")
                                st.session_state.year["close"].append(f"Tu rencontres {candidate['name']} et vous choisissez de commencer par une amitié.")
                            else:
                                st.session_state.year["close"].append(f"Tu déclines poliment la proposition de {candidate['name']}.")
                            st.session_state.dating_candidate = None
                            st.rerun()
                    elif st.button("Faire une rencontre", key="meet_someone"):
                        if st.session_state.orientation == "Asexuel·le":
                            st.session_state.year["close"].append("Tu choisis une activité amicale et rencontres quelqu’un avec qui partager tes passions.")
                            candidate_gender = random.choice(["Fille", "Garçon", "Personne non-binaire"])
                        else:
                            if st.session_state.orientation == "Homosexuel·le":
                                candidate_gender = "Garçon" if st.session_state.gender == "Garçon" else "Fille"
                            elif st.session_state.orientation == "Hétérosexuel·le":
                                candidate_gender = "Fille" if st.session_state.gender == "Garçon" else "Garçon"
                            else:
                                candidate_gender = random.choice(["Fille", "Garçon", "Personne non-binaire"])
                        names = ["Maya", "Noa", "Sacha", "Inès", "Léo", "Camille", "Yanis", "Ari"]
                        occupations = ["étudiant·e", "infirmier·ère", "musicien·ne", "joueur·se de basket", "journaliste", "développeur·se", "artiste"]
                        traits = ["aime les voyages", "est passionné·e de sport", "préfère les soirées calmes", "s’intéresse à la musique", "est très curieux·se", "aime aider les autres"]
                        st.session_state.dating_candidate = {"name": random.choice(names), "gender": candidate_gender, "occupation": random.choice(occupations), "trait": random.choice(traits), "status": "Rencontre"}
                        st.rerun()
        with radio:
            st.markdown("#### 📻 Actualités de l’univers")
            st.caption("Les nouvelles du monde continuent même lorsque tu ne les vis pas directement.")
            for headline in st.session_state.year.get("world_news", []): st.markdown(f'<div class="card">🌐 {headline}</div>', unsafe_allow_html=True)
            st.markdown("#### Ton histoire cette année")
            for event in st.session_state.year["events"]: st.markdown(f'<div class="card">📡 {event}</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="card"><b>Ton statut</b><br>{stage} · {st.session_state.rank}<br><span class="muted">Les activités et interactions sont limitées par ton âge et ton grade.</span></div>', unsafe_allow_html=True)

    with tab_shop:
        st.markdown(f"#### 🪙 Boutique Destin · {st.session_state.coins} pièces")
        st.caption(f"Récompense prévue à la fin de cette vie : {st.session_state.pending_coins} pièces. Les pièces acquises restent dans ta dynastie.")
        shop_items = {"Beauté +10": ("Beauté", 10, 120), "Talent +10": ("Talent", 10, 120), "Santé +10": ("Santé", 10, 120), "Intelligence +10": ("Intelligence", 10, 120), "Bonheur +10": ("Bonheur", 10, 90)}
        item = st.selectbox("Amélioration", list(shop_items))
        stat, amount, price = shop_items[item]
        st.markdown(f'<div class="card"><b>{item}</b><br>Coût : {price} pièces Destin. Achat appliqué à la vie actuelle.</div>', unsafe_allow_html=True)
        if st.button("Acheter", type="primary", disabled=st.session_state.coins < price):
            st.session_state.coins -= price
            st.session_state.stats[stat] = min(100, st.session_state.stats.get(stat, 50) + amount)
            st.success(f"{item} acheté.")
            st.rerun()
        st.markdown("#### 🛒 Boutique de vie")
        st.caption(f"Argent disponible : {st.session_state.money:,} crédits · Les prix montent avec les extrêmes d’honneur ou de réputation négative.")
        life_shop = {
            "Équipement de mission": ("Équipement polyvalent · réduit le risque critique", 650),
            "Livre d’entraînement": ("+8 Intelligence", 420),
            "Matériel sportif": ("+8 Talent · sport", 520),
            "Trousse de soins": ("+10 Santé", 480),
            "Tenue de prestige": ("+8 Beauté", 390),
        }
        if world == "Monde réel" and st.session_state.career == "Héros indépendant":
            life_shop.update({name: (description, price) for name, (price, description) in HERO_ARMORS.items()})
        if world == "Naruto":
            life_shop.update({name: (description, price) for name, (price, description) in NARUTO_GEAR.items()})
        shop_choice = st.selectbox("Article", list(life_shop), key="life_shop_choice")
        description, base_price = life_shop[shop_choice]
        price_multiplier = 1 + abs(st.session_state.honor) / 100
        life_price = round(base_price * price_multiplier)
        consumable = shop_choice in ("Parchemin de jutsu", "Parchemin du mentor ermite", "Parchemin des pupilles")
        owned = shop_choice in st.session_state.inventory and not consumable
        pupil_scroll_locked = shop_choice == "Parchemin des pupilles" and st.session_state.mission_counts.get("S_success", 0) < 1
        jutsu_scroll_locked = shop_choice == "Parchemin de jutsu" and st.session_state.get("world") == "Naruto" and st.session_state.jutsu_level >= len(CLAN_JUTSU.get(st.session_state.clan, CLAN_JUTSU["Inconnu"]))
        st.markdown(f'<div class="card"><b>{shop_choice}</b><br>{description}<br>Prix : {life_price:,} crédits · facteur d’honneur ×{price_multiplier:.2f}</div>', unsafe_allow_html=True)
        if pupil_scroll_locked: st.caption("🔒 Le parchemin des pupilles se débloque après une mission de rang S réussie.")
        if st.button("Acheter avec mes crédits", key="buy_life_item", disabled=owned or st.session_state.money < life_price or pupil_scroll_locked or jutsu_scroll_locked, use_container_width=True):
            st.session_state.money -= life_price
            if not consumable: st.session_state.inventory.append(shop_choice)
            if shop_choice == "Parchemin de jutsu":
                jutsu_list = CLAN_JUTSU.get(st.session_state.clan, CLAN_JUTSU["Inconnu"])
                if st.session_state.jutsu_level < len(jutsu_list):
                    jutsu = jutsu_list[st.session_state.jutsu_level]
                    st.session_state.jutsu_level += 1
                    st.session_state.known_jutsu.append(jutsu)
                    st.success(f"Parchemin déchiffré : tu apprends {jutsu}.")
                else: st.info("Ton clan ne possède plus de nouveau jutsu à apprendre.")
            elif shop_choice == "Parchemin du mentor ermite":
                if "mentor_ermite" not in st.session_state.story_paths: st.session_state.story_paths.append("mentor_ermite")
                st.session_state.event_followups.append("Un mentor ermite reçoit ton parchemin et t’invite à commencer un entraînement spécial.")
            elif shop_choice == "Parchemin des pupilles":
                st.session_state.pupil_power = "Rinnegan"
                st.session_state.pupil_stage = 0
                st.success("Le parchemin t’ouvre une voie rare : le Rinnegan pourra être entraîné à partir de 10 ans.")
            elif shop_choice == "Livre d’entraînement": st.session_state.stats["Intelligence"] = min(100, st.session_state.stats["Intelligence"] + 8)
            elif shop_choice == "Matériel sportif":
                sport_stat = "Basket" if world == "Kuroko Basket" else "Talent"
                st.session_state.stats[sport_stat] = min(100, st.session_state.stats.get(sport_stat, 48) + 8)
            elif shop_choice == "Trousse de soins": st.session_state.stats["Santé"] = min(100, st.session_state.stats["Santé"] + 10)
            elif shop_choice == "Tenue de prestige": st.session_state.stats["Beauté"] = min(100, st.session_state.stats["Beauté"] + 8)
            elif shop_choice in HERO_ARMORS:
                st.session_state.stats["Santé"] = min(100, st.session_state.stats["Santé"] + 4)
                st.session_state.stats["Talent"] = min(100, st.session_state.stats["Talent"] + 3)
            elif shop_choice in ("Étui de kunai renforcé", "Tanto de chakra", "Lot de fumigènes et de fils", "Gants de scellement"):
                st.session_state.year["events"].append(f"Ton équipement {shop_choice.lower()} est ajouté à ton inventaire ninja.")
            st.session_state.year["activities"].append(f"Tu achètes {shop_choice.lower()} pour {life_price} crédits.")
            st.rerun()
        if st.session_state.inventory: st.caption("Possessions : " + " · ".join(st.session_state.inventory))
        st.markdown("#### Défis et récompenses")
        challenges = [("school", "Aller à l’école", "100 pièces"), ("child", "Avoir un enfant", "200 pièces"), ("age_18", "Atteindre 18 ans", "100 pièces"), ("age_25", "Atteindre 25 ans", "100 pièces")]
        for key, label, reward in challenges:
            status = "✅ Accompli" if key in st.session_state.challenges else "À accomplir"
            st.markdown(f'<div class="card">{status} · {label} · 🪙 {reward}</div>', unsafe_allow_html=True)

    with tab_save:
        st.markdown("#### Sauvegarder ou reprendre ta partie")
        save_keys = ["started", "age", "year", "stats", "family", "friends", "children", "clubs", "history", "story_paths", "mission_counts", "jutsu_level", "known_jutsu", "mentor_jutsu", "pupil_power", "pupil_stage", "mentor_training", "mentor_progress", "tailed_beast", "beast_mastery", "orientation", "partner", "dating_candidate", "hero_affiliation", "npc_roster", "npc_memories", "career_skills", "fatigue", "technique_level", "job_tasks", "career_level", "technique", "techniques", "zones", "money", "coins", "pending_coins", "rank", "career", "challenges", "dead", "death_reason", "heir_count", "world", "first", "surname", "gender", "hair", "beard", "avatar", "place", "clan", "generation", "honor", "fame", "inventory", "captured", "event_followups", "event_memory", "news_memory"]
        save_data = {key: st.session_state.get(key) for key in save_keys if key in st.session_state}
        st.download_button("⬇️ Télécharger ma sauvegarde", json.dumps(save_data, ensure_ascii=False, indent=2), file_name="destins_sauvegarde.json", mime="application/json", use_container_width=True)
        uploaded = st.file_uploader("Charger un fichier de sauvegarde", type=["json"])
        if uploaded is not None and st.button("Charger cette partie", type="primary"):
            try:
                loaded = json.loads(uploaded.getvalue().decode("utf-8"))
                for key, value in loaded.items():
                    if key in save_keys: st.session_state[key] = value
                st.success("Sauvegarde chargée.")
                st.rerun()
            except (json.JSONDecodeError, UnicodeDecodeError):
                st.error("Ce fichier de sauvegarde n’est pas valide.")

st.markdown('<p style="text-align:center;color:#8491a2;margin-top:34px">DESTINS · Prototype narratif · Tes choix façonnent la suite</p>', unsafe_allow_html=True)
