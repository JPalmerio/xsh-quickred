This file contains an overview of the structure and content of your download request from the ESO Science Archive.


For every downloaded dataset, files are listed below with the following structure:

dataset_name
        - archive_file_name (technical name, as saved on disk)	original_file_name (user name, contains relevant information) category size


Please note that, depending on your operating system and method of download, at download time the colons (:) in the archive_file_name as listed below may be replaced by underscores (_).


In order to rename the files on disk from the technical archive_file_name to the more meaningful original_file_name, run the following shell command:
    cat THIS_FILE | awk '$2 ~ /^ADP/ {print "test -f",$2,"&& mv",$2,$3}' | sh


In case you have requested cutouts, the file name on disk contains the TARGET name that you have provided as input. To order files by it when listing them, run the following shell command:
    cat THIS_FILE | awk '$2 ~ /^ADP/ {print $2}' | sort -t_ -k3,3


Your feedback regarding the data quality of the downloaded data products is greatly appreciated. Please contact the ESO Archive Science Group via https://support.eso.org/ , subject: Phase 3 ... thanks!
XSHOO.2024-02-19T05:14:05.485 
	- XSHOO.2024-02-19T05:14:05.485		Raw data for which no processed data is available	2438747
XSHOO.2024-02-19T05:14:13.809 
	- XSHOO.2024-02-19T05:14:13.809		Raw data for which no processed data is available	10284425
XSHOO.2024-02-19T04:38:37.850 
	- XSHOO.2024-02-19T04:38:37.850		Raw data for which no processed data is available	10282409
XSHOO.2024-02-19T04:50:09.741 
	- XSHOO.2024-02-19T04:50:09.741		Raw data for which no processed data is available	10304707
XSHOO.2024-02-19T04:50:06.565 
	- XSHOO.2024-02-19T04:50:06.565		Raw data for which no processed data is available	3766007
XSHOO.2024-02-19T05:00:17.832 
	- XSHOO.2024-02-19T05:00:17.832		Raw data for which no processed data is available	10283149
XSHOO.2024-02-19T04:50:01.364 
	- XSHOO.2024-02-19T04:50:01.364		Raw data for which no processed data is available	2489653
XSHOO.2024-02-19T05:35:51.795 
	- XSHOO.2024-02-19T05:35:51.795		Raw data for which no processed data is available	10265489
XSHOO.2024-02-19T05:35:48.624 
	- XSHOO.2024-02-19T05:35:48.624		Raw data for which no processed data is available	3720727
XSHOO.2024-02-19T05:14:10.675 
	- XSHOO.2024-02-19T05:14:10.675		Raw data for which no processed data is available	3745143
XSHOO.2024-02-19T04:28:26.616 
	- XSHOO.2024-02-19T04:28:26.616		Raw data for which no processed data is available	3780127
XSHOO.2024-02-19T04:28:29.757 
	- XSHOO.2024-02-19T04:28:29.757		Raw data for which no processed data is available	10271529
XSHOO.2024-02-19T05:45:59.892 
	- XSHOO.2024-02-19T05:45:59.892		Raw data for which no processed data is available	10258007
XSHOO.2024-02-19T05:35:43.424 
	- XSHOO.2024-02-19T05:35:43.424		Raw data for which no processed data is available	2333493
XSHOO.2024-02-19T05:24:21.902 
	- XSHOO.2024-02-19T05:24:21.902		Raw data for which no processed data is available	10264549
XSHOO.2024-02-19T04:28:21.466 
	- XSHOO.2024-02-19T04:28:21.466		Raw data for which no processed data is available	2537469
