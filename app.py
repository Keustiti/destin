import random
import json
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Destins — simulation de vie", page_icon="✨", layout="wide")
st.session_state.setdefault("night_mode", False)

WORLDS = {
    "Monde réel": {"icon": "🌍", "places": ["Lyon, France", "Montréal, Canada", "Dakar, Sénégal", "Tokyo, Japon"], "families": ["Martin", "Diallo", "Moreau", "Bernard", "Leroy"]},
    "Tokyo Revengers": {"icon": "🏍️", "places": ["Shibuya, Tokyo", "Shinjuku, Tokyo", "Yokohama, Japon"], "families": ["Sato", "Mori", "Kobayashi", "Tanaka", "Fujita"]},
    "Kuroko Basket": {"icon": "🏀", "places": ["Tokyo, Japon", "Kanagawa, Japon", "Kyoto, Japon"], "families": ["Kagami", "Kuroko", "Aomine", "Midorima", "Kise"]},
    "Naruto": {"icon": "🍥", "places": ["Konoha", "Suna", "Kiri", "Iwa", "Kumo"], "families": ["Uchiha", "Hyûga", "Nara", "Uzumaki", "Inuzuka", "Akimichi", "Aburame", "Inconnu"]},
    "Jujutsu Kaisen": {"icon": "🔮", "places": ["Tokyo, Japon", "Kyoto, Japon", "Sendai, Japon"], "families": ["Gojo", "Zenin", "Kamo", "Inconnu"]},
}
TOKYO_GANGS = ["Toman", "Black Dragons", "Valhalla", "Tenjiku", "Brahman", "Rokuhara Tandai"]
TOKYO_HIERARCHY = ["Nouveau", "Membre", "Combattant", "Lieutenant", "Capitaine", "Vice-chef", "Chef"]
TOKYO_TERRITORIES = ["Shibuya", "Shinjuku", "Ikebukuro", "Yokohama", "Chiba", "Kawasaki"]
CHAKRA = {"Uchiha": "Feu", "Hyûga": "Foudre", "Nara": "Yin", "Uzumaki": "Vent", "Inuzuka": "Terre", "Akimichi": "Terre", "Aburame": "Terre", "Inconnu": "Vent"}
HAIR = ["Courts et bouclés", "Courts et lisses", "Mi-longs", "Longs", "Ébouriffés", "Tressés"]
BEARDS = ["Pas de barbe", "Barbe légère", "Barbe courte", "Barbe fournie"]
JOBS = ["Facteur", "Analyste", "Livreur", "Militaire", "Vendeur", "Infirmier", "Cuisinier", "Professeur", "Ingénieur", "Journaliste", "Footballeur professionnel", "Sportif professionnel"]
CAREER_TASKS = {
    "Facteur": ["Préparer une tournée prioritaire", "Retrouver un colis mal adressé", "Aider un nouveau collègue"],
    "Analyste": ["Vérifier un rapport avant présentation", "Résoudre une anomalie de données", "Présenter une recommandation à l’équipe"],
    "Livreur": ["Organiser une livraison urgente", "Résoudre un problème d’adresse", "Aider un client à recevoir un colis fragile"],
    "Militaire": ["Participer à un exercice de secours", "Coordonner la logistique de l’unité", "Suivre une formation de spécialité"],
    "Vendeur": ["Conseiller un client sur un achat important", "Organiser la mise en rayon", "Aider un collègue pendant une forte affluence"],
    "Infirmier": ["Préparer le matériel pour le service", "Accompagner un patient et sa famille", "Suivre une formation de soins"],
    "Cuisinier": ["Préparer le service avec l’équipe", "Créer un plat avec les produits disponibles", "Former un nouveau collègue"],
    "Professeur": ["Préparer une activité de classe", "Accompagner un élève en difficulté", "Organiser un projet scolaire"],
    "Ingénieur": ["Vérifier un prototype", "Résoudre un défaut de conception", "Présenter une amélioration à l’équipe"],
    "Journaliste": ["Vérifier une information auprès de deux sources", "Préparer un reportage local", "Protéger une source confidentielle"],
    "Footballeur professionnel": ["Participer à une séance tactique", "Préparer un match avec l’équipe", "Travailler les tirs après l’entraînement"],
    "Sportif professionnel": ["Suivre ton programme de récupération", "Préparer une compétition", "Analyser une performance avec ton entraîneur"],
}
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
MUSIC_TRACKS = [
    ("Piste 1", "wx1GWA_NihQ"), ("Piste 2", "08kp3Cs31Ow"), ("Piste 3", "2uuPU2K_w9c"),
    ("Piste 4", "tZLR2IgoEXM"), ("Piste 5", "fABIBm5OEj4"), ("Piste 6", "2upuBiEiXDk"),
    ("Piste 7", "gcgKUcJKxIs"), ("Piste 8", "By_JYrhx-WY"),
]

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
@keyframes card-enter{from{opacity:0;transform:translateY(10px)}to{opacity:1;transform:translateY(0)}}
@keyframes avatar-float{0%,100%{transform:translateY(0)}50%{transform:translateY(-3px)}}
@keyframes avatar-blink{0%,94%,100%{transform:scaleY(1)}96%{transform:scaleY(.12)}}
@keyframes action-fx-fade{0%{opacity:0}12%{opacity:1}76%{opacity:1}100%{opacity:0}}
@keyframes action-fx-slash{0%{transform:translate(-135px,55px) rotate(-35deg) scale(.5)}45%{transform:translate(15px,-10px) rotate(30deg) scale(1.15)}100%{transform:translate(135px,-65px) rotate(75deg) scale(.45)}}
@keyframes action-fx-spark{0%,100%{opacity:0;transform:scale(.2) rotate(0)}40%{opacity:1;transform:scale(1.35) rotate(70deg)}75%{opacity:.7;transform:scale(.75) rotate(140deg)}}
@keyframes action-fx-shot{0%{transform:translate(-100px,80px) rotate(0) scale(.7)}62%{transform:translate(56px,-48px) rotate(420deg) scale(1.05)}82%{transform:translate(78px,-20px) rotate(540deg) scale(.82)}100%{transform:translate(84px,10px) rotate(650deg) scale(.4);opacity:0}}
@keyframes action-fx-hoop{0%,60%,100%{transform:scale(1);filter:drop-shadow(0 0 0 transparent)}78%{transform:scale(1.18);filter:drop-shadow(0 0 15px #ffb22c)}}
@keyframes action-fx-energy{0%{transform:scale(.25) rotate(-30deg);opacity:0}35%{transform:scale(1.3) rotate(100deg);opacity:1}75%{transform:scale(.8) rotate(240deg);opacity:.8}100%{transform:scale(1.4) rotate(360deg);opacity:0}}
@keyframes action-fx-hero{0%,100%{transform:translateY(-80px) scale(.5);opacity:0}28%{transform:translateY(0) scale(1.2);opacity:1}65%{transform:translateY(8px) scale(1);opacity:1}}
@keyframes action-fx-work{0%{transform:translateY(42px) rotate(-20deg) scale(.4);opacity:0}40%{transform:translateY(-9px) rotate(10deg) scale(1.15);opacity:1}75%{transform:translateY(0) rotate(0) scale(1);opacity:1}100%{transform:translateY(-18px) scale(.8);opacity:0}}
@keyframes action-fx-moto{0%{transform:translate(-135px,15px) rotate(-14deg) scale(.7);opacity:0}18%{opacity:1}54%{transform:translate(16px,-12px) rotate(7deg) scale(1.15)}100%{transform:translate(135px,12px) rotate(14deg) scale(.75);opacity:0}}
.action-fx{position:fixed;inset:0;z-index:1100;display:grid;place-items:center;pointer-events:none;animation:action-fx-fade 1.8s ease-out both}
.action-fx__stage{position:relative;width:250px;height:180px;border-radius:28px;background:radial-gradient(ellipse,#ffffffd9 0%,#f5f8fc88 45%,transparent 74%);filter:drop-shadow(0 8px 20px #102b3d24)}
.action-fx__object,.action-fx__target,.action-fx__spark{position:absolute;display:grid;place-items:center;line-height:1}
.action-fx__object{left:84px;top:61px;font-size:64px}
.action-fx__target{right:38px;top:48px;font-size:42px}
.action-fx__spark{left:102px;top:41px;font-size:37px}
.scene-kunai .action-fx__object{animation:action-fx-slash 1.25s cubic-bezier(.2,.72,.26,1) both}
.scene-gang .action-fx__object{animation:action-fx-moto 1.4s cubic-bezier(.2,.72,.26,1) both;filter:drop-shadow(0 0 14px #ef642e)}
.scene-gang .action-fx__spark{animation:action-fx-spark .9s .4s ease-out both}
.scene-kunai .action-fx__spark{animation:action-fx-spark .8s .48s ease-out both}
.scene-basket .action-fx__object{animation:action-fx-shot 1.35s cubic-bezier(.25,.6,.3,1) both}
.scene-basket .action-fx__target{right:43px;top:47px;width:58px;height:37px;border:5px solid #ef792c;border-top:0;border-radius:0 0 26px 26px;animation:action-fx-hoop 1.35s ease-out both}
.scene-basket .action-fx__target:before{content:"";position:absolute;right:-10px;top:-27px;width:5px;height:26px;background:#405a72;box-shadow:10px 0 #405a72,20px 0 #405a72}
.scene-basket .action-fx__target:after{content:"";position:absolute;top:0;width:36px;height:24px;background:repeating-linear-gradient(115deg,transparent 0 7px,#d9e2ec 7px 9px,transparent 9px 15px);clip-path:polygon(0 0,100% 0,75% 100%,25% 100%)}
.scene-chakra .action-fx__object,.scene-occult .action-fx__object{animation:action-fx-energy 1.35s ease-out both;filter:drop-shadow(0 0 16px #8061ff)}
.scene-chakra .action-fx__spark,.scene-occult .action-fx__spark{animation:action-fx-spark .9s .2s ease-out both}
.scene-hero .action-fx__object{animation:action-fx-hero 1.25s ease-out both;color:#f5ad25;filter:drop-shadow(0 0 12px #ffda66)}
.scene-hero .action-fx__target{animation:action-fx-energy 1.1s .12s ease-out both}
.scene-work .action-fx__object,.scene-sport .action-fx__object,.scene-life .action-fx__object{animation:action-fx-work 1.35s ease-out both}
.scene-work .action-fx__spark,.scene-sport .action-fx__spark,.scene-life .action-fx__spark{animation:action-fx-spark .9s .3s ease-out both}
.card{animation:card-enter .38s ease-out both}
.avatar svg{animation:avatar-float 4s ease-in-out infinite}
.avatar .eye{transform-box:fill-box;transform-origin:center;animation:avatar-blink 5.5s ease-in-out infinite}
.stButton>button{transition:transform .16s ease,filter .16s ease,box-shadow .16s ease}
.stButton>button:hover{filter:brightness(1.06);box-shadow:0 4px 12px #102b3d22}
.stButton>button:active{transform:scale(.97)}
.stProgress>div>div>div>div{transition:width .55s ease}
@media(prefers-reduced-motion:reduce){*,*::before,*::after{animation-duration:.01ms!important;animation-iteration-count:1!important;scroll-behavior:auto!important;transition-duration:.01ms!important}}
@media(max-width:600px){
  .block-container{padding:0 14px 10.5rem;margin:0 auto}
  .hero{margin-left:-14px;margin-right:-14px}
  .face{font-size:2.7rem}
  [data-testid="stTabs"] [role="tablist"]{
    bottom:54px;left:0;transform:none;width:100vw;max-width:100vw;
    display:flex;justify-content:flex-start;gap:4px;padding:6px 8px;
    overflow-x:auto;overflow-y:hidden;scrollbar-width:none;
    -webkit-overflow-scrolling:touch;overscroll-behavior-x:contain
  }
  [data-testid="stTabs"] [role="tablist"]::-webkit-scrollbar{display:none}
  [data-testid="stTabs"] button[role="tab"],.stTabs button[role="tab"]{
    flex:0 0 auto;width:76px;min-width:76px;min-height:48px;
    padding:7px 4px;font-size:.68rem;line-height:1.1
  }
  [data-testid="stTabs"] button[role="tab"]:nth-child(4){display:none}
  .st-key-advance_year_fixed{bottom:112px;width:112px}
  .st-key-advance_year_fixed button{min-height:42px;font-size:.72rem}
  [data-testid="stMarkdown"] h3,[data-testid="stMarkdown"] h4{font-size:1.1rem;line-height:1.3}
  .card{padding:12px 13px;margin:7px 0}
  [data-testid="stSelectbox"] label,[data-testid="stRadio"] label{font-size:.95rem}
}
</style>""", unsafe_allow_html=True)

if st.session_state.get("night_mode"):
    st.markdown("""<style>
    .stApp,[data-testid="stAppViewContainer"],[data-testid="stMain"]{background:#101722!important;color:#edf2f7!important}
    [data-testid="stMarkdownContainer"],.stMarkdown,p,label,h1,h2,h3,h4,h5,h6,li,small{color:#edf2f7}
    .card,.avatar,[data-testid="stMetric"],[data-testid="stVerticalBlockBorderWrapper"]{background:#1a2533!important;color:#edf2f7!important;border-color:#344255!important}
    .muted{color:#b4c0cf!important}
    .stTextInput input,.stTextArea textarea,[data-baseweb="select"]>div,[data-baseweb="input"]>div,
    [data-testid="stNumberInput"] input,[data-testid="stDateInput"] input{background:#15202d!important;color:#f4f7fb!important;border-color:#47566a!important}
    [data-baseweb="popover"],[role="listbox"],[role="option"]{background:#1a2533!important;color:#f4f7fb!important}
    [data-testid="stDataFrame"]{filter:brightness(.82) contrast(1.05)}
    [data-testid="stFileUploader"],[data-testid="stAlert"]{background:#1a2533;color:#edf2f7}
    .action-fx__stage{background:radial-gradient(ellipse,#26364ddd 0%,#15202d88 45%,transparent 74%)}
    .stButton>button:not([data-testid="stBaseButton-primary"]){background:#24364a;color:#f4f7fb;border-color:#53647a}
    </style>""", unsafe_allow_html=True)

def init():
    defaults = {"started": False, "age": 0, "year": {"activities": [], "events": [], "close": [], "training_counts": {}}, "stats": {"Bonheur": 72, "Santé": 88, "Intelligence": 54, "Talent": 48, "Beauté": 55}, "family": [], "friends": [], "children": [], "clubs": [], "history": [], "story_paths": [], "mission_counts": {}, "jutsu_level": 0, "known_jutsu": [], "mentor_jutsu": [], "pupil_power": "", "pupil_stage": 0, "mentor_training": [], "mentor_progress": {}, "tailed_beast": "", "beast_mastery": 0, "orientation": "Je préfère ne pas préciser", "partner": None, "dating_candidate": None, "hero_affiliation": "", "npc_roster": [], "npc_memories": [], "career_skills": {}, "fatigue": 10, "technique_level": 1, "job_tasks": 0, "career_level": 0, "money": 1200, "coins": 0, "pending_coins": 0, "rank": "Civil", "career": "Aucune", "technique": "Aucune", "techniques": [], "zones": [], "challenges": [], "dead": False, "death_reason": "", "heir_count": 0, "current_page": "Année en cours", "honor": 0, "fame": 0, "inventory": [], "captured": False, "event_followups": [], "event_memory": [], "news_memory": [], "music_open": True, "music_track": "wx1GWA_NihQ"}
    defaults["action_animation"] = None
    defaults.update(gang="", gang_rank="Nouveau", gang_renown=0, gang_reputation=0, gang_allies=[], gang_territories=[], gang_members=1, gang_mission_successes=0, school_attendance=0)
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value
    st.session_state.setdefault("family_bonds", {})
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
    elif world == "Tokyo Revengers":
        jobs = ["élève et membre de gang", "mécanicienne de motos", "capitaine de division", "gérante d’un café", "médiateur de quartier"]
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
    elif world == "Tokyo Revengers": names = ["Combat", "Endurance", "Leadership", "Réputation", "Mécanique"]
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
    jobs = {"Naruto": ["genin studieuse", "sensei de taijutsu", "ninja médecin", "archiviste du village", "rival de ton équipe"], "Kuroko Basket": ["meneur de jeu", "entraîneuse du club", "rival au tir", "arbitre bénévole", "recruteur régional"], "Jujutsu Kaisen": ["élève exorciste", "mentor de terrain", "gardienne des archives", "rival de Kyoto", "médecin de l’école"], "Tokyo Revengers": ["capitaine de division", "rival de gang", "mécanicienne moto", "médiateur de quartier", "ami du lycée"], "Monde réel": ["apprentie cuisinière", "mécanicien", "étudiant en arts", "soigneuse bénévole", "journaliste locale", "entraîneur de quartier"]}
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
    positive = any(word in choice.lower() for word in ["aider", "aide", "encourager", "s’excuser", "protéger", "partager", "conseil", "entraîner", "service", "soutenir", "message", "discuter", "activité", "sortie", "inviter"])
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
    elif world == "Tokyo Revengers":
        target = "Leadership" if any(word in text for word in ("alliance", "recrut", "chef", "capitaine")) else "Réputation" if any(word in text for word in ("territoire", "gang", "rival")) else "Mécanique" if any(word in text for word in ("moto", "garage")) else "Combat" if any(word in text for word in ("mission", "défi", "combat")) else "Endurance"
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
        "Tokyo Revengers": ["La radio locale annonce une trêve fragile entre deux factions de Tokyo.", "Un rassemblement de gangs est signalé près d’une gare; les habitants demandent le calme.", "Un atelier de mécanique propose des apprentissages aux jeunes du quartier.", "Une association organise un tournoi sportif pour éloigner les adolescents des conflits.", "Un chef de gang disparaît et plusieurs divisions attendent des nouvelles.", "Une réunion de médiation pourrait éviter une rivalité territoriale.", "Des motos customisées attirent l’attention lors d’un rassemblement nocturne.", "Une ancienne faction cherche à recruter dans les collèges du secteur.", "Les commerçants de Shibuya lancent une initiative pour sécuriser les rues.", "Un conflit de leadership divise une organisation en deux camps.", "Un club scolaire ouvre ses portes après les cours.", "Une rumeur annonce une alliance entre gangs de Tokyo et de Yokohama.", "Un capitaine respecte une promesse faite à un ancien rival.", "Un quartier demande aux jeunes leaders d’organiser une collecte solidaire.", "Une course caritative de motos anciennes réunit plusieurs générations.", "La police renforce sa présence après une série d’incidents dans le centre-ville."],
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
    if world == "Tokyo Revengers":
        return (stats.get("Talent", 48) + stats.get("Santé", 50) + st.session_state.get("gang_renown", 0)) // 3 + TOKYO_HIERARCHY.index(st.session_state.get("gang_rank", "Nouveau")) * 5 - fatigue_penalty
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
    if world == "Tokyo Revengers":
        gang_missions = {"D": ["Patrouille de quartier", "Retrouver une moto volée", "Aider un commerce local"], "C": ["Escorter un membre jusqu’au QG", "Enquête sur un symbole rival", "Régler un différend sans escalade"], "B": ["Défi de territoire · négociation", "Protéger une réunion de division", "Épreuve de loyauté du gang"], "A": ["Conflit de factions · protéger les alliés", "Défi de territoire · stratégie d’équipe", "Retrouver un capitaine disparu"], "S": ["Grande réunion des gangs de Tokyo", "Alliance menacée · mission de médiation", "Défi de leadership entre divisions"], "SS": ["Guerre des factions · avenir de Tokyo", "Dernière bataille pour l’unité du gang", "Sommet des gangs · décision historique"]}
        return f"{gang_missions[rank][st.session_state.mission_counts.get(rank, 0) % len(gang_missions[rank])]} · {st.session_state.get('gang', 'gang indépendant')}"
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
    if world == "Tokyo Revengers": return ["Protéger les membres et les passants", "Négocier une trêve", "Mener la stratégie de la division", "Provoquer le gang rival"]
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
        if world == "Tokyo Revengers":
            st.session_state.gang_renown = min(100, st.session_state.get("gang_renown", 0) + {"D": 2, "C": 4, "B": 6, "A": 9, "S": 13, "SS": 18}[rank])
            st.session_state.gang_mission_successes = st.session_state.get("gang_mission_successes", 0) + 1
            territory_options = [area for area in TOKYO_TERRITORIES if area not in st.session_state.gang_territories]
            if "territoire" in title.lower() and territory_options:
                gained_territory = territory_options[0]
                st.session_state.gang_territories.append(gained_territory)
                result += f" {st.session_state.gang} gagne l’influence sur {gained_territory} après ce défi."
            current_index = TOKYO_HIERARCHY.index(st.session_state.get("gang_rank", "Membre"))
            if st.session_state.gang_mission_successes >= max(2, current_index + 1) and current_index < len(TOKYO_HIERARCHY) - 1:
                st.session_state.gang_rank = TOKYO_HIERARCHY[current_index + 1]
                st.session_state.gang_mission_successes = 0
                st.session_state.gang_renown = min(100, st.session_state.gang_renown + 4)
                result += f" Tes actes sont reconnus : tu montes au rang de {st.session_state.gang_rank}."
            st.session_state.gang_reputation = max(-100, min(100, st.session_state.get("gang_reputation", 0) + (3 if any(word in approach.lower() for word in ("protéger", "négocier")) else -2)))
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
    trigger_action_animation(world, f"mission match combat {title}", st.session_state.career)
    return result, chance, risk

def exploration_catalog(world, age, career, rank, place, clubs, hero_affiliation):
    """Return age-, world-, and career-appropriate places with one-year visit actions."""
    spots = {}

    def option(label, stat, bonus, messages, followups, training=False, money=0):
        return (label, stat, bonus, messages, followups, training, money)

    if world == "Monde réel":
        if age < 3:
            spots["Maison familiale"] = [option("Jouer avec un proche", "Bonheur", 3, ["Tu découvres un nouvel objet avec un parent.", "Un proche te raconte une histoire que tu écoutes attentivement."], ["Ton proche garde une photo de cette journée.", "Un membre de la famille propose une sortie pour l’année prochaine."])]
            spots["Parc avec un parent"] = [option("Observer les oiseaux et les passants", "Bonheur", 3, ["La promenade t’apaise et attire les sourires des passants.", "Tu découvres les couleurs et les sons du parc avec ton proche."], ["Un voisin croisé au parc reconnaît ta famille et vient prendre des nouvelles.", "Ton proche te propose de retrouver une autre famille au parc."])]
        elif age < 6:
            spots["Parc du quartier"] = [option("Jouer sur les jeux avec un proche", "Bonheur", 3, ["Tu prends confiance en explorant le parc.", "Tu te fais un petit camarade pendant que ton parent te surveille."], ["Un parent propose une sortie avec le nouvel ami que tu as rencontré.", "Ta famille reçoit une invitation d’un voisin croisé au parc."])]
            spots["Maternelle"] = [option("Participer à l’atelier créatif", "Talent", 3, ["Tu fabriques un objet coloré et le rapportes à la maison.", "La maîtresse remarque ton imagination pendant l’atelier."], ["La maternelle prépare une fête où ta famille sera invitée.", "Un camarade veut refaire l’activité avec toi la semaine prochaine."])]
        else:
            spots["Centre-ville · " + place] = [option("Découvrir une nouvelle rue", "Bonheur", 2, ["Tu découvres une petite librairie et un café apprécié du quartier.", "Un commerçant t’indique un passage piéton plus calme.", "Une affiche annonce un événement local inattendu."], ["Une personne rencontrée en ville te recontacte avec une proposition.", "Une animation du quartier prépare une nouvelle sortie."]), option("Aider lors d’un événement de quartier", "Honneur", 2, ["Tu aides les organisateurs et fais la connaissance de plusieurs habitants.", "Ton coup de main permet à l’événement de se dérouler sans retard."], ["L’association du quartier te sollicite pour une autre initiative.", "Un habitant te confie une information utile sur un prochain événement."]) ]
            spots["Parc municipal"] = [option("Marcher et prendre l’air", "Santé", 2, ["La marche te fait du bien et baisse ta fatigue.", "Tu prends le temps de discuter avec un voisin du quartier."], ["Un proche te propose une promenade commune.", "Un voisin rencontré au parc te demande un conseil l’année prochaine."]), option("Observer une activité sportive", "Intelligence", 2, ["Tu repères une nouvelle activité qui pourrait te plaire.", "Tu analyses les exercices d’un groupe qui s’entraîne."], ["Le club local organise une journée découverte.", "Une personne du groupe te propose de venir essayer une séance."]) ]
            spots["Médiathèque"] = [option("Lire et emprunter un livre", "Intelligence", 3, ["Tu découvres un sujet qui nourrit ta curiosité.", "Un bibliothécaire te conseille un livre adapté à tes projets."], ["La médiathèque organise une rencontre autour de ce sujet.", "Le livre te donne une idée de projet à essayer l’année prochaine."]), option("Participer à un atelier", "Talent", 2, ["Tu apprends une nouvelle façon de créer ou de présenter tes idées.", "L’atelier te met en contact avec des personnes curieuses comme toi."], ["Un participant te propose de continuer le projet ensemble.", "L’atelier annonce un niveau avancé pour l’année prochaine."]) ]
            if age >= 12:
                spots["Gymnase municipal"] = [option("Faire une séance d’essai", "Santé", 4, ["La séance te donne envie de bouger plus souvent.", "Un entraîneur remarque ton sérieux et te donne un conseil."], ["Le club ouvrira bientôt de nouvelles inscriptions.", "Un joueur du gymnase t’invite à un match amical."], training=True), option("Parler à un entraîneur", "Intelligence", 2, ["Tu découvres les horaires et les exigences d’un club local.", "Un entraîneur te conseille une préparation progressive."], ["Une sélection ouverte sera organisée prochainement.", "Un stage sportif pourrait se libérer pendant les vacances."]) ]
        if age >= 18 and career != "Aucune":
            job = career.split(" ·")[0]
            job_places = {
                "Facteur": ("Centre de tri postal", "Préparer une tournée inhabituelle", "Talent", "Tu repères un itinéraire plus sûr et aides un collègue à rattraper son retard.", "Un pli urgent trouvé au centre de tri ouvre une tournée spéciale.", "Le responsable te confie bientôt une tournée plus complexe.", True, 100),
                "Analyste": ("Bureau d’analyse", "Vérifier un dossier de données", "Intelligence", "Tu découvres une anomalie qui avait échappé à l’équipe.", "Une série de données inexpliquées mérite un nouvel examen.", "Ta vérification attire l’attention d’une équipe spécialisée.", False, 120),
                "Livreur": ("Dépôt de livraison", "Organiser une tournée urgente", "Talent", "Tu réorganises les colis pour éviter un détour inutile.", "Un colis sans destinataire clair lance une recherche inattendue.", "Le dépôt reçoit une mission de livraison prioritaire.", True, 100),
                "Militaire": ("Base de l’unité", "Étudier un exercice de secours", "Intelligence", "Tu identifies un point faible dans le plan et proposes une amélioration.", "Une simulation révèle un nouveau scénario à préparer.", "Ton unité reçoit une affectation d’entraînement hors site.", True, 120),
                "Vendeur": ("Boutique", "Aider un client à choisir", "Bonheur", "Tu trouves une solution adaptée et gagnes la confiance d’un client régulier.", "Un client revient avec une demande qui sort de l’ordinaire.", "La boutique prépare une opération commerciale importante.", False, 100),
                "Infirmier": ("Hôpital", "Accompagner une équipe de soins", "Intelligence", "Tu aides l’équipe à mieux organiser l’accueil des patients.", "Un patient reconnaissant revient partager une nouvelle importante.", "Le service prépare une formation à laquelle tu pourrais participer.", True, 100),
                "Cuisinier": ("Cuisine du restaurant", "Préparer le service avec l’équipe", "Talent", "Tu adaptes le menu aux réserves et le service se déroule sans gaspillage.", "Un critique culinaire réserve une table sans prévenir.", "Le chef te propose de créer un plat pour une soirée spéciale.", True, 100),
                "Professeur": ("Établissement scolaire", "Préparer un atelier avec les élèves", "Intelligence", "Tes élèves proposent un projet qui les motive à travailler ensemble.", "Une famille te confie une inquiétude qui demande un suivi.", "L’établissement prépare une sortie éducative originale.", False, 100),
                "Ingénieur": ("Atelier de prototypage", "Tester un prototype", "Intelligence", "Tu repères une pièce à renforcer avant la prochaine démonstration.", "Un prototype oublié révèle une piste technique prometteuse.", "Une équipe partenaire propose un essai sur le terrain.", True, 120),
                "Journaliste": ("Rédaction", "Recouper une information", "Intelligence", "Tu retrouves une seconde source et évites une erreur de publication.", "Une source anonyme propose de parler d’un dossier sensible.", "La rédaction reçoit un document qui pourrait changer une enquête.", False, 120),
                "Footballeur professionnel": ("Stade et centre d’entraînement", "Analyser une séquence de match", "Intelligence", "Tu repères un espace libre que ton équipe pourrait exploiter.", "Un recruteur étranger assiste discrètement à la prochaine rencontre.", "Le staff annonce une séance avec un entraîneur invité.", True, 150),
                "Sportif professionnel": ("Centre sportif", "Évaluer ta récupération", "Santé", "Tu ajustes ta préparation et évites une surcharge.", "Un partenaire d’entraînement te propose un défi amical.", "Le centre reçoit un spécialiste qui propose un stage.", True, 150),
            }
            if job in job_places:
                location, label, stat, first, second, followup, training, money = job_places[job]
                spots[location] = [option(label, stat, 3, [first, second], [followup, "Une rencontre au travail te donne une piste à suivre l’année prochaine."], training=training, money=money), option("Échanger avec un collègue", "Bonheur", 2, ["Un collègue partage une astuce qui te sera utile.", "Tu aides un collègue à résoudre un problème pressant."], ["Ce collègue te proposera bientôt de travailler sur un nouveau dossier.", "Un autre membre de l’équipe veut te présenter un contact."], money=80)]
            elif "Héros" in career:
                association_base = f"Base · {hero_affiliation}" if hero_affiliation else "Base de l’association héroïque"
                spots[association_base] = [option("Préparer une intervention avec l’équipe", "Talent", 4, ["Tu coordonnes les rôles et l’équipe se prépare à intervenir.", "Une simulation révèle un point faible que tu peux corriger."], ["Une alerte de quartier mobilise bientôt ton association.", "Un héros d’une autre équipe te demande conseil."], training=True), option("Étudier les alertes de la ville", "Intelligence", 3, ["Tu repères un motif récurrent dans les signalements.", "Une carte des incidents révèle une zone à surveiller."], ["Une nouvelle piste apparaît près du centre-ville.", "L’association reçoit une demande d’aide inhabituelle."])]

    elif world == "Kuroko Basket" and age < 6:
        spots["Parc avec un proche"] = [option("Faire rouler le ballon avec ta famille", "Bonheur", 3, ["Tu découvres le ballon en jouant avec un proche.", "Un petit panier improvisé fait rire toute la famille."], ["Un proche garde une photo de cette première partie.", "Ta famille propose de revenir au parc lors d’une prochaine belle journée."]) ]
        spots["Petit terrain de quartier"] = [option("Lancer le ballon dans un mini-panier", "Talent", 2, ["Tu t’amuses à viser un panier adapté à ta taille.", "Tu applaudis quand le ballon passe dans le petit panier."]) ]
    elif world == "Kuroko Basket":
        spots["Terrain de quartier · " + place] = [option("Jouer un un-contre-un", "Basket", 3, ["Un duel amical t’oblige à varier tes appuis.", "Un joueur inconnu te pousse à accélérer ton jeu."], ["Ce joueur te propose une revanche avec un coéquipier.", "Un observateur du club local a remarqué ton style."], training=True), option("Inviter un proche à regarder", "Bonheur", 2, ["Un proche découvre ce qui te plaît dans le basket.", "Vous partagez un moment convivial autour du terrain."], ["Ton proche veut assister à un futur match.", "Un autre membre de ta famille souhaite venir t’encourager."]) ]
        if age < 12:
            spots["Atelier de mini-basket"] = [option("Apprendre les passes et les appuis", "Basket", 3, ["Un éducateur adapte les exercices à ton âge.", "Tu réussis une passe précise à un nouveau camarade."], ["L’éducateur prépare une rencontre amicale entre ateliers.", "Un camarade te propose de former un duo au prochain entraînement."], training=True), option("Participer au jeu collectif", "Bonheur", 2, ["Tu apprends à jouer avec les autres plutôt que seul.", "Ton équipe invente une célébration après un beau panier."], ["L’atelier reçoit une invitation pour une petite rencontre locale.", "Un parent propose d’accompagner l’équipe au prochain événement."]) ]
        elif age < 15:
            spots["Gymnase du collège Teikō"] = [option("Répéter les fondamentaux", "Basket", 4, ["Tu travailles tes appuis et tes passes sous le regard des entraîneurs.", "La séance te confronte à un joueur au talent exceptionnel."], ["Un ancien coéquipier de Teikō te lance un défi.", "Un tournoi scolaire pourrait réunir les meilleurs joueurs."], training=True), option("Observer les meilleurs joueurs", "Intelligence", 3, ["Tu repères comment les joueurs créent de l’espace pour leurs coéquipiers.", "Le jeu d’un prodige te donne une idée à essayer."], ["Un joueur de la Génération des Miracles entend parler de toi.", "Un entraîneur te conseille de développer une spécialité."]) ]
        else:
            seirin_available = "Club de basket" in clubs or "Espoir du basket" in career or "Footballeur professionnel" in career
            if seirin_available:
                spots["Gymnase du lycée Seirin"] = [option("Répéter les combinaisons d’équipe", "Basket", 4, ["Tes passes rapides déstabilisent les défenseurs pendant l’exercice.", "Un coéquipier improvise une combinaison qui pourrait surprendre un rival."], ["Le coach prépare une rencontre contre un lycée réputé.", "Un rival a observé votre entraînement et prépare une réponse."], training=True), option("Analyser une vidéo de match", "Intelligence", 3, ["Tu repères une faille dans la défense d’une équipe rivale.", "Une séquence de match révèle un nouveau mouvement à travailler."], ["Le coach reçoit une demande pour un match amical.", "Une vidéo de l’équipe circule auprès de recruteurs universitaires."]) ]
            spots["Arène du tournoi inter-lycées"] = [option("Observer les équipes rivales", "Intelligence", 3, ["Tu notes les stratégies de plusieurs équipes favorites.", "Un match intense te donne une idée pour un prochain duel."], ["Un tirage au sort prépare une rencontre difficile.", "Un joueur adverse te propose un duel après le tournoi."]), option("Participer à un concours de tirs", "Basket", 3, ["Tu réussis une série de tirs sous pression.", "Tu rates de peu un tir mais trouves un meilleur rythme."], ["Un recruteur demande à revoir tes statistiques.", "Un joueur rival veut comparer vos tirs au prochain entraînement."], training=True)]
        if age >= 10:
            spots["Centre sportif municipal"] = [option("Faire une séance de mobilité", "Santé", 3, ["Tu améliores ton équilibre et récupères mieux après les matchs.", "Un préparateur te recommande un exercice adapté à ton poste."], ["Un stage de préparation physique ouvre bientôt ses portes.", "Un préparateur invite ton équipe à une séance collective."], training=True), option("Rencontrer d’autres joueurs", "Bonheur", 2, ["Tu échanges des conseils avec des joueurs d’autres clubs.", "Une nouvelle amitié naît autour d’un défi de tirs."], ["Les joueurs rencontrés organisent un tournoi amical.", "Un nouveau rival veut se mesurer à ton équipe."]) ]

    elif world == "Tokyo Revengers":
        if age < 12:
            spots["Parc du quartier · " + place] = [option("Jouer avec des camarades", "Bonheur", 3, ["Tu rencontres des enfants du quartier pendant une partie improvisée.", "Un proche te présente à une famille du voisinage."], ["Un camarade t’invite à un club scolaire l’année prochaine.", "Une famille rencontrée au parc propose une sortie commune."]) ]
        else:
            spots["Centre-ville · " + place] = [option("Aider un commerce de quartier", "Honneur", 3, ["Tu aides les commerçants à ranger après une journée chargée.", "Les habitants apprécient ton aide et retiennent ton visage."], ["Une commerçante te demande de l’aider à organiser la fête du quartier.", "Un commerçant te signale qu’un autre groupe cherche à intimider les boutiques."]) ]
            spots["Garage associatif"] = [option("Apprendre les bases de la mécanique moto", "Talent", 3, ["Un mécanicien t’apprend à vérifier les freins et l’éclairage.", "Tu aides à remettre en état une vieille moto de quartier."], ["Le garage prépare une course caritative et cherche des bénévoles.", "Un ancien du quartier te propose un apprentissage régulier."], training=True), option("Discuter avec les jeunes du quartier", "Bonheur", 2, ["Tu fais connaissance avec des jeunes qui ne fréquentent pas ton gang.", "Une conversation calme évite un malentendu entre deux groupes."], ["Un ami te demande d’organiser une rencontre entre les deux groupes.", "Un jeune que tu as aidé vient te demander conseil."]) ]
            if st.session_state.get("gang"):
                spots[f"QG · {st.session_state.gang}"] = [option("Préparer la réunion de division", "Intelligence", 3, ["Tu organises les priorités de la division et écoutes chaque membre.", "Une bonne préparation aide le gang à éviter une dispute inutile."], ["Le capitaine te confie bientôt une tâche plus importante.", "Une information sur une faction rivale arrive au QG."]), option("Entraîner les membres", "Talent", 3, ["Tu organises un entraînement encadré axé sur la discipline et la cohésion.", "Les membres apprennent à rester soudés sans mettre les passants en danger."], ["Un membre veut te défier pour gagner une place dans la division.", "Le capitaine propose un exercice collectif entre divisions."], training=True)]
                territory = next((area for area in TOKYO_TERRITORIES if area not in st.session_state.get("gang_territories", [])), None)
                if territory:
                    spots[f"Territoire contesté · {territory}"] = [option("Négocier une influence locale", "Intelligence", 3, ["Tu proposes une entente aux associations locales au lieu d’imposer ta présence.", "Une médiation ouvre une discussion avec la faction qui contrôle le secteur."], [f"La faction rivale accepte un sommet à propos de {territory}.", "Les commerçants souhaitent participer aux prochaines négociations."]), option("Organiser un défi de territoire", "Talent", 4, ["Ton équipe se mesure aux rivaux dans un défi encadré loin des passants.", "Un face-à-face tendu se termine par un accord provisoire."], [f"Le résultat du défi sur {territory} attire l’attention d’un autre gang.", "Le rival propose une revanche ou une trêve durable."], training=True)]
    elif world == "Naruto":
        village = place or "Konoha"
        if age < 6:
            spots[f"Domaine familial · clan {st.session_state.get('surname', 'inconnu')}"] = [option("Écouter une histoire du clan", "Intelligence", 3, ["Un ancien de la famille te raconte une histoire transmise depuis plusieurs générations.", "Tu apprends pourquoi ton clan protège certaines traditions."], ["Un membre du clan promet de te montrer un objet familial.", "Une question sur l’histoire du clan reste sans réponse." ]), option("Aider un proche au village", "Bonheur", 2, ["Tu accompagnes ta famille et salues plusieurs voisins.", "Un habitant remercie ta famille pour son aide."], ["Un voisin te transmettra une demande adressée à ton clan.", "Un proche prépare une visite chez un autre membre de la famille."]) ]
        else:
            spots[f"Académie ninja de {village}"] = [option("Réviser les règles et les bases", "Intelligence", 3, ["Tu maîtrises mieux les règles de l’académie.", "Un enseignant te confie un exercice supplémentaire."], ["Un examen pratique est annoncé à l’académie.", "Un camarade te demande de l’aider à réviser." ]), option("Aider un autre élève", "Bonheur", 2, ["Ton camarade n’oublie pas que tu l’as aidé.", "Vous trouvez ensemble une façon plus simple de réussir l’exercice."], ["Ton camarade viendra te demander conseil avant l’examen.", "Un sensei remarque votre coopération et vous confie une tâche d’équipe."]) ]
            spots[f"Terrain d’entraînement de {village}"] = [option("Travailler le contrôle du chakra", "Talent", 4, ["Tu stabilises ton chakra sur une surface difficile.", "Ton contrôle s’améliore après plusieurs essais méthodiques."], ["Un sensei te propose une épreuve de contrôle avancée.", "Un autre élève veut tester son contrôle contre le tien."], training=True), option("Répéter les lancers de kunai", "Talent", 3, ["Tes tirs se rapprochent du centre de la cible.", "Tu ajustes ta posture et gagnes en précision."], ["Un instructeur te propose un exercice en mouvement.", "Un adversaire de l’académie te défie au lancer de kunai."], training=True)]
            if age >= 12 and rank in ("Genin", "Chûnin", "Jônin", "Hokage"):
                spots[f"Bureau des missions · {village}"] = [option("Étudier un rapport de mission", "Intelligence", 3, ["Tu découvres une piste oubliée dans un ancien rapport.", "Les détails du rapport indiquent que la mission pourrait avoir une suite."], ["Le bureau reçoit un nouvel indice lié au rapport.", "Un chef d’équipe te convoque pour parler de ta découverte."]), option("Proposer une patrouille", "Talent", 2, ["Le responsable accepte que tu participes à une patrouille adaptée à ton grade.", "Tu repères un mouvement suspect sans mettre ton équipe en danger."], ["La patrouille découvre une piste près d’une frontière.", "Un rapport diplomatique demande une vérification discrète."]) ]
                if village == "Konoha":
                    spots["Terrain 44 · Forêt de la Mort"] = [option("Observer les pièges depuis la lisière", "Intelligence", 3, ["Tu repères les marques d’un piège avant de t’approcher.", "Une trace inhabituelle suggère que quelqu’un est passé récemment."], ["Un parchemin manquant est signalé près du terrain 44.", "Un groupe prépare une épreuve dans la forêt et cherche des volontaires." ]), option("Parcourir un sentier balisé", "Talent", 3, ["Tu traverses un parcours difficile, mais reviens épuisé(e).", "Un détour imprévu te fait découvrir une piste dissimulée."], ["Le bureau des missions demande un rapport sur le sentier.", "Un autre genin affirme avoir vu un symbole inconnu dans la forêt."], training=True)]
                if village == "Konoha" and age >= 15 and rank in ("Chûnin", "Jônin", "Hokage"):
                    spots["Vallée de la Fin"] = [option("Étudier les statues et le terrain", "Intelligence", 3, ["Le paysage rappelle les rivalités anciennes qui ont façonné le village.", "Tu observes des traces d’un affrontement récent au pied des statues."], ["Une équipe demande un rapport sur des mouvements près de la vallée.", "Un témoin affirme avoir aperçu un visiteur inattendu à la vallée." ]), option("T’entraîner au bord de la rivière", "Talent", 4, ["Le bruit de la rivière t’aide à rester concentré(e) malgré la fatigue.", "Tu perfectionnes tes appuis sur un terrain irrégulier."], ["Un sensei te propose un entraînement de suivi près de la vallée.", "Une présence observée de loin t’oblige à interrompre la séance."], training=True)]

    elif world == "Jujutsu Kaisen" and age < 6:
        spots["Maison familiale"] = [option("Écouter une histoire racontée par un proche", "Bonheur", 3, ["Un proche raconte une vieille légende en te bordant.", "Tu t’endors après une journée rassurante en famille."], ["La légende évoque un lieu que ta famille évite depuis longtemps.", "Un proche te promet de t’expliquer cette vieille histoire plus tard."]) ]
        spots["Parc du quartier"] = [option("Explorer le parc avec un adulte", "Santé", 2, ["La sortie au grand air te fait du bien.", "Tu remarques un petit talisman oublié près d’un banc; l’adulte le confie à un responsable."]) ]
    elif world == "Jujutsu Kaisen":
        if age < 15:
            spots["Lycée et club de ton quartier"] = [option("Rester après les cours avec le club", "Bonheur", 2, ["Tu passes un moment avec tes camarades après les cours.", "Un objet étrange attire l’attention du club."], ["Une rumeur sur un objet maudit circule au lycée.", "Un membre du club te demande de revenir après les cours." ]), option("Examiner une salle vide", "Intelligence", 2, ["Une sensation étrange disparaît avant que tu puisses l’identifier.", "Tu trouves un symbole qui ressemble à un sceau ancien."], ["Un mentor veut examiner le symbole que tu as trouvé.", "Une présence occulte est détectée dans un bâtiment voisin."]) ]
        else:
            school = "École d’exorcisme de Tokyo" if "Tokyo" in place else "École d’exorcisme de Kyoto" if "Kyoto" in place else "École d’exorcisme de Sendai"
            spots[school] = [option("Travailler ta technique avec un mentor", "Talent", 4, ["Ton mentor t’aide à ajuster le contrôle de ton énergie occulte.", "Un exercice encadré t’apprend à éviter le gaspillage d’énergie."], ["Ton mentor te confie une technique à essayer sur le terrain.", "Un rapport d’exorcisme demande une équipe d’appui."], training=True), option("Consulter les archives", "Intelligence", 3, ["Tu trouves un cas ancien qui ressemble à une affaire récente.", "Les archives mentionnent une technique dont le dossier a été retiré."], ["Un document manquant mène à une enquête confidentielle.", "Un archiviste retrouve un rapport qui pourrait éclairer une prochaine mission."]) ]
            district = "Shibuya · Tokyo" if "Tokyo" in place else "Centre-ville · " + place
            spots[district] = [option("Repérer les traces d’énergie occulte", "Intelligence", 3, ["Tu découvres une trace récente et préviens ton mentor.", "Un résidu occulte mène à un lieu qui n’apparaît dans aucun rapport."], ["Une équipe est envoyée vérifier la trace que tu as repérée.", "Un fléau semble suivre les déplacements des passants." ]), option("Protéger les passants pendant une patrouille", "Honneur", 3, ["Tu éloignes plusieurs passants avant l’arrivée des exorcistes.", "Une patrouille coordonnée évite la panique dans le quartier."], ["Un témoin revient avec un détail sur le fléau.", "L’école te confie une patrouille de suivi dans ce quartier."]) ]
            spots["Station désaffectée"] = [option("Étudier les sceaux à distance", "Intelligence", 3, ["Tu repères une marque maudite sans franchir le périmètre.", "Un sceau ancien réagit à ton énergie, puis s’éteint."], ["Un exorciste supérieur réclame un rapport sur le sceau.", "La station est liée à une seconde anomalie détectée en ville."]), option("Faire une reconnaissance avec l’équipe", "Talent", 3, ["Tu suis les consignes de l’équipe et repères un passage sûr.", "Un bruit dans le tunnel révèle un mouvement sous les quais."], ["Ton équipe prépare une intervention pour la prochaine année.", "Un fléau a laissé une marque qui correspond à un dossier scolaire."], training=True)]

    return spots

def action_animation_style(world, action, career="Aucune"):
    text = f"{action} {career}".lower()
    if world == "Tokyo Revengers": return ("life", "🎒", "✨") if st.session_state.get("age", 0) < 12 else ("gang", "🏍️", "⚡")
    if world == "Naruto":
        return ("kunai", "🗡️", "✨") if any(word in text for word in ("mission", "combat", "attaque", "affront", "évasion", "examen", "kunai")) else ("chakra", "🌀", "✨")
    if world == "Kuroko Basket":
        return ("basket", "🏀", "") if any(word in text for word in ("match", "tir", "tournoi", "défi", "essai")) else ("sport", "🏀", "⭐")
    if world == "Jujutsu Kaisen":
        return ("occult", "🌀", "✨")
    if "héros" in text or "association héroïque" in text or "super-héros" in text:
        return ("hero", "⚡", "🛡️")
    job_icons = {
        "facteur": "📩", "analyste": "📊", "livreur": "📦", "militaire": "🪖", "vendeur": "🛍️",
        "infirmier": "🩺", "cuisinier": "🍳", "professeur": "📚", "ingénieur": "⚙️", "journaliste": "📰",
    }
    role = next((icon for job, icon in job_icons.items() if job in text), None)
    if role:
        return ("work", role, "✨")
    if "footballeur" in text:
        return ("sport", "⚽", "🥅")
    if "sportif professionnel" in text:
        return ("sport", "🏅", "⭐")
    if any(word in text for word in ("année suivante", "grandir", "anniversaire")):
        return ("life", "🎂", "✨")
    return ("life", "🎉", "✨")

def trigger_action_animation(world, action, career="Aucune"):
    scene, symbol, accent = action_animation_style(world, action, career)
    sequence = st.session_state.get("action_animation_sequence", 0) + 1
    st.session_state.action_animation_sequence = sequence
    st.session_state.action_animation = {"scene": scene, "symbol": symbol, "accent": accent, "sequence": sequence}

def render_action_animation():
    animation = st.session_state.get("action_animation")
    if not animation:
        return
    scene = animation["scene"]
    symbol = animation["symbol"]
    accent = animation["accent"]
    target_class = "action-fx__target basket-hoop" if scene == "basket" else "action-fx__target"
    st.markdown(
        f'<div class="action-fx scene-{scene}" data-sequence="{animation["sequence"]}" aria-hidden="true">'
        f'<div class="action-fx__stage"><span class="action-fx__object">{symbol}</span>'
        f'<span class="{target_class}">{accent}</span><span class="action-fx__spark">✨</span></div></div>',
        unsafe_allow_html=True,
    )

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
    hair_shine = "#765846" if gender == "Garçon" else "#9a668f" if gender == "Fille" else "#5790a1"
    beard_shape = '<path d="M34 58 Q38 63 42 60 Q50 66 58 60 Q62 63 66 58 L62 70 Q50 79 38 70 Z" fill="#49332d"/><path d="M39 66 Q50 71 61 66" fill="none" stroke="#715247" stroke-width="1.2"/>' if gender != "Fille" and beard != "Pas de barbe" else ""
    svg = f'''<svg class="face-svg" viewBox="0 0 120 120" width="126" height="126" role="img" aria-label="Portrait illustré du personnage">
    <defs><linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop stop-color="#d9edff"/><stop offset="1" stop-color="#fff0d9"/></linearGradient><linearGradient id="skin" x1="0" y1="0" x2="1" y2="1"><stop stop-color="#f8d8bd"/><stop offset="1" stop-color="#d99b79"/></linearGradient><clipPath id="portrait"><circle cx="60" cy="60" r="58"/></clipPath></defs>
    <g clip-path="url(#portrait)"><circle cx="60" cy="60" r="59" fill="url(#bg)"/><circle cx="17" cy="26" r="13" fill="#fff" opacity=".35"/><path d="M12 120 Q16 83 60 81 Q104 83 108 120" fill="#315e83"/><path d="M43 84 L60 102 L77 84 L91 120 L29 120 Z" fill="#f5f7fa"/><path d="M50 82 L60 101 L70 82" fill="#d75569"/>
    <path d="M29 51 Q27 20 60 19 Q93 20 91 51 L86 76 Q78 91 60 92 Q42 91 34 76 Z" fill="url(#skin)"/>
    <ellipse cx="32" cy="57" rx="5" ry="9" fill="#dfaa8a"/><ellipse cx="88" cy="57" rx="5" ry="9" fill="#dfaa8a"/><path d="M34 52 Q43 45 51 51 M69 51 Q78 45 86 52" fill="none" stroke="{hair_color}" stroke-width="3" stroke-linecap="round"/>
    <ellipse class="eye" cx="43" cy="57" rx="4.2" ry="5.8" fill="#315a82"/><ellipse class="eye" cx="77" cy="57" rx="4.2" ry="5.8" fill="#315a82"/><circle cx="44" cy="56" r="1.5" fill="#fff"/><circle cx="78" cy="56" r="1.5" fill="#fff"/><path d="M58 57 Q54 66 58 68" fill="none" stroke="#bd8065" stroke-width="1.8" stroke-linecap="round"/><path d="M52 75 Q60 80 68 75" fill="none" stroke="#a94f65" stroke-width="2" stroke-linecap="round"/><ellipse cx="40" cy="69" rx="6" ry="3" fill="#e98e88" opacity=".25"/><ellipse cx="80" cy="69" rx="6" ry="3" fill="#e98e88" opacity=".25"/>
    <path d="{hair_paths.get(hair, hair_paths['Courts et lisses'])}" transform="translate(10 4) scale(1.02 1.05)" fill="{hair_color}"/><path d="M40 30 Q55 18 72 27" fill="none" stroke="{hair_shine}" stroke-width="2.5" stroke-linecap="round" opacity=".75"/>{beard_shape}</g><circle cx="60" cy="60" r="58" fill="none" stroke="#ffffff" stroke-width="3"/></svg>'''
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
    if world == "Tokyo Revengers" and age >= 12 and random.random() < .75:
        if not st.session_state.get("gang"):
            return random.choice(["Un camarade t’invite à une réunion de quartier organisée par le Toman.", "Un membre des Black Dragons te propose de faire tes preuves, mais tes cours importants approchent.", "Un capitaine de division te demande si tu veux rejoindre son gang ou rester concentré sur l’école.", "Une dispute entre deux groupes éclate près de ton collège. Un ami attend de voir si tu interviens."])
        if st.session_state.get("gang_rank") == "Chef":
            return random.choice(["Un gang voisin propose une trêve après plusieurs semaines de tension.", "Un territoire neutre cherche un nouveau protecteur et plusieurs gangs négocient.", "Un ancien allié demande ton aide pour empêcher une division de se séparer.", "Une réunion des chefs de gangs pourrait changer l’équilibre de Tokyo."])
        return random.choice([f"Un rival du gang {st.session_state.gang} te provoque et attend ta réponse.", "Le capitaine de ta division te confie une tâche qui pourrait changer ta réputation.", "Une faction rivale propose une alliance secrète à certains membres.", "Un ami te rappelle qu’un examen scolaire approche malgré les activités du gang."])
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
            "Tokyo Revengers": ["Une faction rivale propose un défi pour un territoire neutre.", "Le chef du gang convoque les capitaines après une rumeur de trahison.", "Un rival blessé demande de l’aide au lieu de poursuivre le conflit.", "Un ami hésite entre les cours du lendemain et une réunion importante du gang.", "Un membre tente de recruter ton meilleur ami sans t’en parler.", "Une alliance entre deux gangs menace de bouleverser l’équilibre de Tokyo.", "Un garage du quartier offre un travail honnête à plusieurs membres.", "Un capitaine démissionne et sa division doit choisir un nouveau responsable.", "Une médiation entre gangs échoue; tu peux encore proposer une trêve.", "Un groupe rival revendique une rue commerçante que vous aviez promis de protéger.", "Une sortie scolaire tombe le jour d’une réunion cruciale.", "Un ancien membre revient et révèle pourquoi il avait quitté le gang.", "Une course caritative rassemble des gangs qui se méfient les uns des autres.", "Un proche te demande de choisir entre une promesse familiale et ton rang.", "Un territoire change de mains sans affrontement et chacun soupçonne une manœuvre."],
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
    if world == "Tokyo Revengers":
        if age < 12: return random.choice(["Une activité sportive après les cours te fait rencontrer de nouveaux camarades.", "Un atelier de mécanique organise une journée découverte pour les jeunes.", "Un proche t’accompagne à un festival de quartier."])
        if age < 15: return random.choice(["Un camarade te parle d’un gang du quartier, mais les examens du collège approchent.", "Un club scolaire cherche un nouveau membre pour organiser les activités.", "Une réunion de quartier réunit plusieurs groupes de jeunes."])
        if age < 18: return random.choice(["Les cours du lycée et les réunions du gang se chevauchent cette semaine.", "Une faction rivale propose une trêve pendant un tournoi sportif.", "Ton capitaine remarque ton sens de l’organisation et te confie une responsabilité."])
        return random.choice(["Un sommet des gangs de Tokyo prépare une nouvelle alliance.", "Un commerce du quartier demande au gang de l’aider à organiser un événement sûr.", "Une ancienne faction revient avec une proposition qui divise tes alliés."])
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

def surprise_event(world, age):
    """Second, independent life event so every year has another decision to make."""
    events = {
        "Monde réel": [
            ("Un ami t’écrit après une longue période sans nouvelles.", ["L’inviter à sortir", "Lui demander ce qui ne va pas", "Répondre plus tard"]),
            ("Un proche te propose une sortie imprévue ce week-end.", ["Accepter la sortie", "Proposer une activité moins chère", "Décliner gentiment"]),
            ("Une personne de ton établissement ou de ton travail te confie un problème.", ["Prendre le temps d’écouter", "L’aider à chercher une solution", "Garder tes distances"]),
            ("Une annonce locale cherche des volontaires pour un événement solidaire.", ["Donner un coup de main", "En parler à un ami", "Passer ton tour"]),
            ("Tu reçois une proposition inattendue qui pourrait changer tes projets.", ["Saisir l’occasion", "Demander conseil à un proche", "Prendre le temps d’y réfléchir"]),
        ],
        "Kuroko Basket": [
            ("Ton équipe organise une sortie après un match serré.", ["Fêter la victoire ensemble", "Encourager un coéquipier déçu", "Rentrer te reposer"]),
            ("Un rival te propose un duel de tirs après l’entraînement.", ["Accepter le duel", "Lui proposer un défi en équipe", "Décliner aujourd’hui"]),
            ("L’entraîneur hésite entre toi et un coéquipier pour le cinq de départ.", ["Lui parler de ton rôle", "Soutenir ton coéquipier", "Prouver ta valeur au prochain match"]),
            ("Un recruteur demande à te parler après un tournoi.", ["Écouter sa proposition", "En discuter avec ton entraîneur", "Te concentrer sur ton équipe actuelle"]),
        ],
        "Naruto": [
            ("Un camarade de ton équipe revient blessé d’un entraînement.", ["L’aider à récupérer", "Demander l’avis du sensei", "Continuer la mission prévue"]),
            ("La radio du village annonce une tension à la frontière.", ["Proposer une patrouille", "Prévenir le bureau des missions", "Rester en attente des ordres"]),
            ("Un ancien rouleau de ton clan est découvert dans les archives.", ["Demander l’autorisation de l’étudier", "En parler à ton sensei", "Ne pas t’en mêler"]),
            ("Un rival te défie devant les autres élèves.", ["Accepter l’épreuve", "Répondre sans combattre", "Demander un arbitrage au sensei"]),
        ],
        "Jujutsu Kaisen": [
            ("Un élève repère une trace occulte près d’un lieu fréquenté.", ["Avertir le mentor", "Examiner la trace avec un partenaire", "Faire évacuer les alentours"]),
            ("Une rumeur circule sur un objet maudit qui aurait changé de mains.", ["Consulter les archives", "Interroger les élèves", "Signaler la rumeur au responsable"]),
            ("Ton mentor te propose une séance de contrôle de l’énergie.", ["Accepter l’entraînement", "Demander une démonstration", "Prendre une journée de repos"]),
            ("Un fléau semble suivre un camarade depuis plusieurs jours.", ["Le protéger et prévenir l’école", "Analyser les signes ensemble", "Ne pas agir seul·e"]),
        ],
        "Tokyo Revengers": [
            ("Un commerce du quartier demande de l’aide pour préparer une fête locale.", ["Mobiliser tes amis", "Demander l’accord du gang", "Laisser les habitants s’organiser"]),
            ("Un membre de ta faction veut quitter le groupe après un désaccord.", ["L’écouter en privé", "Organiser une réunion", "Le laisser partir sans pression"]),
            ("Une faction voisine propose de discuter autour d’un repas.", ["Accepter le rendez-vous", "Demander à un allié de t’accompagner", "Refuser et expliquer pourquoi"]),
            ("Tes amis veulent organiser une sortie, mais tu as aussi des cours à préparer.", ["Étudier puis les rejoindre", "Leur consacrer la soirée", "Proposer une autre date"]),
        ],
    }
    pool = events.get(world, events["Monde réel"])
    if age < 6 and world == "Monde réel":
        pool = [
            ("Un parent t’emmène découvrir un nouveau parc.", ["Jouer avec lui/elle", "Observer les autres enfants", "Rester près de la famille"]),
            ("Un proche te lit une histoire avant de dormir.", ["Choisir une autre histoire", "Poser des questions", "Écouter tranquillement"]),
            ("Un enfant de ton âge veut partager ses jouets.", ["Jouer ensemble", "Lui montrer ton jouet", "Demander à un parent de vous aider"]),
        ]
    recent = st.session_state.get("event_memory", [])[-12:]
    fresh = [item for item in pool if item[0] not in recent]
    event = random.choice(fresh or pool)
    st.session_state.event_memory = (st.session_state.get("event_memory", []) + [event[0]])[-30:]
    return event

def action_menu_category(label):
    text = label.lower()
    if any(word in text for word in ("école", "cours", "étud", "devoir", "révis", "bibliothèque", "lecture", "formation", "stage", "examen", "apprendre", "livre")):
        return "Études"
    if any(word in text for word in ("travail", "métier", "carrière", "emploi", "profession", "postuler", "mission au", "association héroïque")):
        return "Carrière"
    if any(word in text for word in ("proche", "parent", "famille", "ami", "camarade", "sortie", "cinéma", "rencontr", "rendez-vous", "partenaire", "relation", "fêter", "appeler", "inviter", "copain")):
        return "Proches & sorties"
    if any(word in text for word in ("entraînement", "entraîner", "s’entraîner", "sport", "tir", "match", "chakra", "jutsu", "technique", "mission de rang", "mentor", "sensei", "fléau", "gang", "territoire", "zone", "mission spéciale", "exorc", "énergie occulte")):
        return "Univers & progression"
    return "Loisirs & santé"

init()
st.markdown('<div class="hero"><h1>✨ DESTINS</h1><p>Une vie, mille chemins. Chaque choix écrit la suite.</p></div>', unsafe_allow_html=True)
theme_col, _ = st.columns([1, 4])
with theme_col:
    theme_label = "☀️ Jour" if st.session_state.night_mode else "🌙 Nuit"
    if st.button(theme_label, key="toggle_night_mode", help="Changer le thème de l’application", use_container_width=True):
        st.session_state.night_mode = not st.session_state.night_mode
        st.rerun()
render_action_animation()

if st.session_state.music_open:
    with st.container(border=True):
        music_head, music_close = st.columns([3, 1])
        with music_head:
            st.markdown("**🎵 Radio Destins**")
        with music_close:
            if st.button("✕ Fermer", key="close_music", use_container_width=True):
                st.session_state.music_open = False
                st.rerun()
        track_labels = {video_id: label for label, video_id in MUSIC_TRACKS}
        selected_track = st.selectbox(
            "Choisir une piste", list(track_labels),
            index=next((i for i, (_, video_id) in enumerate(MUSIC_TRACKS) if video_id == st.session_state.music_track), 0),
            format_func=lambda video_id: track_labels[video_id],
            key="music_track_choice", label_visibility="collapsed",
        )
        st.session_state.music_track = selected_track
        playlist = ",".join(video_id for _, video_id in MUSIC_TRACKS)
        music_url = f"https://www.youtube-nocookie.com/embed/{selected_track}?autoplay=1&mute=1&controls=1&playsinline=1&loop=1&playlist={playlist}&rel=0"
        components.html(
            f'<iframe title="Radio Destins" width="100%" height="225" '
            f'src="{music_url}" frameborder="0" '
            'allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture; web-share" '
            'referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>',
            height=235, scrolling=False,
        )
        st.caption("La lecture démarre automatiquement en mode muet. Utilise le bouton 🔊 du lecteur pour activer le son. La politique de ton navigateur peut demander un appui sur Lecture.")
else:
    if st.button("🎵 Ouvrir la radio", key="open_music"):
        st.session_state.music_open = True
        st.rerun()

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
                st.session_state.update(started=True, world=world, first=first.strip() or "Alex", surname=family, gender=gender, orientation=orientation, hair=hair, beard=beard, avatar="", place=place, clan=clan, pupil_power=pupil_power, pupil_stage=0, known_jutsu=[], mentor_jutsu=[], mentor_training=[], mentor_progress={}, tailed_beast="", beast_mastery=0, partner=None, dating_candidate=None, hero_affiliation="", gang="", gang_rank="Nouveau", gang_renown=0, gang_reputation=0, gang_allies=[], gang_territories=[], gang_members=1, school_attendance=0, npc_roster=[], npc_memories=[], career_skills=career_skill_profile(world), fatigue=10, age=0, rank="Étudiant de l’académie" if world == "Naruto" else "Élève", career="Aucune", career_level=0, job_tasks=0, technique=random.choice(OCCULT_TECHNIQUES) if world == "Jujutsu Kaisen" else "Aucune", techniques=[], zones=[], technique_level=1, jutsu_level=0, mission_counts={}, year={"activities": [], "events": [f"{first or 'Alex'} {family} naît à {place}. Sa famille l’accueille dans ce nouvel univers."], "close": [], "training_counts": {}, "world_news": world_news(world), "event_resolved": False}, family=family_members(world, family), friends=[], children=[], clubs=[], history=[], story_paths=[], stats=stats, money=1200, dead=False, death_reason="", generation=1, honor=0, fame=0, inventory=[], captured=False, event_followups=[], event_memory=[])
                st.session_state.family_bonds = {}
                st.rerun()
    with right:
        st.markdown('<div class="card"><div class="big">2 · Prévisualise ton avatar</div><p>Ton personnage t’accompagnera dans sa chronologie. La coiffure et la barbe évolueront avec le temps.</p></div>', unsafe_allow_html=True)
        descriptions = {"Monde réel": "École, loisirs, orientation et métiers.", "Tokyo Revengers": "École, gangs, divisions, alliances et territoires.", "Kuroko Basket": "Clubs, matchs, entraînement et recrutement.", "Naruto": "Clans, chakra, missions et examens ninja.", "Jujutsu Kaisen": "École d’exorcisme, fléaux et missions occultes."}
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
        if world == "Tokyo Revengers": st.caption(f"🏍️ {st.session_state.gang or 'Indépendant·e'} · {st.session_state.gang_rank} · renommée {st.session_state.gang_renown} · membres {st.session_state.gang_members}")
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
        trigger_action_animation(world, "Année suivante", st.session_state.career)
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
            if world == "Tokyo Revengers" and age >= 12 and any(word in event_text for word in ("gang", "faction", "territoire", "capitaine", "alliance", "division")):
                opportunity = True
            if opportunity:
                reactions = ["Tenter ma chance", "Demander conseil à un proche", "Laisser passer cette occasion"]
                if world == "Tokyo Revengers" and age < 18: reactions.append("Privilégier les cours")
            elif "ton rival" in event_text and "déf" in event_text:
                reactions = ["Relever le défi", "Lui parler franchement", "Demander conseil à un proche"]
            elif "sensei" in event_text or "mentor" in event_text:
                reactions = ["Accepter l’entraînement", "Poser des questions", "Décliner poliment"]
            elif "demande de l’aide" in event_text:
                reactions = ["L’aider", "L’écouter d’abord", "Refuser et expliquer pourquoi"]
            elif age < 3:
                reactions = ["Demander à un proche de t’aider", "Observer calmement", "Tendre la main"]
            elif world == "Tokyo Revengers" and age >= 12:
                reactions = ["Protéger les passants et les amis", "Négocier une trêve", "Répondre au défi du gang"] if st.session_state.gang else ["Rester concentré sur les cours", "Demander conseil à un proche", "Rencontrer la faction"]
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
                        elif world == "Tokyo Revengers":
                            path, title = "tokyo_gang_story", "Une place dans les factions de Tokyo"
                            if not st.session_state.gang:
                                st.session_state.gang = random.choice(TOKYO_GANGS[:3])
                                st.session_state.gang_rank = "Membre"
                                st.session_state.gang_members = 5
                                st.session_state.clubs.append(f"Gang · {st.session_state.gang}")
                                detail = f"Tu gagnes la confiance de {st.session_state.gang}, qui t’accueille comme membre. Tu pourras gravir ses rangs, mais tes choix scolaires resteront importants."
                            else:
                                st.session_state.gang_renown = min(100, st.session_state.gang_renown + 10)
                                detail = f"Ton initiative donne de la renommée à {st.session_state.gang}. Une nouvelle intrigue de faction s’ouvre : alliances, rivalités et territoires seront désormais en jeu."
                            st.session_state.gang_story_unlocked = True
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
                    "Tokyo Revengers": ["Une faction te recontacte après ta réponse et propose une rencontre entre capitaines.", "Un membre du gang se souvient de ton choix et t’invite à une mission de confiance.", "Un rival interprète ta décision comme un signe de trêve ou un défi et réagit l’année prochaine."],
                    "Kuroko Basket": ["Un entraîneur analyse ta réaction et t’invite à un défi d’équipe.", "Ton rival prépare une nouvelle stratégie pour votre prochaine rencontre.", "Un coéquipier partage une piste vers un tournoi régional."],
                    "Naruto": ["Le bureau des missions reçoit un rapport lié à ton choix et ouvre une nouvelle affectation.", "Une rumeur à la radio révèle une piste près de la frontière.", "Un ninja de ton équipe te confie une information qui mènera à une mission."],
                    "Jujutsu Kaisen": ["Ton mentor repère une nouvelle trace occulte liée à ton enquête.", "Un rapport confidentiel révèle un fléau qui pourrait être lié à l’incident.", "Un autre élève demande ton aide pour une affaire qui vient d’émerger."]}
                st.session_state.event_followups.append(random.choice(followup_options[world]))
                add_year_item("activities", f"Face à l’événement, tu as choisi : {response.lower()}.")
                if world == "Tokyo Revengers":
                    if "trêve" in response.lower() or "protéger" in response.lower():
                        st.session_state.gang_reputation = min(100, st.session_state.gang_reputation + 2)
                        st.session_state.honor = min(100, st.session_state.honor + 2)
                    elif "défi" in response.lower() and st.session_state.gang:
                        st.session_state.gang_renown = min(100, st.session_state.gang_renown + 2)
                        st.session_state.gang_reputation = max(-100, st.session_state.gang_reputation - 1)
                    elif "cours" in response.lower():
                        st.session_state.school_attendance += 1
                        st.session_state.year["school_action_done"] = True
                        finish_challenge("school", "Fréquenter l’école", 100)
                if any(word in response.lower() for word in ["protéger", "aider", "conseil", "renfort", "protocole", "équipe"]): st.session_state.honor = min(100, st.session_state.honor + 1)
                if any(word in response.lower() for word in ["à tout prix", "ignorer", "abandonner"]): st.session_state.honor = max(-100, st.session_state.honor - 2)
                stat = "Talent" if any(word in response.lower() for word in ["accepter", "défi", "participer", "saisir"]) else "Bonheur"
                st.session_state.stats[stat] = min(100, st.session_state.stats[stat] + 3)
                if "ami" in response.lower() or "équipe" in response.lower():
                    add_year_item("close", "Un proche ou un coéquipier a répondu à ton invitation et a partagé ce moment avec toi.")
                trigger_action_animation(world, f"{response} {event_text}", st.session_state.career)
                st.rerun()
            # A second, separate event gives the player another meaningful
            # decision each year, even after the headline story is resolved.
            if "surprise_event" not in st.session_state.year:
                st.session_state.year["surprise_event"] = surprise_event(world, age)
                st.session_state.year["surprise_resolved"] = False
            surprise_text, surprise_choices = st.session_state.year["surprise_event"]
            st.markdown("**✨ Un imprévu dans ton année**")
            st.markdown(f'<div class="card event">{surprise_text}</div>', unsafe_allow_html=True)
            surprise_choice = st.selectbox("Que fais-tu ?", surprise_choices, key=f"surprise_choice_{age}")
            if st.button("Décider", key=f"resolve_surprise_{age}", disabled=st.session_state.year.get("surprise_resolved", False), use_container_width=True):
                st.session_state.year["surprise_resolved"] = True
                choice_text = surprise_choice.lower()
                challenge_choice = any(word in choice_text for word in ("défi", "examiner", "saisir", "accepter", "proposer", "mobiliser"))
                skill_name = "Intelligence" if any(word in choice_text for word in ("étudier", "archives", "conseil", "analyser", "réfléchir")) else "Talent" if challenge_choice else "Bonheur"
                chance = min(92, max(20, 32 + st.session_state.stats[skill_name] // 2 + st.session_state.honor // 8 - st.session_state.fatigue // 8))
                succeeded = (not challenge_choice) or random.randint(1, 100) <= chance
                if succeeded:
                    gain = random.randint(2, 5)
                    st.session_state.stats[skill_name] = min(100, st.session_state.stats[skill_name] + gain)
                    response_text = random.choice(["La situation évolue favorablement et tu gagnes en confiance.", "Ton choix rapproche les personnes concernées et ouvre une nouvelle possibilité.", "Tu obtiens une réponse encourageante, même si la suite dépendra de tes prochains choix."])
                    if any(word in choice_text for word in ("aider", "protéger", "écouter", "soutenir", "prévenir", "féliciter")):
                        st.session_state.honor = min(100, st.session_state.honor + 1)
                        if st.session_state.family:
                            target_name = st.session_state.family[0].split(" ·")[0]
                            bond = st.session_state.family_bonds.get(target_name, 50)
                            st.session_state.family_bonds[target_name] = min(100, bond + 2)
                    elif "faction" in surprise_text.lower() or "gang" in surprise_text.lower():
                        st.session_state.gang_renown = min(100, st.session_state.gang_renown + 2)
                    elif "rival" in surprise_text.lower() and world == "Kuroko Basket":
                        st.session_state.stats["Basket"] = min(100, st.session_state.stats.get("Basket", 48) + 2)
                    else:
                        st.session_state.stats["Bonheur"] = min(100, st.session_state.stats["Bonheur"] + 2)
                else:
                    response_text = random.choice(["L’autre personne n’est pas prête à accepter ta proposition.", "Tu n’obtiens pas le résultat espéré, mais tu comprends mieux la situation.", "Le moment est mal choisi. Une autre approche ou un peu de temps pourrait aider."])
                    st.session_state.stats["Bonheur"] = max(0, st.session_state.stats["Bonheur"] - 1)
                    if world == "Kuroko Basket" and "rival" in surprise_text.lower():
                        st.session_state.event_followups.append("Ton rival réclame une revanche après votre dernier échange.")
                    elif "faction" in surprise_text.lower() or "gang" in surprise_text.lower():
                        st.session_state.event_followups.append("Un membre de la faction te recontactera pour reparler de cette décision.")
                full_result = f"{surprise_choice} — {response_text}"
                st.session_state.year["events"].append(f"✨ Imprévu : {full_result}")
                st.session_state.year["activities"].append(full_result)
                st.session_state.history.append({"age": age, "événement": surprise_text, "choix": surprise_choice, "réussite": succeeded})
                add_year_item("close", f"Ton choix face à cet imprévu : {surprise_choice.lower()}.")
                trigger_action_animation(world, surprise_choice, st.session_state.career)
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
        elif world == "Tokyo Revengers":
            gang_score = min(99, st.session_state.gang_renown + st.session_state.gang_members + st.session_state.gang_reputation // 3)
            rows = [("Toman", "Shibuya", 92), ("Black Dragons", "Shinjuku", 89), ("Tenjiku", "Yokohama", 86), (st.session_state.gang or name, st.session_state.place, gang_score)]
            st.dataframe([{"Gang": gang, "Base / influence": area, "Indice": score} for gang, area, score in sorted(rows, key=lambda row: row[2], reverse=True)], hide_index=True, use_container_width=True)
            st.caption(f"Tes territoires : {', '.join(st.session_state.gang_territories) or 'aucun'} · Alliances : {', '.join(st.session_state.gang_allies) or 'aucune'}")
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
        # Un catalogue de loisirs change avec l’âge pour que chaque année offre
        # plusieurs chemins, au lieu de répéter les mêmes quatre actions.
        if age < 3:
            actions.extend([
                ("Jouer avec des cubes", "Intelligence", "Tu empiles, observes et recommences avec curiosité."),
                ("Écouter de la musique avec la famille", "Bonheur", "Un moment musical partagé apaise et amuse toute la famille."),
                ("Apprendre de nouveaux mots", "Intelligence", "Tu découvres de nouveaux mots avec l’aide d’un proche."),
            ])
        elif age < 6:
            actions.extend([
                ("Jouer avec un camarade", "Bonheur", "Tu inventes un jeu et apprends à partager."),
                ("Visiter la bibliothèque avec un parent", "Intelligence", "Tu choisis un album et l’écoutes avec un proche."),
                ("Aider à préparer le goûter", "Talent", "Tu participes à une petite tâche et en es fier/fière."),
            ])
        elif age < 11:
            actions.extend([
                ("Faire ses devoirs avec un proche", "Intelligence", "Un proche t’aide à comprendre une leçon difficile."),
                ("Inviter un ami à la maison", "Bonheur", "Vous jouez ensemble et partagez un bon goûter."),
                ("Apprendre à cuisiner en famille", "Talent", "Tu prépares une recette simple avec un membre de ta famille."),
                ("Participer à une activité artistique", "Talent", "Tu découvres le dessin, la musique ou le théâtre."),
            ])
        elif age < 15:
            actions.extend([
                ("Réviser avec un camarade", "Intelligence", "Vous comparez vos méthodes et progressez ensemble."),
                ("Aller au cinéma avec des amis", "Bonheur", "Une sortie entre amis vous laisse un nouveau souvenir."),
                ("Passer l’après-midi avec un parent", "Bonheur", "Tu prends le temps de discuter et de partager une activité."),
                ("Découvrir un nouveau loisir", "Talent", "Tu essaies une activité et découvres peut-être une passion."),
            ])
        elif age < 18:
            actions.extend([
                ("Réviser pour un examen avec un ami", "Intelligence", "Vous vous interrogez mutuellement avant les examens."),
                ("Organiser une sortie de groupe", "Bonheur", "Tu réunis tes amis pour une sortie qui resserre le groupe."),
                ("Faire du bénévolat", "Honneur", "Tu consacres du temps à une cause locale et gagnes en expérience."),
                ("Parler de ton avenir avec un proche", "Intelligence", "Un proche t’aide à envisager plusieurs chemins possibles."),
            ])
        else:
            actions.extend([
                ("Inviter un ami à dîner", "Bonheur", "Vous partagez un repas et prenez des nouvelles."),
                ("Prendre un jour de repos", "Santé", "Tu ralentis et récupères après une période chargée."),
                ("Faire du bénévolat dans ton quartier", "Honneur", "Ton aide est remarquée par les personnes du quartier."),
                ("Retrouver un ancien camarade", "Bonheur", "Vous évoquez vos souvenirs et reprenez contact."),
            ])
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
        elif world == "Tokyo Revengers":
            if age >= 12:
                if age < 18 and not st.session_state.year.get("school_action_done", False):
                    actions.append(("Assister aux cours", "Intelligence", "Tu vas en cours, avances dans tes études et gardes ouvertes tes options d’avenir."))
                if not st.session_state.get("gang"):
                    actions.append(("Rejoindre un gang", "Talent", "Tu rencontres les factions locales et décides si tu es prêt(e) à entrer dans un gang."))
                else:
                    actions.append(("Participer à la réunion de division", "Leadership", f"Tu aides {st.session_state.gang} à préparer ses priorités et à garder ses membres unis."))
                    if age < 18 and not st.session_state.year.get("school_action_done", False):
                        actions.append(("Sécher les cours pour le gang", "Réputation", "Tu réponds à l’appel du gang, mais cela peut peser sur tes études et tes relations."))
                    elif age >= 18:
                        actions.append(("Consacrer du temps au gang", "Réputation", "Tu réponds à l’appel du gang et consolides ta réputation dans le quartier."))
                    actions.append(("Entraînement de cohésion", "Talent", "Tu entraînes ta discipline et ta condition avec les membres de ta division."))
                    actions.append(("Proposer une alliance", "Leadership", "Tu prends contact avec une faction rivale afin de négocier une alliance."))
                    actions.append(("Recruter un membre", "Leadership", "Tu invites un jeune du quartier à rejoindre votre groupe après avoir gagné sa confiance."))
                    if age >= 16 and (st.session_state.gang_rank == "Chef" or st.session_state.gang_renown >= 25):
                        actions.append(("Créer ton propre gang", "Leadership", "Ta renommée suffit pour fonder une faction et attirer tes premiers membres."))
                    if age >= 14 and st.session_state.get("gang_territories") is not None and len(st.session_state.gang_territories) < len(TOKYO_TERRITORIES):
                        actions.append(("Défier un gang pour un territoire", "Talent", "Tu organises un défi encadré ou une négociation pour gagner de l’influence dans un quartier."))
            if age >= 10:
                actions.append(("Entraînement sportif", "Santé", "Tu développes ta condition physique et apprends à canaliser ton énergie."))
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
        career_training_ready = (world == "Monde réel" and st.session_state.career != "Aucune" and age >= 18) or (world == "Kuroko Basket" and age >= 6) or (world == "Tokyo Revengers" and age >= 10) or (world == "Naruto" and age >= 6) or (world == "Jujutsu Kaisen" and age >= 12)
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
        training_terms = ["entraînement", "entraîner", "s’entraîner", "tirs", "musculation", "faire du sport", "match", "camp d’été", "essai dans une académie", "chakra", "énergie occulte", "jutsu", "technique occulte", "technique héréditaire", "zone", "ermite", "association", "mentorat", "sensei", "cohésion"]
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
        elif world == "Tokyo Revengers":
            if age < 12: st.info("Parcours de quartier : l’école, les amis et les activités locales façonnent ta réputation avant l’âge des gangs.")
            elif not st.session_state.gang: st.info("Choisis entre poursuivre tes études et rejoindre une faction. Les gangs s’ouvrent dès 12 ans; créer le tien demande 25 de renommée ou le rang de Chef.")
            else: st.info(f"Gang : {st.session_state.gang} · rang {st.session_state.gang_rank} · renommée {st.session_state.gang_renown}/100 · territoires {len(st.session_state.gang_territories)} · alliances {len(st.session_state.gang_allies)}. Les missions réussies et tes choix font évoluer ta hiérarchie.")
        st.markdown("**📂 Menus d’activités**")
        menu_categories = ["Proches & sorties", "Études", "Loisirs & santé", "Carrière", "Univers & progression"]
        actions_by_category = {category: [item for item in actions if action_menu_category(item[0]) == category] for category in menu_categories}
        actions_by_category = {category: items for category, items in actions_by_category.items() if items}
        activity_menu = st.selectbox("Quel menu veux-tu ouvrir ?", list(actions_by_category), key=f"activity_menu_{age}")
        chosen_menu = actions_by_category[activity_menu]
        st.caption(f"{len(chosen_menu)} choix disponibles · les activités changent selon ton âge, ton univers et ton parcours.")
        selected = st.selectbox("Choisis une activité", [item[0] for item in chosen_menu], key=f"activity_choice_{age}_{activity_menu}")
        family_activity = any(word in selected.lower() for word in ("avec un proche", "avec un parent", "avec un ami", "avec des amis", "avec tes amis", "avec un camarade", "avec un membre de la famille", "en famille"))
        family_activity_target = None
        if family_activity and st.session_state.family:
            family_activity_target = st.selectbox("Avec qui ?", [person.split(" ·")[0] for person in st.session_state.family], key=f"activity_relative_{age}_{selected}")
        job_choice = st.selectbox("Métier visé", JOBS, key=f"job_choice_{age}") if selected == "Postuler à un métier" else None
        hero_choice = st.selectbox("Association visée", HERO_ASSOCIATIONS, key=f"hero_choice_{age}") if selected == "Postuler à une association héroïque" else None
        gang_choice = st.selectbox("Faction à rejoindre ou à rallier", TOKYO_GANGS, key=f"gang_choice_{age}") if world == "Tokyo Revengers" and selected in ("Rejoindre un gang", "Proposer une alliance") else None
        new_gang_name = st.text_input("Nom de ton gang", key=f"new_gang_name_{age}") if world == "Tokyo Revengers" and selected == "Créer ton propre gang" else ""
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
            effective_stat = action[1] if action[1] in st.session_state.stats else "Talent"
            if world == "Kuroko Basket": st.session_state.stats.setdefault("Basket", 48)
            is_training = any(word in selected.lower() for word in ["entraînement", "entraîner", "s’entraîner", "tirs", "musculation", "faire du sport", "match", "camp d’été", "essai dans une académie", "chakra", "énergie occulte", "jutsu", "technique occulte", "technique héréditaire", "zone", "ermite", "association", "mentorat", "sensei"])
            special_activity = selected in ("Postuler à une association héroïque", "Entraînement de l’association", "Maîtriser le démon à queue", "S’entraîner avec le mentor ermite", "Rejoindre un gang", "Créer ton propre gang", "Proposer une alliance", "Recruter un membre", "Défier un gang pour un territoire", "Assister aux cours", "Sécher les cours pour le gang", "Consacrer du temps au gang", "Participer à la réunion de division") or selected.startswith("Apprendre une technique héréditaire :") or selected.startswith("Séance de mentorat :")
            if selected == "Rejoindre un gang":
                join_chance = min(92, 40 + st.session_state.stats["Talent"] // 3 + st.session_state.gang_renown // 3 + st.session_state.honor // 8)
                if age < 12:
                    activity_text = "Tu es encore trop jeune pour rejoindre un gang. Tes activités scolaires et de quartier te préparent à choisir plus tard."
                elif random.randint(1, 100) <= join_chance:
                    st.session_state.gang = gang_choice
                    st.session_state.gang_rank = "Membre"
                    st.session_state.gang_members = max(5, st.session_state.gang_members)
                    st.session_state.clubs.append(f"Gang · {gang_choice}")
                    st.session_state.gang_renown = min(100, st.session_state.gang_renown + 3)
                    activity_text = f"Tu rejoins {gang_choice} comme membre. Le capitaine t’explique les règles de la division et les quartiers où le gang est actif."
                    new_contact = create_npc(world, age, "Allié")
                    if new_contact:
                        st.session_state.npc_roster.append(new_contact)
                        st.session_state.friends.append(new_contact["name"])
                        activity_text += f" Tu fais connaissance avec {new_contact['name']}, membre de ta division ({new_contact['job']})."
                    st.session_state.event_followups.append(f"Un capitaine de {gang_choice} te confie une première mission de confiance. Une faction rivale observe ta progression.")
                else:
                    activity_text = f"{gang_choice} ne t’intègre pas encore. Tu dois gagner la confiance du quartier et montrer que tu sais éviter les conflits inutiles."
            elif selected == "Créer ton propre gang":
                if age >= 16 and st.session_state.gang_renown >= 25 and new_gang_name.strip():
                    old_gang = st.session_state.gang
                    st.session_state.gang = new_gang_name.strip()[:32]
                    st.session_state.gang_rank = "Chef"
                    st.session_state.gang_members = max(3, st.session_state.gang_members // 2)
                    st.session_state.gang_allies = [old_gang] if old_gang else st.session_state.gang_allies
                    st.session_state.gang_renown = max(10, st.session_state.gang_renown - 8)
                    st.session_state.clubs.append(f"Gang · {st.session_state.gang}")
                    activity_text = f"Tu fondes {st.session_state.gang}. Tes premiers membres te reconnaissent comme chef; tu peux proposer des alliances et gagner des quartiers par défi ou médiation."
                    new_contact = create_npc(world, age, "Allié")
                    if new_contact:
                        st.session_state.npc_roster.append(new_contact)
                        st.session_state.friends.append(new_contact["name"])
                        activity_text += f" {new_contact['name']} devient le premier membre de ta division ({new_contact['job']})."
                    st.session_state.event_followups.append(f"Les autres factions réagissent à la création de {st.session_state.gang}. Une proposition d’alliance ou un défi pourrait arriver.")
                else:
                    activity_text = "Il te faut au moins 25 de renommée, avoir 16 ans et choisir un nom pour fonder ton gang."
            elif selected == "Proposer une alliance":
                alliance_chance = min(90, max(15, 30 + st.session_state.gang_renown // 2 + st.session_state.career_skills.get("Leadership", 20) // 3 + st.session_state.honor // 4))
                if gang_choice == st.session_state.gang:
                    activity_text = "Cette faction est déjà ton gang. Choisis une autre faction pour proposer une alliance."
                elif random.randint(1, 100) <= alliance_chance:
                    if gang_choice not in st.session_state.gang_allies: st.session_state.gang_allies.append(gang_choice)
                    st.session_state.gang_reputation = min(100, st.session_state.gang_reputation + 5)
                    activity_text = f"{gang_choice} accepte une alliance avec {st.session_state.gang}. Vos membres s’engagent à régler les différends par la discussion."
                    st.session_state.event_followups.append(f"Un membre de {gang_choice} te contacte pour honorer l’alliance lors d’un conflit territorial.")
                else:
                    activity_text = f"{gang_choice} refuse pour l’instant. Un médiateur conseille de bâtir la confiance avant une nouvelle proposition."
            elif selected == "Recruter un membre":
                chance = min(90, 35 + st.session_state.gang_renown // 2 + st.session_state.career_skills.get("Leadership", 20) // 3)
                if random.randint(1, 100) <= chance:
                    st.session_state.gang_members += 1
                    st.session_state.gang_renown = min(100, st.session_state.gang_renown + 2)
                    activity_text = f"Un jeune du quartier rejoint {st.session_state.gang}. Votre groupe compte maintenant {st.session_state.gang_members} membres."
                else:
                    activity_text = "La personne préfère rester indépendante pour le moment. Vous gardez le contact et pourrez lui reparler plus tard."
            elif selected == "Défier un gang pour un territoire":
                target = next((area for area in TOKYO_TERRITORIES if area not in st.session_state.gang_territories), None)
                power = mission_power(world)
                chance = min(90, max(15, 25 + power + st.session_state.gang_members // 2 + len(st.session_state.gang_allies) * 5 - len(st.session_state.gang_territories) * 4))
                if target and random.randint(1, 100) <= chance:
                    st.session_state.gang_territories.append(target)
                    st.session_state.gang_renown = min(100, st.session_state.gang_renown + 8)
                    activity_text = f"Ton défi ou ta négociation aboutit : {st.session_state.gang} gagne de l’influence à {target}. Le quartier reste ouvert aux habitants."
                    st.session_state.event_followups.append(f"Une faction rivale conteste l’influence de {st.session_state.gang} à {target} et demande une médiation.")
                    st.balloons()
                else:
                    st.session_state.gang_reputation = max(-100, st.session_state.gang_reputation - 2)
                    activity_text = "Le défi n’aboutit pas. Tu choisis de retirer ton équipe sans mettre les habitants au milieu du différend. Une nouvelle négociation reste possible."
            elif selected == "Rejoindre un club de basket":
                if "Club de basket" not in st.session_state.clubs: st.session_state.clubs.append("Club de basket")
            if selected == "Assister aux cours":
                st.session_state.school_attendance += 1
                st.session_state.year["school_action_done"] = True
                finish_challenge("school", "Fréquenter l’école", 100)
                activity_text = "Tu assistes aux cours et rends les devoirs attendus. Tes résultats scolaires progressent, même si cela laisse moins de temps pour les réunions du gang."
            elif selected == "Sécher les cours pour le gang":
                st.session_state.stats["Intelligence"] = max(0, st.session_state.stats["Intelligence"] - 2)
                st.session_state.honor = max(-100, st.session_state.honor - 1)
                st.session_state.gang_renown = min(100, st.session_state.gang_renown + 3)
                st.session_state.year["school_action_done"] = True
                activity_text = "Tu manques les cours pour soutenir ton gang. Sa confiance envers toi augmente, mais tes résultats scolaires en souffrent (Intelligence −2)."
            elif selected == "Participer à la réunion de division":
                st.session_state.gang_renown = min(100, st.session_state.gang_renown + 2)
                st.session_state.career_skills["Leadership"] = min(100, st.session_state.career_skills.get("Leadership", 20) + 3)
                activity_text = f"Tu aides {st.session_state.gang} à préparer ses priorités. Ta division te fait davantage confiance."
            elif selected == "Consacrer du temps au gang":
                st.session_state.gang_renown = min(100, st.session_state.gang_renown + 2)
                activity_text = f"Tu représentes {st.session_state.gang} lors d’une réunion de quartier et renforces tes liens avec la division."
            elif selected == "Postuler à une association héroïque":
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
                if family_activity_target:
                    bond = st.session_state.family_bonds.get(family_activity_target, 50)
                    new_bond = min(100, bond + random.randint(3, 7))
                    st.session_state.family_bonds[family_activity_target] = new_bond
                    activity_text += f" {family_activity_target} partage ce moment avec toi. Votre lien passe à {new_bond}%."
                    st.session_state.year["close"].append(f"Tu as choisi {selected.lower()} avec {family_activity_target}. Ce moment renforce votre lien.")
                    st.session_state.history.append({"age": age, "proche": family_activity_target, "activité": selected, "lien": new_bond})
                if selected == "Faire du bénévolat" or selected == "Faire du bénévolat dans ton quartier":
                    st.session_state.honor = min(100, st.session_state.honor + 3)
                    activity_text += " Ton honneur augmente de 3."
                if selected in ("Inviter un ami à dîner", "Inviter un ami à la maison", "Aller au cinéma avec des amis", "Organiser une sortie de groupe", "Retrouver un ancien camarade") and st.session_state.friends:
                    friend_name = random.choice(st.session_state.friends).split(" ·")[0]
                    activity_text += f" {friend_name} accepte l’invitation et vous reparlez de vos projets."
                    st.session_state.year["close"].append(f"Tu passes un moment avec {friend_name} : {selected.lower()}.")
                if selected == "Prendre un jour de repos":
                    st.session_state.fatigue = max(0, st.session_state.fatigue - 18)
                    activity_text += " Fatigue −18."
            st.session_state.year["activities"].append(activity_text)
            st.session_state.history.append({"age": age, "choix": selected, "détail": activity_text})
            if is_training:
                count = st.session_state.year["training_counts"].get("bonus", 0)
                if count < 3:
                    st.session_state.stats[effective_stat] = min(100, st.session_state.stats.get(effective_stat, 48) + random.randint(3, 7))
                    st.session_state.year["training_counts"]["bonus"] = count + 1
                    st.session_state.stats["Bonheur"] = min(100, st.session_state.stats["Bonheur"] + 2)
                else:
                    st.session_state.year["activities"][-1] += " Tu as déjà atteint la limite de trois entraînements avec bonus cette année."
            else:
                st.session_state.stats[effective_stat] = min(100, st.session_state.stats.get(effective_stat, 48) + random.randint(3, 7))
                st.session_state.stats["Bonheur"] = min(100, st.session_state.stats["Bonheur"] + (2 if effective_stat != "Bonheur" else 0))
            if selected == "Récupération et repos":
                st.session_state.fatigue = max(0, st.session_state.fatigue - 22)
                st.session_state.year["activities"][-1] += f" Fatigue −22 · niveau actuel {st.session_state.fatigue}%."
            elif is_training or selected == "Effectuer une tâche au travail":
                st.session_state.fatigue = min(100, st.session_state.fatigue + (8 if selected == "Effectuer une tâche au travail" else 6))
            update_career_skill(world, f"{selected} {activity_text}", st.session_state.career)
            if "stage" in selected.lower(): st.session_state.money += 100
            selected_role = job_choice if selected == "Postuler à un métier" else st.session_state.career
            trigger_action_animation(world, selected, selected_role)
            st.success("Activité ajoutée à l’année en cours.")
            st.rerun()

        st.markdown("#### 🗺️ Explorer les lieux")
        st.caption("Chaque lieu peut être exploré une fois par année. Les sorties, entraînements et rencontres nourrissent ta chronologie.")
        st.session_state.year.setdefault("explored_locations", [])
        place_actions = exploration_catalog(world, age, st.session_state.career, st.session_state.rank, st.session_state.place, st.session_state.clubs, st.session_state.hero_affiliation)
        available_places = [location for location in place_actions if location not in st.session_state.year["explored_locations"]]
        st.session_state.year.setdefault("training_counts", {})
        exploration_training_count = st.session_state.year["training_counts"].get("bonus", 0)
        st.caption(f"Lieux visités : {len(st.session_state.year['explored_locations'])} · entraînements bonus : {exploration_training_count}/3")
        if not available_places:
            st.info("Tu as déjà exploré les lieux accessibles cette année. D’autres destinations s’ouvriront avec ton âge, ton grade ou ton métier.")
        else:
            explore_place = st.selectbox("Où veux-tu aller ?", available_places, key=f"explore_place_{age}")
            available_exploration_actions = [item for item in place_actions[explore_place] if not item[5] or exploration_training_count < 3]
            explore_choice = st.selectbox("Que faire sur place ?", available_exploration_actions, format_func=lambda item: item[0], key=f"explore_action_{age}_{explore_place}")
            if explore_choice[5] and exploration_training_count >= 3:
                st.caption("Les trois bonus d’entraînement de l’année sont utilisés.")
            if st.button(f"🚶 Aller à {explore_place}", key=f"explore_button_{age}_{explore_place}", type="secondary", use_container_width=True):
                label, stat, bonus, messages, followups, is_exploration_training, money_reward = explore_choice
                result = random.choice(messages)
                if world == "Tokyo Revengers" and "Territoire contesté" in explore_place:
                    target_area = explore_place.split("·", 1)[-1].strip()
                    negotiation = "négocier" in label.lower()
                    influence = st.session_state.career_skills.get("Leadership", 20) if negotiation else mission_power(world) + st.session_state.gang_members // 2
                    territory_chance = min(88, max(20, (38 if negotiation else 25) + influence // 2 + len(st.session_state.gang_allies) * 6))
                    if random.randint(1, 100) <= territory_chance:
                        if target_area not in st.session_state.gang_territories: st.session_state.gang_territories.append(target_area)
                        st.session_state.gang_renown = min(100, st.session_state.gang_renown + (6 if negotiation else 8))
                        result += f" Réussite : {st.session_state.gang} gagne une influence durable à {target_area}. La médiation ou le défi reste encadré et les habitants ne sont pas pris à partie."
                        st.session_state.event_followups.append(f"Une faction rivale réagit à l’influence de {st.session_state.gang} à {target_area} et propose un sommet entre responsables.")
                    else:
                        st.session_state.gang_reputation = max(-100, st.session_state.gang_reputation - 1)
                        result += f" Le gang rival garde son influence à {target_area}; tu peux préparer une autre approche l’année prochaine."
                if stat == "Honneur":
                    st.session_state.honor = min(100, st.session_state.honor + bonus)
                elif not is_exploration_training or exploration_training_count < 3:
                    st.session_state.stats[stat] = min(100, st.session_state.stats.get(stat, 48) + bonus)
                if is_exploration_training and exploration_training_count < 3:
                    st.session_state.year["training_counts"]["bonus"] = exploration_training_count + 1
                    st.session_state.stats["Bonheur"] = min(100, st.session_state.stats["Bonheur"] + 1)
                    st.session_state.fatigue = min(100, st.session_state.fatigue + 5)
                    result += f" Bonus d’entraînement {exploration_training_count + 1}/3."
                elif is_exploration_training:
                    result += " Tu as déjà utilisé tes trois bonus d’entraînement cette année."
                if money_reward:
                    st.session_state.money += money_reward
                    result += f" +{money_reward} crédits."
                st.session_state.year["explored_locations"].append(explore_place)
                activity_result = f"🗺️ {explore_place} · {label} : {result}"
                st.session_state.year["activities"].append(activity_result)
                st.session_state.year["events"].append(f"Pendant ton exploration à {explore_place}, {result}")
                st.session_state.event_followups.append(random.choice(followups))
                st.session_state.history.append({"age": age, "lieu": explore_place, "choix": label, "résultat": result})
                update_career_skill(world, f"{explore_place} {label} {result}", st.session_state.career)
                animation_action = f"{explore_place} {label}"
                if world == "Naruto" and ("Forêt" in explore_place or "kunai" in label.lower()):
                    animation_action = "mission combat " + animation_action
                trigger_action_animation(world, animation_action, st.session_state.career)
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
            elif world == "Tokyo Revengers":
                mission_ready = age >= 14 and bool(st.session_state.get("gang"))
                max_rank = {"Nouveau": "D", "Membre": "C", "Combattant": "B", "Lieutenant": "B", "Capitaine": "A", "Vice-chef": "S", "Chef": "SS"}.get(st.session_state.get("gang_rank", "Nouveau"), "D")
                if age < 16: max_rank = "C"
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
        if world == "Monde réel":
            st.markdown("#### 📌 Offres et reconversion")
            if age < 16:
                st.info("Les premières expériences professionnelles s’ouvriront à partir de 16 ans. Pour l’instant, les études, les stages et les clubs préparent ton avenir.")
            else:
                available_jobs = JOBS if age >= 18 else ["Vendeur", "Cuisinier", "Livreur", "Facteur"]
                sports_ready = age >= 18 and (bool(st.session_state.clubs) or st.session_state.stats["Santé"] >= 75) and st.session_state.stats["Talent"] >= 55
                job_offers = [job for job in available_jobs if job not in ("Footballeur professionnel", "Sportif professionnel") or sports_ready]
                if age >= 18 and not sports_ready:
                    st.caption("🔒 Les carrières sportives demandent une bonne santé, du talent ou un parcours en club. Tu peux toujours viser les autres métiers.")
                if st.session_state.career != "Aucune":
                    st.markdown(f'<div class="card event"><b>Poste actuel · {st.session_state.career}</b><br>Niveau {st.session_state.career_level} · {st.session_state.job_tasks}/3 missions avant l’évaluation<br><span class="muted">Tu peux continuer ici, candidater à un autre poste ou te reconvertir.</span></div>', unsafe_allow_html=True)
                offer, apply = st.columns([3, 1])
                with offer:
                    job_target = st.selectbox("Poste à viser", job_offers, key="career_market_job")
                with apply:
                    st.write("")
                    apply_job = st.button("Postuler", key="career_market_apply", type="primary", use_container_width=True)
                if apply_job:
                    profile = career_skill_profile(world, job_target)
                    skill_average = sum(profile.values()) // max(1, len(profile))
                    chance = min(92, max(18, 24 + st.session_state.stats["Intelligence"] // 3 + st.session_state.stats["Talent"] // 5 + skill_average // 4 + st.session_state.career_level * 3))
                    st.session_state.career_applications = st.session_state.get("career_applications", 0) + 1
                    if random.randint(1, 100) <= chance:
                        previous = st.session_state.career
                        st.session_state.career = job_target
                        st.session_state.career_level = 1
                        st.session_state.job_tasks = 0
                        result = f"Ta candidature pour {job_target.lower()} est retenue ({chance}% estimés). Tu commences au niveau 1" + (f" après ta reconversion depuis {previous}." if previous != "Aucune" else ".")
                        st.session_state.career_skills = career_skill_profile(world, job_target)
                        st.balloons()
                    else:
                        result = f"Ta candidature pour {job_target.lower()} n’aboutit pas ({chance}% estimés). L’employeur te conseille de gagner de l’expérience, suivre un stage ou renforcer tes aptitudes. Tu pourras retenter ta chance."
                    st.session_state.year["activities"].append(result)
                    st.session_state.year["events"].append(result)
                    st.session_state.history.append({"age": age, "choix": f"Candidature · {job_target}", "résultat": result})
                    trigger_action_animation(world, "travail candidature carrière", job_target)
                    st.rerun()
                if st.session_state.career != "Aucune" and st.session_state.career in CAREER_TASKS:
                    task_pool = CAREER_TASKS[st.session_state.career]
                    task_choice = st.selectbox("Mission professionnelle", task_pool, key="career_market_task")
                    task_done = st.session_state.year.get("career_task_done", False)
                    if st.button("Accomplir la mission", key="career_market_task_button", disabled=task_done, use_container_width=True):
                        st.session_state.year["career_task_done"] = True
                        st.session_state.job_tasks += 1
                        wage = random.randint(300, 650)
                        st.session_state.money += wage
                        update_career_skill(world, task_choice, st.session_state.career)
                        promoted = st.session_state.job_tasks >= 3
                        if promoted:
                            st.session_state.career_level += 1
                            st.session_state.job_tasks = 0
                        st.session_state.fatigue = min(100, st.session_state.fatigue + random.randint(4, 9))
                        result = f"Mission accomplie : {task_choice}. +{wage} crédits." + (f" Ton sérieux te vaut une promotion au niveau {st.session_state.career_level} !" if promoted else f" Encore {3 - st.session_state.job_tasks} mission(s) avant l’évaluation.")
                        st.session_state.year["activities"].append(result)
                        st.session_state.history.append({"age": age, "choix": task_choice, "métier": st.session_state.career, "niveau": st.session_state.career_level})
                        trigger_action_animation(world, task_choice, st.session_state.career)
                        st.rerun()
                    if task_done:
                        st.caption("Mission annuelle déjà accomplie. Tes progrès reprendront l’année prochaine.")
                elif st.session_state.career == "Aucune":
                    st.caption("Un premier poste te donnera accès à des missions propres au métier, des revenus et des promotions.")
        if world == "Tokyo Revengers":
            hierarchy_index = min(TOKYO_HIERARCHY.index(st.session_state.gang_rank), len(TOKYO_HIERARCHY) - 1)
            promotion_target = TOKYO_HIERARCHY[min(hierarchy_index + 1, len(TOKYO_HIERARCHY) - 1)]
            promotion_goal = max(2, hierarchy_index + 1)
            st.markdown(f'<div class="card event"><b>🏍️ {st.session_state.gang or "Aucun gang"} · {st.session_state.gang_rank}</b><br>Prochain rang : {promotion_target} · missions réussies {st.session_state.gang_mission_successes}/{promotion_goal}<br>Renommée {st.session_state.gang_renown}/100 · Réputation locale {st.session_state.gang_reputation:+d} · {st.session_state.gang_members} membres<br>Territoires : {", ".join(st.session_state.gang_territories) or "aucun"}<br>Alliances : {", ".join(st.session_state.gang_allies) or "aucune"}<br>Présence scolaire : {st.session_state.school_attendance} année(s)</div>', unsafe_allow_html=True)
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
                npc = next(item for item in active_npcs if item["name"] == npc_name)
                npc_actions = ["Discuter de sa journée", "Envoyer un message", "Encourager et soutenir", "Demander de l’aide", "Lui rendre un service", "Lui demander un service", "Partager un secret", "Proposer une activité", "Proposer un projet commun", "Proposer une sortie", "Inviter chez toi", "Offrir un petit cadeau", "Demander un conseil de carrière", "Présenter un autre ami", "Défier sur son terrain", "S’excuser après un désaccord", "Prendre mes distances"]
                if world == "Naruto": npc_actions += ["Demander un entraînement de jutsu", "Proposer une mission d’équipe"]
                elif world == "Kuroko Basket": npc_actions += ["S’entraîner au tir ensemble", "Proposer un match amical"]
                elif world == "Jujutsu Kaisen": npc_actions += ["S’entraîner à contrôler l’énergie", "Enquêter ensemble sur un fléau"]
                elif world == "Tokyo Revengers": npc_actions += ["Organiser une réunion de gang", "Proposer une alliance de quartier"]
                else: npc_actions += ["Travailler sur une mission ensemble", "Demander une recommandation professionnelle"]
                npc_choice = st.selectbox("Interaction", npc_actions, key="npc_interaction_choice")
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
                        prior = npc.get("memories", [])
                        accepted = npc.get("trust", 50) >= 42 or not prior
                        if npc_choice == "Offrir un petit cadeau":
                            if st.session_state.money >= 60:
                                st.session_state.money -= 60
                                result = f"Tu offres un petit cadeau à {npc_name}. Le geste lui fait plaisir et restera dans sa mémoire. (−60 crédits)"
                                npc["trust"] = min(100, npc.get("trust", 50) + 8)
                            else:
                                result = f"Tu voulais offrir un cadeau à {npc_name}, mais ton budget ne le permet pas encore. Vous choisissez de discuter à la place."
                        elif npc_choice in ("Défier sur son terrain",) or "match" in npc_choice.lower() or "mission" in npc_choice.lower() or "entraînement" in npc_choice.lower() or "entraîner" in npc_choice.lower() or "s’entraîner" in npc_choice.lower():
                            if accepted:
                                update_career_skill(world, npc_choice, st.session_state.career)
                                if "basket" in npc_choice.lower() or "tir" in npc_choice.lower():
                                    st.session_state.stats["Talent"] = min(100, st.session_state.stats["Talent"] + 2)
                                if world in ("Naruto", "Jujutsu Kaisen"):
                                    st.session_state.stats["Intelligence"] = min(100, st.session_state.stats["Intelligence"] + 1)
                                result = f"{npc_name} accepte : {npc_choice.lower()}. Vous progressez ensemble, et cette séance renforce votre confiance mutuelle."
                            else:
                                result = f"{npc_name} garde en tête votre dernier désaccord et décline pour l’instant. Il faudra renouer le lien avant de proposer un projet commun."
                        elif npc_choice == "Lui demander un service":
                            if npc.get("trust", 50) >= 60:
                                result = f"{npc_name} accepte de t’aider. Tu lui devras une faveur et ce service pourra compter lors d’un prochain événement."
                                st.session_state.event_followups.append(f"{npc_name} te demandera bientôt un coup de main en retour.")
                                st.session_state.stats["Bonheur"] = min(100, st.session_state.stats["Bonheur"] + 2)
                            else:
                                result = f"{npc_name} n’est pas assez proche de toi pour rendre ce service. Commence par passer du temps ensemble et réparer votre lien."
                        elif npc_choice in ("Proposer une activité", "Proposer une sortie", "Inviter chez toi"):
                            if accepted:
                                result = f"{npc_name} accepte : vous choisissez ensemble une activité et partagez un moment qui renforce votre amitié."
                                st.session_state.stats["Bonheur"] = min(100, st.session_state.stats["Bonheur"] + 4)
                            else:
                                result = f"{npc_name} décline pour l’instant. Votre dernier désaccord n’est pas encore oublié."
                        elif npc_choice == "Présenter un autre ami":
                            if st.session_state.friends:
                                introduced = random.choice(st.session_state.friends).split(" ·")[0]
                                result = f"Tu présentes {introduced} à {npc_name}. Ils s’entendent bien et proposent de se revoir tous les trois."
                                st.session_state.friends.append(f"{npc_name} · ami de {introduced}")
                            else:
                                result = f"Tu n’as pas encore de nouvel ami à présenter à {npc_name}. Une rencontre ou une activité de groupe pourrait changer cela."
                        elif npc_choice == "Demander un conseil de carrière" or npc_choice == "Demander une recommandation professionnelle":
                            result = f"{npc_name} partage son expérience de {npc.get('job', 'son métier')} et te recommande de miser sur la régularité."
                            st.session_state.stats["Intelligence"] = min(100, st.session_state.stats["Intelligence"] + 2)
                            st.session_state.event_followups.append(f"{npc_name} te propose de revenir après avoir suivi une formation, avec une piste de carrière concrète.")
                        elif accepted:
                            result = random.choice([f"{npc_name} accepte ta proposition et vous fixez une date.", f"{npc_name} hésite, puis se confie à toi. Votre lien devient plus solide.", f"{npc_name} te répond avec une proposition inattendue à son tour."])
                        else:
                            result = f"{npc_name} n’est pas encore prêt·e à accepter. Son souvenir de votre dernier échange pèse sur sa réponse."
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
            if st.session_state.family:
                family_names = [person.split(" ·")[0] for person in st.session_state.family]
                family_target = st.selectbox("Avec quel proche ?", family_names, key="family_interaction_target")
                family_person = next(person for person in st.session_state.family if person.split(" ·")[0] == family_target)
                bond = st.session_state.family_bonds.get(family_target, 50)
                st.caption(f"Lien avec {family_target} · {bond}% · {family_person.split(' ·')[1] if len(family_person.split(' ·')) > 1 else 'proche'}")
                if st.button("📞 Appeler et prendre des nouvelles", key="call_selected_relative"):
                    st.session_state.family_bonds[family_target] = min(100, bond + 5)
                    st.session_state.year["close"].append(f"Tu appelles {family_target} et prends de ses nouvelles. Votre lien passe à {min(100, bond + 5)}%.")
                    st.session_state.stats["Bonheur"] = min(100, st.session_state.stats["Bonheur"] + 4)
                    st.session_state.history.append({"age": age, "choix": f"Appeler · {family_target}", "lien": min(100, bond + 5)})
                    st.rerun()
                interact = st.selectbox("Interaction", ["Encourager un proche", "Demander conseil", "Proposer une sortie", "Aider pour une tâche", "Partager un secret", "Fêter une réussite", "S’excuser après une dispute", "Présenter un nouvel ami", "Lancer un projet ensemble", "Prendre des nouvelles après une absence"], key="family_interaction_choice")
                if st.button("Interagir", key="family_interaction_button"):
                    bond_change = -3 if interact == "Présenter un nouvel ami" and bond < 30 else 6 if interact in ("Aider pour une tâche", "Partager un secret", "S’excuser après une dispute", "Encourager un proche") else 3
                    new_bond = max(0, min(100, bond + bond_change))
                    st.session_state.family_bonds[family_target] = new_bond
                    response = random.choice(["accepte avec plaisir", "te remercie et propose son aide en retour", "est occupé·e, mais promet de te revoir bientôt", "se confie et vous rapproche", "hésite puis finit par accepter", "réagit mal sur le moment avant de revenir s’expliquer", "te surprend avec une proposition à son tour", "te demande de l’accompagner dans une décision importante"])
                    result = f"Tu choisis de {interact.lower()} avec {family_target}. Cette personne {response}. Votre lien atteint {new_bond}%."
                    st.session_state.year["close"].append(result)
                    st.session_state.history.append({"age": age, "choix": f"{interact} · {family_target}", "lien": new_bond})
                    st.session_state.stats["Bonheur"] = min(100, st.session_state.stats["Bonheur"] + (4 if bond_change > 0 else 1))
                    if new_bond >= 80 and bond < 80:
                        st.session_state.event_followups.append(f"{family_target} se souvient de ta présence et te proposera bientôt son aide pour un projet important.")
                    if new_bond < 20:
                        st.session_state.event_followups.append(f"{family_target} garde en mémoire votre dernier désaccord. Une excuse ou une conversation pourrait réparer votre lien.")
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
                    partner_action = st.selectbox("Avec ton/ta partenaire", ["Discuter de sa journée", "Passer du temps ensemble", "Organiser une sortie au parc", "Aller au cinéma", "Préparer un repas ensemble", "Rencontrer ses proches", "Parler d’un projet commun", "Faire une surprise", "Avoir une conversation difficile", "Mettre fin à la relation"], key="partner_action")
                    if st.button("Confirmer l’interaction", key="partner_interaction"):
                        if partner_action == "Mettre fin à la relation":
                            st.session_state.year["close"].append(f"Tu mets fin à ta relation avec {partner['name']}. Cette décision marque une nouvelle étape.")
                            st.session_state.event_followups.append(f"{partner['name']} se souviendra de votre histoire. Il/elle pourrait reprendre contact ou tourner la page avec le temps.")
                            st.session_state.partner = None
                        else:
                            partner.setdefault("affection", 50)
                            if partner_action == "Avoir une conversation difficile":
                                partner["affection"] = max(0, partner["affection"] - random.randint(1, 7))
                                reaction = random.choice(["écoute ton point de vue et vous trouvez un compromis", "se braque au début, puis accepte d’en reparler", "n’est pas prêt·e à en parler et demande du temps"])
                            else:
                                delta = random.randint(4, 9) if partner_action in ("Faire une surprise", "Rencontrer ses proches", "Parler d’un projet commun") else random.randint(2, 6)
                                partner["affection"] = min(100, partner["affection"] + delta)
                                reaction = random.choice(["apprécie ton attention et te propose de remettre ça", "se confie davantage et vous vous rapprochez", "répond avec enthousiasme et partage une idée à son tour"])
                            st.session_state.stats["Bonheur"] = min(100, st.session_state.stats["Bonheur"] + (1 if partner_action == "Avoir une conversation difficile" else 4))
                            result = f"Tu choisis de {partner_action.lower()} avec {partner['name']}. Cette personne {reaction}. Affection : {partner['affection']}%."
                            st.session_state.year["close"].append(result)
                            st.session_state.history.append({"age": age, "relation": partner["name"], "choix": partner_action, "affection": partner["affection"]})
                            if partner["affection"] >= 80:
                                st.session_state.event_followups.append(f"{partner['name']} se sent prêt·e à parler d’un grand projet avec toi.")
                        st.rerun()
                else:
                    if st.session_state.dating_candidate:
                        candidate = st.session_state.dating_candidate
                        st.markdown(f'<div class="card event">✨ Tu rencontres <b>{candidate["name"]}</b> · {candidate["occupation"]}<br><span class="muted">{candidate["trait"]} · {candidate.get("meeting_place", "une rencontre inattendue")}</span></div>', unsafe_allow_html=True)
                        choices = ["Proposer une sortie amicale", "Commencer par une amitié", "Décliner la rencontre"] if st.session_state.orientation == "Asexuel·le" else ["Proposer un café", "Proposer une sortie culturelle", "Commencer par une amitié", "Décliner la rencontre"]
                        meeting_choice = st.radio("Que souhaites-tu faire ?", choices, key="meeting_choice", horizontal=True)
                        if st.button("Valider mon choix", key="meeting_decision"):
                            if meeting_choice in ("Proposer un rendez-vous", "Proposer une sortie amicale", "Proposer un café", "Proposer une sortie culturelle"):
                                chance = min(90, max(15, 25 + st.session_state.stats["Beauté"] // 5 + st.session_state.stats["Bonheur"] // 6 + (10 if meeting_choice == "Proposer un café" else 0)))
                                if random.randint(1, 100) <= chance:
                                    candidate["status"] = "Lien de confiance" if st.session_state.orientation == "Asexuel·le" else "Relation naissante"
                                    candidate["affection"] = random.randint(45, 65)
                                    st.session_state.partner = candidate
                                    st.session_state.year["close"].append(f"Ta proposition ({meeting_choice.lower()}) plaît à {candidate['name']}. Vous passez un bon moment à {candidate.get('meeting_place', 'votre rendez-vous')} et décidez de vous revoir.")
                                    st.session_state.event_followups.append(f"{candidate['name']} te propose une sortie qui pourrait faire évoluer votre relation.")
                                    st.balloons()
                                else:
                                    st.session_state.year["close"].append(f"{candidate['name']} décline ta proposition. Vous échangez encore un peu et vous quittez en bons termes.")
                            elif meeting_choice == "Commencer par une amitié":
                                st.session_state.friends.append(f"{candidate['name']} · nouvel ami")
                                st.session_state.year["close"].append(f"Tu rencontres {candidate['name']} et vous choisissez de commencer par une amitié.")
                            else:
                                st.session_state.year["close"].append(f"Tu déclines poliment la proposition de {candidate['name']}.")
                            st.session_state.dating_candidate = None
                            st.rerun()
                    else:
                        meeting_places = ["À une sortie entre amis", "À l’école ou à la fac", "Dans un club sportif", "À un concert ou une exposition"]
                        if age >= 18:
                            meeting_places.extend(["Au travail", "Par l’intermédiaire d’un proche"])
                        meeting_place = st.selectbox("Où faire une rencontre ?", meeting_places, key="meeting_place_choice")
                        if st.button("✨ Faire une rencontre", key="meet_someone"):
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
                            occupations = ["élève", "joueur·se de basket", "musicien·ne", "artiste", "passionné·e de lecture"] if age < 18 else ["étudiant·e", "infirmier·ère", "musicien·ne", "joueur·se de basket", "journaliste", "développeur·se", "artiste", "collègue de travail"]
                            traits = ["aime les voyages", "est passionné·e de sport", "préfère les soirées calmes", "s’intéresse à la musique", "est très curieux·se", "aime aider les autres"]
                            st.session_state.dating_candidate = {"name": random.choice(names), "gender": candidate_gender, "occupation": random.choice(occupations), "trait": random.choice(traits), "status": "Rencontre", "meeting_place": meeting_place}
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
        save_keys = ["started", "age", "year", "stats", "family", "family_bonds", "friends", "children", "clubs", "history", "story_paths", "mission_counts", "jutsu_level", "known_jutsu", "mentor_jutsu", "pupil_power", "pupil_stage", "mentor_training", "mentor_progress", "tailed_beast", "beast_mastery", "orientation", "partner", "dating_candidate", "hero_affiliation", "npc_roster", "npc_memories", "career_skills", "fatigue", "technique_level", "job_tasks", "career_level", "technique", "techniques", "zones", "money", "coins", "pending_coins", "rank", "career", "challenges", "dead", "death_reason", "heir_count", "world", "first", "surname", "gender", "hair", "beard", "avatar", "place", "clan", "generation", "honor", "fame", "inventory", "captured", "event_followups", "event_memory", "news_memory", "night_mode"]
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
