if [ -d ./pdf ]; then
    :
else
    mkdir -p pdf
fi

cd html
for h in *.html;
do
    wkhtmltopdf -q "$h" "../pdf/`echo "$h"|sed "s/\.html/\.pdf/"`"
done
