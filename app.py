import random
import streamlit as st

st.set_page_config(page_title="Destins — simulation de vie", page_icon="✨", layout="wide")

WORLDS = {
    "Monde réel": {"icon": "🌍", "places": ["Lyon, France", "Montréal, Canada", "Dakar, Sénégal", "Tokyo, Japon"], "families": ["Martin", "Diallo", "Moreau", "Bernard", "Leroy"]},
    "Kuroko Basket": {"icon": "🏀", "places": ["Tokyo, Japon", "Kanagawa, Japon", "Kyoto, Japon"], "families": ["Kagami", "Kuroko", "Aomine", "Midorima", "Kise"]},
    "Naruto": {"icon": "🍥", "places": ["Konoha", "Suna", "Kiri", "Iwa", "Kumo"], "families": ["Uchiha", "Hyûga", "Nara", "Uzumaki", "Inuzuka", "Akimichi", "Aburame", "Inconnu"]},
    "Jujutsu Kaisen": {"icon": "🔮", "places": ["Tokyo, Japon", "Kyoto, Japon", "Sendai, Japon"], "families": ["Gojo", "Zenin", "Kamo", "Inconnu"]},
}
JOBS = ["Facteur", "Analyste", "Livreur", "Militaire", "Vendeur", "Infirmier", "Cuisinier", "Professeur", "Ingénieur", "Journaliste"]
CHAKRA = {"Uchiha": "Feu", "Hyûga": "Foudre", "Nara": "Yin", "Uzumaki": "Vent", "Inuzuka": "Terre", "Akimichi": "Terre", "Aburame": "Terre", "Inconnu": "Vent"}

st.markdown("""<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Space+Grotesk:wght@500;600;700&display=swap');
html,body,[class*="css"]{font-family:'DM Sans',sans-serif} .stApp{background:#f5f7fa;color:#1d2735}
.block-container{max-width:1180px;padding-top:1.2rem;padding-bottom:3rem}
.hero{background:linear-gradient(115deg,#152b4c,#244b72 65%,#2f7790);border-radius:24px;padding:28px 32px;color:white;margin-bottom:20px}
.hero h1{font-family:'Space Grotesk';font-size:2.1rem;margin:0}.hero p{color:#d9e6f3;margin:.35rem 0 0}
.card{background:#fff;border:1px solid #e6eaf0;border-radius:18px;padding:18px 20px;margin:10px 0;box-shadow:0 5px 20px #162a4010}
.event{border-left:4px solid #e4ad37}.muted{color:#718096;font-size:.9rem}.big{font-family:'Space Grotesk';font-size:1.35rem;font-weight:700}
.stButton>button{border-radius:12px;font-weight:600;min-height:2.7rem}.stProgress>div>div>div>div{background:#48a890}
[data-testid="stMetric"]{background:white;border:1px solid #e6eaf0;padding:12px 16px;border-radius:14px}
</style>""", unsafe_allow_html=True)

def init():
    for k, v in {"started": False, "age": 0, "log": [], "stats": {"Bonheur": 72, "Santé": 88, "Intelligence": 54, "Talent": 48}, "family": [], "friends": [], "mission": 0, "money": 1200}.items():
        if k not in st.session_state: st.session_state[k] = v

def add_log(text):
    st.session_state.log.insert(0, (st.session_state.age, text))

init()
st.markdown('<div class="hero"><h1>✨ DESTINS</h1><p>Une vie, mille chemins. Chaque choix écrit la suite.</p></div>', unsafe_allow_html=True)

