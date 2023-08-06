"""
pypsxlib: Unofficial python library for reading and writing Agisoft Photoscan/Metashape psx project files.

Copyright (c) 2019 Luke Miller

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@&&@@@@@@@%%@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@%@@@@@@@@@(/****%@@@@@@@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@&@@@@@&/*,,,,,,*&@@@@@@@@@@@@@@@@@@@@@@@@&@@@@@@@@@*//*****/**//*/#@@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@@@@,(*,,,,,,,,*(,,,,,/*,,,,,,,(@@@@@@@@@@@@@@@@@@@@@@@@&*(%(//****************/@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@@@,,,,***#*,,,,,,,,,,,,,,,,,,,,,*@@@@@@@@@@@@@@@@&@@@@@(********************/(***@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@@*,,,,*,*,,*/**(%%&&@@@@@@@@@#/**@@@@@@@@@@@@@@@&@@@@@************##%******(**(.*(@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@@#,,,,*,*,,*@(((((((((((((((((%/*@@@@@@@@@@@@@@@@@@@@/*/*%%**/****/#/*****(*/./**&@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@%%@,,,,*,*,,,#(((((((((((((((((@**@@@@@@@@@@@@@@@@@@@@**(&%%/***/&%&(**@&//(***#*@@@@@@@@@@@@@@@
@@@@@@@@@@@@@&@@@@@@@@&@,,,,*,*,*,#(((((((((((((((((@**@@@@@@@@@@@@&@@@@@@@#**(/(//***(%#,/@*#/@/*/(***@@@@@@@@@@@@@@
@@@@@@@@@@@@@&@@@@@@@@@@,,,,*,*,*,%(((((((((((((((((@/*@@@@@@@@@@@@@@@@@@@(**#/****//**%%.(%@*(***@@*****&@@@@@@@@@@@@@
@@@@@@@@@@@@@@@&@@@@@@@@,,,,*,,*,*&(((((((((((((((((@/*@@@@@@@@@@@@@@@@@@@*****(@@@@@@/****//@*****@@****(@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@&&@@@@,,,,,*,*,*@(((((((((((((((((@/*@@@@@@@@@@%@@@@@@@@*****@@@@@@@@((#@@@%******@@/**/@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@@@*,,,,*,*,/@(((((((((((((((((%/*@@@@@@@@&@@@@@@@@@@****@@@@@@@@#**&**&@@******@@@#@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@@@/,,,,*,*,,(/%@&&%%%&@@@@@%/*/,*&&&@@@@&@@@@@@%@@@@@//@@@@@@@@@&/%*(%%@@@@&/**@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@@@(*#,,/,(,,,,,*********,,,,,,,,*@@@@@@&@@@@@@@@@&@@@@@@@@@@@@@@%&%%&@%&@@@@/**@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@@@((,#*(,%//*********,**////////(@@@@@@@@@@@@&@@@@&@@@@@%@@@@@%%%@@@@@%%%%&@***(@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@@@@/#**#,*,,,,,,,,,,,,,,,,,,,,,,(@@@@@&@@@@@%@@@@@@@@@@@*/&@&%%%%%@@@%%%%%%@****@%@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@@@@@@/(#,,*&@&%&%%#%&&@@&&&@@@@@@@@@@@@@@@@@&&@@&@@@@%**&%%%%%%%%@&%%%%%%@*****(&@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@@@@@@%(#*,,,,,,,,,,,,,,,,,,,,,(/@@@@@@@&@@@@@%@@@@@@@@@***@%%%%%%%%@@&%%%%%@*****//@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@@@@@/////%////((#@***##%..&(/@///@@@@@@@@@&&@@@@@@@@@@&***#%%%%%%@@@@@@@@@@&%*****/@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@@@///////&////(...(%%/....*///(#///@@@@@@@@@@@@@@@@@@@/***/@%%%@@@@@@@@@@@%%@&****/@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@@*/#////////(//*..*,./.....(%//((***@@@@@@@@@@@@@@@@@&****@@%%%&@@@@@@@@@%%%@@@/**@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@%(@***#///////(@...........&////%*,(@@@@@@@@@@@@@@@@#****@@@@%%%@@@@@@@@&%%%@@@@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@%,,,,*/**%/////#*............&///#,***&@@@@@@@@@@@@@(****@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@,,,,,,,@*&////(&,,(/((/,......(//%,,,,,,#@@@@@@@@@@@***/@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@/*,,,*,@//////#@................%#/%,,,,,,,#@@@@@@@@***@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@&,,,,,@@/////////.................%%//*,,,,,,,,,,*%***/@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@(,,,,,*@(#/#(//(@................&(#%(@@@@@,,,,,,,%%#**@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@(,,,,,*@#//////#@&%(&@&*...*#@(((%((&(@@@@**/**,#%*%@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@*,,,,*@@@@&%@@@%(((((((((((((#(#(((((#%(#%@@//#%%#*#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@#,,,,*@@@@@(((((((((((((((%%@#(%(&(((((((/((%@@@@@@@&/%#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@/**,,,,,*@@@@@%(((((((((((((((((((#(((((((((%%(((@@@@@@@@@@@@@@@@@@**/#&@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@@@@@@@@@%%*(/,,,(,*@@@@@@@(((((((((((((((((((@((((((((((((((@@@@@@@@@@@@@@@@///(%#***(/%#(/(///%@@@@@@@@@@@@@@@@@@@@@@
@@@@@@@@@@(**&@@@@@@@@@@@@@@@@#((((((((((((((((@((((((((%#%&(*@@@@@@@@@@@@@@&////////#////%/***/@@@@@@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@&((((((((((((#((&@((((((/,,,,,@@@@@@@@@@@@@@/*******/&////////@@@@@@@@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@%(#(#%(*%%%@@@#((((##%&@@@@@@@@@@@@@*********/****///#@@@@@@@@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@#((((((((#/,,,/@@@@@&(((%%%%(@@@@@@@@@@@@@/,......%.,*****@@@@@@@@@@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@#(((((((((((,(@@@@@@@((((((((%@@@@@@@@@@@@@.......,&...**@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@%((((((((((((((#@@@@@@@@@@(((((#((#@@@@@@@@@@@@@@...*****%...@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@@@@@@@(/@(((((((((((@@@@@@@@@@@@@((((&&@@((@@@@@@@@@@@@@@******//(*&@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@@@@@@@///(#((((&@@@@@@@@@@@@@@@@@@&@(#(//((@@@@@@@@@@@@@@@///////(#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@@@@&*,,,%/(/#@@@@@@@@@@@@@@@@@@@@@%((#/,*(/%,,,(,,*@@@@@@@@(///***@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@@(/%*/*,#/@@@@@@@@@@@@@@@@@@@@@@@@@@@*,*/#*,,,#,,,%&@@@@@@@@%*****.@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@@@&/(,*(**(@@@@@@@@@@@@@@@@@@@@@@@@@@@###(((///#/@@@@@@@@@@@#%...../@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@@@@@%#,,,,,%@@@@@@@@@@@@@@@@@@@@@@@@@@(//@%/%&%@@@@@@@@@@@@@..,*.***@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@@@@@&/**,,,,/@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@(*,..#***//@@@@@@@@@@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@@@@@@@//#*,,#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@****@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@&@@@/@(&/@#*.*@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@(**&@@@@@@#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@**@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@&@@@@@&%@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@&&@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
"""

