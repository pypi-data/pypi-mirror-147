# Slope Difference Distribution Segmentation

The python implementation of algorithm proposed by Z. Wang, "A New Approach for Segmentation and Quantification of Cells or Nanoparticles," in IEEE Transactions on Industrial Informatics, vol. 12, no. 3, pp. 962-971, June 2016, DOI: 10.1109/TII.2016.

## Description

## Badges

TODO: Add bagdes https://shields.io/
## Installation

You can install ``sdd-segmentation`` directly from PyPi via ``pip``:

```bash
    pip install sdd-segmentation
```

## Usage

```python
import cv2
from sdd_segmentation.sdd import sdd_threshold_selection

img_np = cv2.imread("image.png")
T = sdd_threshold_selection(img_np.astype(float), 15)
print(T)
th_image_np = img_np > T[-1]
```

## License

This software is licensed under the BSD 3-Clause License.

If you use this software in your scientific research, please cite our paper:

```bibtex

```

AND original [work](https://doi.org/10.1109/TII.2016.2542043):
```bibtex
@ARTICLE{Wang2016,
    author={Wang, ZhenZhou},
    journal={IEEE Transactions on Industrial Informatics}, 
    title={A New Approach for Segmentation and Quantification of Cells or Nanoparticles}, 
    year={2016},
    volume={12},
    number={3},
    pages={962-971},
    doi={10.1109/TII.2016.2542043}
}
```
