"""
航空航天大尺度三维重建Demo
"""
from Aerospace_Space.hardware_adapt.satellite_aerial_parser import SatelliteAerialParser
from Aerospace_Space.noise_optimize.remote_sensing_stripe_denoise import RemoteSensingDenoise
from Aerospace_Space.scene_constraint.large_scale_distortion_constraint import LargeScaleDistortionConstraint
from Common_LSG.slice_rebuild import SectionRebuilder

def aerospace_rebuild_pipeline(tiff_path, output_path):
    parser = SatelliteAerialParser()
    rs_data = parser.load_remote_sensing_tiff(tiff_path)
    
    denoiser = RemoteSensingDenoise()
    denoised_stack = [denoiser.stripe_noise_remove(s) for s in rs_data.section_stack]
    
    constraint = LargeScaleDistortionConstraint()
    constrained_stack = constraint.atmospheric_refraction_correct(denoised_stack, [0, 10000])
    
    rebuilder = SectionRebuilder()
    terrain_model = rebuilder.non_orthogonal_rebuild(constrained_stack, rs_data.spacing)
    
    print("航空航天大尺度三维重建完成")
    return terrain_model

if __name__ == "__main__":
    aerospace_rebuild_pipeline("./aerial.tif", "./output/aerial_model.stl")