import copy
import os.path
import warnings
import xml.etree.ElementTree as ET

from PIL import Image
from pathlib import Path
from zipfile import ZipFile
import numpy as np
from numpy.linalg import inv, norm

from pypsxlib import array2str, str2matrix, str2array, matrix2str, Masks, __version_psx__, Project, Sensor, ChunkCamera, Chunk, Frame, FrameCamera, Resolution, Photo


def parse_xml(cwd, root, project_name):
    warnings.warn("`parse_xml` is a provisional function and may not exist in future versions.")
    # print out a psx project (call from parse_xmlfile)
    depth = " " * len(Path(cwd).parts)
    if root.text:
        print(depth, root.tag, root.attrib, root.text)
    else:
        print(depth, root.tag, root.attrib)

    if "path" in root.attrib:
        fname = root.attrib["path"]
        fname = fname.replace("{projectname}", project_name)
        fpath = Path(cwd, fname)
        if fpath.suffix == ".zip":
            print(depth, "z--", fpath.name)
            with ZipFile(fpath, 'r') as zf:
                for chunkfname in zf.filelist:
                    chunkfpath = Path(chunkfname.filename)
                    if chunkfpath.suffix == ".xml":
                        xmlstr = zf.read(chunkfname)
                        print(depth, "--z", chunkfpath.name)
                        cwd = Path(cwd).joinpath(fpath.parent)
                        xml = ET.fromstring(xmlstr)
                        # xmlprettyprint(xml)
                        parse_xml(cwd, xml, project_name)
                    else:
                        print(depth, "FILE IN ZIP", chunkfpath)
                        print()
        else:
            print(depth, "FILE", fpath)
            print()

    for child in root:
        parse_xml(cwd, child, project_name)


