from whacc import PoleTracking
import whacc
import glob
import os

mp4_path = "/Volumes/GoogleDrive-114825029448473821206/My Drive/colab_batch_processing_test/add_files_here_FINISHED"

folders_with_MP4s = whacc.utils.recursive_dir_finder(mp4_path, '*.mp4')
_ = [print(str(i) + ' ' + k) for i, k in enumerate(folders_with_MP4s)]


crop_size=[61, 61]
# we are just creating the template image no need to
for i, video_directory in enumerate(folders_with_MP4s):
    template_img_full_name = glob.glob(video_directory + os.path.sep + '*template_img.png')
    if len(template_img_full_name) != 1:
        PT = PoleTracking(video_directory=video_directory)  # create the class
        PT.cut_out_pole_template(crop_size=crop_size, frame_num=2000, file_ind=2)
        PT.save_template_img(cust_save_dir=PT.video_directory)


PT = PoleTracking(video_directory=video_directory)  # create the class
PT.cut_out_pole_template(crop_size=crop_size, frame_num=2000, file_ind=0)
PT.save_template_img(cust_save_dir=PT.video_directory)

if False:
    from whacc import utils
    import cv2

    template_img = utils.get_whacc_path() + '/whacc_data/template_img.png'
    self.load_template_img(template_img)
    res = cv2.matchTemplate(frame2, self.template_image, cv2.TM_CCOEFF)
    min_val, max_val, min_loc, top_left = cv2.minMaxLoc(res)
    crop_img, crop_top_left2, crop_bottom_right2 = self.crop_image_from_top_left(og_frame, top_left + crop_top_left, [w, h])
