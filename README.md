# Imaging_Processing

Conda Environment Setup
In order to continue with this image processing pipeline, you need to have a suitable environment with the necessary packages. For the Image Format Conversion as well as Registration, Crop and Merge, you can find image_processing.yml file above to create the environment. For running Cellpose, you can find cellpose.yml file above to create the environment. (Additional information for creating the environment with the yml files can be found: here)

Image Format Conversion
The TIF image format is usually the preferred format for preprocessing. Therefore if the raw images are in a different format, one would need to convert it to TIF. For example, if the images are IMS (imaris file format) they would need to be converted from IMS to TIF. Refer to this documentation for an in depth description of the IMS to TIF conversion pipeline.

Registration, Merge and Crop
Registration is a pre-processing step for cyclic imaging data. For example, if there is a dataset with 5 Cycles of imaging (Cycle 0, Cycle 1, Cycle 2, Cycle 3, Cycle 4), Cycle 0 will likely be the reference, where the rest of the cycles will be aligned onto the Cycle 0 images. It is important to visualize the X and Y shift so that one can filter out any egregiously shifted images or erroneously registered images. This step is an aid to do so holistically. Merging is concatenating all of the cycles together into one image. Cropping is for removing empty space that might result from X and Y shifts from registration as well as rotation. Using trigonometry, the empty space is calculated with the transformation matrix numbers, and the dimensions are applied in the code to crop out the appropriate amount of space. The jupyter notebook for this step of the pipeline is here. Refer to this documentation for a description of how to get started with the pipeline.

Cell Segmentation (Using Cellpose)
Segmentation comes after Registration, Merge and Crop (if registration was not necessary, this step comes right after ims to tif conversion) which is a necessary step to make single cell labels to extract features from each of the cells from each image. Typically, the soma and nuclei are segmented for each image using Cellpose 2. (Refer to this documentation for an in depth description of the segmentation pipeline)
