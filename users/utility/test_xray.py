from .ROI_revision import *
from .ROI_extraction import *
from .middle_line_via_snake import *
from .jaw_separation import separate_jaws
import time
import os
from django.conf import settings


def process_xray_image(filename):
    filename = os.path.join(settings.MEDIA_ROOT, filename)
    from pathlib import Path
    new_name = Path(filename).stem
    #new_name = os.path.splitext(filename)[0]
    print("File Name:",new_name)
    output_image = os.path.join(settings.MEDIA_ROOT, 'tested', new_name+".bmp")
    upper_image = os.path.join(settings.MEDIA_ROOT, 'upper_jaw', new_name+".bmp")
    lower_image = os.path.join(settings.MEDIA_ROOT, 'lower_jaw', new_name+".bmp")

    img = cv2.imread(filename, 0)
    img_copy = copy.deepcopy(x=filename)

    print('original image dimensions:', img.shape)
    t0 = time.time()
    initial_roi, initial_boundaries = extract_roi(image=img, return_result=1)
    print('initial ROI dimensions:', initial_roi.shape)
    revised_roi, revised_boundaries = revise_boundaries(image=initial_roi, return_result=1)
    print('final ROI dimensions:', revised_roi.shape)
    t1 = time.time()
    print('elapsed time for ROI extraction & revision: %.2f secs' % (t1 - t0))

    upper_height = initial_boundaries[3] + revised_boundaries[3]
    left_width = initial_boundaries[0] + revised_boundaries[0]
    lower_height = upper_height + revised_roi.shape[0]
    right_width = left_width + revised_roi.shape[1]

    top_left_corner = (left_width, upper_height)
    top_right_corner = (right_width, upper_height)
    bottom_left_corner = (left_width, lower_height)
    bottom_right_corner = (right_width, lower_height)

    # print('roi points:', top_left_corner, top_right_corner, bottom_left_corner, bottom_right_corner)
    # cv2.rectangle(img_copy, top_left_corner, bottom_right_corner, 0, 7)
    # plt.imshow(X=img_copy, cmap='gray')
    # plt.show()
    # print("save & continue? (y/n)")
    # if input() != 'y':
    #     print("process terminated!")
    #     exit()

    cv2.imwrite(output_image, revised_roi)
    cropped_img = revised_roi
    """do any preprocessing needed"""
    cropped_img_edited = preprocessing.CLAHE(image=cropped_img)
    cropped_img_edited = preprocessing.sauvola(image=cropped_img_edited, window_size=175, return_result=1)
    # change pixels with the value of 255 to 254; in order to distinguish the white pixels of middle line from the image
    cropped_img_edited = preprocessing.eliminate_white_pixels(image=cropped_img_edited)
    t0 = time.time()
    # change the num_part variable to get the best result!
    these_points = find_points(image=cropped_img_edited, num_parts=20, v_bound=50, v_stride=2)
    cropped_img = preprocessing.eliminate_white_pixels(image=cropped_img)
    img_with_line = draw_middle_line(image=cropped_img, points=these_points)
    t1 = time.time()
    print('elapsed time for  algorithm: %.2f secs' % (t1 - t0))
    plt.imshow(X=img_with_line, cmap='gray')
    # plt.show()
    # print("continue? (y/n)")
    # if input() != 'y':
    #     print("process terminated!")
    #     exit()
    t0 = time.time()
    upper_jaw, lower_jaw = separate_jaws(image=img_with_line)
    t1 = time.time()
    print('elapsed time for jaw separation: %.2f secs' % (t1 - t0))
    # plt.imshow(X=upper_jaw, cmap='gray')
    # plt.show()
    # plt.imshow(X=lower_jaw, cmap='gray')
    # plt.show()

    # print("save results? (y/n)")
    # if input() == 'y':
    cv2.imwrite(upper_image, upper_jaw)
    cv2.imwrite(lower_image, lower_jaw)
    print("results saved!")

    return filename, output_image, upper_image, lower_image
