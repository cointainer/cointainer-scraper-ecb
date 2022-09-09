#!/bin/bash

LANGUAGE="en"
URL="https://www.ecb.europa.eu/euro/coins/comm/html/comm_%d.%s.html"

for i in {2004..2022}
do
	printf -v formatted_url $URL $i $LANGUAGE
	wget $formatted_url
done