def parse_xmlfile(cwd, fname=None, project_name=None):
    warnings.warn("`parse_xmlfile` is a provisional function and may not exist in future versions.")

    # print out a psx project
    import xml.etree.ElementTree as ET
    if not fname:
        project_name = Path(cwd).stem
        fname = cwd
        cwd = Path(cwd).parent.as_posix()
    print("---", Path(fname).name)
    tree = ET.parse(fname)
    root = tree.getroot()
    parse_xml(cwd, root, project_name)


def copy_cameras_to_chunk(project: Project, from_chunk_id, to_chunk_id, camera_ids=[]):
    """
    Utility to copy images to other chunks, along with their masks.

    Useful for when you have "static" images you know are good and can work across multiple chunks
    """
    # add to chunk.cameras
    # add to frame.cameras
    # add to thumbnails
    # add to sensors
    # add to masks
    warnings.warn("`copy_cameras_to_chunk` is definitely a provisional function and will not exist in future versions.")

    from_chunk = project.apps[0].documents[0].chunks[from_chunk_id]
    from_frame = from_chunk.frames[0]

    to_chunk = project.apps[0].documents[0].chunks[to_chunk_id]
    to_frame = to_chunk.frames[0]

    for camera_id in camera_ids:
        new_id = len(to_chunk.cameras)
        # copy the chunk details
        chunkCamera = None
        for cc in from_chunk.cameras:
            if cc.id == camera_id:
                chunkCamera = cc
                break

        if not chunkCamera:
            warnings.warn(f"Unable to find {camera_id} in chunk cameras")
            return
        nc = copy.deepcopy(chunkCamera)
        nc.id = new_id
        to_chunk.cameras.append(nc)

        # copy the sensor details

        # copy the frame details
        frameCamera = None
        for fc in from_frame.cameras:
            if fc.camera_id == camera_id:
                frameCamera = fc
                break

        if not frameCamera:
            warnings.warn(f"Unable to find {camera_id} in frame cameras")
            return
        nc = copy.deepcopy(frameCamera)
        nc.camera_id = new_id
        to_frame.cameras.append(nc)

        # copy thumbnail details

        # check for a mask
        try:
            index = from_frame.masks.camera_ids.index(camera_id)
        except ValueError:
            continue
        # there is a mask, so add it to the new chunk too.
        if not to_frame.masks:
            to_frame.masks = Masks(version=__version_psx__)
            to_frame.masks._mask_data = {}
        if camera_id in from_frame.masks.camera_ids:
            to_frame.masks.camera_ids.append(new_id)
            mask_path = from_frame.masks.mask_paths[index]
            to_frame.masks.mask_paths.append(mask_path)
            data = copy.copy(from_frame.masks._mask_data[mask_path])
            to_frame.masks._mask_data[mask_path] = data
        print("finished copy for ", camera_id, " as ", new_id)


def duplicate_chunk(project: Project, chunk_id: int, number_of_repeats:int=1):
    """ Copy a chunk and add it to the end of the document """
    chunk = project.document.chunks[chunk_id]
    for i in range(number_of_repeats):
        new_chunk = copy.deepcopy(chunk)
        project.document.chunks.append(new_chunk)


def merge_chunk(project: Project, source_chunk_id: int, destination_chunk_id: int,
                merge_mesh_meta=True,
                merge_mesh_path=True,
                merge_cameras=True,
                merge_photo_meta=True,
                merge_photo_path=True):
    """ Merge the details of a chunk with another """
    warnings.warn("incomplete, do not use")
    src_chunk = project.document.chunks[source_chunk_id]
    dest_chunk = project.document.chunks[destination_chunk_id]
    for camera in src_chunk.cameras:
        dest_camera_id = dest_chunk.get_camera_index_by_label(camera.label)
        if dest_camera_id is not None:
            if merge_cameras:
                dest_chunk.cameras[dest_camera_id] = copy.deepcopy(camera)
        else:  # new camera
            pass


