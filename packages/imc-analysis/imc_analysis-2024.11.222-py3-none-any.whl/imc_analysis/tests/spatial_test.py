# Tests
from imc_analysis.tl import impute_roi_area
import imc_analysis as imc
from imc_analysis.logging import *
from tqdm import tqdm
logger.setLevel(logging.DEBUG)

if __name__ == '__main__':
    
    logger.info('Downloading sample file')
    
    import scanpy as sc
    adata = sc.read(
        'data/healthy_lung_adata.h5ad',
        backup_url='https://zenodo.org/record/6376767/files/healthy_lung_adata.h5ad?download=1')

    logger.debug(adata)

    spatial_distance = imc.tl.spatial_distance(adata, celltype = 'celltype', roi_key='roi')
    dist_df = imc.utils.adata_to_dist_df(spatial_distance, celltype = 'celltype', roi_key = 'roi')
