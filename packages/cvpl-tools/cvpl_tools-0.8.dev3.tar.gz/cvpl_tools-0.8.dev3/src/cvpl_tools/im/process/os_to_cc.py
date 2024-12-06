from cvpl_tools.im.seg_process import SegProcess
import numpy as np
import numpy.typing as npt
from cvpl_tools.im.ndblock import NDBlock
import cvpl_tools.im.process.os_to_lc as os_to_lc
import cvpl_tools.im.process.lc_to_cc as lc_to_cc
import dask.array as da
from cvpl_tools.im.fs import CachePointer


class CountOSBySize(SegProcess):
    """Counting ordinal segmentation contours

    Several features:
    1. A size threshold, below which each contour is counted as a single cell (or part of a single cell,
    in the case it is neighbor to boundary of the image)
    2. Above size threshold, the contour is seen as a cluster of cells an estimate of cell count is given
    based on the volume of the contour
    3. For cells on the boundary location, their estimated ncell is penalized according to the distance
    between the cell centroid and the boundary of the image; if the voxels of the cell do not touch
    edge, this penalty does not apply
    4. A min_size threshold, below (<=) which the contour is simply discarded because it's likely just
    an artifact
    """

    def __init__(self,
                 size_threshold: int | float = 25.,
                 volume_weight: float = 6e-3,
                 border_params: tuple[float, float, float] = (3., -.5, 2.),
                 min_size: int | float = 0,
                 reduce: bool = False,
                 is_global: bool = False):
        super().__init__()
        self.size_threshold = size_threshold
        self.volume_weight = volume_weight
        self.border_params = border_params
        self.min_size = min_size
        self.reduce = reduce

        self.os_to_lc = os_to_lc.DirectOSToLC(min_size=min_size, reduce=False, is_global=is_global,
                                              ex_statistics=['nvoxel', 'edge_contact'])
        self.lc_to_cc = lc_to_cc.CountLCBySize(size_threshold=size_threshold,
                                               volume_weight=volume_weight,
                                               border_params=border_params,
                                               reduce=reduce)

    async def forward(self,
                im: npt.NDArray[np.int32] | da.Array,
                cptr: CachePointer,
                viewer_args: dict = None
                ) -> npt.NDArray[np.float64]:
        cdir = cptr.subdir()
        lc = await self.os_to_lc.forward(im, cdir.cache(cid='os_to_lc'), viewer_args)
        cc = await self.lc_to_cc.forward(lc,  im.ndim, cdir.cache(cid='lc_to_cc'), viewer_args)

        return cc
