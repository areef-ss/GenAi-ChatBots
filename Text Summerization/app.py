import validators,streamlit as st
from langchain.prompts import PromptTemplate
from langchain_groq import ChatGroq
from langchain.chains.summarize import load_summarize_chain
from langchain_community.document_loaders import YoutubeLoader,UnstructuredURLLoader

## streamlit App

st.set_page_config(page_title="Langchain Text Summarizer from Youtube or web url")
st.title("Langchain Text Summarizer from Youtube or web url")
st.subheader('Summarize URL')



## Get the groq API key and url to be summarized
groq_api_key=""
with st.sidebar:
    groq_api_key=st.text_input("Enter your Groq API key",value="",type="password")

if groq_api_key:
    llm=ChatGroq(groq_api_key=groq_api_key,model_name="llama3-8b-8192",streaming=True)


prompt_template='''
Provide a summary of the following content in 300 words
content:{text}
'''
prompt=PromptTemplate(input_variables=['text'],template=prompt_template)
url=st.text_input("Enter the URL to be summarized",label_visibility="collapsed")

if st.button("Summarize the content from yt or website"):
    if not groq_api_key.strip() or not url.strip():
        st.error("Please enter the groq api key and the url")
    elif not validators.url(url):
        st.error("Please enter a valid url")
    else:
        try:
            with st.spinner("Summarizing the content from yt or website"):
                ##loaing the websie or yt url
                if "youtube.com" in url:
                    loader=YoutubeLoader.from_youtube_url(url,add_transcript=True)
                else:
                    loader=UnstructuredURLLoader(urls=[url],ssl_verify=False,
                                                 header={"user-Agent:""Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36 Edg/109.0.1518.61"})
                docs=loader.load()


                ## Chain fro summarization
                chain=load_summarize_chain(llm,chain_type="stuff",prompt=prompt)
                output_summary=chain.run(docs)
                st.success(output_summary)
        except Exception as e:
            st.exception(F"Exception:{e}")
