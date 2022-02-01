import cv2 as cv
LOGITECH_RESIZE_HEIGHT = 288
LOGITECH_RESIZE_WIDTH = 352
MACBOOK_CAM_RESIZE_HEIGHT = 288
MACBOOK_CAM_RESIZE_WIDTH = 352


def get_dimensions() :

    # 1.1. Ouvrir le flux video
    cap = cv.VideoCapture(0)
    if not cap.isOpened():
        print("Cannot open camera")
        exit()

    # 1.2. Récupérer les dimensions dans capX et capY
    capX = cap.get(cv.CAP_PROP_FRAME_WIDTH)
    capY = cap.get(cv.CAP_PROP_FRAME_HEIGHT)

    # 2. Set VideoCapture dimensions to (capX = 160, capY = 90)

    # 2.0. On vérifie les valeurs des variables avant modification
    # print("capX = " + str(capX))
    # print("capY = " + str(capY))

    # 2.1. Set dimensions
    cap.set(cv.CAP_PROP_FRAME_WIDTH, LOGITECH_RESIZE_WIDTH)
    cap.set(cv.CAP_PROP_FRAME_HEIGHT, LOGITECH_RESIZE_HEIGHT)

    # 2.2. On récupère les nouvelles valeurs dans capX et capY
    capX = cap.get(cv.CAP_PROP_FRAME_WIDTH)#160
    capY = cap.get(cv.CAP_PROP_FRAME_HEIGHT)#90

    # 2.3. On vérifie les valeurs des variables après modification
    # print("capX = " + str(capX))
    # print("capY = " + str(capY))

    # 2.4. On vérifie la possibilité de prendre une capture dans le flux
    success, frame = cap.read()
    if success is True :
        capY = int(frame.shape[0])
        capX = int(frame.shape[1])
        #print("capX orginal frame = " + str(capX))
        #print("capY orignal frame = " + str(capY))
    else :
        print("Problem capturing a frame")
        exit()

    # 2.5 on retourne capX, capY
    return cap, capX, capY