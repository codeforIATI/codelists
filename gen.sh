#!/bin/bash

rm -rf codelists
if [ -d IATI-Codelists-NonEmbedded ]; then
    cd IATI-Codelists-NonEmbedded || exit 1
    git pull
    git checkout master
else
    git clone https://github.com/codeforIATI/IATI-Codelists-NonEmbedded.git
    cd IATI-Codelists-NonEmbedded || exit 1
    git checkout master
fi
cd .. || exit 1

codelists=("AidType-category" "AidType" "CollaborationType" "Country" "CRSChannelCode" "Currency" "EarmarkingCategory" "FileFormat" "FinanceType-category" "FinanceType" "FlowType" "Language" "LocationType-category" "LocationType" "OrganisationRegistrationAgency" "PolicyMarker" "PolicySignificance" "Region" "Sector" "SectorCategory" "UNSDG-Goals" "UNSDG-Targets")
mkdir codelists
for f in ${codelists[*]}; do
    cp IATI-Codelists-NonEmbedded/xml/$f.xml codelists
done

rm -rf docs
cp -r static docs

rm -rf docs/.vuepress/public/clv*
mkdir -p docs/.vuepress/public/clv2/xml docs/.vuepress/public/clv3
cp -r codelists docs/.vuepress/public/clv3/xml
for f in codelists/*; do
    python v3tov2.py $f > docs/.vuepress/public/clv2/xml/`basename $f`;
done
python gen.py docs/.vuepress/public/clv2
python v2tov1.py docs/.vuepress/public/clv2 docs/.vuepress/public/clv1
cp -r docs/.vuepress/public/clv2/{codelists.json,codelists.xml,csv,json} docs/.vuepress/public/clv3/
