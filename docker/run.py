import click
import os
import shutil
import subprocess
import sys
import time
from PIL import Image

__version__ = '0.1.0'


@click.command()
@click.argument('in-dir', type=click.Path(exists=True, file_okay=False))
@click.option('--mp4-out', type=click.Path(), help='output mp4 location')
@click.option('--gif-out', type=click.Path(), help='output gif location')
@click.option('--mask-rect', type=click.STRING, help='image mask rectagle as "x1,y1,x2,y2"')
@click.version_option(version=__version__, prog_name='Generate timelapse videos from images')
def run(in_dir, mp4_out, gif_out, mask_rect):
    files = [os.path.join(in_dir, f) for f in sorted(os.listdir(in_dir))]
    in_img = Image.open(files[0])
    os.mkdir('/artifacts')

    # Create the mask image
    x1, y1, x2, y2 = [int(v) for v in mask_rect.split(',')]
    xmin, xmax = min(x1, x2), max(x1, x2)
    ymin, ymax = min(y1, y2), max(y1, y2)
    mask = Image.new('RGB', (in_img.width, in_img.height), (0, 0, 0))
    mask.paste((255, 255, 255), [xmin, ymin, xmax, ymax])
    mask.save('/artifacts/__mask__.png')

    # Register the images
    print('Registering images')
    start = time.time()
    basename = os.path.basename(files[0])
    name, ext = os.path.splitext(basename)
    reg_images = ['/artifacts/%s_reg%s' % (name, ext)]

    shutil.copy(files[0], reg_images[0])
    for image in files[1:]:
        print(image)
        name, ext = os.path.splitext(os.path.basename(image))
        out_file = '/artifacts/%s_reg%s' % (name, ext)
        subprocess.check_call([
            '/bin/ImageSimilarityRegistration',
            files[0], image, '/artifacts/__mask__.png', out_file
        ], stdout=sys.stdout, stderr=sys.stderr)
        reg_images.append(out_file)
    print('Finished in %s s\n' % (time.time() - start))

    # Run optical flow
    print('Running optical flow')
    start = time.time()
    interp_images = [files[0]]
    for i in range(len(files) - 1):
        print(files[i])
        subprocess.check_call([
            '/bin/InterpByOpticalFlow',
            files[i], files[i+1]
        ], stdout=sys.stdout, stderr=sys.stderr)
        name, ext = os.path.splitext(files[i])
        for j in range(1, 10):
            interp_images.append('%s_%s%s' % (name, j, ext))
    interp_images.append(files[-1])
    print('Finished in %s s\n' % (time.time() - start))

    # Create a GIF from the interpolated images
    if gif_out:
        try:
            os.mkdir(gif_out)
        except Exception:
            pass
        path = os.path.join(gif_out, 'OpticalFlow.gif')
        print('Creating GIF output')
        subprocess.check_call([
            '/usr/bin/convert', '-delay', '10', '-loop', '0'
        ] + interp_images + [path], stdout=sys.stdout, stderr=sys.stderr)

    if mp4_out:
        try:
            os.mkdir(mp4_out)
        except Exception:
            pass


if __name__ == '__main__':
    run()