if not st.session_state.started:
    a, b = st.columns([1.05, .95], gap="large")
    with a:
        st.markdown('<div class="card"><div class="big">Crée ton personnage</div><p class="muted">Choisis un univers et découvre la vie qui t’attend.</p></div>', unsafe_allow_html=True)
        world = st.selectbox("Univers", list(WORLDS), format_func=lambda x: f"{WORLDS[x]['icon']}  {x}")
        first = st.text_input("Prénom", "Rick")
        surname_choice = st.selectbox("Nom de famille", ["Aléatoire"] + WORLDS[world]["families"])
        gender = st.selectbox("Personnage", ["Garçon", "Fille", "Non-binaire"])
        hair = st.selectbox("Coiffure de départ", ["Courte", "Mi-longue", "Longue", "Ébouriffée", "Tressée"])
        if world == "Naruto":
            st.caption("Le clan sera attribué à la naissance selon ton choix ou le hasard.")
            clan_mode = st.radio("Origine", ["Clan aléatoire", "Choisir un clan"], horizontal=True)
            clan = st.selectbox("Clan", WORLDS[world]["families"]) if clan_mode == "Choisir un clan" else "Aléatoire"
        else: clan = ""
        if st.button("✨  Commencer ma vie", type="primary", use_container_width=True):
            family = random.choice(WORLDS[world]["families"]) if surname_choice == "Aléatoire" else surname_choice
            if world == "Naruto" and clan:
                family = random.choice(WORLDS[world]["families"]) if clan == "Aléatoire" else clan
            st.session_state.update(started=True, world=world, first=first.strip() or "Alex", surname=family, gender=gender, hair=hair, place=random.choice(WORLDS[world]["places"]), clan=family if world == "Naruto" else "")
            st.session_state.family = [f"{random.choice(['Maya','Noah','Lina','Eli'])} {family} · parent", f"{random.choice(['Samir','Lou','Jules','Inès'])} {family} · frère / sœur"]
            st.session_state.log = [(0, f"{first or 'Alex'} {family} vient de naître à {random.choice(WORLDS[world]['places'])}. Une nouvelle histoire commence.")]
            st.rerun()
    with b:
        st.markdown('<div class="card"><div class="big">Quatre univers, des destins uniques</div><p>Vis une carrière, noue des liens et fais face aux imprévus. Tes proches grandissent avec toi et tes décisions laissent une trace.</p></div>', unsafe_allow_html=True)
        for name, data in WORLDS.items(): st.markdown(f'<div class="card">{data["icon"]} <b>{name}</b><br><span class="muted">'+{"Monde réel":"Carrière, études, famille et occasions rares.","Kuroko Basket":"Entraînement, matchs et rêve professionnel.","Naruto":"Clans, chakra, missions et examens ninja.","Jujutsu Kaisen":"Techniques occultes, fléaux et exorcisme."}[name]+'</span></div>', unsafe_allow_html=True)
