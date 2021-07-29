#!/usr/bin/env bash

TARGET="${1}"
WHITELIST="
	pitch.tex
	article.tex
	poster.tex
	slides.tex
	"

if [[ "$TARGET" = "all" ]] || [[ "$TARGET" == "" ]]; then
	for ITER_TARGET in *.tex; do
		if [[ $WHITELIST =~ (^|[[:space:]])$ITER_TARGET($|[[:space:]]) ]];then
			ITER_TARGET=${ITER_TARGET%".tex"}
			./compile.sh "${ITER_TARGET}"
		fi
	done
else
	pdflatex -shell-escape "${TARGET}.tex" || { echo "Initial pdflatex failed"; exit $ERRCODE; }

#  Only execute pythontex if indicated in latex file
	first_line=$(head -n 1 "${TARGET}.tex")
  if [ "${first_line}" = "% pythontex" ]; then
    	pythontex "$(basename "${TARGET}").tex" || { echo "PythonTeX failed"; exit $ERRCODE; }
#    	pythontex "${TARGET}.tex" || { echo "PythonTeX failed"; exit $ERRCODE; }
	    pdflatex -shell-escape "${TARGET}.tex" || { echo "pdflatex failed after PythonTeX"; exit $ERRCODE; }
  fi

	bibtex "$(basename "${TARGET}")" || { echo "bibtex failed"; exit $ERRCODE; }
	pdflatex -shell-escape "${TARGET}.tex" || { echo "pdflatex failed after bibtex"; exit $ERRCODE; }
	pdflatex -shell-escape "${TARGET}.tex"
	if [ ! -d logs ]; then
	  mkdir logs
	fi

	for CLEAN_TARGET in "*.aux" "*.log" "*.out" "*.bbl" "*.pytxcode" "*blx.bib" "*.blg" "*.run.xml" "*.bcf"; do
	  mv $CLEAN_TARGET logs/
  done

  python scripts_/upload.py "$(pwd)/$(basename "${TARGET}.pdf")"
fi
