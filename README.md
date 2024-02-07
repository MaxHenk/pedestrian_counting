# Develping an advanced machine learning pipeline for pedestrian counting from video sources.
## Performance comparison using different video sources and varying model parameters.
This GitHub repository presents the results to my Master's thesis project on pedestrian counting using video sources. It contains the scripts used for the detection of pedestrians on videos, the script used to perform the tracking and the scripts used to extract the origin destination counts.

### Data
The data used for this study was extracted using the [youtube-dl](https://github.com/ytdl-org/youtube-dl). The videos used are directly taken from the official City of Lausanne [livestream](https://www.youtube.com/watch?v=y3sMI1HtZfE). The Bessières bridge is shown in this video.

### Repository structure

The detections folder contains the main script launched on the Jetson Nano Developer Kit along with some requirements for use.

The tracking folder contains the main script along with some instructions for use.

The counting folder contains the scripts used for producing some of the visualisations and counts. Along with some requirements.


### Author
This project was done for a Master's thesis at the University of Lausanne by Max Henking under the supervision of Christian Kaiser.
