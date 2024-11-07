import boto3
import streamlit as st
from langchain_community.retrievers import AmazonKnowledgeBasesRetriever
import json
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
for message in st.session_state.chat_history:
    with st.chat_message(message['role']):
        st.markdown(message['text'])
bedrockClient = boto3.client('bedrock-agent-runtime', 'us-west-2')
knowledge_base_id="TSPB72N2IC"
def getAnswers(questions):
    knowledgeBaseResponse = bedrockClient.retrieve_and_generate(
        input={'text': questions},
        retrieveAndGenerateConfiguration={
            'knowledgeBaseConfiguration': {
                'generationConfiguration': {
                    'inferenceConfig': { 
                        'textInferenceConfig': { 
                            'temperature': 0.75,
                            'topP': 1
                        }
                    }
                },
                'knowledgeBaseId': knowledge_base_id,
                'modelArn': 'arn:aws:bedrock:us-west-2::foundation-model/anthropic.claude-3-sonnet-20240229-v1:0',
                'retrievalConfiguration': {
                        'vectorSearchConfiguration': {
                            'numberOfResults': 100,
                            'overrideSearchType': 'HYBRID'
                        }
                    }
            },
            'type': 'KNOWLEDGE_BASE'
        })
    return knowledgeBaseResponse

def getreply(query):
    response = bedrockClient.retrieve(
    knowledgeBaseId=knowledge_base_id,
    retrievalQuery={'query':query},
    retrievalConfiguration={
                'vectorSearchConfiguration': {
                    'numberOfResults': 10, 
                    'overrideSearchType': 'HYBRID'
                }
            },
            nextToken='loan'
    )
    return response
def open_sidebar():
    st.session_state.sidebar = True
def letschat():
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    for message in st.session_state.chat_history:
        with st.chat_message(message['role']):
            st.markdown(message['text'])
    message_placeholder = st.empty()
    questions = st.chat_input('Enter you questions here...')
    if questions:
        with st.chat_message('user'):
            st.markdown(questions)
        st.session_state.chat_history.append({"role":'user', "text":questions})
        with st.spinner("Thinking..."):
         query=json.dumps(questions)
         response = getAnswers(questions)
        answer = response['output']['text']
        with st.chat_message('assistant'):
            with st.spinner("Thinking..."):
                st.markdown(answer)
        st.session_state.chat_history.append({"role":'assistant', "text": answer})
        with st.container():
            st.write("&nbsp;")
        if len(response['citations'][0]['retrievedReferences']) != 0:
            for idx, ref in enumerate(response['citations'][0]['retrievedReferences']):
                context = ref['content']['text']
                doc_url = ref['location']['s3Location']['uri']
                
                # Truncate context if it's too long
                context_display = context[:300] + "..." if len(context) > 200 else context
                
                # Display each reference with a bullet point
                st.markdown(f"""
                **Reference {idx + 1}:**
                - **Context used:** {context_display}
                - **Source Document:** [{doc_url}]({doc_url})
                """, unsafe_allow_html=True)
        else:
            st.markdown(f"<span style='color:red'>No Context</span>", unsafe_allow_html=True)