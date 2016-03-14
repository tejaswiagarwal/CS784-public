Each file (GoldenData.tsv, setI and setJ) has the following format separated by tab spaces:
Product_ID Product_Name  Predicted_or_Expected_Brand_Name 

To run the script: 

First run extract.py: 

python extract.py $dictionary_file $file_to_be_classified



Then on the results from extract.py run the following to compute precision and recall:

python precision_recall.py $extracted_brand_names_file $golden_data_file


