from PIL import Image
import numpy
import imagehash

def resize_image_nearest(original, new_width, new_height):
    # Load the image (with PIL for demonstration purposes)
    # original = Image.open(input_path)
    original_pixels = original.load()

    # Get original dimensions
    original_width, original_height = original.size

    # Create a new blank image with the desired size
    resized = Image.new('L', (new_width, new_height))
    resized_pixels = resized.load()
    resized_pixels = Image.new()

    # Apply nearest neighbor scaling
    for x in range(new_width):
        for y in range(new_height):
            # src_x = round(x * (original_width / new_width))
            # src_y = round(y * (original_height / new_height))
            src_x = int( round( float(x) / float(new_width) * float(original_width) ) )
            src_y = int( round( float(y) / float(new_height) * float(original_height) ) )
            src_x = min( src_x, original_width-1)
            src_y = min( src_y, original_height-1)
            resized_pixels[x, y] = original_pixels[src_x, src_y]
    
    return resized
    # Save the resized image
    # resized.save(output_path)
    # print(f"Resized image saved to {output_path}")
            


def average_hash(image, hash_size=8, mean=numpy.mean):
    if hash_size < 2:
        raise ValueError('Hash size must be greater than or equal to 2')

    image = image.convert('L')
    # image = image.convert('L').resize((hash_size, hash_size), Image.NEAREST)

    # Example usage
    new_width = 8
    new_height = 8
    # pixels = resize_image_nearest(image, 320, 240)
    # pixels = resize_image_nearest(pixels, 160, 120)
    # pixels = resize_image_nearest(pixels, 80, 60)
    # pixels = resize_image_nearest(pixels, 40, 30)
    # pixels = resize_image_nearest(pixels, 20, 15)
    # pixels = resize_image_nearest(pixels, 10, 8)
    pixels = resize_image_nearest(image, 8, 8)
    pixels2 = image.resize((8, 8), Image.NEAREST)
    # pixels = numpy.asarray(image)
    # pixels = image
    avg = mean(pixels)
    avg2 = mean(pixels2)

	
    diff = pixels > avg
    diff2 = pixels2 > avg2
	
    return imagehash.ImageHash(diff), imagehash.ImageHash(diff2)



hash1, hash2 = average_hash(Image.open('../samples/FHD.png'))

print(hash1)
print(hash2)

# otherhash = imagehash.average_hash(Image.open('tests/data/peppers.png'))
