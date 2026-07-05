"""
深度相机/双目视觉适配接口
底层依赖：Common-LSG io_utils 通用IO工具
功能：解析RGB-D深度数据，轻量化适配嵌入式设备
"""
import numpy as np
from Common_LSG.io_utils import SectionDataStandard

class DepthCameraParser(SectionDataStandard):
    def load_rgbd_frame(self, depth_path, rgb_path=None):
        """加载单帧RGB-D深度数据"""
        try:
            import cv2
        except ImportError:
            raise ImportError("需安装opencv依赖：pip install opencv-python")
        
        depth_map = cv2.imread(depth_path, cv2.IMREAD_UNCHANGED)
        depth_map = depth_map.astype(np.float32) / 1000.0  # 转换为米
        
        standard_data = self.format_section_stack(
            np.expand_dims(depth_map, axis=0),
            spacing=[0.001, 0.001, 0.001],
            origin=[0, 0, 0]
        )
        return standard_data