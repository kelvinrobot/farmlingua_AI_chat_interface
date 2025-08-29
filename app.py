import streamlit as st
import requests

API_URL = "https://remostart-milestone-one-farmlingua-ai.hf.space/ask"

st.set_page_config(page_title= ' FarmLingua AI', page_icon= 'FARMAI',layout= 'centered')

st.title('FarmLingua AI Assistant')
st.write('Ask me anything about farming in nigeria NG')

with st.form(key = 'query_form'):
     user_query = st.text_area('User Question:', placeholder='example: how can i improve rice yield in northern nigeria?')
     submit_button = st.form_submit_button('Ask')

if submit_button and user_query.strip():
    with st.spinner('Thinking...') :
        try:
            response = requests.post(
                API_URL,
                headers = {'Conten-Type': 'application/json'},
                json = {'query': user_query},
                timeout = 1000
            )

            if response.status_code == 200:
              data = response.json()
              answer = data.get('response') or data.get('answer') or 'No response.'
              st.success('### Answer:')
              st.write(answer)
            else:
              st.error(f'Error {response.status_code}: {response.text}')  
        except Exception as e:
            st.error(f"An error occurred: {e}")