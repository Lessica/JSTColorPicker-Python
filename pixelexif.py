#!/usr/bin/env python3

import argparse
import base64
import exifread
import json
import jstcolorpicker
import sys
import timeit

from json import JSONEncoder

from bpylist2 import archiver
from exifread import exif_log
from exifread.classes import IfdTag
from exifread.tags import FIELD_TYPES


logger = exif_log.get_logger()

def wrapped_default(self, obj):
    return getattr(obj.__class__, "__json__", wrapped_default.default)(obj)

wrapped_default.default = JSONEncoder().default
JSONEncoder.original_default = JSONEncoder.default
JSONEncoder.default = wrapped_default

def get_args():
    parser = argparse.ArgumentParser(
        prog='pixelexif.py',
        description=" ".join(jstcolorpicker.__doc__.splitlines()).strip(),
    )
    parser.add_argument(
        'files', metavar='FILE', type=str, nargs='+',
        help='files to process',
    )
    parser.add_argument(
        '-v', '--version', action='version',
        version='pixelexif.py Version %s on Python%s' % (jstcolorpicker.__version__, sys.version_info[0]),
        help='display version information and exit'
    )
    parser.add_argument(
        '-s', '--strict', action='store_true', dest='strict',
        help='run in strict mode (stop on errors).',
    )
    parser.add_argument(
        '-d', '--debug', action='store_true', dest='debug',
        help='run in debug mode (display extra info).',
    )
    parser.add_argument(
        '-c', '--color', action='store_true', dest='color',
        help='output in color (only works with debug on POSIX).',
    )
    args = parser.parse_args()
    return args

def main(args) -> None:
    """Extract tags based on options (args)."""

    exif_log.setup_logger(args.debug, args.color)

    # register JSTColorPicker data models
    archiver.update_class_map({
        'JSTColorPicker.Content': jstcolorpicker.Content,
        'JSTColorPicker.PixelArea': jstcolorpicker.PixelArea,
        'JSTColorPicker.PixelColor': jstcolorpicker.PixelColor,
        'JSTPixelColor': jstcolorpicker.JSTPixelColor,
    })

    # output info for each file
    for filename in args.files:

        # avoid errors when printing to console
        escaped_fn = escaped_fn = filename.encode(
            sys.getfilesystemencoding(), 'surrogateescape'
        ).decode()

        file_start = timeit.default_timer()
        try:
            img_file = open(escaped_fn, 'rb')
        except IOError:
            logger.error("'%s' is unreadable", escaped_fn)
            continue

        logger.debug('opening: %s', escaped_fn)

        tag_start = timeit.default_timer()

        # get the tags
        exif_tags = exifread.process_file(img_file, details=True, strict=args.strict, debug=args.debug)
        img_file.close()

        tag_stop = timeit.default_timer()

        if not exif_tags:
            logger.warning('no EXIF information found')
            print()
            continue

        if 'JPEGThumbnail' in exif_tags:
            logger.debug('file has JPEG thumbnail')
            del exif_tags['JPEGThumbnail']
        
        if 'TIFFThumbnail' in exif_tags:
            logger.debug('file has TIFF thumbnail')
            del exif_tags['TIFFThumbnail']
        
        if 'EXIF UserComment' in exif_tags:

            # extract UserComment from exif tags
            exif_user_comment: IfdTag = exif_tags['EXIF UserComment']

            # decode archived content object from exif UserComment tag as base64
            binary_plist = base64.b64decode(exif_user_comment.printable)

            # unarchive content object
            content_object: jstcolorpicker.Content = archiver.unarchive(binary_plist)

            # ... then access content object as usual
            print(json.dumps(content_object, indent=4, sort_keys=True))

            del exif_tags['EXIF UserComment']
        
        tag_keys = list(exif_tags.keys())
        tag_keys.sort()

        for i in tag_keys:
            try:
                logger.debug('%s (%s): %s', i, FIELD_TYPES[exif_tags[i].field_type][2], exif_tags[i].printable)
            except:
                logger.error("%s : %s", i, str(exif_tags[i]))
        
        file_stop = timeit.default_timer()

        logger.debug("tags processed in %s seconds", tag_stop - tag_start)
        logger.debug("file processed in %s seconds", file_stop - file_start)
        print()


if __name__ == '__main__':
    main(get_args())
