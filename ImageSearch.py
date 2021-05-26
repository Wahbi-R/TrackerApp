import cv2
import numpy as np
import os
import pytesseract

#TODO: ASK USER ZONE, ASK USER FOR INVENTORY SCREENSHOT
inventory = cv2.imread('public/Full_InventoryAsh.png', 1)
#Take Area from User prompt
grindArea = "/public/Zones/AshForest"
#Look for folder with area in it
directoryPath = os.path.dirname(os.path.realpath(__file__)) + grindArea

itemsInInventory = []
pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'
#Make a list of items to search for
items = []
for filename in os.listdir(directoryPath):
    item = cv2.imread(os.path.join(directoryPath,filename), 1)
    if item is not None:
        items.append(item)

#item = cv2.imread('public/Zones/BlackStones/ArmorStone.png', 1)
#iterate and search through the list
for i in range(len(items)):
    
    w, h = items[i].shape[:-1]
    #print(items[i].shape)
    #print(items[i].shape[:-1])
    #Get the matching
    
    res = cv2.matchTemplate(inventory,items[i],cv2.TM_CCOEFF_NORMED)
    #Get values for matched location
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

    #Check if matched image is within threshold
    threshold = 0.75
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    if max_val > threshold:
        #setting corners of item
        top_left = max_loc
        bottom_right = (top_left[0] + w*2, top_left[1] + h)

        #Creating square around it
        cv2.rectangle(inventory, top_left, bottom_right, (0,0,255), 2)
        #print("Top Left: ", top_left)
        #print("Bottom Right: ", bottom_right)

        #cropping image to square
        tempItem = inventory[top_left[1]+20:bottom_right[1], top_left[0]:bottom_right[0]]

        #make it black and white
        gray = cv2.cvtColor(tempItem, cv2.COLOR_BGR2GRAY)
        # cv2.imshow("cropped", tempItem)
        # cv2.waitKey(0)
        itemsInInventory.append(tempItem)

        #this doesn't work properly! TRYING TO MAKE TEXT CLEARER (NOT IN ACTUAL USE)
        sharpen_kernel = np.array([[-1,-1,-1], [-1,9,-1], [-1,-1,-1]])
        sharpen = cv2.filter2D(gray, -1, sharpen_kernel)
        cv2.imshow('sharpen.png', sharpen)
        sharpen = 255 - sharpen
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2,2))
        #dilate = cv2.dilate(sharpen, kernel, iterations=1)
        result = 255 - kernel
        cv2.imshow('result.png', gray)
        cv2.waitKey(0)
        
        #gray = cv2.cvtColor(sharpen, cv2.COLOR_BGR2GRAY)
        #Making the image text easier to read
        thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
        invert = 255 - thresh
        #converting text to string
        text = pytesseract.image_to_string(invert, lang='eng', config='--psm 11 -c tessedit_char_whitelist=0123456789')
        print(text)
    if max_val < threshold:
        print("No matches found")
    #print(max_val)

#Show inventory
# for i in range(len(itemsInInventory)):
#     text = pytesseract.image_to_string(itemsInInventory[i])
#     print(text)
cv2.imshow('Inventory', inventory)  
cv2.waitKey(0)