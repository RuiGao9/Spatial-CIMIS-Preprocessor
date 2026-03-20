import arcpy
import os
import gzip
import shutil
from tqdm import tqdm

class SpatialCIMISProcessor:
    def __init__(self, input_root, output_root, spatial_ref_code=3310):
        """
        Initialize the processor
        :param input_root: Root directory for the original .asc.gz data
        :param output_root: Root directory for the processed .tif data
        :param spatial_ref_code: Spatial reference code, default is 3310 (California Albers)
        """
        self.input_root = input_root
        self.output_root = output_root
        self.spatial_ref = arcpy.SpatialReference(spatial_ref_code)
        
        # ArcPy Environment Settings
        arcpy.env.overwriteOutput = True
        arcpy.SetLogHistory(False)

    def run_pipeline(self, start_year=2004, end_year=2026):
        """Execute the complete processing pipeline"""
        all_tasks = []
        years_to_process = range(start_year, end_year + 1)
        
        print(f"Step 1: Scanning directories from {start_year} to {end_year}...")
        for year in years_to_process:
            year_path = os.path.join(self.input_root, str(year))
            if not os.path.exists(year_path): continue
            
            for month in range(1, 13):
                month_str = f"{month:02d}"
                month_path = os.path.join(year_path, month_str)
                if not os.path.exists(month_path): continue
                
                for day_folder in os.listdir(month_path):
                    day_path = os.path.join(month_path, day_folder)
                    if os.path.isdir(day_path):
                        gz_files = [f for f in os.listdir(day_path) if f.endswith(".asc.gz")]
                        if gz_files:
                            all_tasks.append({
                                'year': str(year), 
                                'month': month_str, 
                                'day': day_folder, 
                                'path': day_path, 
                                'files': gz_files
                            })

        total_days = len(all_tasks)
        print(f"Status: Found {total_days} daily folders. Starting processing...\n")

        success_count = 0
        error_count = 0

        # Initialize Progress Bar
        with tqdm(total=total_days, desc="Overall Progress", unit="day", dynamic_ncols=True) as pbar:
            for task in all_tasks:
                target_dir = os.path.join(self.output_root, task['year'], task['month'], task['day'])
                if not os.path.exists(target_dir):
                    os.makedirs(target_dir)

                for file_name in task['files']:
                    gz_path = os.path.join(task['path'], file_name)
                    temp_asc = os.path.join(target_dir, file_name[:-3])
                    temp_raster_name = "tmp_rast" 
                    out_tif = os.path.join(target_dir, file_name.replace(".asc.gz", ".tif"))

                    try:
                        # 1. Decompress
                        with gzip.open(gz_path, 'rb') as f_in:
                            with open(temp_asc, 'wb') as f_out:
                                shutil.copyfileobj(f_in, f_out)

                        # 2. Convert
                        arcpy.env.workspace = target_dir
                        arcpy.ASCIIToRaster_conversion(temp_asc, temp_raster_name, "FLOAT")
                        
                        # 3. Define Projection and Project Raster
                        arcpy.management.DefineProjection(temp_raster_name, self.spatial_ref)
                        arcpy.management.ProjectRaster(
                            in_raster=temp_raster_name,
                            out_raster=out_tif,
                            out_coor_system=self.spatial_ref,
                            resampling_type="NEAREST",
                            cell_size="2000 2000"
                        )

                        # 4. Cleanup
                        if os.path.exists(temp_asc): os.remove(temp_asc)
                        if arcpy.Exists(temp_raster_name): arcpy.management.Delete(temp_raster_name)
                        
                        success_count += 1

                    except Exception as e:
                        error_count += 1
                        tqdm.write(f"[ERROR] {task['year']}-{task['month']}-{task['day']} | {file_name}: {str(e)}")
                
                pbar.update(1)
                pbar.set_postfix({"Date": f"{task['year']}-{task['month']}"})

        print(f"\nCOMPLETED. Success: {success_count}, Errors: {error_count}")