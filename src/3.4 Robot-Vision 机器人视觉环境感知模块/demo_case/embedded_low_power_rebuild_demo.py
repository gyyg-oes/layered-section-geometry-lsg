"""
嵌入式低算力环境重建Demo
优化目标：最小化内存占用与计算量，适配ARM嵌入式设备
"""
from Robot_Vision.hardware_adapt.depth_camera_parser import DepthCameraParser
from Robot_Vision.noise_optimize.motion_blur_optimize import MotionBlurOptimize
from Robot_Vision.scene_constraint.workspace_constraint import WorkspaceConstraint
from Common_LSG.slice_rebuild import SectionRebuilder

def embedded_rebuild_pipeline(depth_path, workspace_boundary):
    # 轻量化解析
    parser = DepthCameraParser()
    depth_data = parser.load_rgbd_frame(depth_path)
    
    # 低算力优化
    optimizer = MotionBlurOptimize()
    optimized = optimizer.motion_blur_restore(depth_data.section_stack[0])
    
    # 空间裁剪降维
    constraint = WorkspaceConstraint()
    constrained = constraint.workspace_range_constrain(optimized, workspace_boundary)
    
    # 轻量化重建
    rebuilder = SectionRebuilder(lightweight_mode=True)
    env_model = rebuilder.non_orthogonal_rebuild([constrained], depth_data.spacing)
    
    print("嵌入式低算力环境重建完成，支持实时避障")
    return env_model

if __name__ == "__main__":
    embedded_rebuild_pipeline("./depth.png", [[0,0,0],[2,2,2]])