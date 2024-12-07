import os
import requests
from PIL import Image
from concurrent.futures import ThreadPoolExecutor, as_completed
import numpy as np
from tqdm import tqdm
import random
from requests.exceptions import ProxyError
import glob

class ImageTool():

    @staticmethod
    def concat_horizontally(im1, im2):
        """
        Description of concat_horizontally
        Horizontally concatenates two images

        Args:
            im1 (undefined): first PIL image
            im2 (undefined): second PIL image

        """
        dst = Image.new('RGB', (im1.width + im2.width, im1.height))
        dst.paste(im1, (0, 0))
        dst.paste(im2, (im1.width, 0))
        return dst

    @staticmethod
    def concat_vertically(im1, im2):
        """
        Description of concat_vertically
        Vertically concatenates two images

        Args:
            im1 (undefined): first PIL image
            im2 (undefined): second PIL image

        """
        dst = Image.new('RGB', (im1.width, im1.height + im2.height))
        dst.paste(im1, (0, 0))
        dst.paste(im2, (0, im1.height))
        return dst
                
    @staticmethod
    def fetch_image_with_proxy(pano_id, zoom, x, y, ua, proxies):
        """
        Fetches an image using a proxy.

        Args:
            pano_id (str): GSV panorama id
            zoom (int): Zoom level for the image
            x (int): The x coordinate of the tile
            y (int): The y coordinate of the tile
            ua (str): User agent string
            proxies (list): A list of available proxies

        Returns:
            Image: The fetched image
        """
        while True:
            # Choose a random proxy for each request
            proxy = random.choice(proxies)
            url_img = f'https://cbk0.google.com/cbk?output=tile&panoid={pano_id}&zoom={zoom}&x={x}&y={y}'
            try:
                image = Image.open(requests.get(url_img, headers=ua, proxies=proxy, stream=True).raw)
                return image
            except ProxyError as e:
                print(f"Proxy {proxy} is not working. Exception: {e}")
                continue

    @staticmethod
    def is_bottom_black(image, row_count=3, intensity_threshold=10):
        """
        Check if the bottom 'row_count' rows of the image are near black, with a given intensity threshold.
        This method uses linear computation instead of nested loops for faster execution.

        Args:
            image (PIL.Image): The image to check.
            row_count (int): Number of rows to check.
            intensity_threshold (int): The maximum intensity for a pixel to be considered black.

        Returns:
            bool: True if the bottom rows are near black, False otherwise.
        """
        # Convert the bottom rows to a numpy array for fast processing
        bottom_rows = np.array(image)[-row_count:, :]
        # Check if all pixels in the bottom rows are less than or equal to the intensity threshold
        return np.all(bottom_rows <= intensity_threshold)

    @staticmethod
    def process_image(image, zoom):
        """
        Crop and resize the image based on zoom level if the bottom is black.

        Args:
            image (PIL.Image): The image to process.
            zoom (int): The zoom level.

        Returns:
            PIL.Image: The processed image.
        """
        if ImageTool.is_bottom_black(image):
            # Compute the crop and resize dimensions based on zoom level
            crop_height, crop_width = 208 * (2 ** zoom), 416 * (2 ** zoom)
            resize_height, resize_width = 256 * (2 ** zoom), 512 * (2 ** zoom)

            # Crop the image
            image = image.crop((0, 0, crop_width, crop_height))

            # Resize the image
            image = image.resize((resize_width, resize_height), Image.LANCZOS)

        return image            

    @staticmethod
    def get_and_save_image(pano_id, identif, zoom, vertical_tiles, horizontal_tiles, out_path, ua, proxies, cropped=False, full=True):
        """
        Description of get_and_save_image
        
        Downloads an image tile by tile and composes them together.

        Args:
            pano_id (undefined): GSV anorama id
            identif (undefined): custom identifier
            size (undefined):    image resolution
            vertical_tiles (undefined): number of vertical tiles
            horizontal_tiles (undefined): number of horizontal tiles
            out_path (undefined): output path
            cropped=False (undefined): set True if the image split horizontally in half is needed
            full=True (undefined): set to True if the full image is needed

        """
        for x in range(horizontal_tiles):
            for y in range(vertical_tiles):
                new_img = ImageTool.fetch_image_with_proxy(pano_id, zoom, x, y, ua, proxies)
                if not full:
                    new_img.save(f'{out_path}/{identif}_x{x}_y{y}.jpg')
                if y == 0:
                    first_slice = new_img
                else:
                    first_slice = ImageTool.concat_vertically(first_slice, new_img)

            if x == 0:
                final_image = first_slice
            else:
                final_image = ImageTool.concat_horizontally(final_image, first_slice)

        if full:
            name = f'{out_path}/{identif}'
            if cropped or zoom == 0:
                h_cropped = final_image.size[1] // 2
                final_image = final_image.crop((0, 0, final_image.size[0], h_cropped))

            # Validate image before saving
            if final_image.size[0] > 0 and final_image.size[1] > 0:
                final_image = ImageTool.process_image(final_image, zoom)
                final_image.save(f'{name}.jpg')
            else:
                raise ValueError(f"Invalid image for pano_id {pano_id}")

        return identif


    @staticmethod
    def dwl_multiple(panoids, zoom, v_tiles, h_tiles, out_path, uas, proxies, cropped, full, batch_size = 1000, logger = None):
        """
        Description of dwl_multiple
        
        Calls the get_and_save_image function using multiple threads.
        
        Args:
            panoids (undefined): GSV anorama id
            zoom (undefined):    image resolution
            v_tiles (undefined): number of vertical tiles
            h_tiles (undefined): number of horizontal tiles
            out_path (undefined): output path
            cropped=False (undefined): set True if the image split horizontally in half is needed
            full=True (undefined): set to True if the full image is needed
            log_path=None (undefined): path to a log file
        """

        if not os.path.exists(out_path):
            os.makedirs(out_path)

        errors = 0

        # Calculate current highest batch number
        existing_batches = glob.glob(os.path.join(out_path, "batch_*"))
        existing_batch_numbers = [int(os.path.basename(batch).split('_')[-1]) for batch in existing_batches]
        start_batch_number = max(existing_batch_numbers, default=0)

        num_batches = (len(panoids) + batch_size - 1) // batch_size

        for counter, i in tqdm(enumerate(range(start_batch_number, start_batch_number + num_batches)), desc=f"Downloading images by batch size {min(batch_size, len(panoids))}"):
            # Create a new sub-folder for each batch
            batch_out_path = os.path.join(out_path, f"batch_{i+1}")
            os.makedirs(batch_out_path, exist_ok=True)

            with ThreadPoolExecutor(max_workers=min(len(uas), batch_size)) as executor:
                jobs = []
                batch_panoids = panoids[counter*batch_size : (counter+1)*batch_size]
                batch_uas = uas[counter*batch_size : (counter+1)*batch_size]
                for pano, ua in zip(batch_panoids, batch_uas):
                    kw = {
                        "pano_id": pano,
                        "identif": pano,
                        "ua": ua,
                        "proxies": proxies,
                        "zoom": zoom,
                        "vertical_tiles": v_tiles,
                        "horizontal_tiles": h_tiles,
                        "out_path": batch_out_path,  # Pass the new sub-folder path
                        "cropped": cropped,
                        "full": full
                    }
                    jobs.append(executor.submit(ImageTool.get_and_save_image, **kw))

                for job in tqdm(as_completed(jobs), total=len(jobs), desc=f"Downloading images for batch #{i+1}"):
                    try:
                        job.result()
                    except Exception as e:
                        print(e)
                        errors += 1
                        failed_panoid = batch_panoids[jobs.index(job)]
                        if logger:
                            logger.log_failed_pids(failed_panoid)

        print("Total images downloaded:", len(panoids) - errors, "Errors:", errors)  
        if logger:
            logger.log_info(f"Total images downloaded: {len(panoids) - errors}, Errors: {errors}")