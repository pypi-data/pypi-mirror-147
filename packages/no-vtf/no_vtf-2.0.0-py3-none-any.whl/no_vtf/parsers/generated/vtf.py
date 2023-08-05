# This is a generated file! Please edit source .ksy file and use kaitai-struct-compiler to rebuild

from pkg_resources import parse_version
import kaitaistruct
from kaitaistruct import KaitaiStruct, KaitaiStream, BytesIO
from enum import Enum


if parse_version(kaitaistruct.__version__) < parse_version('0.9'):
    raise Exception("Incompatible Kaitai Struct Python API: 0.9 or later is required, but you have %s" % (kaitaistruct.__version__))

class Vtf(KaitaiStruct):
    """
    .. seealso::
       Source - https://developer.valvesoftware.com/wiki/Valve_Texture_Format
    
    
    .. seealso::
       Source - https://github.com/NeilJed/VTFLib
    """

    class ImageFormat(Enum):
        rgba8888 = 0
        abgr8888 = 1
        rgb888 = 2
        bgr888 = 3
        rgb565 = 4
        i8 = 5
        ia88 = 6
        p8 = 7
        a8 = 8
        rgb888_bluescreen = 9
        bgr888_bluescreen = 10
        argb8888 = 11
        bgra8888 = 12
        dxt1 = 13
        dxt3 = 14
        dxt5 = 15
        bgrx8888 = 16
        bgr565 = 17
        bgrx5551 = 18
        bgra4444 = 19
        dxt1_onebitalpha = 20
        bgra5551 = 21
        uv88 = 22
        uvwq8888 = 23
        rgba16161616f = 24
        rgba16161616 = 25
        uvlx8888 = 26
        none = 4294967295

    class ResourceTag(Enum):
        low_res_image = 65536
        particle_sheet = 1048576
        high_res_image = 3145728
        crc = 4411971
        key_values_data = 4937284
        lod_control = 5001028
        extended_flags = 5526351
    def __init__(self, _io, _parent=None, _root=None):
        self._io = _io
        self._parent = _parent
        self._root = _root if _root else self
        self._read()

    def _read(self):
        self.header = Vtf.Header(self._io, self, self._root)

    class Body(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            if  ((self._root.header.base.version.minor < 3) and (self._root.header.v7_0.low_res_image_format != Vtf.ImageFormat.none) and (self._root.header.v7_0.low_res_image_width != 0) and (self._root.header.v7_0.low_res_image_height != 0)) :
                self.low_res_image = Vtf.Image(self._root.header.v7_0.low_res_image_width, self._root.header.v7_0.low_res_image_height, self._root.header.v7_0.low_res_image_format, self._io, self, self._root)

            if  ((self._root.header.base.version.minor < 3) and (self._root.header.v7_0.high_res_image_format != Vtf.ImageFormat.none)) :
                self.high_res_image = Vtf.HighResImage(self._io, self, self._root)

            if self._root.header.base.version.minor >= 3:
                self.resources = [None] * (self._root.header.logical.num_resources)
                for i in range(self._root.header.logical.num_resources):
                    self.resources[i] = Vtf.Resource(self._io, self, self._root)




    class Image(KaitaiStruct):
        def __init__(self, logical_width, logical_height, image_format, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self.logical_width = logical_width
            self.logical_height = logical_height
            self.image_format = image_format
            self._read()

        def _read(self):
            self.image_data = self._io.read_bytes(((self.physical_width * self.physical_height) * self.bpp) // 8)

        @property
        def image_format_to_bpp(self):
            if hasattr(self, '_m_image_format_to_bpp'):
                return self._m_image_format_to_bpp if hasattr(self, '_m_image_format_to_bpp') else None

            self._m_image_format_to_bpp = Vtf.ImageFormatToBpp(self.image_format, self._io, self, self._root)
            return self._m_image_format_to_bpp if hasattr(self, '_m_image_format_to_bpp') else None

        @property
        def physical_height(self):
            if hasattr(self, '_m_physical_height'):
                return self._m_physical_height if hasattr(self, '_m_physical_height') else None

            self._m_physical_height = (self.logical_height if not (self.is_compressed) else (self.logical_height if self.logical_height >= 4 else 4))
            return self._m_physical_height if hasattr(self, '_m_physical_height') else None

        @property
        def is_compressed(self):
            if hasattr(self, '_m_is_compressed'):
                return self._m_is_compressed if hasattr(self, '_m_is_compressed') else None

            self._m_is_compressed = self.image_format_to_is_compressed.is_compressed_container.value
            return self._m_is_compressed if hasattr(self, '_m_is_compressed') else None

        @property
        def bpp(self):
            if hasattr(self, '_m_bpp'):
                return self._m_bpp if hasattr(self, '_m_bpp') else None

            self._m_bpp = self.image_format_to_bpp.bpp_container.value
            return self._m_bpp if hasattr(self, '_m_bpp') else None

        @property
        def physical_width(self):
            if hasattr(self, '_m_physical_width'):
                return self._m_physical_width if hasattr(self, '_m_physical_width') else None

            self._m_physical_width = (self.logical_width if not (self.is_compressed) else (self.logical_width if self.logical_width >= 4 else 4))
            return self._m_physical_width if hasattr(self, '_m_physical_width') else None

        @property
        def image_format_to_is_compressed(self):
            if hasattr(self, '_m_image_format_to_is_compressed'):
                return self._m_image_format_to_is_compressed if hasattr(self, '_m_image_format_to_is_compressed') else None

            self._m_image_format_to_is_compressed = Vtf.ImageFormatToIsCompressed(self.image_format, self._io, self, self._root)
            return self._m_image_format_to_is_compressed if hasattr(self, '_m_image_format_to_is_compressed') else None


    class ImageFace(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.image_slices = [None] * (self._parent.num_slices)
            for i in range(self._parent.num_slices):
                self.image_slices[i] = Vtf.Image(self._parent.width, self._parent.height, self._parent.image_format, self._io, self._parent, self._root)



    class ImageFormatToIsCompressed(KaitaiStruct):
        def __init__(self, image_format, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self.image_format = image_format
            self._read()

        def _read(self):
            pass

        @property
        def is_compressed_container(self):
            if hasattr(self, '_m_is_compressed_container'):
                return self._m_is_compressed_container if hasattr(self, '_m_is_compressed_container') else None

            _on = self.image_format
            if _on == Vtf.ImageFormat.dxt5:
                self._m_is_compressed_container = Vtf.B1Container(True, self._io, self, self._root)
            elif _on == Vtf.ImageFormat.dxt1_onebitalpha:
                self._m_is_compressed_container = Vtf.B1Container(True, self._io, self, self._root)
            elif _on == Vtf.ImageFormat.dxt1:
                self._m_is_compressed_container = Vtf.B1Container(True, self._io, self, self._root)
            elif _on == Vtf.ImageFormat.dxt3:
                self._m_is_compressed_container = Vtf.B1Container(True, self._io, self, self._root)
            else:
                self._m_is_compressed_container = Vtf.B1Container(False, self._io, self, self._root)
            return self._m_is_compressed_container if hasattr(self, '_m_is_compressed_container') else None


    class HeaderV72(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.num_slices = self._io.read_u2le()
            if not self.num_slices >= 1:
                raise kaitaistruct.ValidationLessThanError(1, self.num_slices, self._io, u"/types/header_v7_2/seq/0")


    class HeaderBase(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.magic = self._io.read_bytes(4)
            if not self.magic == b"\x56\x54\x46\x00":
                raise kaitaistruct.ValidationNotEqualError(b"\x56\x54\x46\x00", self.magic, self._io, u"/types/header_base/seq/0")
            self.version = Vtf.Version(self._io, self, self._root)
            self.header_size = self._io.read_u4le()


    class HeaderFlags(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            pass

        @property
        def onebitalpha(self):
            if hasattr(self, '_m_onebitalpha'):
                return self._m_onebitalpha if hasattr(self, '_m_onebitalpha') else None

            self._m_onebitalpha = (True if (self._root.header.v7_0.flags & 4096) != 0 else False)
            return self._m_onebitalpha if hasattr(self, '_m_onebitalpha') else None

        @property
        def eightbitalpha(self):
            if hasattr(self, '_m_eightbitalpha'):
                return self._m_eightbitalpha if hasattr(self, '_m_eightbitalpha') else None

            self._m_eightbitalpha = (True if (self._root.header.v7_0.flags & 8192) != 0 else False)
            return self._m_eightbitalpha if hasattr(self, '_m_eightbitalpha') else None

        @property
        def envmap(self):
            if hasattr(self, '_m_envmap'):
                return self._m_envmap if hasattr(self, '_m_envmap') else None

            self._m_envmap = (True if (self._root.header.v7_0.flags & 16384) != 0 else False)
            return self._m_envmap if hasattr(self, '_m_envmap') else None


    class Version(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.major = self._io.read_u4le()
            if not self.major >= 7:
                raise kaitaistruct.ValidationLessThanError(7, self.major, self._io, u"/types/version/seq/0")
            if not self.major <= 7:
                raise kaitaistruct.ValidationGreaterThanError(7, self.major, self._io, u"/types/version/seq/0")
            self.minor = self._io.read_u4le()
            if not self.minor >= 0:
                raise kaitaistruct.ValidationLessThanError(0, self.minor, self._io, u"/types/version/seq/1")
            if not self.minor <= 5:
                raise kaitaistruct.ValidationGreaterThanError(5, self.minor, self._io, u"/types/version/seq/1")


    class HighResImage(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.image_mipmaps = [None] * (self._root.header.v7_0.num_mipmaps)
            for i in range(self._root.header.v7_0.num_mipmaps):
                self.image_mipmaps[i] = Vtf.ImageMipmap(i, self._io, self, self._root)



    class ImageFrame(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.image_faces = [None] * (self._root.header.logical.num_faces)
            for i in range(self._root.header.logical.num_faces):
                self.image_faces[i] = Vtf.ImageFace(self._io, self._parent, self._root)



    class Resource(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.tag = KaitaiStream.resolve_enum(Vtf.ResourceTag, self._io.read_bits_int_be(24))
            self._io.align_to_byte()
            self.flags = self._io.read_u1()
            if  ((False) or (self.tag == Vtf.ResourceTag.low_res_image) or (self.tag == Vtf.ResourceTag.high_res_image) or (self.tag == Vtf.ResourceTag.particle_sheet) or (self.tag == Vtf.ResourceTag.key_values_data)) :
                self.ofs_resource = self._io.read_u4le()

            if  ((True) and (self.tag != Vtf.ResourceTag.low_res_image) and (self.tag != Vtf.ResourceTag.high_res_image) and (self.tag != Vtf.ResourceTag.particle_sheet) and (self.tag != Vtf.ResourceTag.key_values_data)) :
                self._unnamed3 = self._io.read_u4le()


        @property
        def high_res_image(self):
            if hasattr(self, '_m_high_res_image'):
                return self._m_high_res_image if hasattr(self, '_m_high_res_image') else None

            if  ((self.tag == Vtf.ResourceTag.high_res_image) and (self._root.header.v7_0.high_res_image_format != Vtf.ImageFormat.none)) :
                _pos = self._io.pos()
                self._io.seek(self.ofs_resource)
                self._m_high_res_image = Vtf.HighResImage(self._io, self, self._root)
                self._io.seek(_pos)

            return self._m_high_res_image if hasattr(self, '_m_high_res_image') else None

        @property
        def low_res_image(self):
            if hasattr(self, '_m_low_res_image'):
                return self._m_low_res_image if hasattr(self, '_m_low_res_image') else None

            if  ((self.tag == Vtf.ResourceTag.low_res_image) and (self._root.header.v7_0.low_res_image_format != Vtf.ImageFormat.none)) :
                _pos = self._io.pos()
                self._io.seek(self.ofs_resource)
                self._m_low_res_image = Vtf.Image(self._root.header.v7_0.low_res_image_width, self._root.header.v7_0.low_res_image_height, self._root.header.v7_0.low_res_image_format, self._io, self, self._root)
                self._io.seek(_pos)

            return self._m_low_res_image if hasattr(self, '_m_low_res_image') else None


    class Header(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.base = Vtf.HeaderBase(self._io, self, self._root)
            self.v7_0 = Vtf.HeaderV70(self._io, self, self._root)
            if self.base.version.minor >= 2:
                self.v7_2 = Vtf.HeaderV72(self._io, self, self._root)

            if self.base.version.minor >= 3:
                self.v7_3 = Vtf.HeaderV73(self._io, self, self._root)

            self.logical = Vtf.HeaderLogical(self._io, self, self._root)


    class B1Container(KaitaiStruct):
        def __init__(self, value, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self.value = value
            self._read()

        def _read(self):
            pass


    class HeaderV73(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.reserved2 = self._io.read_bytes(3)
            self.num_resources = self._io.read_u4le()
            self.reserved3 = self._io.read_bytes(8)


    class HeaderLogical(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            pass

        @property
        def flags(self):
            if hasattr(self, '_m_flags'):
                return self._m_flags if hasattr(self, '_m_flags') else None

            self._m_flags = Vtf.HeaderFlags(self._io, self, self._root)
            return self._m_flags if hasattr(self, '_m_flags') else None

        @property
        def num_faces(self):
            if hasattr(self, '_m_num_faces'):
                return self._m_num_faces if hasattr(self, '_m_num_faces') else None

            self._m_num_faces = (1 if not (self.flags.envmap) else (6 if  ((self._root.header.base.version.minor < 1) or (self._root.header.base.version.minor > 4))  else (6 if self._root.header.v7_0.first_frame == 255 else 7)))
            return self._m_num_faces if hasattr(self, '_m_num_faces') else None

        @property
        def num_slices(self):
            if hasattr(self, '_m_num_slices'):
                return self._m_num_slices if hasattr(self, '_m_num_slices') else None

            self._m_num_slices = (self._root.header.v7_2.num_slices if self._root.header.base.version.minor >= 2 else 1)
            return self._m_num_slices if hasattr(self, '_m_num_slices') else None

        @property
        def num_resources(self):
            if hasattr(self, '_m_num_resources'):
                return self._m_num_resources if hasattr(self, '_m_num_resources') else None

            self._m_num_resources = (self._root.header.v7_3.num_resources if self._root.header.base.version.minor >= 3 else 0)
            return self._m_num_resources if hasattr(self, '_m_num_resources') else None


    class HeaderV70(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.width = self._io.read_u2le()
            if not self.width >= 1:
                raise kaitaistruct.ValidationLessThanError(1, self.width, self._io, u"/types/header_v7_0/seq/0")
            self.height = self._io.read_u2le()
            if not self.height >= 1:
                raise kaitaistruct.ValidationLessThanError(1, self.height, self._io, u"/types/header_v7_0/seq/1")
            self.flags = self._io.read_u4le()
            self.num_frames = self._io.read_u2le()
            self.first_frame = self._io.read_u2le()
            self.reserved0 = self._io.read_bytes(4)
            self.reflectivity = [None] * (3)
            for i in range(3):
                self.reflectivity[i] = self._io.read_f4le()

            self.reserved1 = self._io.read_bytes(4)
            self.bumpmap_scale = self._io.read_f4le()
            self.high_res_image_format = KaitaiStream.resolve_enum(Vtf.ImageFormat, self._io.read_u4le())
            self.num_mipmaps = self._io.read_u1()
            self.low_res_image_format = KaitaiStream.resolve_enum(Vtf.ImageFormat, self._io.read_u4le())
            self.low_res_image_width = self._io.read_u1()
            self.low_res_image_height = self._io.read_u1()


    class U4Container(KaitaiStruct):
        def __init__(self, value, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self.value = value
            self._read()

        def _read(self):
            pass


    class ImageFormatToBpp(KaitaiStruct):
        def __init__(self, image_format, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self.image_format = image_format
            self._read()

        def _read(self):
            pass

        @property
        def bpp_container(self):
            if hasattr(self, '_m_bpp_container'):
                return self._m_bpp_container if hasattr(self, '_m_bpp_container') else None

            _on = self.image_format
            if _on == Vtf.ImageFormat.argb8888:
                self._m_bpp_container = Vtf.U4Container(32, self._io, self, self._root)
            elif _on == Vtf.ImageFormat.bgra8888:
                self._m_bpp_container = Vtf.U4Container(32, self._io, self, self._root)
            elif _on == Vtf.ImageFormat.abgr8888:
                self._m_bpp_container = Vtf.U4Container(32, self._io, self, self._root)
            elif _on == Vtf.ImageFormat.rgb888_bluescreen:
                self._m_bpp_container = Vtf.U4Container(24, self._io, self, self._root)
            elif _on == Vtf.ImageFormat.rgba16161616:
                self._m_bpp_container = Vtf.U4Container(64, self._io, self, self._root)
            elif _on == Vtf.ImageFormat.dxt5:
                self._m_bpp_container = Vtf.U4Container(8, self._io, self, self._root)
            elif _on == Vtf.ImageFormat.a8:
                self._m_bpp_container = Vtf.U4Container(8, self._io, self, self._root)
            elif _on == Vtf.ImageFormat.ia88:
                self._m_bpp_container = Vtf.U4Container(16, self._io, self, self._root)
            elif _on == Vtf.ImageFormat.bgr565:
                self._m_bpp_container = Vtf.U4Container(16, self._io, self, self._root)
            elif _on == Vtf.ImageFormat.uvlx8888:
                self._m_bpp_container = Vtf.U4Container(32, self._io, self, self._root)
            elif _on == Vtf.ImageFormat.bgr888:
                self._m_bpp_container = Vtf.U4Container(24, self._io, self, self._root)
            elif _on == Vtf.ImageFormat.dxt1_onebitalpha:
                self._m_bpp_container = Vtf.U4Container(4, self._io, self, self._root)
            elif _on == Vtf.ImageFormat.p8:
                self._m_bpp_container = Vtf.U4Container(8, self._io, self, self._root)
            elif _on == Vtf.ImageFormat.rgb888:
                self._m_bpp_container = Vtf.U4Container(24, self._io, self, self._root)
            elif _on == Vtf.ImageFormat.rgba8888:
                self._m_bpp_container = Vtf.U4Container(32, self._io, self, self._root)
            elif _on == Vtf.ImageFormat.i8:
                self._m_bpp_container = Vtf.U4Container(8, self._io, self, self._root)
            elif _on == Vtf.ImageFormat.bgrx5551:
                self._m_bpp_container = Vtf.U4Container(16, self._io, self, self._root)
            elif _on == Vtf.ImageFormat.uvwq8888:
                self._m_bpp_container = Vtf.U4Container(32, self._io, self, self._root)
            elif _on == Vtf.ImageFormat.bgr888_bluescreen:
                self._m_bpp_container = Vtf.U4Container(24, self._io, self, self._root)
            elif _on == Vtf.ImageFormat.bgra5551:
                self._m_bpp_container = Vtf.U4Container(16, self._io, self, self._root)
            elif _on == Vtf.ImageFormat.bgrx8888:
                self._m_bpp_container = Vtf.U4Container(32, self._io, self, self._root)
            elif _on == Vtf.ImageFormat.bgra4444:
                self._m_bpp_container = Vtf.U4Container(16, self._io, self, self._root)
            elif _on == Vtf.ImageFormat.dxt1:
                self._m_bpp_container = Vtf.U4Container(4, self._io, self, self._root)
            elif _on == Vtf.ImageFormat.dxt3:
                self._m_bpp_container = Vtf.U4Container(8, self._io, self, self._root)
            elif _on == Vtf.ImageFormat.rgb565:
                self._m_bpp_container = Vtf.U4Container(16, self._io, self, self._root)
            elif _on == Vtf.ImageFormat.uv88:
                self._m_bpp_container = Vtf.U4Container(16, self._io, self, self._root)
            elif _on == Vtf.ImageFormat.rgba16161616f:
                self._m_bpp_container = Vtf.U4Container(64, self._io, self, self._root)
            return self._m_bpp_container if hasattr(self, '_m_bpp_container') else None


    class ImageMipmap(KaitaiStruct):
        def __init__(self, mipmap_index, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self.mipmap_index = mipmap_index
            self._read()

        def _read(self):
            self.image_frames = [None] * (self._root.header.v7_0.num_frames)
            for i in range(self._root.header.v7_0.num_frames):
                self.image_frames[i] = Vtf.ImageFrame(self._io, self, self._root)


        @property
        def height(self):
            if hasattr(self, '_m_height'):
                return self._m_height if hasattr(self, '_m_height') else None

            self._m_height = ((self._root.header.v7_0.height >> self.bit_shift) if (self._root.header.v7_0.height >> self.bit_shift) >= 1 else 1)
            return self._m_height if hasattr(self, '_m_height') else None

        @property
        def image_format(self):
            if hasattr(self, '_m_image_format'):
                return self._m_image_format if hasattr(self, '_m_image_format') else None

            self._m_image_format = self._root.header.v7_0.high_res_image_format
            return self._m_image_format if hasattr(self, '_m_image_format') else None

        @property
        def num_slices(self):
            if hasattr(self, '_m_num_slices'):
                return self._m_num_slices if hasattr(self, '_m_num_slices') else None

            self._m_num_slices = ((self._root.header.logical.num_slices >> self.bit_shift) if (self._root.header.logical.num_slices >> self.bit_shift) >= 1 else 1)
            return self._m_num_slices if hasattr(self, '_m_num_slices') else None

        @property
        def width(self):
            if hasattr(self, '_m_width'):
                return self._m_width if hasattr(self, '_m_width') else None

            self._m_width = ((self._root.header.v7_0.width >> self.bit_shift) if (self._root.header.v7_0.width >> self.bit_shift) >= 1 else 1)
            return self._m_width if hasattr(self, '_m_width') else None

        @property
        def bit_shift(self):
            if hasattr(self, '_m_bit_shift'):
                return self._m_bit_shift if hasattr(self, '_m_bit_shift') else None

            self._m_bit_shift = ((self._root.header.v7_0.num_mipmaps - self.mipmap_index) - 1)
            return self._m_bit_shift if hasattr(self, '_m_bit_shift') else None


    @property
    def body(self):
        if hasattr(self, '_m_body'):
            return self._m_body if hasattr(self, '_m_body') else None

        _pos = self._io.pos()
        self._io.seek((self.header.base.header_size - (self.header.logical.num_resources * 8)))
        self._m_body = Vtf.Body(self._io, self, self._root)
        self._io.seek(_pos)
        return self._m_body if hasattr(self, '_m_body') else None


