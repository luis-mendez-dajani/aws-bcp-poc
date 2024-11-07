import streamlit as st
import boto3
import os
from QandA import letschat
import json
s3 = boto3.client('s3')
bucket_name="kb-bcp-poc"
def upload_to_s3(file, bucket_name):
    try:
        object_name = os.path.basename(file.name)
        s3.upload_fileobj(file, bucket_name, object_name)
        st.success(f"File '{object_name}' successfully uploaded ")
        return
    except Exception as e:
        st.error(f"Error uploading file: {e}")
def get_file():
    uploaded_files = st.file_uploader("Choose files or drag them here", type=["txt", "pdf", "jpg", "png"], accept_multiple_files=True)
    if uploaded_files is not None:
        for uploaded_file in uploaded_files:
            upload_to_s3(uploaded_file, bucket_name)
if __name__ == "__main__":
    get_file()
    letschat()