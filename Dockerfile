FROM mambaorg/micromamba:latest

WORKDIR /home/mambauser

COPY --chown=$MAMBA_USER:$MAMBA_USER environment.yml /tmp/environment.yml

RUN micromamba install -y -n base -f /tmp/environment.yml && \
    micromamba clean --all --yes

COPY --chown=$MAMBA_USER:$MAMBA_USER src/opera_rtc_s1_browse/create_browse.py /home/mambauser/create_browse.py

ENTRYPOINT ["/usr/local/bin/_entrypoint.sh", "python", "-m", "create_browse"]
