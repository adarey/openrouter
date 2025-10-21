import requests
import json

def get_openrouter_free_models():
    """
    Script pour lister les modèles gratuits d'OpenRouter
    avec indication des modèles non censurés
    """
    
    # URL de l'API OpenRouter pour récupérer la liste des modèles
    url = "https://openrouter.ai/api/v1/models"
    
    headers = {
        "Content-Type": "application/json"
    }
    
    try:
        # Récupérer la liste des modèles
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        models = response.json()
        
        # Filtrer les modèles gratuits
        free_models = []
        uncensored_models = []
        
        for model in models.get('data', []):
            model_id = model.get('id', '')
            name = model.get('name', '')
            pricing = model.get('pricing', {})
            
            # Vérifier si le modèle est gratuit
            prompt_price = float(pricing.get('prompt', 0))
            completion_price = float(pricing.get('completion', 0))
            
            if prompt_price == 0 and completion_price == 0:
                model_info = {
                    'id': model_id,
                    'name': name,
                    'context_length': model.get('context_length', 'N/A'),
                    'description': model.get('description', '')
                }
                
                free_models.append(model_info)
                
                # Identifier les modèles non censurés
                if any(keyword in model_id.lower() or keyword in name.lower() 
                       for keyword in ['uncensored', 'dolphin', 'venice', 'lumimaid']):
                    uncensored_models.append(model_info)
        
        # Afficher les résultats
        print("=" * 80)
        print(f"MODÈLES GRATUITS OPENROUTER ({len(free_models)} trouvés)")
        print("=" * 80)
        
        for model in free_models:
            print(f"\n✓ {model['name']}")
            print(f"  ID: {model['id']}")
            print(f"  Contexte: {model['context_length']} tokens")
            if model['description']:
                print(f"  Description: {model['description'][:100]}...")
        
        print("\n" + "=" * 80)
        print(f"MODÈLES NON CENSURÉS GRATUITS ({len(uncensored_models)} trouvés)")
        print("=" * 80)
        
        for model in uncensored_models:
            print(f"\n🔓 {model['name']}")
            print(f"  ID: {model['id']}")
            print(f"  Contexte: {model['context_length']} tokens")
        
        # Enregistrer dans un fichier JSON
        output = {
            'free_models': free_models,
            'uncensored_models': uncensored_models,
            'total_free': len(free_models),
            'total_uncensored': len(uncensored_models)
        }
        
        with open('openrouter_free_models.json', 'w', encoding='utf-8') as f:
            json.dump(output, f, indent=2, ensure_ascii=False)
        
        print(f"\n✅ Résultats sauvegardés dans 'openrouter_free_models.json'")
        
        return output
        
    except requests.exceptions.RequestException as e:
        print(f"❌ Erreur lors de la récupération des modèles: {e}")
        return None

def test_model_interaction(model_id, api_key):
    """
    Fonction pour tester l'interaction avec un modèle
    """
    url = "https://openrouter.ai/api/v1/chat/completions"
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "HTTP-Referer": "http://localhost",
        "X-Title": "Test OpenRouter"
    }
    
    payload = {
        "model": model_id,
        "messages": [
            {"role": "user", "content": "Bonjour, peux-tu te présenter?"}
        ]
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        result = response.json()
        
        print(f"\n✅ Test réussi avec {model_id}")
        print(f"Réponse: {result['choices'][0]['message']['content']}")
        
    except requests.exceptions.RequestException as e:
        print(f"❌ Erreur avec {model_id}: {e}")

# Exécution principale
if __name__ == "__main__":
    print("🔍 Récupération des modèles gratuits OpenRouter...\n")
    results = get_openrouter_free_models()
    
    # Pour tester l'interaction, décommentez et ajoutez votre clé API:
    # API_KEY = "votre_cle_api_openrouter"
    # test_model_interaction("venice/uncensored:free", API_KEY)
