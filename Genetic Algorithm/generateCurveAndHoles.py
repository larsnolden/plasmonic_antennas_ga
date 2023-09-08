import numpy as np
import scipy as sp
import cv2


def generateCurve(antenna_representation, padding, image_path="", antenna_name=""):
    # use the antenna representation as a unique name

    upscaled_image = sp.ndimage.zoom(antenna_representation, 200, order=0)

    # add padding zeros
    upscaled_image = np.pad(
        upscaled_image, [(padding, padding), (padding, padding)], mode="constant"
    )
    # use this to cut extrude
    inverted_image = np.logical_not(upscaled_image)

    # make integer value for cv2
    upscaled_image_uint8 = (inverted_image * 255).astype(np.uint8)

    # calculate the kernel size to achieve the desired fillet radius
    fillet_radius = 11  # radius in nm
    image_size = np.size(
        upscaled_image_uint8[0]
    )  # number of pixels on one side of the image
    substrate_size = 500  # nm, the sidelength of our simulation boundaries

    pixel_per_nm = image_size / substrate_size
    kernel_size = int(2 * fillet_radius * pixel_per_nm)

    # create the structuring element
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (kernel_size, kernel_size))

    # dilate and then erode the image
    rounded_image = cv2.morphologyEx(upscaled_image_uint8, cv2.MORPH_OPEN, kernel)
    rounded_image = cv2.morphologyEx(rounded_image, cv2.MORPH_CLOSE, kernel)

    # save the image for visualization later
    cv2.imwrite(image_path, rounded_image)

    # Convert image to contours for COMSOL
    ret, threshold = cv2.threshold(cv2.bitwise_not(rounded_image), 127, 255, 0)
    contours, hierarchy = cv2.findContours(
        threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE
    )

    # Divide contours into outer and inner based on hierarchy
    outer_contours = []
    inner_contours = []
    for i in range(len(contours)):
        contour = contours[i]
        if hierarchy[0][i][3] == -1:  # If no parent contour, it's an outer contour
            outer_contours.append(
                [[int(point[0][0]), int(point[0][1])] for point in contour]
            )
        else:  # Else, it's an inner contour
            inner_contours.append(
                [[int(point[0][0]), int(point[0][1])] for point in contour]
            )

    # Write outer contours to .txt file
    filename_outer = f"./contours/outer_{antenna_name}.txt"
    writeContoursToFile(filename_outer, outer_contours)

    # Write inner contours to another .txt file
    filename_inner = f"./contours/inner_{antenna_name}.txt"
    writeContoursToFile(filename_inner, inner_contours)

    if(len(inner_contours) == 0):
        return filename_outer, None
    return filename_outer, filename_inner


def writeContoursToFile(filename, contours):
    with open(filename, "w") as f:
        f.write("%Coordinates\n")
        total_points = 0
        for contour in contours:
            for point in contour:
                f.write(f"{point[0]} {point[1]}\n")
                total_points += 1

        f.write("\n%Elements\n")
        start_point = 1
        for contour in contours:
            contour_len = len(contour)
            for i in range(start_point, start_point + contour_len - 1):
                # Connect each point with the next within the same contour
                f.write(f"{i} {i+1}\n")
            # Connect the last point with the first of the same contour
            f.write(f"{start_point + contour_len - 1} {start_point}\n")
            start_point += contour_len
