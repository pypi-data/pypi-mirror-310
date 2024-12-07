"""Main module."""

import glob
import logging
import os
import shutil as sh
import subprocess as sp
import pandas as pd
import numpy as np
import nibabel as nb

from fw_gear_rtp2_pipeline.parser import create_config_file
from fw_gear_rtp2_pipeline.utils import die
from fw_gear_rtp2_pipeline.utils import create_zipinfo


log = logging.getLogger(__name__)

join = os.path.join


def do_reslice(data_dir: str, filename: str, interp_method: str) -> str:
    """Reslices a filename to the anatomical

    It runs MRtrix's mrgrid function to reslice a file using
    the T1w file of the subject and uses a given interpolation method

    Arguments:
        data_dir (str): directory where the data is.
        filename (str): file to be resliced.
        interp_method (str): interpolation method to be used when reslicing.

    Returns:
        str: name of the resliced file
    """

    common = "-force -quiet"
    t1w = join(data_dir, "RTP", "t1.nii.gz")
    log.info("Reslicing to t1.nii.gz, as the ROIs...")
    newname = filename.replace(".nii.gz", "_reslicedT1.nii.gz")
    cmd = f"mrgrid {filename} regrid -template {t1w} {newname} {common} -interp {interp_method}"
    log.info(
        "Reslicing the data to the requested isotropic voxel size, so that "
        "the ROI can be used to extract information, with: %s",
        cmd,
    )

    sp.run(cmd, shell=True)

    return newname


def get_metrics(roi_dir: str, data_file: str) -> pd.DataFrame:
    """Obtains metrics using MRtrix's mrstats.

    It runs MRtrix's mrstats function to obtain metrics.
    The output of mrstats looks like this:
        volume       mean     median        std        min        max      count
        [ 0 ]    60.2422         53    34.0176          3        215        450
    This functions parses it, and adds it to a pandas table

    Arguments:
        roi_dir (str): directory where the ROIs are.
        data_file (str): file with the metrics.

    Returns:
        pd.DataFrame: metrics for the ROIs in pandas Data Frame format.
    """

    # Create pandas and write as csv
    # Define column names
    col_names = ["roi", "mean", "median", "std", "min", "max", "count"]
    # Create empty DataFrame to store values
    roi_metrics = pd.DataFrame(columns=col_names)

    # Check if there are ROIs
    ROIs = glob.glob(join(roi_dir, "*.nii.gz"))
    if len(ROIs) == 0:
        log.info("There are no ROIs to obtain metrics from\n")
        log.info("Returning empty DataFrame\n")
        return roi_metrics

    # There are ROIs, obtain metrics.

    # Calculate
    # cmd = f"mrstats {data_file} -mask roi_file"
    for mask_file in ROIs:
        if "Unknown" not in mask_file:
            cmd = f"mrstats {data_file} -mask {mask_file}"
            log.info("Running command to obtain metrics:\n%s", cmd)
            res = sp.run(cmd, shell=True, capture_output=True, text=True)

            roi_metric = pd.DataFrame(columns=col_names)
            roi_metric.loc[0, "roi"] = os.path.basename(mask_file)
            # Sometimes there is no response, create empty line for the roi
            if len(res.stdout) > 0:
                # Obtain results. The output of mrstats looks like this:
                # volume       mean     median        std        min        max      count
                # [ 0 ]    60.2422         53    34.0176          3        215        450
                # The line below extracts the values:
                str_results = np.array(res.stdout.split("\n")[1].split("]")[1].split())
                roi_metric.iloc[0, 1:7] = str_results
                # Clip min negative values with zeros
                if roi_metric.loc[0, "min"] != "N/A":
                    if float(roi_metric.loc[0, "min"]) < 0:
                        roi_metric.loc[0, "min"] = str(0)

            # Concatenate the result to the rest of ROIs
            roi_metrics = pd.concat([roi_metrics, roi_metric])

    return roi_metrics


