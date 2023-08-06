#!/usr/bin/env python

# pyak-view (installed name)
# View text with given font (using AppKit)

import argparse
import math

# This is designed to run on macOS using PyObjC
# https://pypi.org/project/pyobjc/
import Cocoa
import CoreText  # for CT*


def main(argv=None):

    parser = argparse.ArgumentParser()
    parser.add_argument("--font-file")
    parser.add_argument("--font-size", type=float, default=256.0)
    parser.add_argument("--margin", type=commaList, default="16")
    parser.add_argument("--output-file", default="-")
    parser.add_argument("file", nargs="?")
    parser.add_argument("text")

    args = parser.parse_args(argv)

    if args.file is not None:
        args.font_file = args.file

    if args.font_file is None:
        raise ValueError("A font file must be given")

    toImage(args)


def commaList(s):
    """Convert list of comma separated numbers,
    from string to Python list.
    """

    return [float(x) for x in s.split(",")]


def toImage(args):
    # https://stackoverflow.com/a/2703206/242457
    # revised by
    # https://stackoverflow.com/a/60031253/242457
    url = Cocoa.CFURLCreateWithFileSystemPath(
        Cocoa.kCFAllocatorDefault, args.font_file, Cocoa.kCFURLPOSIXPathStyle, False
    )
    fds = CoreText.CTFontManagerCreateFontDescriptorsFromURL(url)
    font = CoreText.CTFontCreateWithFontDescriptor(fds[0], args.font_size, None)

    # https://stackoverflow.com/q/1229830/242457
    s = Cocoa.NSString.stringWithString_(args.text)
    attr = {
        Cocoa.NSFontAttributeName: font,
        Cocoa.NSForegroundColorAttributeName: Cocoa.NSColor.blackColor(),
    }

    # Allocate margins, then estimate size of rendered text.
    # The margin is nominally [top, right, bottom, left]
    # but can be made shorter for abbreviated forms.
    margin = args.margin
    if len(margin) == 1:
        # Only top margin specified, repeat for right-margin
        margin = [margin[0], margin[0]]
    if len(margin) == 2:
        # Only top- and right-margin specified, repeat
        # for bottom- and left-margin
        margin = margin + margin
    if len(margin) == 3:
        margin = (margin + margin)[:4]

    size = s.sizeWithAttributes_(attr)

    height = math.ceil(size.height + margin[0] + margin[2])
    width = math.ceil(size.width + margin[1] + margin[3])

    # Allocate image.
    image = Cocoa.NSImage.alloc().initWithSize_((width, height))
    # See section "Drawing to an Image by Locking Focus" of
    # https://developer.apple.com/library/archive/documentation/Cocoa/Conceptual/CocoaDrawingGuide/Images/Images.html
    image.lockFocus()

    background = Cocoa.NSMakeRect(0, 0, *image.size())
    path = Cocoa.NSBezierPath.bezierPathWithRect_(background)
    Cocoa.NSColor.whiteColor().set()
    path.fill()

    bl = Cocoa.NSMakePoint(margin[3], margin[2])
    s.drawAtPoint_withAttributes_(bl, attr)

    image.unlockFocus()

    # Write image to PNG;
    # https://stackoverflow.com/a/60450819/242457
    tiffData = image.TIFFRepresentation()
    rep = Cocoa.NSBitmapImageRep.alloc().initWithData_(tiffData)
    pngData = rep.representationUsingType_properties_(
        Cocoa.NSBitmapImageFileTypePNG, {}
    )

    if args.output_file == "-":
        Cocoa.NSFileHandle.fileHandleWithStandardOutput().writeData_(pngData)
    else:
        pngData.writeToFile_atomically_(args.output_file, False)


if __name__ == "__main__":
    main()
