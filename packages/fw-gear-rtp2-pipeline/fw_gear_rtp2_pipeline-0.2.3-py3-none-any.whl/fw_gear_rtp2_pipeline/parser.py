"""Parser module to parse gear config.json."""

import json
import logging
import os
from typing import Tuple

from fw_gear_rtp2_pipeline.utils import get_valid_qmap_list

from flywheel_gear_toolkit import GearToolkitContext

log = logging.getLogger(__name__)

join = os.path.join
dirname = os.path.dirname


# This function mainly parses gear_context's config.json file and returns relevant
# inputs and options.
def parse_config(
    gear_context: GearToolkitContext,
) -> Tuple[dict, dict]:
    """Inputs and config options parser.

    It parses gear_context's config.json file and returns relevant inputs and options.

    Arguments:
        gear_context (GearToolkitContext): gear context.

    Returns:
        tuple: dictionaries with inputs and configs
    """

    # Gear inputs
    # Validate qmap inputs first
    out_dir = gear_context.output_dir
    qmap_input = gear_context.get_input_path("qmap")

    if qmap_input:
        list_of_paths_with_valid_maps = get_valid_qmap_list(out_dir, qmap_input)
    else:
        list_of_paths_with_valid_maps = []

    gear_inputs = {
        "anatomical": gear_context.get_input_path("anatomical"),
        "fs": gear_context.get_input_path("fs"),
        "tractparams": gear_context.get_input_path("tractparams"),
        "dwi": gear_context.get_input_path("dwi"),
        "bval": gear_context.get_input_path("bval"),
        "bvec": gear_context.get_input_path("bvec"),
        "fsmask": gear_context.get_input_path("fsmask"),
        "qmap_list": list_of_paths_with_valid_maps,
        "output_dir": gear_context.output_dir,
    }

    # Gear configs
    gear_config = {
        "debug": gear_context.config.get("debug"),
        "numberOfNodes": gear_context.config.get("numberOfNodes"),
        "fiberWeighting": gear_context.config.get("fiberWeighting"),
        "track_faFodThresh": gear_context.config.get("track_faFodThresh"),
        "track_faMaskThresh": gear_context.config.get("track_faMaskThresh"),
        "bval_for_fa": gear_context.config.get("bval_for_fa"),
        "mrtrix_mrTrixAlgo": gear_context.config.get("mrtrix_mrTrixAlgo"),
        "mrtrix_useACT": gear_context.config.get("mrtrix_useACT"),
        "mrtrix_autolmax": gear_context.config.get("mrtrix_autolmax"),
        "mrtrix_lmax": gear_context.config.get("mrtrix_lmax"),
        "get_vofparc": gear_context.config.get("get_vofparc"),
        "sift_runSift": gear_context.config.get("sift_runSift"),
        "sift_nFibers": gear_context.config.get("sift_nFibers"),
        "life_runLife": gear_context.config.get("life_runLife"),
        "life_saveOutput": gear_context.config.get("life_saveOutput"),
        "life_discretization": gear_context.config.get("life_discretization"),
        "life_num_iterations": gear_context.config.get("life_num_iterations"),
        "life_test": gear_context.config.get("life_test"),
        "life_writePDB": gear_context.config.get("life_writePDB"),
        "ET_numberFibers": gear_context.config.get("ET_numberFibers"),
        "ET_minlength": gear_context.config.get("ET_minlength"),
        "ET_maxlength": gear_context.config.get("ET_maxlength"),
        "ET_angleValues": gear_context.config.get("ET_angleValues"),
        "ET_track_stepSizeMm": gear_context.config.get("ET_track_stepSizeMm"),
        "save_output": gear_context.config.get("save_output"),
    }

    return gear_inputs, gear_config