def replace_chunk_but_keep_photo_paths(project: Project, source_chunk_id: int, destination_chunk_id: int):
    """ Replace a chunk with a copy of another chunk, but keep the photos from the original chunk
        Useful if you have chunks with identical fixed cameras but changing photos (eg a video rig)
    """
    src_chunk = project.document.chunks[source_chunk_id]
    dest_chunk = project.document.chunks[destination_chunk_id]
    new_chunk = copy.deepcopy(src_chunk)
    warnings.warn("this is a very dumb substitution, assumes identical frame cameras are at the start of the list")
    warnings.warn("And the resulting PSX MUST be saved at the same directory depth for the relative file paths to work")
    new_chunk.label = dest_chunk.label
    new_chunk.next_id = dest_chunk.next_id
    for findex, new_frame in enumerate(new_chunk.frames):
        old_frame = dest_chunk.frames[findex]
        # go through the old cameras and copy their paths to the new
        for index, camera in enumerate(old_frame.cameras):
            replace_camera = new_frame.get_camera_by_id(camera.camera_id)
            if replace_camera:
                old_path = camera.photo.path
                print(f"  {old_frame.name}.{replace_camera.camera_id} replacing {replace_camera.photo.path} with {old_path}")
                replace_camera.photo.path = old_path

    project.document.chunks[destination_chunk_id] = new_chunk


def replace_chunk_photos(project: Project, chunk_id: int, new_photos: list):
    """ Replace the file paths for a photos in a chunk (good for switching textures on a model) """
    """ WORK IN PROGRESS"""
    chunk = project.document.chunks[chunk_id]
    if len(chunk.frames) > 1:
        warnings.warn(f"replace chunk only works on a single frame "
                      "Please open an issue at https://gitlab.com/dodgyville/pypsxlib/issues")

    # XXX: does not take into account relative paths.
    # XXX: This must be fixed.
    for frames in chunk.frames:
        for index, camera in enumerate(frames.cameras):
            abspath = Path(project.psx_directory,  f"0/{chunk_id}", camera.photo.path).absolute().resolve()
            chunkpath = Path(project.psx_directory, f"0/{chunk_id}").absolute().resolve()
            new_abspath = Path(Path(".").absolute(), new_photos[index])
            commonpath = Path(os.path.commonpath([abspath, new_abspath]))
            # we want a path that's relative to the chunk dir
            warnings.warn(f"replace chunk uses absolute paths to images instead of relative"
                "Please open an issue at https://gitlab.com/dodgyville/pypsxlib/issues")
            camera.photo.path = new_abspath.as_posix() #new_abspath.relative_to(abspath)


def get_image_dimensions(path: Path):
    im = Image.open(path)
    return im.size

def add_photo_to_chunk(project: Project, chunk_id: int, photo_filename: str):
    warnings.warn("This does not play well with relative paths, use absolute paths")
    psx_chunk = project.document.chunks[chunk_id]
    # will add new camera to first frame cameras
    psx_frame = psx_chunk.frames[0]
    psx_sensor = Sensor(data_type="uint8", type="frame")
    w,h = get_image_dimensions(photo_filename)
    print(" Chunk sensor w,h: ", w, h)
    psx_sensor.resolution = Resolution(width=w, height=h)
    psx_sensor.bands.extend([
        "Red",
        "Green",
        "Blue",
    ])

    psx_photo_index = len(psx_frame.cameras)

    psx_frame_camera = FrameCamera(camera_id=psx_photo_index)
    photo_path = Path(photo_filename)
    label = photo_path.stem
    psx_chunk_camera = ChunkCamera(id=psx_photo_index, sensor_id=len(psx_chunk.sensors), label=label)
    psx_photo = psx_frame_camera.photo = Photo()
    psx_photo.sensor_id = len(psx_chunk.sensors)
    psx_photo.path = photo_path.absolute().as_posix()
    psx_photo.generate_meta()

    psx_chunk.sensors.append(psx_sensor)
    psx_frame.cameras.append(psx_frame_camera)
    psx_chunk.cameras.append(psx_chunk_camera)
    psx_photo_index += 1
    return True

