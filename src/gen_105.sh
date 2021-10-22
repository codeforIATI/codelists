#!/bin/bash

if [ -d IATI-Codelists-105 ]; then
    cd IATI-Codelists-105 || exit 1
    git pull
    git checkout version-1.05
    cd ..
else
    git clone --branch version-1.05 https://github.com/IATI/IATI-Codelists.git IATI-Codelists-105
fi

echo ' *** Copy source XML to CLv3 ***'
mkdir -p docs/.vuepress/public/api/105/clv3/xml docs/.vuepress/public/api/105/clv2/xml
cp IATI-Codelists-105/xml/*.xml docs/.vuepress/public/api/105/clv3/xml

echo ' *** Convert CLv3 XML to CLv2 XML ***'
for f in IATI-Codelists-105/xml/*.xml; do
    python src/v3tov2.py $f > docs/.vuepress/public/api/105/clv2/xml/`basename $f`;
done
echo ' *** Generate CLv3 other formats (CSV; JSON; XLSX) ***'
python src/gen.py docs/.vuepress/public/api/105/clv3

echo ' *** Copy CLv3 other formats (CSV; JSON; XLSX) to CLv2 ***'
cp -r docs/.vuepress/public/api/105/clv3/{codelists.json,codelists.xml,csv,json,xlsx} docs/.vuepress/public/api/105/clv2/

echo ' *** Convert CLv2 all formats to CLv1 ***'
python src/v2tov1.py docs/.vuepress/public/api/105/clv2 docs/.vuepress/public/api/105/clv1

echo ' *** Copy Clv3 all formats to root ***'
cp -r docs/.vuepress/public/api/105/clv3/* docs/.vuepress/public/api/105
