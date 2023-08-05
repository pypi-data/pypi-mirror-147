from __future__ import annotations

from typing import List, Optional

from justpy import WebPage

from .scene_object3d import Object3D


class Scene(Object3D):

    def __init__(self, view):
        super().__init__('scene', view)


class Group(Object3D):

    def __init__(self):
        super().__init__('group')


class Box(Object3D):

    def __init__(self,
                 width: float = 1.0,
                 height: float = 1.0,
                 depth: float = 1.0,
                 wireframe: bool = False,
                 ):
        super().__init__('box', width, height, depth, wireframe)


class Sphere(Object3D):

    def __init__(self,
                 radius: float = 1.0,
                 width_segments: int = 32,
                 height_segments: int = 16,
                 wireframe: bool = False,
                 ):
        super().__init__('sphere', radius, width_segments, height_segments, wireframe)


class Cylinder(Object3D):

    def __init__(self,
                 top_radius: float = 1.0,
                 bottom_radius: float = 1.0,
                 height: float = 1.0,
                 radial_segments: int = 8,
                 height_segments: int = 1,
                 wireframe: bool = False,
                 ):
        super().__init__('cylinder', top_radius, bottom_radius, height, radial_segments, height_segments, wireframe)


class Extrusion(Object3D):

    def __init__(self,
                 outline: List[List[float, float]],
                 height: float,
                 wireframe: bool = False,
                 ):
        super().__init__('extrusion', outline, height, wireframe)


class Stl(Object3D):

    def __init__(self,
                 url: str,
                 wireframe: bool = False,
                 ):
        super().__init__('stl', url, wireframe)


class Line(Object3D):

    def __init__(self,
                 start: List[float, float, float],
                 end: List[float, float, float],
                 ):
        super().__init__('line', start, end)


class Curve(Object3D):

    def __init__(self,
                 start: List[float, float, float],
                 control1: List[float, float, float],
                 control2: List[float, float, float],
                 end: List[float, float, float],
                 num_points: int = 20,
                 ):
        super().__init__('curve', start, control1, control2, end, num_points)


class Texture(Object3D):

    def __init__(self,
                 url: str,
                 coordinates: List[List[Optional[List[float]]]],
                 ):
        super().__init__('texture', url, coordinates)

    async def set_url(self, url: str):
        self.args[0] = url
        for socket in WebPage.sockets.get(self.page.page_id, {}).values():
            await self.view.run_method(f'set_texture_url("{self.id}", "{url}")', socket)

    async def set_coordinates(self, coordinates: List[List[Optional[List[float]]]]):
        self.args[1] = coordinates
        for socket in WebPage.sockets.get(self.page.page_id, {}).values():
            await self.view.run_method(f'set_texture_coordinates("{self.id}", {coordinates})', socket)
