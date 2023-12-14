mamba create -n KG-S2S python=3.11 -y; mamba activate KG-S2S
pip install -r requirements.txt

rm -rf transformers-*; pip download --no-binary :all: --no-deps transformers==4.16.2
rm -rf pytorch-lightning-*; pip download --no-binary :all: --no-deps pytorch-lightning==1.9.5
tar zxf transformers-*.tar.gz; rm transformers-*.tar.gz; pip install --editable transformers-*
tar zxf pytorch-lightning-*.tar.gz; rm pytorch-lightning-*.tar.gz; pip install --editable pytorch-lightning-*
