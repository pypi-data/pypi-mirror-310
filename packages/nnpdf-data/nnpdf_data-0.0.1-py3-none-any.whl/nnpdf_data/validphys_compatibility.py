"""
    This file exists solely for me to be able to upload a package to PyPI for the nnpdf data which does not depend
    on the rest of the NNPDF code.
    This file should not be modified. Everything in this file is deprecated and should be removed, and the only reason
    this is needed is because we are still mixing new and old data.

    This also means that _things_ that would've been loaded as a kinematic transformation or result transformation
    are loaded as boring strings that cannot do anything, as it should be.
"""

import dataclasses
import typing

labeler_functions = []


@dataclasses.dataclass
class PlottingOptions:
    func_labels: dict = dataclasses.field(default_factory=dict)
    dataset_label: typing.Optional[str] = None
    experiment: typing.Optional[str] = None
    nnpdf31_process: typing.Optional[str] = None
    data_reference: typing.Optional[str] = None
    theory_reference: typing.Optional[str] = None
    process_description: typing.Optional[str] = None
    y_label: typing.Optional[str] = None
    x_label: typing.Optional[str] = None
    kinematics_override: typing.Optional[str] = None
    result_transform: typing.Optional[str] = None
    x: typing.Optional[str] = None
    plot_x: typing.Optional[str] = None
    x_scale: typing.Optional[str] = None
    y_scale: typing.Optional[str] = None
    line_by: typing.Optional[list] = None
    figure_by: typing.Optional[list] = None
    extra_labels: typing.Optional[typing.Mapping[str, typing.List]] = None
    normalize: typing.Optional[dict] = None
    # Note that this "PlottingOptions" start already digested, because it actually does nothing!
    already_digested: typing.Optional[bool] = True
