import cv2
import imutils
import numpy as np
from matplotlib import pyplot as plt

class PipelineImg:

    @staticmethod
    def do_full_pipeline(img, height=900, auto_canny_sigma=0.33, bordersize=15,*,debug=False, figsize=(10, 10)):
        """
            This method was made for a more easy execution of preprocessing 
        """
        res_img = PipelineImg.resizing_img(img, height = height)
        resized_shape = res_img.shape
        bin_img = PipelineImg.binarization_img(res_img)
        den_img = PipelineImg.denoise_img(bin_img)
        unb_img, dimensions = PipelineImg.drop_border_img(den_img, original=res_img, sigma=auto_canny_sigma, bordersize=bordersize)
        #end_img = PipelineImg.add_white_border(unb_img, bordersize=bordersize)
        if debug:
            PipelineImg.plot_imgs_grid([img, res_img, bin_img, den_img, unb_img], 
                ["original", "resize", "binarizated", "denoised","unbordered + border"], figsize=figsize)
        return unb_img, resized_shape, dimensions


    @staticmethod
    def resizing_img(img, height=900):
        return imutils.resize(img, height = height)


    @staticmethod
    def binarization_img(img):
        """
            Based on: https://docs.opencv.org/master/d7/d4d/tutorial_py_thresholding.html
        """
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY);
        img = cv2.medianBlur(img,5)
        thld = cv2.adaptiveThreshold(img,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                    cv2.THRESH_BINARY,11,2)
        return thld


    @staticmethod
    def denoise_img(img):
        """
            Based on: https://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_photo/py_non_local_means/py_non_local_means.html
        """
        return cv2.fastNlMeansDenoising(img, None, 20,7,21)



    @staticmethod
    def drop_border_img(img, original, sigma=0.33, bordersize=15):
        """
            
        """
        edged = PipelineImg.auto_canny(original, sigma=sigma)
        (x,y,w,h) =cv2.boundingRect(edged.copy())
        dimensions = (max(0, y-bordersize),min(y+h+bordersize, original.shape[0]-1),
                      max(x-bordersize,0), min(x+w+bordersize,original.shape[1]-1))
        crop_img = img[dimensions[0]:dimensions[1], dimensions[2]:dimensions[3]]
        return crop_img, dimensions


    @staticmethod
    def auto_canny(image, sigma=0.33):
        """
            copied from: https://www.pyimagesearch.com/2015/04/06/zero-parameter-automatic-canny-edge-detection-with-python-and-opencv/
        """
        # compute the median of the single channel pixel intensities
        v = np.median(image)
        # apply automatic Canny edge detection using the computed median
        lower = int(max(0, (1.0 - sigma) * v))
        upper = int(min(255, (1.0 + sigma) * v))
        edged = cv2.Canny(image, lower, upper)
        # return the edged image
        return edged


    @staticmethod
    def add_white_border(img, bordersize=5):
        """
            
        """
        return cv2.copyMakeBorder(
            img,
            top=bordersize,
            bottom=bordersize,
            left=bordersize,
            right=bordersize,
            borderType=cv2.BORDER_CONSTANT,
            value=255
        )


    # Visualization methods
    @staticmethod
    def plot_imgs_grid(imgs, titles,*,ncols=3, figsize=(5,5)):
        nrows = int(np.ceil(len(imgs)/ncols))
        f, axarr = plt.subplots(nrows,ncols, figsize=figsize,constrained_layout=True)
        for indx_img in range(nrows*ncols):
            rw = int(np.floor(indx_img/ncols))
            cl = indx_img%ncols
            if(indx_img < len(imgs)):
                axarr[rw][cl].imshow(cv2.cvtColor(imgs[indx_img], cv2.COLOR_BGR2RGB))
                axarr[rw, cl].set_aspect('equal')
                
                axarr[rw, cl].set_xticklabels([])
                axarr[rw, cl].set_yticklabels([])
                axarr[rw, cl].set_title(titles[indx_img])
            else:
                f.delaxes(axarr[rw, cl])
                pass
        
        f.set_constrained_layout_pads(w_pad=0.0, h_pad=0.0, hspace= -0.87, wspace=0.0)