def add_photos_to_chunk(project: Project, chunk_id: int, photo_filenames: list):
    """ take a list of file paths and add them to a chunk as new photos
        Uses the same sensor for all new photos.
        All photos must have the same dimensions (and ideally come from the same camera)
        For a different sensor per photo, use add_photo_chunk

        Good for adding a bunch of static photos to a frame generated from videos
    """
    warnings.warn("This does not play well with relative paths, use absolute paths")
    psx_chunk = project.document.chunks[chunk_id]
    # will add new camera to first frame cameras
    psx_frame = psx_chunk.frames[0]
    psx_sensor = Sensor(data_type="uint8", type="frame")
    w,h = get_image_dimensions(photo_filenames[0])
    psx_sensor.resolution = Resolution(width=w, height=h)
    psx_sensor.bands.extend([
        "Red",
        "Green",
        "Blue",
    ])

    for photo_filename in photo_filenames:
        psx_photo_index = len(psx_frame.cameras)
        psx_frame_camera = FrameCamera(camera_id=psx_photo_index)
        photo_path = Path(photo_filename)
        label = photo_path.stem
        psx_chunk_camera = ChunkCamera(id=psx_photo_index, sensor_id=len(psx_chunk.sensors), label=label)
        psx_photo = psx_frame_camera.photo = Photo()
        psx_photo.sensor_id = len(psx_chunk.sensors)
        psx_photo.path = photo_path.absolute().as_posix()
        psx_photo.generate_meta()
        psx_frame.cameras.append(psx_frame_camera)
        psx_chunk.cameras.append(psx_chunk_camera)

    psx_chunk.sensors.append(psx_sensor)
    psx_photo_index += 1
    return True


def add_photos_to_all_chunks(project: Project, photo_filenames: list):
    for i, chunk in enumerate(project.document.chunks):
        add_photos_to_chunk(project, i, photo_filenames)


def make_absolute(project: Project):
    """ Convert image files to absolute paths
        Useful when saving project to a new location
    """
    for chunk_index, psx_chunk in enumerate(project.document.chunks):
        for frame_index, psx_frame in enumerate(psx_chunk.frames):
            for index, camera in enumerate(psx_frame.cameras):
                new_abspath = Path(Path(".").absolute(), camera.photo.path)
                # we want a path that's relative to the chunk dir
                project_directory = project.psx_directory
                frame_directory = Path(project_directory) / str(chunk_index) / str(frame_index)
                new_abspath = Path(Path(frame_directory).absolute(), camera.photo.path)
                camera.photo.path = new_abspath.as_posix()


def copy_camera_transforms_from_chunk_to_chunk(project: Project, source_chunk_id: int, destination_chunk_id: int):
    """
    Copy camera transform from one chunk to another chunk.
    Assumes other chunk cameras are same cameras as source chunk.
    Good for duplicating camera transforms to other chunks when you know cameras are all in the same position (eg video camera rig)

      <transform>-6.0888642049114705e-02 2.9530005089950240e-01 -9.5346235017863490e-01 3.4215475288685893e+00 1.9052132026580237e-02 -9.5471685741483758e-01 -2.9690526844968312e-01 6.2355554759368004e-01 -9.9796271951143367e-01 -3.6243649191105870e-02 5.2505317432194443e-02 -4.1769471234769924e+00 0 0 0 1</transform>
      <rotation_covariance>2.7036774367035179e-05 -7.3513989792594117e-05 2.8967552678175575e-06 -7.3513989792594131e-05 2.2275417540986944e-04 -1.3310478132970499e-05 2.8967552678175592e-06 -1.3310478132970506e-05 1.9048740061018637e-06</rotation_covariance>
      <location_covariance>1.1146502116338337e-03 1.7634026625505302e-05 4.4980447388441326e-04 1.7634026625505302e-05 6.6619010157494224e-04 2.9021855411393133e-03 4.4980447388441326e-04 2.9021855411393133e-03 1.3947041311288469e-02</location_covariance>
    """
    # XXXX NOT DONE YET, THIS IS A COPY OF AN ABOVE FUNCTION
    src_chunk = project.document.chunks[source_chunk_id]
    dest_chunk = project.document.chunks[destination_chunk_id]
    new_chunk = copy.deepcopy(src_chunk)
    warnings.warn("this is a very dumb substitution, assumes identical frame cameras are at the start of the list")
    warnings.warn("And the resulting PSX MUST be saved at the same directory depth for the relative file paths to work")
    new_chunk.label = dest_chunk.label
    new_chunk.next_id = dest_chunk.next_id
    for findex, new_frame in enumerate(new_chunk.frames):
        old_frame = dest_chunk.frames[findex]
        # go through the old cameras and copy their paths to the new
        for index, camera in enumerate(old_frame.cameras):
            replace_camera = new_frame.get_camera_by_id(camera.camera_id)
            if replace_camera:
                old_path = camera.photo.path
                print(f"  {old_frame.name}.{replace_camera.camera_id} replacing {replace_camera.photo.path} with {old_path}")
                replace_camera.photo.path = old_path

