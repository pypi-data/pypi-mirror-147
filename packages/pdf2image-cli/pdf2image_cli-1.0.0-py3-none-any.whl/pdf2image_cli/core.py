import os
import sys
import argparse
from enum import IntEnum, unique
import pathlib
from typing import List

from .status import ExitStatus

from pdf2image import convert_from_path, convert_from_bytes
from pdf2image.exceptions import (
    PDFInfoNotInstalledError,
    PDFPageCountError,
    PDFSyntaxError
)


@unique
class PathType(IntEnum):
    FILE = 0
    FOLDER = 1


def pathQuery(path: pathlib.Path) -> PathType:
    if os.path.exists(path) and os.path.isfile(path):
        return PathType.FILE
    elif os.path.exists(path) and os.path.isdir(path):
        return PathType.FOLDER
    else:
        raise Exception("Path does not exist")


def fileLookup(path: pathlib.Path) -> List:
    files = []
    for file in os.listdir(path):
        if file.endswith('.pdf'):
            files.append(pathlib.Path(path, file))

    return files


def extractImages(path: pathlib.Path, output: pathlib.Path, imageType):
    try:
        if not output.exists():
            output.mkdir()
            print(f'{output} folder created')

        print(f'\nConverting {path.name}')
        images = convert_from_path(path, fmt=imageType)
        i = 0

        for image in images:
            pdfName = path.name.replace('.pdf', '')
            fileName = pathlib.Path(output, f'{pdfName}_{i}.{imageType}')
            image.save((fileName))
            print(f"Image: {str(fileName)} saved")
            i += 1

    except Exception as e:
        print(e)


def saveImages(path: pathlib.Path, output: pathlib.Path, imageType) -> ExitStatus:
    try:
        if not output.exists():
            output.mkdir()
            print(f'{output} folder created')

        pathType: PathType = None
        pathType = pathQuery(path)

        if pathType == PathType.FILE:
            extractImages(path, output, imageType)
        elif pathType == PathType.FOLDER:
            files = fileLookup(path)
            for file in files:
                newOutput = pathlib.Path(output, file.name.replace('.pdf', ''))
                extractImages(file, newOutput, imageType)

    except (Exception, IOError) as e:
        print(e)
        return ExitStatus.ERROR

    return ExitStatus.SUCCESS


def parser():
    try:
        parser = argparse.ArgumentParser(description="Convert pdf to images.")
        parser.add_argument('path', type=pathlib.Path)
        parser.add_argument('--output',
                            default='./output',
                            type=pathlib.Path,
                            help="Output folder to save images to")
        parser.add_argument('--image_type',
                            default="jpeg",
                            choices=['jpeg', 'png'])
        args = parser.parse_args()

        if args.output.exists() and args.output.is_file():
            raise Exception("Cannot set output path pointing to a file.")

        return saveImages(path=args.path, output=args.output, imageType=args.image_type)
    except Exception as e:
        print(e)
        return ExitStatus.ERROR


def main() -> ExitStatus:
    return parser()
