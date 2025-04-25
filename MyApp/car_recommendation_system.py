# Importar as bibliotecas
import streamlit as st
import fitz
from groq import Groq

# Configurar chave da Groq (substitua pela sua chave válida)
GROQ_API_KEY = "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"
client = Groq(api_key=GROQ_API_KEY)

# Função para extrair texto de arquivos PDF
def extract_files(uploader):
    text = ""
    for pdf in uploader:
        try:
            with fitz.open(stream=pdf.read(), filetype="pdf") as doc:
                for page in doc:
                    text += page.get_text("text") + "\n"
        except Exception as e:
            st.error(f"Erro ao processar o PDF: {e}")
    return text

# Motor de inferência para o sistema inteligente
def chat_with_groq(prompt, context):
    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "Você é um assistente especializado em vendas de carros. Responda com base nas informações fornecidas no documento e ofereça respostas claras e úteis sobre modelos, preços, características e disponibilidade."},
                {"role": "user", "content": f"Contexto do documento:\n{context}\n\nPergunta: {prompt}"}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Erro ao processar a pergunta: {e}"

# Interface do Streamlit
def main():
    st.title("Sistema Inteligente de Recomendações de Carros 2025")
    
    # Adicionar uma imagem temática na sidebar
    with st.sidebar:
        st.header("Upload de Recomendações")
        uploader = st.file_uploader("Carregue as recomendações de carros (PDF)", type="pdf", accept_multiple_files=True)
    
    # Processar o PDF carregado
    if uploader:
        with st.spinner("Extraindo informações do arquivo..."):
            text = extract_files(uploader)
            st.session_state["document-text"] = text
            st.success("Arquivo carregado com sucesso!")
    
    # Campo para perguntas do usuário
    user_input = st.text_input("Digite sua pergunta sobre os carros (ex.: 'Qual o preço do Honda Civic 2025?' ou 'Quais SUVs estão disponíveis?')")
    
    # Processar a pergunta e exibir a resposta
    if user_input and "document-text" in st.session_state:
        with st.spinner("Processando sua pergunta..."):
            response = chat_with_groq(user_input, st.session_state["document-text"])
            st.write("**Resposta:**")
            st.write(response)

if __name__ == "__main__":
    main()