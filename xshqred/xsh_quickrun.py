import os
import sys
import logging
import shutil
from pathlib import Path
from astropy.io import fits
from xshqred.UVB.UVB_cl import run_UVB_pipeline
from xshqred.VIS.VIS_cl import run_VIS_pipeline
from xshqred.NIR.NIR_cl import run_NIR_pipeline

log = logging.getLogger(__name__)
logging.basicConfig(
    stream=sys.stdout,
    level=logging.DEBUG,
    format="%(asctime)s.%(msecs)03d | %(levelname)-8s | %(funcName)s - %(filename)s:%(lineno)d : %(message)s",
)


def main():
    cwd = Path().resolve()
    log.info(f"Working directory: {str(cwd)}")

    output_dir = cwd/"quick_reduction"
    output_dir.mkdir(parents=True, exist_ok=True)
    log.info(f"Will store everything under {str(output_dir)}")

    # Unzip files
    os.system(f"gunzip {str(cwd)}/archive/*.Z")

    arms = ("UVB", "VIS", "NIR")

    # Create directories
    dirs = {arm: output_dir/arm for arm in arms}

    for arm in arms:
        log.info(f"Starting processing of {arm} arm")

        raw_data_dir = dirs[arm]/"raw_data"
        reduced_dir = dirs[arm]/"reduced"
        raw_data_dir.mkdir(parents=True, exist_ok=True)
        reduced_dir.mkdir(parents=True, exist_ok=True)

        # Get files
        all_files = [f for f in (cwd/"archive").iterdir() if f.suffix.lower() == '.fits']

        log.info("Looking for corresponding files")
        files = [f for f in all_files if fits.getheader(f, ext=0)["HIERARCH ESO SEQ ARM"] == arm]

        if files:
            log.info(f"Found {len(files)} files for {arm} arm")
            log.info(f"Moving files to :\n{str(raw_data_dir)}")
            for f in files:
                shutil.move(f, raw_data_dir/f.name)
        else:
            log.info(f"No input files for {arm} arm (maybe they have already been moved)")

        if arm == 'UVB':
            run_UVB_pipeline(
                input_dir=raw_data_dir,
                output_dir=reduced_dir,
                mode="nodding",
            )
        elif arm == 'VIS':
            run_VIS_pipeline(
                input_dir=raw_data_dir,
                output_dir=reduced_dir,
                mode="nodding",
            )
        elif arm == 'NIR':
            run_NIR_pipeline(
                input_dir=raw_data_dir,
                output_dir=reduced_dir,
                mode="nodding",
            )


if __name__ == '__main__':
    main()