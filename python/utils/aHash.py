from PIL import Image
import numpy
import imagehash

def resize_image_nearest(original, new_width, new_height):
    
    original_pixels = original.load()

    # Get original dimensions
    original_width, original_height = original.size

    # Create a new blank image with the desired size
    resized = Image.new('L', (new_width, new_height))
    resized_pixels = resized.load()

    # Apply nearest neighbor scaling
    for x in range(new_width):
        for y in range(new_height):
            src_x = int(x * (original_width / new_width))
            src_y = int(y * (original_height / new_height))
            resized_pixels[x, y] = original_pixels[src_x, src_y]
    
    return resized


def average_hash(image, hash_size=8, mean=numpy.mean):
    if hash_size < 2:
        raise ValueError('Hash size must be greater than or equal to 2')

    image = image.convert('L')
    
    new_width = 8
    new_height = 8
    pixels = resize_image_nearest(image, new_width, new_height)
    avg = mean(pixels)
    	
    diff = pixels > avg
    
    return imagehash.ImageHash(diff)


hash1, hash2 = average_hash(Image.open('../samples/FHD.png'))

print(hash1)
