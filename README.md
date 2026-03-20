[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo..svg)](https://doi.org/10.5281/zenodo.)
![Visitors Badge](https://visitor-badge.laobi.icu/badge?page_id=RuiGao9/spatial-cimis-)<br>

# A Python and Shell-based Toolkit for Spatial CIMIS Data Acquisition and Geospatial Preprocessing
## Purpose
This repository is designed to bridge the gap between raw data acquisition and research-ready geospatial products.<br> Spatial [CIMIS](https://cimis.water.ca.gov/Default.aspx) (California Irrigation Management Information System) provides invaluable daily ETo and solar radiation data, yet the raw ASCII formats often lack spatial reference metadata required for modern GIS and remote sensing workflows. This toolkit provides a reproducible, two-step pipeline to automate the retrieval and standardization of these datasets, supporting further research purposes.

## Two-Step Workflow
### Step 1: Automated Data Acquisition (Ubuntu on Windows 11 / WSL2)
We use `wget` to recursively retrieve the daily ASCII grids. This is most efficient when executed in an Ubuntu terminal (via WSL2 on Windows 11).<br>
```bash
# Replace [LOCAL_PATH] with your target directory, e.g., /mnt/d/CIMIS_Data/
wget -r -np -nH --cut-dirs=1 --reject="index.html*" \
     -c -P "[LOCAL_PATH]" \
     https://spatialcimis.water.ca.gov/cimis/2005/
```
Note: `-c` flag ensures the download can resume if interrupted. The `2005` in the URL can be replaced with the specific year you require.

### Step 2: Geospatial Standardization (Python with ArcGIS Pro API)


## Acknowledgements
I would like to express my sincere graditude to the CIMIS Scientist, Dr. Ricardo Treeza, for providing exceptional guidance and technical insights that helped shape the logic of this preprocessing workflow. His expertise was instrumental in streamlining the data transformation process.

## How to cite this work
Rui Gao, Khan, M., & Viers, J. (2026). A Python and Shell-based Toolkit for Spatial CIMIS Data Acquistion and Geospatial Preprocessing (initials). Zenodo. https://doi.org/10.5281/zenodo.xxxxxxx

## Repository update information
- Creation date: 2026-03-20
- Last update: 2026-03-20
- **Contact:** If you encounter any issues or have questions, please contact Rui Gao:
    - Rui.Ray.Gao@gmail.com
    - RuiGao@ucmerced.edu
