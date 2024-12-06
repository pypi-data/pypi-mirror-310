# Colab Load #

## What is this? ##
Library to download .ipynb from google colab

## Quick Guide ##
	pip install colab-load
One url:

    from colab_load.load import StartLoad
    
    s = StartLoad(logs=True)
    s.load_file_single("https://colab.research.google.com/drive/1QD1TM2TroOEqqtTURpk5sVOmGLQeREv_?usp=sharing", save_dir="file")

Lots of url:

	from colab_load.load import StartLoad
    
	urls=["https://colab.research.google.com/drive/1QD1TM2TroOEqqtTURpk5sVOmGLQeREv_?usp=sharing", "https://colab.research.google.com/drive/1QD1TM2TroOEqqtTURpk5sVOmGLQeREv_?usp=sharing"]
	s = StartLoad(logs=True)
	s.load_file_all(urls, save_dir="file", count=2)
