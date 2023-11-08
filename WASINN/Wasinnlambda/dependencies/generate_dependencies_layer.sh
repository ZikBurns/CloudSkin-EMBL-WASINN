# Activate python 3.7 before executing
eval "$(conda shell.bash hook)"
conda activate python37

#Delete previous installation
rm -rf python site-packages* python.zip

# Install requirements.txt
pip install -r requirements.txt -t ./python/

# Show big files
du -hs python/* | sort -h

# Clean unnecessary files
cd python
find . -type d -name "tests" -exec rm -rf {} +
find . -type d -name "__pycache__" -exec rm -rf {} +
rm -rf ./{caffe2,wheel,wheel-*,boto*,aws*,pip,pip-*,pipenv}
rm -rf ./{*.egg-info,*.dist-info}
find . -name \*.pyc -delete
# NEEDED PACKAGES: matplotlib, yaml, packaging, pyparsing, kiwi, pandas, pytz, fastprogress,tqdm
# TO DELETE: typing*
#rm -rf {catalogue*,bs4*,srsly*,pydantic*,murmurhash*,click*,wasabi*,urllib3*,typer*,smart*,six*,setuptools*,preshed*,packaging*,[mM]arkup[sS]afe*,idna*,confection*,charset*,certifi*,tzdata*,tqdm*,spacy*,soupsieve*,requests*,pytz*,python-dateutil*,pyparsing*,pathy*,langcodes*,jinja2*,font[tT]ools*,contourpy*,spacy*,scipy*,*yaml*,nvidia*,numexpr*,matplotlib*,fastprogress*,[bB]ottleneck*,beautifulsoup4*,torchaudio*,dateutil*,kiwi*,jinja*,pandas*,plac*,pydantic*}
rm -rf {catalogue*,bs4*,srsly*,pydantic*,murmurhash*,click*,wasabi*,urllib3*,typer*,smart*,six*,preshed*,typing*,[mM]arkup[sS]afe*,idna*,confection*,charset*,certifi*,tzdata*,spacy*,soupsieve*,requests*,setuptools*,python-dateutil*,pathy*,langcodes*,jinja2*,font[tT]ools*,contourpy*,spacy*,nvidia*,numexpr*,[bB]ottleneck*,beautifulsoup4*,torchaudio*,dateutil*,jinja*,plac*,pydantic*}

# Zip up torch
zip -r9 torch.zip torch
rm -r torch

# Show result
du -hs * | sort -h

# Zip dependencies+model
cd ..
zip -r9 site-packages.zip python torchscript_model.pt

# Upload to S3
aws s3 cp site-packages.zip s3://off-sample/site-packages.zip

# Create new version of layer
aws lambda publish-layer-version \
    --no-paginate  \
    --no-cli-pager \
    --layer-name LayerTorchscript \
    --description "My dependencies layer" \
    --content S3Bucket=off-sample-s3,S3Key=site-packages.zip \
    --compatible-runtimes python3.7 \
    --license-info "MIT" \
    --region eu-north-1
    
#rm -rf python site-packages* python.zip
