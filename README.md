# Create-Custom-Haar-Cascade
This script allows you to create custom haar cascades with ease.

# Before using it
This script is heavily influenced from the Youtube video https://www.youtube.com/watch?v=jG3bu0tjFbk by "sentdex". I learned creating a haar cascade from that video series itself. I highly recommend you to watch it before using this tool. This tool is just used to semi automate the processes sentdex did on the video series.

# Significance of the folders

<b>input_images</b> - This folder will contain the image(s) of the object you want to detect. Try keeping them small in size<br>
<b>input_resized_images</b> - This folder will contain the resized image(s) of the object you want to detect.<br>
<b>negatives</b> - This folder will contain the negative images that will be downloaded from image-net.org.<br>
<b>output_cascade</b> - This folder will contain the cascade that is created using opencv_traincascade command.<br>
<b>positives</b> - This folder stores the created positive samples. The positive samples are created using the images in input_resized_images and negatives using opencv_createsamples command.<br>
<b>uglies</b> - Put one of each ugly images here to remove them from negatives folder.

# Usage
> python createCustomHaarCascade.py
