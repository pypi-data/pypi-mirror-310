# Med-Imagetools: Transparent and Reproducible Medical Image Processing Pipelines in Python

[![main-ci](https://github.com/bhklab/med-imagetools/actions/workflows/main-ci.yml/badge.svg)](https://github.com/bhklab/med-imagetools/actions/workflows/main-ci.yml)
![GitHub repo size](https://img.shields.io/github/repo-size/bhklab/med-imagetools)
![GitHub contributors](https://img.shields.io/github/contributors/bhklab/med-imagetools)
![GitHub stars](https://img.shields.io/github/stars/bhklab/med-imagetools?style=social)
![GitHub forks](https://img.shields.io/github/forks/bhklab/med-imagetools?style=social)

## Latest Updates (v0.4.4) - July 27th, 2022

New features include:

* AutoPipeline CLI
* `nnunet` nnU-Net compatibility mode
* Built-in train/test split for both normal/nnU-Net modes
* `random_state` for reproducible seeds
* Region of interest (ROI) yaml dictionary intake for RTSTRUCT processing
* Markdown report output post-processing
* `continue_processing` flag to continue autopipeline
* `dry_run` flag to only crawl the dataset

Med-Imagetools, a python package offers the perfect tool to transform messy medical dataset folders to deep learning ready format in few lines of code. It not only processes DICOMs consisting of different modalities (like CT, PET, RTDOSE and RTSTRUCTS), it also transforms them into deep learning ready subject based format taking the dependencies of these modalities into consideration.  

## Introduction

A medical dataset, typically contains multiple different types of scans for a single patient in a single study. As seen in the figure below, the different scans containing DICOM of different modalities are interdependent on each other. For making effective machine learning models, one ought to take different modalities into account.

<img src="images/graph.png" align="center" width="480" ><figcaption>Fig.1 - Different network topology for different studies of different patients</figcaption></a>  

Med-Imagetools is a unique tool, which focuses on subject based Machine learning. It crawls the dataset and makes a network by connecting different modalities present in the dataset. Based on the user defined modalities, med-imagetools, queries the graph and process the queried raw DICOMS. The processed DICOMS are saved as nrrds, which med-imagetools converts to torchio subject dataset and eventually torch dataloader for ML pipeline.

<img src="images/autopipeline.png" align="center" width="500"><figcaption>Fig.2 - Med-Imagetools AutoPipeline diagram</figcaption></a>  

## Installing med-imagetools

```sh
pip install med-imagetools
```

### (recommended) Create new conda virtual environment

``` sh
conda create -n mit
conda activate mit
pip install med-imagetools
```

### (optional) Install in development mode

``` sh
conda create -n mit
conda activate mit
pip install -e git+https://github.com/bhklab/med-imagetools.git
```

This will install the package in editable mode, so that the installed package will update when the code is changed.

## Getting Started

Med-Imagetools takes two step approch to turn messy medical raw dataset to ML ready dataset.  

1. ***Autopipeline***: Crawls the raw dataset, forms a network and performs graph query, based on the user defined modalities. The relevant DICOMS, get processed and saved as nrrds

    ``` sh
    autopipeline\
      [INPUT_DIRECTORY] \
      [OUTPUT_DIRECTORY] \
      --modalities [str: CT,RTSTRUCT,PT] \
      --spacing [Tuple: (int,int,int)]\
      --n_jobs [int]\
      --visualize [flag]\
      --nnunet [flag]\
      --train_size [float]\
      --random_state [int]\
      --roi_yaml_path [str]\
      --continue_processing [flag]\
      --dry_run [flag]
    ```

2. ***class Dataset***: This class converts processed nrrds to torchio subjects, which can be easily converted to torch dataset

    ```py
    from imgtools.io import Dataset
    
    subjects = Dataset.load_from_nrrd(output_directory, ignore_multi=True)
    data_set = tio.SubjectsDataset(subjects)
    data_loader = torch.utils.data.DataLoader(data_set, batch_size=4, shuffle=True, num_workers=4)
    ```


### Contributors

Thanks to the following people who have contributed to this project:

* [@mkazmier](https://github.com/mkazmier)
* [@skim2257](https://github.com/skim2257)
* [@fishingguy456](https://github.com/fishingguy456)
* [@Vishwesh4](https://github.com/Vishwesh4)
* [@mnakano](https://github.com/mnakano)

## Contact

If you have any questions/concerns, you can reach the main development team at sejin.kim@uhnresearch.ca or open an issue on our [GitHub repository](https://github.com/bhklab/med-imagetools)

## License

This project uses the following license: [Apache License 2.0](http://www.apache.org/licenses/)
