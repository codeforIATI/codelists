#!/bin/bash

rm -rf codelists
if [ -d IATI-Codelists-NonEmbedded ]; then
    cd IATI-Codelists-NonEmbedded || exit 1
    git pull
    git checkout master
    cd ..
else
    git clone --branch master https://github.com/codeforIATI/IATI-Codelists-NonEmbedded.git
fi

codelists=("AidType-category" "AidType" "CollaborationType" "Country" "CRSChannelCode" "Currency" "EarmarkingCategory" "FileFormat" "FinanceType-category" "FinanceType" "FlowType" "Language" "LocationType-category" "LocationType" "OrganisationRegistrationAgency" "PolicyMarker" "PolicySignificance" "Region" "Sector" "SectorCategory" "UNSDG-Goals" "UNSDG-Targets")
mkdir codelists
for f in ${codelists[*]}; do
    cp IATI-Codelists-NonEmbedded/xml/$f.xml codelists
done

rm -rf docs
cp -r static docs

mkdir -p docs/.vuepress/public/api/clv2/xml docs/.vuepress/public/api/clv3
cp -r codelists docs/.vuepress/public/api/clv3/xml
for f in codelists/*; do
    python src/v3tov2.py $f > docs/.vuepress/public/api/clv2/xml/`basename $f`;
done
python src/gen.py docs/.vuepress/public/api/clv2
python src/v2tov1.py docs/.vuepress/public/api/clv2 docs/.vuepress/public/api/clv1
cp -r docs/.vuepress/public/api/clv2/{codelists.json,codelists.xml,csv,json} docs/.vuepress/public/api/clv3/

cp -r docs/.vuepress/public/api/clv3/* docs/.vuepress/public/api
