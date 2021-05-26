FROM python:3.7

WORKDIR /app

COPY . /app

# For a python-slim version
# RUN apt-get update && apt-get install -y build-essential

RUN pip install -r requirements.txt

# Expose port
EXPOSE 8501

# run streamlit
CMD streamlit run app.py

# streamlit-specific commands for config
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8
RUN mkdir -p /root/.streamlit
RUN bash -c 'echo -e "\
[general]\n\
email = \"\"\n\
" > /root/.streamlit/credentials.toml'

RUN bash -c 'echo -e "\
[server]\n\
enableCORS = false\n\
" > /root/.streamlit/config.toml'