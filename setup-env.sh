mamba create -n KG-S2S python=3.11 -y
mamba activate KG-S2S
pip install -r requirements.txt

pip download --no-binary :all: --no-deps transformers==4.16.2
tar zxf transformers-*.tar.gz; rm transformers-*.tar.gz
pip install --editable transformers-*
