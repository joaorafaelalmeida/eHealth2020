run:
	cd src && \
	python3 main.py -ds ${ds}

evalute-D:
	cd Evaluator && \
	python3 codiespD_P_evaluation.py -g ../Datasets/${ds}/${ds}D.tsv -p ../Submissions/testD/${m}_testD.tsv -c ../Vocabularies/codiesp-D_codes.tsv

evalute-P:
	cd Evaluator && \
	python3 codiespD_P_evaluation.py -g ../Datasets/${ds}/${ds}P.tsv -p ../Submissions/testP/${m}_testP.tsv -c ../Vocabularies/codiesp-P_codes.tsv

evalute-X:
	cd Evaluator && \
	python3 codiespX_evaluation.py -g ../Datasets/${ds}/${ds}X.tsv -p ../Submissions/testX/${m}_testX.tsv -cD ../Vocabularies/codiesp-D_codes.tsv -cP ../Vocabularies/codiesp-P_codes.tsv

evalute:
	make evalute-D ds=${ds} m=${m} evalute-P ds=${ds} m=${m} evalute-X ds=${ds} m=${m}

#########################
# Datasets
#########################
train:
	make run ds=train \
	evalute ds=train m=rule-based

dev:
	make run ds=dev \
	evalute ds=dev m=rule-based

test:
	make run ds=test