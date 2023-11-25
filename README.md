# **Graph of Thoughs Generator**

## Configurations

### Prerequisites and System Requirements
- You must have [graphviz](https://graphviz.org) framework inside your system.
    - Ubuntu:
    ```zsh
    sudo apt-get install graphviz
    ```
    - MacOS:
    ```zsh
    brew install graphviz
    ```

<p align="left">
 <a href=""><img src="https://img.shields.io/badge/python-3.9-aff.svg"></a>
 <a href=""><img src="https://img.shields.io/badge/graphviz-fff.svg"></a>
</p>

### Run locally
- Create conda environment, note that python version should be <span style="color:#9BB8ED;">Python 3.9</span>
```
conda create --name graph-of-thought-genor python=3.9
conda activate graph-of-thought-genor
```

- Install required packages

```
pip install -r requirements.txt --no-cache-dir
```