JSTColorPicker Python SDK
*************************

Extract JSTColorPicker annotation data models from metadata of bitmap images.


Setup
=====

.. code-block:: shell

    $ pip install jstcolorpicker@git+https://github.com/Lessica/JSTColorPicker-Python.git


Usage
=====

.. code-block:: python

    import base64
    import exifread
    import jstcolorpicker

    from bpylist2 import archiver
    from exifread.classes import IfdTag


    # register JSTColorPicker data models
    archiver.update_class_map({
        'JSTColorPicker.Content': jstcolorpicker.Content,
        'JSTColorPicker.PixelArea': jstcolorpicker.PixelArea,
        'JSTColorPicker.PixelColor': jstcolorpicker.PixelColor,
        'JSTPixelColor': jstcolorpicker.JSTPixelColor,
    })

    # ... open input_image_file
    # extract exif tags from image file
    exif_tags = exifread.process_file(input_image_file, details=True)
    input_image_file.close()

    if 'EXIF UserComment' in exif_tags:

        # extract UserComment from exif tags
        exif_user_comment: IfdTag = exif_tags['EXIF UserComment']

        # decode archived content object from exif UserComment tag as base64
        binary_plist = base64.b64decode(exif_user_comment.printable)
        
        # unarchive content object
        content_object: jstcolorpicker.Content = archiver.unarchive(binary_plist)

        # ... then access content object as usual