else:
    world=st.session_state.world; age=st.session_state.age; name=f"{st.session_state.first} {st.session_state.surname}"
    head, action=st.columns([3,1]);
    with head: st.markdown(f"### {WORLDS[world]['icon']} {name}  ·  {st.session_state.place}")
    with action: st.markdown(f"<div style='text-align:right;padding-top:12px'>💰 {st.session_state.money:,} crédits</div>",unsafe_allow_html=True)
    tabs=st.tabs(["📖 Ma vie", "🧭 Actions", "👥 Entourage", "📻 Radio"])
    with tabs[0]:
        left,right=st.columns([1.5,1],gap="large")
        with left:
            st.markdown(f'<div class="card"><div class="big">{st.session_state.hair} · {st.session_state.gender.lower()}</div><p>Âge : <b>{age} ans</b> · {world}</p>'+ (f'<p>Clan {st.session_state.clan} · chakra {CHAKRA.get(st.session_state.clan,"Vent")}</p>' if world=="Naruto" else '')+'</div>',unsafe_allow_html=True)
            st.markdown("#### Chronologie")
            for yr,entry in st.session_state.log[:12]: st.markdown(f'<div class="card event"><b>{yr} ans</b><br>{entry}</div>',unsafe_allow_html=True)
            if st.button("➕  Passer une année",type="primary",use_container_width=True):
                st.session_state.age+=1; st.session_state.money+=random.randint(100,500)
                # Relationships change independently as the years pass.
                if random.random()<.3: st.session_state.stats["Bonheur"]=max(0,min(100,st.session_state.stats["Bonheur"]+random.choice([-8,5,9])))
                if age < 6: msg="Tu découvres le monde et grandis auprès de ta famille."
                elif world=="Monde réel": msg=random.choice(["Une journée ordinaire t’apporte une nouvelle rencontre.","Tu réussis un contrôle et gagnes en confiance.","Une morsure d’insecte étrange te laisse une marque lumineuse…",f"Une opportunité de stage attire ton attention."])
                elif world=="Naruto": msg=random.choice(["Une mission de rang D te permet de faire tes preuves.","Ton entraînement fait progresser ton chakra.","La radio annonce une tension à la frontière.","Un parchemin ancien est signalé près du village."])
                elif world=="Kuroko Basket": msg=random.choice(["L’entraînement se termine par un duel intense.","Un recruteur observe le match depuis les gradins.","Ton équipe prépare un tournoi décisif.","Un coéquipier te demande de travailler tes passes."])
                else: msg=random.choice(["Une énergie occulte inquiétante est détectée en ville.","Ton mentor te confie une mission de repérage.","Un fléau apparaît près de l’école.","Tu affines ta technique pendant l’entraînement."])
                add_log(msg); st.rerun()
        with right:
            st.markdown("#### Mes statistiques")
            for stat,val in st.session_state.stats.items(): st.write(f"{stat}  ·  {val}%"); st.progress(val/100)
            st.markdown('<div class="card"><b>🎯 Prochain objectif</b><br><span class="muted">'+("Réussir une mission pour progresser en grade." if world=="Naruto" else "Entretiens tes aptitudes et saisis les occasions.")+'</span></div>',unsafe_allow_html=True)
    with tabs[1]:
        st.markdown("#### Que veux-tu faire cette année ?")
        options={"Monde réel":["Étudier", "Faire du sport", "Lire", "Postuler à un emploi", "Sortir avec des amis"],"Naruto":["Entraînement chakra", "Entraînement physique", "Mission de rang D", "Étudier un jutsu", "Aider un proche"],"Kuroko Basket":["Tirs au panier", "Travailler les passes", "Musculation", "Match amical", "Réviser"],"Jujutsu Kaisen":["Méditation occulte", "Entraînement au combat", "Mission d’exorcisme", "Étudier les fléaux", "Voir un ami"]}[world]
        choice=st.selectbox("Activité",options)
        if st.button("Effectuer l’activité",use_container_width=True):
            stat="Intelligence" if any(x in choice.lower() for x in ["étud","lire"]) else "Talent" if world!="Monde réel" else "Santé"
            st.session_state.stats[stat]=min(100,st.session_state.stats[stat]+random.randint(3,8)); st.session_state.stats["Bonheur"]=min(100,st.session_state.stats["Bonheur"]+2)
            if "emploi" in choice.lower(): st.session_state.money+=650; msg="Tu décroches un petit emploi. +650 crédits."
            else: msg=f"Tu as consacré du temps à : {choice.lower()}. {stat} progresse."
            add_log(msg); st.success(msg)
        if world in ("Naruto","Kuroko Basket","Jujutsu Kaisen"):
            st.markdown('<div class="card"><b>⚔️ Progression spéciale</b><br><span class="muted">Les missions et entraînements font évoluer tes capacités. Les examens, recrutements et grades apparaîtront au fil de ta progression.</span></div>',unsafe_allow_html=True)
    with tabs[2]:
        st.markdown("#### Ta famille")
        for person in st.session_state.family: st.markdown(f'<div class="card">👤 {person} <span class="muted"> · poursuit sa propre vie</span></div>',unsafe_allow_html=True)
        if st.button("Prendre des nouvelles d’un proche"):
            who=random.choice(st.session_state.family); msg=f"Tu as passé un moment avec {who.split(' ·')[0]}. Votre lien s’est renforcé."; add_log(msg); st.session_state.stats["Bonheur"]=min(100,st.session_state.stats["Bonheur"]+6); st.success(msg)
        st.markdown("#### Relations")
        friend=st.session_state.friends or ["Aucun ami pour l’instant — les rencontres arrivent avec le temps."]
        for f in friend: st.write("💛 "+f)
    with tabs[3]:
        st.markdown("#### 📻 La radio du monde")
        headlines={"Monde réel":["Marché du travail : de nouvelles formations ouvrent près de chez toi.","Vie locale : le club sportif recrute des jeunes."],"Naruto":["Konoha : une mission de rang C est disponible pour les équipes genin.","Diplomatie : des émissaires de Suna arrivent au village."],"Kuroko Basket":["Basket : les qualifications inter-lycées débutent bientôt.","Scouts : un recruteur NBA est annoncé au tournoi d’été."],"Jujutsu Kaisen":["Alerte occulte : activité anormale signalée à la gare.","Écoles : les équipes de Tokyo et Kyoto préparent une rencontre."]}[world]
        for news in headlines: st.markdown(f'<div class="card">📡 {news}</div>',unsafe_allow_html=True)

st.markdown('<p style="text-align:center;color:#8491a2;margin-top:34px">DESTINS · Prototype narratif · Tes choix façonnent la suite</p>',unsafe_allow_html=True)
