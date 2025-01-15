from gimpfu import *
import os  # Import the os module to handle file paths

def resize_canvas_with_white(image, drawable, output_dir, input_dir):
    # Walk through all subdirectories and files in the input directory
    for root, _, files in os.walk(input_dir):
        for filename in files:
            # Skip non-image files
            if not filename.lower().endswith((".png", ".jpg", ".jpeg", ".tiff", ".bmp", ".gif")):
                continue

            try:
                # Construct the full input file path
                input_path = os.path.join(root, filename)

                # Create the corresponding output directory structure
                relative_path = os.path.relpath(root, input_dir)
                target_dir = os.path.join(output_dir, relative_path)
                if not os.path.exists(target_dir):
                    os.makedirs(target_dir)


                # Load the image
                image = pdb.gimp_file_load(input_path, input_path)

                # Start undo group for actions
                pdb.gimp_image_undo_group_start(image)

                # Get the original dimensions
                width = pdb.gimp_image_width(image)
                height = pdb.gimp_image_height(image)

                # Calculate new dimensions (150% of original)
                new_width = int(width * 1.5)
                new_height = int(height * 1.5)

                # Set the new canvas size and center the layer
                pdb.gimp_image_resize(image, new_width, new_height, (new_width - width) // 2, (new_height - height) // 2)

                # Add a white background
                background_layer = pdb.gimp_layer_new(image, new_width, new_height, RGBA_IMAGE, "Background", 100, NORMAL_MODE)
                pdb.gimp_image_insert_layer(image, background_layer, None, 0)
                pdb.gimp_context_set_background((255, 255, 255))  # Set white as the background color
                pdb.gimp_edit_fill(background_layer, BACKGROUND_FILL)  # Fill the layer with the background color
                pdb.gimp_image_lower_item_to_bottom(image, background_layer)

                # Update the drawable to the entire image after modifications
                drawable = pdb.gimp_image_merge_visible_layers(image, CLIP_TO_IMAGE)

                # Save the modified image in the corresponding output directory
                output_path = os.path.join(target_dir, filename)
                pdb.gimp_file_save(image, drawable, output_path, output_path)

                # Finish undo group
                pdb.gimp_image_undo_group_end(image)
            except Exception as e:
                #pdb.gimp_message(f"Error processing image '{filename}': {e}")
                pass

register(
    "python_fu_resize_canvas",
    "Resize canvas to 150% and add a white background",
    "Increase canvas size to 150%, center the original image, and fill the background with white",
    "Your Name",
    "Your Name",
    "2025",
    "<Image>/Filters/Custom/Resize Canvas",
    "*",
    [
        (PF_DIRNAME, "output_dir", "Output directory", ""),
        (PF_DIRNAME, "input_dir", "Input directory", "")
    ],
    [],
    resize_canvas_with_white
)

main()