def obtain_dti_roi_metrics(data_dir: str, interp_method: str) -> None:
    """Obtains the dti metrics per ROI and save as a csv file, one per metric.

    It starts by running dti metric using MRtrix's tensor2metric. Then, it reslices
    every metric to the anatomical space, as the ROIs are in that space. Next it
    gets a table of metrics and writes a csv file with the values.

    Available metrics in MRtrix are:
        -adc image
        compute the mean apparent diffusion coefficient (ADC) of the diffusion
        tensor. (sometimes also referred to as the mean diffusivity (MD))

        -fa image
         compute the fractional anisotropy (FA) of the diffusion tensor.

        -ad image
         compute the axial diffusivity (AD) of the diffusion tensor. (equivalent to
         the principal eigenvalue)

        -rd image
         compute the radial diffusivity (RD) of the diffusion tensor. (equivalent
         to the mean of the two non-principal eigenvalues)

        -cl image
         compute the linearity metric of the diffusion tensor. (one of the three
         Westin shape metrics)

        -cp image
         compute the planarity metric of the diffusion tensor. (one of the three
         Westin shape metrics)

        -cs image
        compute the sphericity metric of the diffusion tensor. (one of the three
         Westin shape metrics)

    Format of the output csv file:
        Columns:
            - roi: ROI name
            - mean: mean value of the metric for all voxels within the ROI
            - median: median value of the metric for all voxels within the ROI
            - std: standard deviation value of the metric for all voxels within the ROI
            - min: minimum value of the metric for all voxels within the ROI
            - max: maximum value of the metric for all voxels within the ROI
            - count: number of voxels in the ROI
        Rows:
            - One per valid ROI.

    Arguments:
        data_dir (str): directory where the data is.
        interp_method (str): interpolation method to be used when reslicing.
    """

    metrics = ["md", "fa", "ad", "rd", "cl", "cp", "cs"]

    RTP_dir = join(data_dir, "RTP")
    fs_dir = join(RTP_dir, "fs")
    roi_dir = join(fs_dir, "ROIs")
    dt_file = join(RTP_dir, "mrtrix", "dwi_dt.mif")
    csv_dir = join(RTP_dir, "csv_files")
    if not os.path.isdir(csv_dir):
        log.info("%s does not exist, creating...", csv_dir)
        os.mkdir(csv_dir)

    if len(glob.glob(join(roi_dir, "*.nii.gz"))) == 0:
        log.info("There are no ROIs to obtain DTI metrics from\n")
        return

    # Only fa.nii.gz was calculated with RTP.m, let's calculate the rest first
    cmd = (
        f"tensor2metric {dt_file} "
        f"-adc {join(RTP_dir, 'bin', 'md.nii.gz')} "
        f"-ad {join(RTP_dir, 'bin', 'ad.nii.gz')} "
        f"-rd {join(RTP_dir, 'bin', 'rd.nii.gz')} "
        f"-cl {join(RTP_dir, 'bin', 'cl.nii.gz')} "
        f"-cp {join(RTP_dir, 'bin', 'cp.nii.gz')} "
        f"-cs {join(RTP_dir, 'bin', 'cs.nii.gz')} "
        f"-force -quiet "
    )
    log.info("Calculating all DTI metric files except fa with:\n%s", cmd)
    sp.run(cmd, shell=True)

    # Per every metric and ROI, calculate
    cmd = "mrstats resliced_metric_file -mask roi_name"
    log.info("Obtaining DTI metrics from each ROI next with: \n%s", cmd)

    for metric in metrics:
        metric_file = join(RTP_dir, "bin", f"{metric}.nii.gz")

        # resliceval = 1
        # Think if we want to calculate it in the future...
        # VAL = (sp.check_output(["mrinfo", "-spacing", "file.nii.gz"])
        #          .decode()
        #          .split()[0])
        resliced = do_reslice(data_dir, metric_file, interp_method)

        roi_metrics = get_metrics(roi_dir, resliced)

        # Save the file as a csv
        roi_metrics.to_csv(join(csv_dir, f"ROI_{metric}.csv"), index=False)


def obtain_qmap_roi_metrics(data_dir: str, qmap_file: str, interp_method: str) -> None:
    """Obtain the qmap metrics per ROI and save as a csv file.

    It assumes that the quantitative map is already in the same space and coregistered
    with the anatomical file (coming from rtp2-preproc), as the ROIs are in that space.
    Next it gets a table of metrics and writes a csv file with the values.

    Arguments:
        data_dir (str):  directory where the data is.
        qmap_file (str): name of the qmap file.
        interp_method (str): interpolation method to be used when reslicing.
    """

    log.info("Now processing file:\n%s", qmap_file)

    RTP_dir = join(data_dir, "RTP")
    t1w = join(RTP_dir, "t1.nii.gz")
    fs_dir = join(RTP_dir, "fs")
    roi_dir = join(fs_dir, "ROIs")
    csv_dir = join(RTP_dir, "csv_files")
    csv_fname = f"ROI_{os.path.basename(qmap_file).replace('nii.gz', 'csv')}"
    if not os.path.isdir(csv_dir):
        os.mkdir(csv_dir)

    qmap_dim = nb.load(qmap_file).header["dim"]
    t1w_dim = nb.load(t1w).header["dim"]

    if not np.array_equal(qmap_dim, t1w_dim):
        log.info(
            "The qmap file and the ROIs are not in the same " "space, regriding it"
        )
        resliced = do_reslice(data_dir, qmap_file, interp_method)
        roi_metrics = get_metrics(roi_dir, resliced)
    else:
        roi_metrics = get_metrics(roi_dir, qmap_file)

    # Save the file as a csv
    roi_metrics.to_csv(join(csv_dir, csv_fname), index=False)


