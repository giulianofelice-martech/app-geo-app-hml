@st.cache_data(ttl=300, show_spinner=False)
def listar_posts_webflow(w_url, w_user, w_pwd):
    """Busca posts para a aba de Auditoria e Revisor"""
    if not (w_url and w_pwd): return []
    
    headers = {
        "accept": "application/json",
        "authorization": f"Bearer {w_pwd.strip()}"
    }
    try:
        res = requests.get(w_url, headers=headers, timeout=15)
        if res.status_code == 200:
            items = res.json().get("items", [])
            lista_formatada = []
            for p in items:
                field_data = p.get('fieldData', {})
                titulo = field_data.get('name', 'Sem Título') 
                slug = field_data.get('slug', '')
                
                # AQUI ESTAVA O ERRO: Alterado para buscar o campo "texto" conforme seu print
                conteudo = field_data.get('texto', '') 
                
                lista_formatada.append({
                    "id": p.get("id"),
                    "title": {"rendered": titulo},
                    "content": {"rendered": conteudo},
                    "link": f"https://isaac.com.br/blog/{slug}" # Atualizado com o URL correto da sua Collection
                })
            return lista_formatada
    except Exception as e:
        print(f"Erro no parser do Webflow: {e}")
    return []

def publicar_webflow(titulo, conteudo_html, meta_dict, w_url, w_user, w_pwd):
    """Envia o rascunho (Draft) direto para o CMS do Webflow"""
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "authorization": f"Bearer {w_pwd.strip()}"
    }
    
    payload = {
        "isArchived": False,
        "isDraft": True, # Vai como rascunho
        "fieldData": {
            "name": titulo,
            "slug": slugify(titulo),
            "texto": conteudo_html, # AQUI ESTAVA O ERRO: Enviando para o campo "texto"
            "chamada": meta_dict.get("meta_description", "") # Mapeei a meta description para o seu campo "Chamada"
        }
    }
    
    try:
        response = requests.post(w_url, json=payload, headers=headers, timeout=30)
        return response
    except Exception as e:
        class ErrorResponse:
            status_code = 500
            text = f"Erro interno de conexão: {str(e)}"
            def json(self): return {}
        return ErrorResponse()
