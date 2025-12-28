# auto-editor
This is an python module which is responsible for editing together a video file based upon the relevant timestamps extracted using OCR from the video itselt

## How to Setup
To run the script you're going to need to configure a few variables. In order to run the script we need to simply follow the steps listed below:

1. Create an anaconda/miniconda environment called auto-editor and install all the requirements listed in the requirements.txt file. If you have not done this yet execute the following code inside this directory:
```
conda create --name auto-editor python=3.13.7
conda activate auto-editor
pip install -r requirements.txt
```

2. Ensure that the CONDA_SCRIPTS variable in run_script.bat file mentions the directory of where the Anaconda Scripts folder is located correctly.

3. If the .bat file does not work then simply open the anaconda terminal and use the following command in the repository.
```
conda activate auto-editor
python src/main.py [VIDEO_LINK_HERE]
```

## How to Run

1. Run the run_script.bat batch file.
2. Enter the url of the stream you are trying to download.
3. Wait for the video to be downloaded and processed.
4. Look through the csv filen for that video in the timestamps folder and verify the time intervals you want to extract from the video.
5. Have fun downloading and editting streams with the code!

OR

6. If you just wish to cut the video according to your own wishes you may create your own csv file with the name of the video in the timestamps folder and run the run_cutter.bat batch file to edit the video according to your specification.

##