def copy_bounding_box_region_from_chunk_to_chunk(project: Project, source_chunk_id: int, destination_chunk_id: int):
    """
    Copy bounding box region from one chunk to another
    Good for duplicating region when you know the shape is roughly the same in all the others (eg video camera rig subject)

  <region>
    <center>6.2389256535366522e-01 -3.2937218996410289e+00 -8.0991465932905946e+00</center>
    <size>1.3171844713394199e+01 2.1981561592270410e+01 1.1718569686539453e+01</size>
    <R>-9.9887454747853144e-01 4.7430353146049806e-02 3.8081219750390778e-22 -4.7430353146049799e-02 -9.9887454747853144e-01 -3.7684139246935819e-22 3.6250989113115023e-22 -3.9447933238394345e-22 1</R>
  </region>
      """
    src_chunk = project.document.chunks[source_chunk_id]
    dest_chunk = project.document.chunks[destination_chunk_id]
    dest_chunk.region = copy.deepcopy(src_chunk.region)


def propogate_camera_transforms_across_all_chunks(project: Project, source_chunk_id: int):
    """
    Copy camera transform from one chunk to another chunk.
    Assumes other chunk cameras are same cameras as source chunk.
    Good for duplicating camera transforms to other chunks when you know cameras are all in the same position (eg video camera rig)

      <transform>-6.0888642049114705e-02 2.9530005089950240e-01 -9.5346235017863490e-01 3.4215475288685893e+00 1.9052132026580237e-02 -9.5471685741483758e-01 -2.9690526844968312e-01 6.2355554759368004e-01 -9.9796271951143367e-01 -3.6243649191105870e-02 5.2505317432194443e-02 -4.1769471234769924e+00 0 0 0 1</transform>
      <rotation_covariance>2.7036774367035179e-05 -7.3513989792594117e-05 2.8967552678175575e-06 -7.3513989792594131e-05 2.2275417540986944e-04 -1.3310478132970499e-05 2.8967552678175592e-06 -1.3310478132970506e-05 1.9048740061018637e-06</rotation_covariance>
      <location_covariance>1.1146502116338337e-03 1.7634026625505302e-05 4.4980447388441326e-04 1.7634026625505302e-05 6.6619010157494224e-04 2.9021855411393133e-03 4.4980447388441326e-04 2.9021855411393133e-03 1.3947041311288469e-02</location_covariance>
    """
    warnings.warn("Assumes chunk cameras are in same order across all chunks")
    src_chunk = project.document.chunks[source_chunk_id]
    for chunk in project.document.chunks:
        if src_chunk == chunk:
            continue
        for i, camera in enumerate(src_chunk.cameras):
            chunk.cameras[i].transform = copy.copy(camera.transform)
            chunk.cameras[i].rotation_covariance = copy.copy(camera.rotation_covariance)
            chunk.cameras[i].location_covariance = copy.copy(camera.location_covariance)


def propogate_bounding_box_across_all_chunks(project: Project, source_chunk_id: int, use_chunk_transform=True):
    src_chunk = project.document.chunks[source_chunk_id]
    for i, chunk in enumerate(project.document.chunks):
        if src_chunk == chunk:
            continue
        if use_chunk_transform:
            if not chunk.transform:
                print("Chunk",i,"has no transform so doing basic copy")
                project.document.chunks[i].region = copy.deepcopy(src_chunk.region)
                continue
            src_region_center = src_chunk.region.center
            src_region_size = src_chunk.region.size
            src_scale = float(src_chunk.transform.scale.value)
            src_translation = src_chunk.transform.translation.value

            orig_region_center = str2array(copy.copy(src_region_center))
            orig_region_size = str2array(copy.copy(src_region_size))
            orig_scale = float(src_scale)
            orig_translation = str2array(copy.copy(src_translation))

            new_scale = float(chunk.transform.scale.value)
            new_translation = str2array(copy.copy(chunk.transform.translation.value))

            # work out the difference in the new chunk's scale and translation to the source chunk
            delta_scale = new_scale / orig_scale
            delta_translation = new_translation - orig_translation
            # then apply that different to the sourcce region to create a region for the new chunk
            new_region_center = orig_region_center + delta_translation
            new_region_size = orig_region_size * delta_scale

            project.document.chunks[i].region.center = np.array2string(new_region_center).strip("[]")
            project.document.chunks[i].region.size = np.array2string(new_region_size).strip("[]")
        else:
            project.document.chunks[i].region = copy.deepcopy(src_chunk.region)



