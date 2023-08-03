#!/bin/bash

COURCEID=125385

MEIBO=meibo.csv
PARTICIPANTS=courseid_${COURCEID}_participants.csv

OUT_CLASSLIST=classlist.lst
OUT_IDNAME=id-name.txt
OUT_SED_ID=id-name.sed
OUT_NAMELIST=namelist.txt

cat $MEIBO | cut -d, -f3-5|sed 's/ /,/' >  $OUT_IDNAME
cat $OUT_IDNAME | sed 's/,/.,\/,/' |sed 's/^/s\/,./'|sed 's/$/,\//' > $OUT_SED_ID
cat $PARTICIPANTS|egrep '[a-z][0-9]*[a-z]$'|awk -F, '{print $3","$3","$2","$1}'| sed -f $OUT_SED_ID > $OUT_NAMELIST


echo "Check bad lines..."
cat $OUT_NAMELIST|sed 's/　/,/'|awk -F, '{if($2!=$6){print($0)} if($3!=$7){print($0)}}'
echo "Done."
echo ""
echo "The number of lines:"
cat $OUT_NAMELIST| wc -l

cat $OUT_NAMELIST| awk -F, '{print $1","$3","$4",,,,,,"$1",,0"}' > $OUT_CLASSLIST

echo "The following are in "$OUT_CLASSLIST":"
cat classlist.lst|cut -d, -f1,2,3,9,11
