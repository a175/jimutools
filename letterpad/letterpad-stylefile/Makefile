LATEX=platex
DVI2PDF=dvipdfmx
STYLEFILE=letterpad

TEXFILE=sample

all: pdf
dvi: ${TEXFILE}.dvi
pdf: ${TEXFILE}.pdf

${TEXFILE}.dvi: ${TEXFILE}.tex ${STYLEFILE}.sty documentonform.sty
	${LATEX} ${TEXFILE} && ${LATEX} ${TEXFILE}
${TEXFILE}.pdf: ${TEXFILE}.dvi
	${DVI2PDF} -V 7 ${TEXFILE}.dvi
clean:
	rm -f ${TEXFILE}.dvi ${TEXFILE}.pdf ${TEXFILE}.log ${TEXFILE}.aux texput.log
