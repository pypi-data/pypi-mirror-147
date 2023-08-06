# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

modules = \
['reorient_nii']
install_requires = \
['nibabel>=3.2.2,<4.0.0']

setup_kwargs = {
    'name': 'reorient-nii',
    'version': '1.0.0',
    'description': 'Load and reorient nifti images',
    'long_description': '# reorient-nii\n\nLoad and reorient nifti images\n\n[![PyPI](https://img.shields.io/pypi/v/reorient-nii)](https://pypi.org/project/reorient-nii/)\n\n## Installation\n\n`pip install reorient-nii`\n\n## Understanding Orientation\n\n- The image voxel orientation indicates how the image array data is stored.\n- The voxel orientation is represented by three axes: Left/Right, Anterior/Posterior, and Inferior/Superior.\n- The orientation is a string of three letters representing the order and increasing direction of the axes.\n    - For example, `"RAS"` orientation corresponds to the first axis being ordered from Left to Right, the second axis from Posterior to Anterior and the third axis from Inferior to Superior.\n    - This orientation is also sometimes referred to as RAS+ to more clearly convey that the letters represent the increasing direction.\n\n## Usage\n\n`reorient-nii` exposes three functions\n- `reorient`\n- `load`\n- `get_orientation`\n\n**`reorient`** will reorient a nifti image to the desired voxel orientation by flipping and / or reordering the voxel axes. The orientation can be provided as a string of three characters or a length three tuple of strings reflecting the desired positive end of the voxel axes. For example, if the desired orientation is RAS+ the orientation can be specified as `"RAS"` or `(\'R\', \'A\', \'S\')`. The orientation must have a single character for each of the voxel axes indicating the positive direction of the voxel axis. This means the orientation must consist of "R" or "L", "A" or "P", "I" or "S", in any order. For example, the orientation `"RLP"` is not valid since "R" and "L" are directions for the same voxel axis and only one can indicate the positive direction. The reoriented nifti image will have voxel axes that match the directions in `orientation`. Note, this function does not resample, register or de-oblique an image, it only flips and / or reorders the voxel axes, chaning the storage of the image array data. The following are valid orientations and can also be specified as a tuple as described above instead of a single string.\n\n`orientation: (\'RAS\' or \'RAI\' or \'RPS\' or \'RPI\' or \'LAS\' or \'LAI\' or\n         \'LPS\' or \'LPI\' or \'RSA\' or \'RSP\' or \'RIA\' or \'RIP\' or \'LSA\' or\n         \'LSP\' or \'LIA\' or \'LIP\' or \'ARS\' or \'ARI\' or \'ALS\' or \'ALI\' or\n         \'PRS\' or \'PRI\' or \'PLS\' or \'PLI\' or \'ASR\' or \'ASL\' or \'AIR\' or\n         \'AIL\' or \'PSR\' or \'PSL\' or \'PIR\' or \'PIL\' or \'SRA\' or \'SRP\' or\n         \'SLA\' or \'SLP\' or \'IRA\' or \'IRP\' or \'ILA\' or \'ILP\' or \'SAR\' or\n         \'SAL\' or \'SPR\' or \'SPL\' or \'IAR\' or \'IAL\' or \'IPR\' or \'IPL\',\n         default value: RAS)`\n\n**`load`** will load the nifti image and reorient it to the desired orientation (default="RAS").\n\n**`get_orientation`** will get the orientation of a nifti image as a tuple of 3 strings indicating the labels for the positive end of the voxel axes.\n\n## API\n\n```python\n# src/reorient_nii.py\n\ndef reorient(\n    nii: nib.Nifti1Image,\n    orientation: str | tuple[str, str, str] = "RAS",\n) -> nib.Nifti1Image:\n    """Reorients a nifti image to specified orientation. Orientation string or tuple\n    must consist of "R" or "L", "A" or "P", and "I" or "S" in any order."""\n\ndef load(\n    filepath: str | Path,\n    orientation: str | tuple[str, str, str] = "RAS",\n) -> nib.Nifti1Image:\n    """Loads and reorients a nifti image. Orientation string or tuple must consist of\n    "R" or "L", "A" or "P", and "I" or "S" in any order."""\n\ndef get_orientation(\n    nii: nib.Nifti1Image,\n) -> tuple[str, str, str]:\n    """Gets the orientation of a nifti image."""\n\n```\n\n\n## License\nThe `reorient` function is a light weight version of Nipype\'s [Reorient function](https://github.com/nipy/nipype/blob/ecd5871b6/nipype/interfaces/image.py#L122-L223), copyright 2009-2016, Nipype developers, licensed under Apache 2.0 license. This project\'s `reorient` function removes several elements from the source code. The function is not a class method for a Nipype interface, it does not compute or save the affine transform, it does not save the reoriented image and it does not support backwards compatibility for Nibabel version < "2.4.0". See [LICENSE](LICENSE) for full license info.\n\n\n## Contributing\n\n1. Have or install a recent version of poetry (version >= 1.1)\n1. Fork the repo\n1. Setup a virtual environment (however you prefer)\n1. Run poetry install\n1. Run pre-commit install\n1. Add your changes (adding/updating tests is always nice too)\n1. Commit your changes + push to your fork\n1. Open a PR\n',
    'author': 'aptinis',
    'author_email': '8akp1@queensu.ca',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/aptinis/reorient-nii',
    'package_dir': package_dir,
    'py_modules': modules,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
