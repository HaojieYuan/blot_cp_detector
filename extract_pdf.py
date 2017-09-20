#!/usr/bin/env python
import os
import logging
import sys
"""
    can't find a very good python library to do this
    so please install pdfimages first
"""

def extract(pdf_path, prefix):
    """
        with given pdfpath, extract images with certain prefix
        default is jpg, when it can not be done with jpg,
        image will be save as ppm.
    """
    if os.path.exists(pdf_path):
        pdf_name = pdf_path.split(os.sep)[-1]
        image_path = os.sep.join(prefix.split(os.sep)) + os.sep
        image_prefix = prefix.split(os.sep)[-1]

        if os.path.isdir(image_path):
            old_files = os.listdir(image_path)
            command = 'pdfimages ' + '-j ' + pdf_path + ' ' + image_path + pdf_name.split('.')[0]
            os.popen(command)
            logging.info("pdf extraction complete.")

            new_files = os.listdir(image_path)

            newly_added = list(set(new_files) - set(old_files))
            if len(newly_added) == 0:
                logging.info("pdf does not contain images, program terminated.")
                sys.exit(0)
            else:
                logging.info("extract %d images from pdf", len(newly_added))
                return newly_added

        else:
            logging.error("image path does not exits, program terminated.")
            sys.exit(0)
    else:
        logging.error("pdf file can not found, program terminated.")
        sys.exit(0)