def propogate_bounding_box_across_all_chunks2(project: Project, source_chunk_id: int):
    src_chunk = project.document.chunks[source_chunk_id]

    src_chunk.transform
    T0 = src_chunk.transform.matrix()

    region = copy.deepcopy(src_chunk.region)
    R0 = str2matrix(region.R, (3,3))

    C0 = str2array(region.center +" 1.0")  # pad vector
    s0 = str2array(region.size)

    for i, chunk in enumerate(project.document.chunks):
        if src_chunk == chunk:
            print("skip",i)
            continue

        T = inv(chunk.transform.matrix()) * T0

        R = np.matrix([[T[0, 0], T[0, 1], T[0, 2]],
                       [T[1, 0], T[1, 1], T[1, 2]],
                       [T[2, 0], T[2, 1], T[2, 2]]])

        scale = norm(R[0])
        #R = R * (1 / scale)

#        region.R = matrix2str(R * R0)
        region.R = matrix2str(R0)
        c = T * C0
        #c = T.mulp(C0)
        region.center = array2str(c[:3])  # chop off padded vector var
        region.size = array2str(s0 * scale / 1.)
        project.document.chunks[i].region = region


def propogate_transform_across_all_chunks(project: Project, source_chunk_id: int):
    src_chunk = project.document.chunks[source_chunk_id]
    for chunk in project.document.chunks:
        if src_chunk == chunk:
            continue
        chunk.transform = copy.deepcopy(src_chunk.transform)

def align_chunks_by_camera_transforms(project: Project, source_chunk_id: int):
    """
    Transform a camera
    """


def generate_chunks_from_first_chunk_and_photos(project: Project, photo_frames: list):
    """
    Assume the first chunk has a mesh and cameras
    For each list of photos in the photo_frames, duplicate the first chunk and replace the photos.

    """
    for new_photos in photo_frames:
        duplicate_chunk(project, 0)
        chunk_id = len(project.document.chunks) - 1
        replace_chunk_photos(project, chunk_id, new_photos)

def chunk_transform_copy(project: Project, source_chunk_id: int, destination_chunk_id: int):
    src_chunk = project.document.chunks[source_chunk_id]
    dest_chunk = project.document.chunks[destination_chunk_id]

    dest_chunk.transform = copy.deepcopy(src_chunk.transform)


def chunk_region_copy(project: Project, source_chunk_id: int, destination_chunk_id: int):
    src_chunk = project.document.chunks[source_chunk_id]
    dest_chunk = project.document.chunks[destination_chunk_id]

    dest_chunk.region = copy.deepcopy(src_chunk.region)



def bounding_box_scale(project: Project, source_chunk_id: int, scale: np.array = np.array([1.0, 1.0, 1.0])):
    src_chunk = project.document.chunks[source_chunk_id]
    src_chunk.region.size *= scale
    #import pdb; pdb.set-trace()
    #project.document.chunks[i].region.size *= scale

def align_bounding_box_scale(project: Project, source_chunk_id: int, destination_chunk_id: int):
    # take two chunks and align the scale of the second chunk's bounding box to the scale of the first """
    src_chunk = project.document.chunks[source_chunk_id]
    dest_chunk = project.document.chunks[destination_chunk_id]

    b1 = b2 = None

    if src_chunk.transform:
        b1 = src_chunk.transform.scale.value
    if dest_chunk.transform:
        b2 = dest_chunk.transform.scale.value
    else:
        print(f"Chunk {destination_chunk_id} has no transform")

    if b1 and b2:
        scale_factor = b1 / b2
        dest_chunk.region.size *= scale_factor



def offset_bounding_box(project: Project, source_chunk_id: int, destination_chunk_id: int):
    # offset bounding box by difference in src and destination transform
    src_chunk = project.document.chunks[source_chunk_id]
    dest_chunk = project.document.chunks[destination_chunk_id]

    offset = src_chunk.transform.translation.value - dest_chunk.transform.translation.value
    dest_chunk.region.center += offset



def fast_disable_cameras(path: str, camera_label_wildcard: str = "FJIMG_*"):
    load_psx