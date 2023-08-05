"""
This module contains classes related to :ref:`data visualization and rendering <rendering_intro>`.

**Rendering:**

  * :py:class:`Viewport`

**Rendering engines:**

  * :py:class:`OpenGLRenderer`
  * :py:class:`TachyonRenderer`
  * :py:class:`OSPRayRenderer`

**Data visualization elements:**

  * :py:class:`DataVis` (base class for all visual elements)
  * :py:class:`BondsVis`
  * :py:class:`DislocationVis`
  * :py:class:`ParticlesVis`
  * :py:class:`SimulationCellVis`
  * :py:class:`SurfaceMeshVis`
  * :py:class:`TrajectoryVis`
  * :py:class:`TriangleMeshVis`
  * :py:class:`VectorVis`
  * :py:class:`VoxelGridVis`

**Viewport overlays:**

  * :py:class:`ViewportOverlay` (base class for all overlay types)
  * :py:class:`ColorLegendOverlay`
  * :py:class:`CoordinateTripodOverlay`
  * :py:class:`PythonViewportOverlay`
  * :py:class:`TextLabelOverlay`

"""
import traits.api

__all__ = ['Viewport', 'OpenGLRenderer', 'DataVis',
        'CoordinateTripodOverlay', 'PythonViewportOverlay', 'TextLabelOverlay', 'ViewportOverlay',
        'TriangleMeshVis']

# A parameter trait whose value is a RGB tuple with values from 0 to 1.
# The default value is (1.0, 1.0, 1.0).
class ColorTrait(traits.api.BaseTuple):
    def __init__(self, default=(1.0, 1.0, 1.0), **metadata):
        super().__init__(default, **metadata)
