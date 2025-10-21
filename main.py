import streamlit as st
import requests

st.set_page_config(page_title="OpenRouter • IA gratuite dynamique", page_icon="🧩")
st.title("😋 Modèles gratuits dynamiques – OpenRouter")
st.markdown("Liste automatisée depuis l’API officielle OpenRouter.\nSélectionne, envoie un prompt, reçois la réponse !")

@st.cache_data(ttl=3600)
def fetch_models():
    url = "https://openrouter.ai/api/v1/models"
    headers = {"Content-Type": "application/json"}
    models = []
    try:
        r = requests.get(url, headers=headers)
        r.raise_for_status()
        data = r.json().get('data', [])
        for m in data:
            pricing = m.get('pricing', {})
            if float(pricing.get('prompt', 0)) == 0 and float(pricing.get('completion', 0)) == 0:
                # Détection du type rapide
                # (Tu peux étoffer par mot-clé dans l'id ou name si tu veux affiner)
                if any(x in m.get('id', '').lower() or x in m.get('name', '').lower() for x in ['uncensored', 'venice', 'dolphin', 'mai', 'lumimaid']):
                    model_type = "Texte (non censuré)"
                else:
                    model_type = "Texte"
                models.append({
                    'id': m.get('id'),
                    'name': m.get('name'),
                    'type': model_type,
                    'desc': m.get('description', '')[:96] or '-'
                })
        return models
    except Exception as e:
        st.error(f"Erreur chargement modèles API OpenRouter : {e}")
        return []

models = fetch_models()

st.sidebar.header("🔑 Clé API OpenRouter")
api_key = st.sidebar.text_input("Entre ta clé API OpenRouter :", type="password")
if not api_key:
    st.sidebar.warning("Ajoute ta clé API OpenRouter pour interroger les modèles.")

if models:
    models_names = [f"{m['name']} – {m['type']}" for m in models]
    model_idx = st.selectbox("Choisis ton modèle IA :", models_names)
    model_selected = models[models_names.index(model_idx)]

    st.write(f"**Type :** {model_selected['type']}")
    st.write(f"**Description :** {model_selected['desc']}")

    prompt = st.text_area("Prompt à envoyer :", "")
    if st.button("Envoyer le prompt"):
        if not api_key:
            st.error("Tu dois saisir une clé API OpenRouter dans la barre latérale.")
        elif not prompt.strip():
            st.warning("Entre un prompt puis réessaie !")
        else:
            url = "https://openrouter.ai/api/v1/chat/completions"
            headers = {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
                "HTTP-Referer": "http://localhost",
                "X-Title": "Streamlit OpenRouter"
            }
            payload = {
                "model": model_selected['id'],
                "messages": [{"role": "user", "content": prompt.strip()}],
            }
            try:
                r = requests.post(url, json=payload, headers=headers, timeout=30)
                r.raise_for_status()
                result = r.json()
                answer = result["choices"][0]["message"]["content"]
                st.success("Réponse de l'IA :")
                st.write(answer)
            except Exception as e:
                st.error(f"Erreur API : {e}")
else:
    st.warning("Aucun modèle gratuit trouvé.")

st.caption("Source : openrouter.ai – liste dynamique, prompt direct !")
