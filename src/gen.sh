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

if [ -d Unofficial-Codelists ]; then
    cd Unofficial-Codelists || exit 1
    git pull
    git checkout master
    cd ..
else
    git clone --branch master https://github.com/codeforIATI/Unofficial-Codelists.git
fi

codelists=("AidType-category" "AidType" "CollaborationType" "Country" "CRSChannelCode" "Currency" "EarmarkingCategory" "FileFormat" "FinanceType-category" "FinanceType" "FlowType" "Language" "LocationType-category" "LocationType" "OrganisationRegistrationAgency" "PolicyMarker" "PolicySignificance" "Region" "Sector" "SectorCategory" "UNSDG-Goals" "UNSDG-Targets")
mkdir codelists
for f in ${codelists[*]}; do
    cp IATI-Codelists-NonEmbedded/xml/$f.xml codelists
done
cp Unofficial-Codelists/xml/*.xml codelists

rm -rf docs
cp -r static docs

echo ' *** Copy source XML to CLv3 ***'
mkdir -p docs/.vuepress/public/api/clv2/xml docs/.vuepress/public/api/clv3
cp -r codelists docs/.vuepress/public/api/clv3/xml

echo ' *** Convert CLv3 XML to CLv2 XML ***'
for f in codelists/*; do
    python src/v3tov2.py $f > docs/.vuepress/public/api/clv2/xml/`basename $f`;
done
echo ' *** Generate CLv3 other formats (CSV; JSON; XLSX) ***'
python src/gen.py docs/.vuepress/public/api/clv3

echo ' *** Copy CLv3 other formats (CSV; JSON; XLSX) to CLv2 ***'
cp -r docs/.vuepress/public/api/clv3/{codelists.json,codelists.xml,csv,json,xlsx} docs/.vuepress/public/api/clv2/

echo ' *** Convert CLv2 all formats to CLv1 ***'
python src/v2tov1.py docs/.vuepress/public/api/clv2 docs/.vuepress/public/api/clv1

echo ' *** Copy Clv3 all formats to root ***'
cp -r docs/.vuepress/public/api/clv3/* docs/.vuepress/public/api
