from PIL import Image

# List of file paths for your uploaded images
file_paths = [
    "Images/People/Joan-Emma-Shea.webp",
    "Images/People/pritam.jpg",
    "Images/People/jackson.jpg",
    "Images/People/sam.jpg",
    "Images/People/lena.jpeg",
    "Images/People/daniel.jpeg",
    "Images/People/leif.jpeg",
    "Images/People/matthew.jpeg"
]

def create_thumbnail(im, size=200):
    # Crop the image to a centered square
    width, height = im.size
    min_dim = min(width, height)
    left = (width - min_dim) // 2
    top = (height - min_dim) // 2
    right = left + min_dim
    bottom = top + min_dim
    im_cropped = im.crop((left, top, right, bottom))
    # Resize the cropped image to a consistent square dimension
    im_thumb = im_cropped.resize((size, size), Image.ANTIALIAS)
    return im_thumb

# Open images and convert them into standardized thumbnails
thumbnails = []
for path in file_paths:
    im = Image.open(path)
    thumb = create_thumbnail(im, size=200)
    thumbnails.append(thumb)

# Set up the dimensions for the collage: 4 columns x 2 rows
cols, rows = 4, 2
cell_size = 200  # each thumbnail is 200x200 pixels
collage_width = cols * cell_size
collage_height = rows * cell_size

# Create a new white background image for the collage
collage = Image.new('RGB', (collage_width, collage_height), color=(255, 255, 255))

# Paste each thumbnail into the collage grid
for index, thumb in enumerate(thumbnails):
    row = index // cols
    col = index % cols
    x = col * cell_size
    y = row * cell_size
    collage.paste(thumb, (x, y))

# Save the final collage image
collage_output_path = "collage.jpg"
collage.save(collage_output_path)

print("Collage saved to", collage_output_path)