def run(gear_inputs: dict, gear_config: dict) -> int:
    """Performs dwi data tracking and tractometry; main function.

    It prepares the function calls and calls them depending on the config options.
    Cleans the working folder at the end.

    Arguments:
        gear_config (dict): gear configuration options.
        gear_inputs (dict): gear input files.

    Returns:
        int: 0 when finished successfully.
    """

    log.info("This is the beginning of the run file")

    # Create folder names
    out_dir = join(gear_inputs["output_dir"])
    RTP_dir = join(out_dir, "RTP")
    allRTP_dir = join(out_dir, "RTP_PIPELINE_ALL_OUTPUT")
    tmp_dir = join(out_dir, "tmp")
    if not os.path.isdir(tmp_dir):
        os.mkdir(tmp_dir)
    csv_dir = join(RTP_dir, "csv_files")
    if not os.path.isdir:
        os.mkdir(csv_dir)

    interp_method = "linear"

    # Create json of the option
    projinfojson = create_config_file(gear_config, gear_inputs)

    # Call to the matlab exe RTP with this file as param
    my_env = os.environ.copy()
    log_dir = join(my_env["FLYWHEEL"], "output", "log")
    RTP_log_file = join(my_env["FLYWHEEL"], "output", "log", "RTP_log.txt")
    if not os.path.isdir(log_dir):
        os.mkdir(log_dir)
    if os.path.isfile(RTP_log_file):
        os.remove(RTP_log_file)
    cmd = f'/usr/local/bin/RTP "{projinfojson}" >> {RTP_log_file}'
    log.info("Calling the matlab function RTP with:\n%s", cmd)
    res = os.system(cmd)
    if res != 0:
        die("Error running RTP. Command returned:\n%s", res)
    log.info("RTP Matlab command finished succesfully, this is the log:")
    if os.path.isfile(RTP_log_file):
        print(open(RTP_log_file, "r").read())
    else:
        log.warning("It was not possible to read the logfile RTP_log_file")

    # This is not passing env variables to Matlab
    # res = sp.run(cmd, shell=True, capture_output=True,
    #              text=True, cwd=my_env['FLYWHEEL'])
    # Formulate the command with the environment variable
    # matlab_bin = '/usr/local/bin/RTP'
    # cmd = f'export MRTRIX_TMPFILE_DIR="{tmp_dir}" && {matlab_bin} "{projinfojson}"'
    # log.info("Calling the matlab function RTP with:\n%s", cmd)
    # # Execute the command
    # res = sp.run(cmd, shell=True, capture_output=True, text=True)
    # # Plot the output and the error messages
    # log.info(f"This is stdout:\n{res.stdout}")
    # log.info(f"This is stderr:\n{res.stderr}")

    # Obtain a csv file with dti metrics per ROI
    obtain_dti_roi_metrics(out_dir, interp_method)

    # Obtain a csv file with qmap metrics per ROI (if file was passed)
    if len(gear_inputs["qmap_list"]) > 0:
        for qmap in gear_inputs["qmap_list"]:
            obtain_qmap_roi_metrics(out_dir, qmap, interp_method)

    # Cleanup
    log.info("Copying files to output directory...")

    for f in glob.glob(join(csv_dir, "*.csv")):
        sh.copy(f, out_dir)
    for f in glob.glob(join(RTP_dir, "bin", "*.nii.gz")):
        sh.copy(f, out_dir)
    for f in glob.glob(join(RTP_dir, "mrtrix", "*wmCsd*mif")):
        sh.copy(f, out_dir)
    sh.copy(join(RTP_dir, "mrtrix", "dwi_dt.mif"), out_dir)
    for f in glob.glob(join(RTP_dir, "*.mat")):
        sh.copy(f, out_dir)

    log.info("Archiving and copying tract files to output directory...")
    tracts_dir = join(RTP_dir, "tracts")
    output_filename = join(out_dir, "tracts")
    os.mkdir(tracts_dir)
    for f in glob.glob(join(RTP_dir, "mrtrix", "*.nii.gz")):
        sh.copy(f, tracts_dir)
    for f in glob.glob(join(RTP_dir, "mrtrix", "*clean*.tck")):
        sh.copy(f, tracts_dir)
    sh.make_archive(output_filename, "zip", join(RTP_dir), "tracts")

    log.info("Archiving and copying fs files to output directory...")
    output_filename = join(out_dir, "fs")
    sh.make_archive(output_filename, "zip", join(RTP_dir), "fs")

    cmd = f"chmod -R 777 {out_dir}"
    log.info("Change permission in out dir using %s", cmd)
    sp.run(cmd, shell=True)

    sh.move(RTP_dir, allRTP_dir)

    if gear_config["save_output"]:
        log.info(
            "save_output=True, archiving and copying all RTP files to "
            "output directory..."
        )
        sh.make_archive(allRTP_dir, "zip", allRTP_dir)

    if os.path.isdir(allRTP_dir):
        sh.rmtree(allRTP_dir)
    if os.path.isdir(join(out_dir, "tmp")):
        sh.rmtree(join(out_dir, "tmp"))
    if os.path.isdir(join(out_dir, "qmap")):
        sh.rmtree(join(out_dir, "qmap"))
    if os.path.isdir(join(out_dir, ".mcrCache9.9")):
        sh.rmtree(join(out_dir, ".mcrCache9.9"))

    # Create a zipinfo.csv file per each zip file in the output.
    zip_files_in_output = glob.glob(join(out_dir, "*.zip"))
    if len(zip_files_in_output) > 0:
        log.info("There are zip files in the output, creating zipinfo.csv per file")
        for f in zip_files_in_output:
            create_zipinfo(out_dir, f)

    log.info("rtp2_pipeline main.py ended succesfully. ")

    return 0
