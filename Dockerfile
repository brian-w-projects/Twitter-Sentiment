FROM continuumio/miniconda3:latest

WORKDIR /app

COPY . ./

RUN chmod +x boot.sh
RUN conda env create -f environment.yml

RUN echo "source activate Twitter" > ~/.bashrc
ENV PATH /opt/conda/envs/Twitter/bin:$PATH

EXPOSE 5000

ENTRYPOINT ["./boot.sh"]
