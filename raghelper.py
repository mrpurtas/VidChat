from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceInferenceAPIEmbeddings


import os
from dotenv import load_dotenv

load_dotenv()
my_key_openai = os.getenv("OPENAI_API_KEY")
my_key_google = os.getenv("GOOGLE_API_KEY")
my_key_hf = os.getenv("HUGGING_FACE_ACCESS_TOKEN")


llm_gemini = ChatGoogleGenerativeAI(google_api_key=my_key_google, model = "gemini-pro")

embeddings = OpenAIEmbeddings(api_key=my_key_openai)







# embeddings = HuggingFaceInferenceAPIEmbeddings(
#     api_key=my_key_hf,
#     model_name="sentence-transformers/all-MiniLM-16-v2"
# )


#1 Dil modeliyle konusma
def ask_gemini(prompt):
    
    AI_Response = llm_gemini.invoke(prompt)

    return AI_Response


#2 Bellek genişletme süreci - video transkript metinleri

def rag_with_video_transricpt(transcript_docs, prompt):

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size = 1000,
        chunk_overlap = 0,
        length_function = len
    )

    splitted_documents = text_splitter.split_documents(transcript_docs)

    vectorstore = FAISS.from_documents(splitted_documents, embeddings)

    retriever = vectorstore.as_retriever()

    relevant_documents = retriever.get_relevant_documents(prompt)

    context_data = ""

    for document in relevant_documents:
        context_data = context_data + " " +document.page_content

    # final_prompt = f"""Şöyle bir sorun var: {prompt}
    # Bu soruyu yanıtlamak için elimizde şu bilgiler var: {context_data}.
    # Bu sorunun yanıtını vermek için yalnızca sana burada verdiğim eldeki bilgileri kullan. Bunların dışına asla çıkma.
    # """
        
    # final_prompt = f"""
    # Soru: {prompt}
    # Mevcut bilgiler: Videonun içeriğinden çıkarılmış ve sorunun bağlamını oluşturan bilgiler: {context_data}.
    # Yanıtı formüle ederken, soruya yanıt olarak yalnızca bu mevcut bilgiler kullanılacak ve verilen bilgilerin ötesine geçilmeyecek. Bu şekilde, videonun içeriğine spesifik ve doğru bilgilerle yanıt verilmesi sağlanacaktır.
    # """
        
    final_prompt = f"""
    Soru: '{prompt}'
    Kaynak bilgi: Video içeriğinin analiz edilerek özetlenmiş hali: {context_data}.
    Bu bilgi, sorulan soruya spesifik ve doğrulanabilir cevaplar sağlamak için kullanılacaktır. Video içeriğinden elde edilen bu bilgiler dışında herhangi bir spekülasyona veya tahmine yer verilmeyecek. Soruya, video içeriğine doğrudan bağlantılı ve onunla sınırlı kalarak yanıt verilecek. Verilen cevap, içeriğin doğruluğunu yansıtacak ve kullanıcıya videonun içeriğini net bir şekilde anlaması için yardımcı olacak.
    """

    AI_Response = ask_gemini(final_prompt)

    return AI_Response, relevant_documents


"""Bu Python kodu, Google ve OpenAI'nin dil modellerini kullanarak, bir YouTube video transkriptinden alınan bilgilere dayanarak kullanıcı sorularına yanıt veren bir sistem oluşturur. ChatGoogleGenerativeAI sınıfını kullanarak Google'ın dil modeli ile etkileşime geçer, OpenAIEmbeddings ile metinler için gömülü vektörler oluşturur ve FAISS ile bu gömülü vektörleri kullanarak en alakalı transkript bölümlerini alır. RecursiveCharacterTextSplitter transkript metnini parçalar ve sonunda ask_gemini fonksiyonu ile oluşturulan son prompt'u Google dil modeline sorarak ve alınan yanıtı döndürerek kullanıcıya video içeriği hakkında bilgi verir."""