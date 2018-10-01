for file in tests/**/test-*.py
do
	echo ''
	echo $file:
	python3 -m unittest $file
done