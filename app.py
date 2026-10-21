import random
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
[data-testid="stTabs"] [role="tablist"]{position:fixed;z-index:999;bottom:0;left:50%;transform:translateX(-50%);width:min(100vw,540px);box-sizing:border-box;background:#174c71;padding:7px 5px max(7px,env(safe-area-inset-bottom));border-radius:0;margin:0;gap:0;justify-content:space-around;box-shadow:0 -3px 14px #152b4c20}
[data-testid="stTabs"] button[role="tab"]{color:#dcecf5;border:0;border-radius:8px;padding:8px 4px;font-size:.76rem;white-space:normal;line-height:1.15}
[data-testid="stTabs"] button[role="tab"][aria-selected="true"]{background:#fff;color:#174c71}
[data-testid="stRadio"] [role="radiogroup"]{gap:5px}
@media(max-width:600px){.block-container{padding-left:12px;padding-right:12px}.hero{margin-left:-12px;margin-right:-12px}.face{font-size:2.7rem}}
</style>""", unsafe_allow_html=True)

def init():
    defaults = {"started": False, "age": 0, "year": {"activities": [], "events": [], "close": []}, "stats": {"Bonheur": 72, "Santé": 88, "Intelligence": 54, "Talent": 48}, "family": [], "friends": [], "money": 1200, "rank": "Civil", "career": "Aucune"}
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

def add_year_item(section, text):
    st.session_state.year[section].append(text)

def age_stage(age):
    if age < 3: return "Petite enfance", "👶"
    if age < 6: return "Maternelle", "🧸"
    if age < 11: return "École primaire", "🎒"
    if age < 15: return "Collège", "📚"
    if age < 18: return "Lycée", "🏫"
    if age < 23: return "Études supérieures", "🎓"
    return "Vie adulte", "🌱"

def yearly_event(world, age):
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
        hair = st.selectbox("Coupe de cheveux", HAIR)
        beard = st.selectbox("Barbe", BEARDS, index=0, disabled=(gender == "Fille"))
        if world == "Naruto": st.info("Le clan sélectionné détermine ton affinité chakra et tes techniques de départ.")
        avatar_col, start_col = st.columns([1, 1.4])
        with avatar_col:
            face = "👩🏻" if gender == "Fille" else "🧑🏻" if gender == "Non-binaire" else "👨🏻"
            st.markdown(f'<div class="avatar"><div class="face">{face}</div><b>{hair}</b><br><span class="muted">{beard if gender != "Fille" else ""}</span></div>', unsafe_allow_html=True)
        with start_col:
            st.write("")
            if st.button("✨  Créer mon personnage", type="primary", use_container_width=True):
                family = random.choice(WORLDS[world]["families"]) if surname_choice == "Attribution aléatoire" else surname_choice
                place = random.choice(WORLDS[world]["places"])
                st.session_state.update(started=True, world=world, first=first.strip() or "Alex", surname=family, gender=gender, hair=hair, beard=beard, avatar=face, place=place, clan=family if world == "Naruto" else "", age=0, rank="Étudiant de l’académie" if world == "Naruto" else "Élève", career="Aucune", year={"activities": [], "events": [f"{first or 'Alex'} {family} naît à {place}. Sa famille l’accueille dans ce nouvel univers."], "close": []}, family=[f"{random.choice(['Maya','Noah','Lina','Eli'])} {family} · parent", f"{random.choice(['Samir','Lou','Jules','Inès'])} {family} · frère / sœur"], friends=[], stats={"Bonheur": 72, "Santé": 88, "Intelligence": 54, "Talent": 48}, money=1200)
                st.rerun()
    with right:
        st.markdown('<div class="card"><div class="big">2 · Prévisualise ton avatar</div><p>Ton personnage t’accompagnera dans sa chronologie. La coiffure et la barbe évolueront avec le temps.</p></div>', unsafe_allow_html=True)
        descriptions = {"Monde réel": "École, loisirs, orientation et métiers.", "Kuroko Basket": "Clubs, matchs, entraînement et recrutement.", "Naruto": "Clans, chakra, missions et examens ninja.", "Jujutsu Kaisen": "École d’exorcisme, fléaux et missions occultes."}
        for title, data in WORLDS.items(): st.markdown(f'<div class="card">{data["icon"]} <b>{title}</b><br><span class="muted">{descriptions[title]}</span></div>', unsafe_allow_html=True)
else:
    world, age = st.session_state.world, st.session_state.age
    name = f"{st.session_state.first} {st.session_state.surname}"
    stage, stage_icon = age_stage(age)
    col_avatar, col_info = st.columns([.55, 2.45], gap="small")
    with col_avatar: st.markdown(f'<div class="avatar"><div class="face">{st.session_state.avatar}</div><b>{st.session_state.hair}</b><br><span class="muted">{st.session_state.beard if age >= 16 else ""}</span></div>', unsafe_allow_html=True)
    with col_info:
        st.markdown(f"### {WORLDS[world]['icon']} {name}")
        st.markdown(f"**{stage_icon} {stage} · {age} ans**　|　📍 {st.session_state.place}　|　🏷️ {st.session_state.rank}　|　💰 {st.session_state.money:,} crédits")
        if world == "Naruto": st.caption(f"Clan {st.session_state.clan} · affinité chakra : {CHAKRA.get(st.session_state.clan, 'Vent')}")
    tab_year, tab_actions, tab_life = st.tabs(["📖 Année en cours", "🎯 Mes actions", "👥 Entourage & radio"])

    with tab_year:
        st.markdown(f"#### {stage_icon} {stage} · année de tes {age} ans")
        ev_col, close_col = st.columns([1.15, .85], gap="large")
        with ev_col:
            st.markdown("**🌍 Ce qui se passe dans ton univers**")
            for event in st.session_state.year["events"]: st.markdown(f'<div class="card event">{event}</div>', unsafe_allow_html=True)
            st.markdown("**📝 Tes activités cette année**")
            if st.session_state.year["activities"]:
                for item in st.session_state.year["activities"]: st.markdown(f'<div class="card">✅ {item}</div>', unsafe_allow_html=True)
            else: st.markdown('<div class="card muted">Tu n’as pas encore choisi d’activité pour cette année.</div>', unsafe_allow_html=True)
        with close_col:
            st.markdown("**👨‍👩‍👧 Actions de tes proches**")
            if st.session_state.year["close"]:
                for item in st.session_state.year["close"]: st.markdown(f'<div class="card">💛 {item}</div>', unsafe_allow_html=True)
            else: st.markdown('<div class="card muted">Ta famille vit aussi son année. Une nouvelle peut arriver à tout moment.</div>', unsafe_allow_html=True)
            st.markdown("**📊 Aptitudes**")
            for stat, value in st.session_state.stats.items(): st.write(f"{stat} · {value}%"); st.progress(value / 100)
        if st.button("➕  Terminer l’année et avancer", type="primary", use_container_width=True):
            st.session_state.age += 1
            new_age = st.session_state.age
            if random.random() < .5:
                relative = random.choice(st.session_state.family)
                st.session_state.year["close"].append(f"{relative.split(' ·')[0]} commence une nouvelle activité et te raconte ses projets.")
            else:
                relative = random.choice(st.session_state.family)
                st.session_state.year["close"].append(f"{relative.split(' ·')[0]} partage une sortie ou un moment important avec toi.")
            st.session_state.stats["Bonheur"] = max(0, min(100, st.session_state.stats["Bonheur"] + random.choice([-5, 0, 3, 6])))
            st.session_state.year = {"activities": [], "events": [yearly_event(world, new_age)], "close": []}
            # The relative's update belongs to the new year's chapter.
            st.session_state.year["close"].append(f"{relative.split(' ·')[0]} commence une nouvelle année de sa vie.")
            st.rerun()

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
        if world == "Kuroko Basket":
            if age < 15: actions.append(("Entraînement de basket", "Talent", "Tes fondamentaux progressent et tes chances d’intégrer une équipe augmentent."))
            else: actions.extend([( "Travailler les tirs", "Talent", "Tu répètes tes tirs sous pression."), ("Match d’entraînement", "Santé", "Un match intense te prépare aux sélections.")])
        elif world == "Naruto":
            if age < 12: actions.extend([( "Exercice de chakra", "Talent", "Tu apprends à mieux contrôler ton chakra."), ("Étudier les bases ninja", "Intelligence", "Tu mémorises les règles et techniques de l’académie.")])
            else: actions.extend([( "Entraînement de chakra", "Talent", "Ton contrôle du chakra s’améliore."), ("Mission adaptée à ton grade", "Santé", "Tu accomplis une mission correspondant à ton expérience.")])
        elif world == "Jujutsu Kaisen":
            actions.extend([( "Entraînement occulte", "Talent", "Tu affines ton énergie occulte."), ("Étudier les fléaux", "Intelligence", "Tu apprends à reconnaître les fléaux.")])
            if age >= 15: actions.append(("Mission d’exorcisme encadrée", "Santé", "Tu participes à une mission sous supervision."))
        selected = st.selectbox("Choisis une activité", [item[0] for item in actions])
        if st.button("Faire cette activité", type="primary", use_container_width=True):
            action = next(item for item in actions if item[0] == selected)
            st.session_state.year["activities"].append(action[2])
            st.session_state.stats[action[1]] = min(100, st.session_state.stats[action[1]] + random.randint(3, 7))
            st.session_state.stats["Bonheur"] = min(100, st.session_state.stats["Bonheur"] + (2 if action[1] != "Bonheur" else 0))
            if "stage" in selected.lower(): st.session_state.money += 100
            if world == "Naruto" and age >= 12 and "Mission" in selected:
                if random.random() < .35: st.session_state.rank = "Genin confirmé"
            st.success("Activité ajoutée à l’année en cours.")
            st.rerun()

    with tab_life:
        relatives, radio = st.columns(2, gap="large")
        with relatives:
            st.markdown("#### Famille et amis")
            for person in st.session_state.family: st.markdown(f'<div class="card">👤 {person}</div>', unsafe_allow_html=True)
            if st.session_state.friends:
                for friend in st.session_state.friends: st.markdown(f'<div class="card">🤝 {friend}</div>', unsafe_allow_html=True)
            if st.button("Appeler un proche"):
                person = random.choice(st.session_state.family)
                st.session_state.year["close"].append(f"Tu appelles {person.split(' ·')[0]} et prends de ses nouvelles.")
                st.session_state.stats["Bonheur"] = min(100, st.session_state.stats["Bonheur"] + 4)
                st.rerun()
        with radio:
            st.markdown("#### 📻 Radio de l’univers")
            for event in st.session_state.year["events"]: st.markdown(f'<div class="card">📡 {event}</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="card"><b>Ton statut</b><br>{stage} · {st.session_state.rank}<br><span class="muted">Les activités et interactions sont limitées par ton âge et ton grade.</span></div>', unsafe_allow_html=True)

st.markdown('<p style="text-align:center;color:#8491a2;margin-top:34px">DESTINS · Prototype narratif · Tes choix façonnent la suite</p>', unsafe_allow_html=True)
