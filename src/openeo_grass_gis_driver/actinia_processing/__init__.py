# -*- coding: utf-8 -*-
# Import the actinia_processing to fill the process.PROCESS_DICT with
# actinia_processing
from . import add_dimension_process
# from . import aggregate_spatial_process
# from . import apply_mask_process
from . import apply_process
from . import array_element_process
# from . import bbox_from_raster_process
from . import filter_bands_process
from . import filter_bbox_process
from . import filter_spatial_process
from . import filter_temporal_process
# from . import hants_process
from . import load_collection_process
# from . import mask_invalid_values_process
from . import mask_process
from . import mask_polygon_process
from . import merge_cubes_process
# from . import multilayer_mask_process
from . import ndvi_process
# from . import evi_process
# from . import normalized_difference_process
# from . import map_algebra_process
# from . import percentile_time_process
# from . import reduce_time_process
from . import reduce_dimension_process
from . import rename_labels_process
from . import resample_spatial_process
from . import run_udf_process
# from . import udf_reduce_time
from . import raster_exporter
from . import save_result_process
from . import trim_cube_process

# from . import rgb_raster_exporter
# from . import scale_minmax_process
# from . import zonal_statistics
# from . import temporal_algebra_process

# logical processes
from . import logic_and_process
from . import logic_if_process
from . import logic_not_process
from . import logic_or_process
from . import logic_xor_process

# math processes
from . import math_abs_process
from . import math_add_process
from . import math_clip_process
from . import math_divide_process
from . import math_eq_process
from . import math_exp_process
from . import math_gt_process
from . import math_int_process
from . import math_isnan_process
from . import math_isnodata_process
from . import math_ln_process
from . import math_lt_process
from . import math_lte_process
from . import math_max_process
from . import math_mean_process
from . import math_median_process
from . import math_min_process
from . import math_mod_process
from . import math_multiply_process
from . import math_neq_process
from . import math_normdiff_process
from . import math_power_process
from . import math_product_process
from . import math_quantiles_process
from . import math_sd_process
from . import math_sgn_process
from . import math_sqrt_process
from . import math_subtract_process
from . import math_sum_process
from . import math_variance_process