def create_config_file(gear_config: dict, gear_inputs: dict) -> str:
    """From inputs and configs, create a json file to pass to the main Matlab function

    Parses and reorganizes the config and input dicts, and creates a combined json
    file that will be the only input to the Matlab compiled executable.

    Arguments:
        gear_config (dict): gear configuration options.
        gear_inputs (dict): gear input files.

    Returns:
        str: path to the json file to be used as input in the Matlab function
    """

    out_dir = gear_inputs["output_dir"]
    output_file = join(out_dir, "config_RTP.json")

    # Rename the config key to params
    config = dict()
    config["params"] = gear_config

    # Handle the 'track' fields
    config["params"]["track"] = {}
    config["params"]["track"]["faMaskThresh"] = config["params"]["track_faMaskThresh"]
    config["params"]["track"]["faFodThresh"] = config["params"]["track_faFodThresh"]

    config["params"]["track"]["bval_for_fa"] = config["params"]["bval_for_fa"]

    config["params"]["track"]["mrtrix_useACT"] = config["params"]["mrtrix_useACT"]
    config["params"]["track"]["mrtrix_autolmax"] = config["params"]["mrtrix_autolmax"]
    config["params"]["track"]["mrtrix_lmax"] = config["params"]["mrtrix_lmax"]
    config["params"]["track"]["mrTrixAlgo"] = config["params"]["mrtrix_mrTrixAlgo"]

    config["params"]["track"]["get_vofparc"] = config["params"]["get_vofparc"]

    config["params"]["track"]["sift_runSift"] = config["params"]["sift_runSift"]
    config["params"]["track"]["sift_nFibers"] = config["params"]["sift_nFibers"]

    config["params"]["track"]["life_runLife"] = config["params"]["life_runLife"]
    config["params"]["track"]["life_discretization"] = config["params"][
        "life_discretization"
    ]
    config["params"]["track"]["life_num_iterations"] = config["params"][
        "life_num_iterations"
    ]
    config["params"]["track"]["life_test"] = config["params"]["life_test"]
    config["params"]["track"]["life_saveOutput"] = config["params"]["life_saveOutput"]
    config["params"]["track"]["life_writePDB"] = config["params"]["life_writePDB"]

    config["params"]["track"]["ET_numberFibers"] = config["params"]["ET_numberFibers"]
    config["params"]["track"]["ET_angleValues"] = [
        float(x) for x in config["params"]["ET_angleValues"].split(",")
    ]
    config["params"]["track"]["ET_maxlength"] = [
        float(x) for x in config["params"]["ET_maxlength"].split(",")
    ]

    config["params"]["track"]["ET_minlength"] = config["params"]["ET_minlength"]
    config["params"]["track"]["ET_stepSizeMm"] = config["params"]["ET_track_stepSizeMm"]

    # Remove the other track_ fields
    del config["params"]["track_faMaskThresh"]
    del config["params"]["track_faFodThresh"]

    del config["params"]["mrtrix_useACT"]
    del config["params"]["mrtrix_autolmax"]
    del config["params"]["mrtrix_lmax"]
    del config["params"]["mrtrix_mrTrixAlgo"]

    del config["params"]["get_vofparc"]

    del config["params"]["sift_runSift"]
    del config["params"]["sift_nFibers"]

    del config["params"]["life_runLife"]
    del config["params"]["life_discretization"]
    del config["params"]["life_num_iterations"]
    del config["params"]["life_test"]
    del config["params"]["life_saveOutput"]
    del config["params"]["life_writePDB"]

    del config["params"]["ET_numberFibers"]
    del config["params"]["ET_angleValues"]
    del config["params"]["ET_maxlength"]
    del config["params"]["ET_minlength"]
    del config["params"]["ET_track_stepSizeMm"]

    # Add input directories for dtiInit
    config["input_dir"] = str(gear_inputs["output_dir"]).replace("output", "input")
    config["output_dir"] = str(gear_inputs["output_dir"])
    config["bvec_dir"] = str(dirname(gear_inputs["bvec"]))
    config["bval_dir"] = str(dirname(gear_inputs["bval"]))
    config["nifti_dir"] = str(dirname(gear_inputs["dwi"]))
    config["anat_dir"] = str(dirname(gear_inputs["anatomical"]))
    if gear_inputs["fsmask"]:
        config["fsmask_dir"] = str(dirname(gear_inputs["fsmask"]))
    else:
        config["fsmask_dir"] = ""
    if len(gear_inputs["qmap_list"]) > 0:
        config["qmap_dir"] = str(dirname(gear_inputs["qmap_list"][0]))
    else:
        config["qmap_dir"] = ""
    if gear_inputs["tractparams"]:
        config["tractparams_dir"] = str(dirname(gear_inputs["tractparams"]))
    else:
        config["tractparams_dir"] = ""
    # config["tractparams_dir"] = str(dirname(gear_inputs["tractparams"]))
    config["fs_dir"] = str(dirname(gear_inputs["fs"]))
    # new parameters: save_output (delcare if save .zip)
    config["params"]["save_output"] = config["params"]["save_output"]
    # Add additional keys
    config["params"]["run_mode"] = ([],)
    config["params"]["outdir"] = []
    config["params"]["input_dir"] = str(config["input_dir"])
    config["params"]["output_dir"] = str(config["output_dir"])

    # Write out the modified configuration
    log.info("Saving config file with content:\n%s", config)
    with open(output_file, "w") as config_json:
        json.dump(config, config_json, sort_keys=True, indent=4, separators=(",", ": "))

    return output_file
