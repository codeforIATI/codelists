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

rm -rf out
mkdir -p out/clv2/xml out/clv3
cp -r codelists out/clv3/xml
for f in codelists/*; do
    python v3tov2.py $f > out/clv2/xml/`basename $f`;
done
python gen.py
python v2tov1.py
cp -r out/clv2/{codelists.json,codelists.xml,csv,json} out/clv3/

mv out/* docs/.vuepress/public
