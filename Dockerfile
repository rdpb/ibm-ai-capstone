FROM continuumio/miniconda3

LABEL maintainer="Rafael Barbosa"
WORKDIR /app

# Create the environment:
COPY environment.yml .
RUN conda env create -f environment.yml

# Use environment:
SHELL ["conda", "run", "-n", "ibm-ai", "/bin/bash", "-c"]


# Make sure the environment is activated:
RUN echo "Make sure flask is installed:"
RUN python -c "import flask"

# The code to run when container is started:
COPY app.py .
ENTRYPOINT ["conda", "run", "-n", "ibm-ai", "python", "app.py"]


#COPY . /app/

#EXPOSE 8080

#CMD ["python", "app.py"]     