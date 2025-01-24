import easygui as gui
import cv2
import numpy as np
import time
import os

# create a welcome message to the program and mentionen the writer of the program
gui.msgbox(title="Welcome", msg="Welcome to the ink area analysis tool.\nPlease follow the instructions to analyse your sample.\n\n(c) Vjekoslav Kokoric")

while True:
    # load image
    image_raw=gui.fileopenbox(title="Please select the image you want to analyse",filetypes=["*.png","*.jpg","*.jpeg"])
    image=cv2.imread(image_raw)


    # now we have to ask the user what this sample is. I want a multitextbox with the following fields: chemical, concentration, replicate number
    msg="Please provide following information about the sample"
    title="Sample Information"
    fieldNames=["Chemical","Concentration","Replicate Number"]
    fieldValues=[]
    fieldValues=gui.multenterbox(msg,title,fieldNames)

    # scale image to fit screen
    #scale=1
    #if image.shape[0]>1000 or image.shape[1]>1000:
    #    scale=0.3 #VK changed from 0.3 to 0.5
    #image=cv2.resize(image,(0,0),fx=scale,fy=scale)
    cv2.imshow("Original Image",image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    # ask user if he wants to change the scale of the image and if yes, ask for a value between 0.3 to 2.0
    change=gui.boolbox("Do you want to change the scale of the image?",choices=("Yes","No"))
    if change:
        scale=gui.enterbox("Please enter a value between 0.3 and 5.0")
        scale=float(scale)
        image=cv2.resize(image,(0,0),fx=scale,fy=scale)
        cv2.imshow("Original Image",image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    else:
        pass

    # ask user to select a rectangle around the object to analyse
    gui.msgbox("Crop the image. Press enter to confirm.")
    r=cv2.selectROI("Crop the image",image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    # show cropped image
    cropped=image[int(r[1]):int(r[1]+r[3]),int(r[0]):int(r[0]+r[2])]
    cropped=cv2.resize(cropped,(0,0),fx=2.3,fy=2.3) # VK changed from 2 to 3
    cv2.imshow("Cropped Image",cropped)
    #cv2.waitKey(0)
    #cv2.destroyAllWindows()

    # ask user if he wants to rotate the image, rotate in 90° steps, ask as long until the user is satisfied
    rotate=gui.boolbox("Do you want to rotate the image?",choices=("Yes","No"))
    while rotate:
        cropped=cv2.rotate(cropped,cv2.ROTATE_90_CLOCKWISE)
        cv2.imshow("Cropped Image",cropped)
        rotate=gui.boolbox("Do you want to rotate the image?",choices=("Yes","No"))
    cv2.destroyAllWindows()

    # We will save the original image and the cropped image. Save the original image in a folder called "original" and the cropped image in a folder called "cropped". The name of the files is based on the information the user entered before, the cropped image will have a suffix "_cropped" and all safed in png format.
    # create folders if they do not exist

    # ask if you want to save the images
    save=gui.boolbox("Do you want to save the images?",choices=("Yes","No"))
    if save:
        if not os.path.exists("original"):
            os.makedirs("original")
        if not os.path.exists("cropped"):
            os.makedirs("cropped")
        # save original image
        name="original/"+fieldValues[0]+"_"+fieldValues[1]+"_"+fieldValues[2]+".png"
        raw=cv2.imread(image_raw)
        cv2.imwrite(name,raw)
        # save cropped image
        name="cropped/"+fieldValues[0]+"_"+fieldValues[1]+"_"+fieldValues[2]+"_cropped.png"
        cv2.imwrite(name,cropped)

    ''' FROM HERE ON WE WILL USE THE CROPPED IMAGE TO ANALYSE THE INK AREA AND DO THE FURTHER ANALYSIS'''
    # Aks the user to select the rectangle around the object to analyse
    gui.msgbox("Please use the rectangle tool to select the metal sheet you want to analyse and press enter to confirm.")
    # crop image using a rectangle tool and confirm with enter. Ask the user if he is satisfied with the selection or wants to select a new rectangle
    r=cv2.selectROI(cropped)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    # show cropped image
    cropped=cropped[int(r[1]):int(r[1]+r[3]),int(r[0]):int(r[0]+r[2])]
    cropped=cv2.resize(cropped,(0,0),fx=2.3,fy=2.3) # VK changed from 2 to 3
    cv2.imshow("Metal sheet only",cropped)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    # Now ask the user to provide the dimension of the long side of the rectangle in mm and calculate the scale from pixel to mm
    length = gui.enterbox("Please enter the length of the object in mm")
    length = float(length)
    length_mm= length
    width_mm = length * r[3] / r[2]
    # the width is the short side of the rectangle in mm with two decimal places
    width_mm=round(width_mm,2)
    # calculate the scale from pixel to mm
    scale_mm_per_pixel = length_mm / r[2]
    scale_mm_per_pixel=round(scale_mm_per_pixel,2)
    gui.msgbox("Length: " + str(length_mm) + " mm\n" + "Width: " + str(width_mm) + " mm\n" + "Scale: " + str(scale_mm_per_pixel) + " mm/pixel\n")

    points = []
    while True:
        # select a point in the image
        gui.msgbox(title="Instructions", msg="Please skirt the outer boarders of the ink stain using multiple points. Press enter to confirm ALL points.")
        def mouse_callback(event, x, y, flags, param):
            if event == cv2.EVENT_LBUTTONDOWN:
                points.append((x, y))
                #cv2.circle(cropped, (x, y), 5, (0, 0, 255), -1)
                cv2.circle(cropped, (x, y), 2, (0, 0, 255), -1)
                cv2.imshow("Ink Area", cropped)

        cv2.imshow("Ink Area", cropped)
        cv2.setMouseCallback("Ink Area", mouse_callback)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        # ask if the user wants to define more points
        if not gui.ynbox("Do you want to define more points?"):
            break

    # connect all points with lines
    for i in range(len(points)-1):
        cv2.line(cropped, points[i], points[i+1], (0, 0, 255), 2)
    cropped_lines=cv2.line(cropped, points[-1], points[0], (0, 0, 255), 2)
    cv2.imshow("Ink Area", cropped_lines)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    # save the image with the lines in the folder cv_analysis
    if not os.path.exists("cv_analysis"):
        os.makedirs("cv_analysis")
    name="cv_analysis/"+fieldValues[0]+"_"+fieldValues[1]+"_"+fieldValues[2]+"_lines.png"
    cv2.imwrite(name,cropped_lines)

    # create a mask based on the points
    mask = np.zeros(cropped.shape[:2], dtype="uint8")
    cv2.fillPoly(mask, [np.array(points)], (255, 255, 255))
    cv2.imshow("Mask", mask)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    # based on the rectangle and the mask, calculate the two different areas in pixels and in mm^2
    area_rectangle_mm = length_mm * width_mm
    area_rectangle_pixel = cropped.shape[0] * cropped.shape[1]
    ratio = area_rectangle_mm / area_rectangle_pixel
    # calculate the area of the mask in pixels in mm^2
    area_mask_pixel = np.count_nonzero(mask)
    area_mask_mm = area_mask_pixel * ratio
    area_mask_mm=round(area_mask_mm,2)

    # Create a report with the following information: original image name based on name="original/"+fieldValues[0]+"_"+fieldValues[1]+"_"+fieldValues[2]+".png", length and width of the rectangle in mm, length and width of the rectangle in pixels, area of the rectangle in mm^2, scale from pixel to mm, area of the mask in pixel and in mm^2 and show it as print command in the terminal and in a msgbox
    report = "Original Image: " + fieldValues[0] + "_" + fieldValues[1] + "_" + fieldValues[2] + "\n" + "Length: " + str(length_mm) + " mm\n" + "Width: " + str(width_mm) + " mm\n" + "Length: " + str(r[2]) + " pixels\n" + "Width: " + str(r[3]) + " pixels\n" + "Area of the rectangle: " + str(area_rectangle_mm) + " mm^2\n" + "Scale: " + str(scale_mm_per_pixel) + " mm/pixel\n" + "Area of the mask: " + str(area_mask_pixel) + " pixels\n" + "Area of the mask: " + str(area_mask_mm) + " mm^2"
    print(report)
    gui.msgbox(report)


    # add the result for the are of the mask in mm to the cropped image as a text in mm². I want to put the text in the lower right corner of the image
    text="Name: "+fieldValues[0]+"_"+fieldValues[1]+"_"+fieldValues[2]
    font = cv2.FONT_HERSHEY_SIMPLEX
    bottomLeftCornerOfText = (10,50)
    fontScale = 1
    fontColor = (255,255,255)
    lineType = 2
    cv2.putText(cropped,text, bottomLeftCornerOfText, font, fontScale,fontColor,lineType)

    text2="Area: "+str(area_mask_mm)+" mm^2"
    font = cv2.FONT_HERSHEY_SIMPLEX
    bottomLeftCornerOfText = (10,80)
    fontScale = 1
    fontColor = (255,255,255)
    lineType = 2
    cv2.putText(cropped,text2, bottomLeftCornerOfText, font, fontScale,fontColor,lineType)
    cv2.imshow("Result of the analysis",cropped)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    # save the image with the mask in the folder cv_analysis
    if not os.path.exists("cv_analysis"):
        os.makedirs("cv_analysis")
    name="cv_analysis/"+fieldValues[0]+"_"+fieldValues[1]+"_"+fieldValues[2]+"_mask_tagged.png"
    cv2.imwrite(name,cropped)

    # save the mask in the folder cv_analysis
    if not os.path.exists("cv_analysis"):
        os.makedirs("cv_analysis")
    name="cv_analysis/"+fieldValues[0]+"_"+fieldValues[1]+"_"+fieldValues[2]+"_mask.png"
    cv2.imwrite(name,mask)

    # save the following variables in a csv file. The file is called "ink_area.csv" and has the following columns: "Name", "Length", "Width", "Area in mm^2", "Mask Area in mm^2", "Scale", "Area in pixels", "Mask Area in pixels". Change the decimal points with a comma and a semi colon as a separator
    import csv
    if not os.path.exists("ink_area.csv"):
        with open("ink_area.csv", mode="w", newline="") as file:
            writer = csv.writer(file, delimiter=";")
            writer.writerow(["Name", "Length", "Width", "Area in mm^2", "Mask Area in mm^2", "Scale", "Area in pixels", "Mask Area in pixels"])
            writer.writerow([fieldValues[0]+"_"+fieldValues[1]+"_"+fieldValues[2], str(length_mm).replace(".",","), str(width_mm).replace(".",","), str(area_rectangle_mm).replace(".",","), str(area_mask_mm).replace(".",","), str(scale_mm_per_pixel).replace(".",","), str(area_rectangle_pixel), str(area_mask_pixel)])
    else:
        with open("ink_area.csv", mode="a", newline="") as file:
            writer = csv.writer(file, delimiter=";")
            writer.writerow([fieldValues[0]+"_"+fieldValues[1]+"_"+fieldValues[2], str(length_mm).replace(".",","), str(width_mm).replace(".",","), str(area_rectangle_mm).replace(".",","), str(area_mask_mm).replace(".",","), str(scale_mm_per_pixel).replace(".",","), str(area_rectangle_pixel), str(area_mask_pixel)])

    print("The data was saved in the file ink_area.csv")

    # ask if the user wants to analyse a new image
    new=gui.boolbox("Do you want to analyse a new image?",choices=("Yes","No"))
    if not new:
        break
    else:
        continue