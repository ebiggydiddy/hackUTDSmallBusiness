
#from imageai.Detection import ObjectDetection
#import osimport 
import googlemaps
import tkinter as tk
import requests
import math

def ObjectAnalysis():
    
    execution_path = "D:\\HackUTD\\couldWork" #wherever your "yolov.pt" file is
    """
    trying to do the extra camera bit:
    import cv2
    cap = cv2.VideoCapture(0)
    """

    fileCarousel=["R2.jpg","R1.jpg","C2.jpg","J1.jpg","J3.jpg","P2.jpg","R1.jpg",]
    """
    folder_path='C:\\path\\to\\picture\\folder'

    files=os.listdir(folder_path)
    files=[os.path.join(folder_path,file) for file in files if os.path.isfile(os.path.join(folder_path,file))]

    if files:
        latest_file= max(files, key= os.path.getmtime)
    """
    detector = ObjectDetection()
    detector.setModelTypeAsYOLOv3()
    detector.setModelPath(os.path.join(execution_path , "yolov3.pt"))
    detector.loadModel()

    detections = detector.detectObjectsFromImage(input_image=os.path.join(execution_path , "R2.jpg"), output_image_path=os.path.join(execution_path , "imagenew.jpg"))

    items = ["plant","clock","vase","chair","table","dining table","person","people"]
    global count
    for eachObject in detections:
        if eachObject["name"] in items:
            count+=1 + items.index(eachObject["name"])
        #print(eachObject["name"] , " : " , eachObject["percentage_probability"] )

    if count != 0:
        print("your buisness has...",count,"...value!")

def proximityAnalysis(userFullAddress):
    API = open("googleMapsAPIKey.txt", "r")
    APIKey = API.read()

    Maps = googlemaps.Client(key = APIKey)

    geocoding_url = 'https://maps.googleapis.com/maps/api/geocode/json?'

    geocoding_params = {
        'address': userFullAddress,
        'key': APIKey
    }

    geocoding_response = requests.get(geocoding_url, params=geocoding_params).json()

    location1 = None

    if geocoding_response['status'] == 'OK':
        # Extract latitude and longitude from the geocoding response
        geometry = geocoding_response['results'][0]['geometry']
        latitude = geometry['location']['lat']
        longitude = geometry['location']['lng']
        location1 = f"{float(latitude)},{float(longitude)}"
    else:
        print("Geocoding request failed with status:", geocoding_response['status'])


    waterResults = Maps.places_nearby(location = location1, radius = 8046.72, open_now = False, keyword = 'lake', type = 'natural_feature')

    closestLocations = {}
    for place in waterResults['results']:
        placeID = place['place_id']
        myFields = ['name', 'geometry/location']
        placeDetails = Maps.place(place_id = placeID, fields = myFields)
        name = placeDetails.get('result').get('name', 'N/A')
        geometry = placeDetails.get('result').get('geometry', {})
        location = geometry.get('location', {})
        lat = location.get('lat', 'N/A')
        lng = location.get('lng', 'N/A')

        lat1 = math.radians(float(latitude))
        lon1 = math.radians(float(longitude))
        lat2 = math.radians(lat)
        lon2 = math.radians(lng)

        # Calculate the distance using the formula
        distanceFromEntered = 0.621371 * 6371 * math.acos(math.sin(lat1) * math.sin(lat2) + math.cos(lat1) * math.cos(lat2) * math.cos(lon2 - lon1))

        if (distanceFromEntered < 10.0 and not('resovoir' in name) and not('Reservoir' in name)):
            closestLocations[name] = round(distanceFromEntered, 2)
    
    return closestLocations

window = tk.Tk()
window.title("Home Screen")
window.geometry("800x800")
window.resizable(False, False)

title = tk.Label(window, text="H2OOPS: Splashing Into Flood Coverage!", font = ("Times New Roman", 40)).pack(pady=7.5)

def userInput():
    global nearestPlaces, option1, option2, option3, option4, option5, result
    nearestPlaces = proximityAnalysis(addressEntry.get())
    
    nameArray = []
    milesArray = []
    
    i = 0
    for name in nearestPlaces:
        nameArray.append(name)
        milesArray.append(nearestPlaces[name])
        i+=1
    if len(nameArray) == 1:
        option1 = tk.Label(proximity, text= nameArray[0] + " is " +  str(milesArray[0]) + " miles away.", font = ("Times New Roman", 20), borderwidth=5, relief="ridge").pack(pady=15)
    elif len(nameArray) == 2:
        option1 = tk.Label(proximity, text= nameArray[0] + " is " +  str(milesArray[0]) + " miles away.", font = ("Times New Roman", 20), borderwidth=5, relief="ridge").pack(pady=15)
        option2 = tk.Label(proximity, text= nameArray[1] + " is " +  str(milesArray[1]) + " miles away.", font = ("Times New Roman", 20), borderwidth=5, relief="ridge").pack(pady=15)
    elif len(nameArray) == 3:
        option1 = tk.Label(proximity, text= nameArray[0] + " is " +  str(milesArray[0]) + " miles away.", font = ("Times New Roman", 20), borderwidth=5, relief="ridge").pack(pady=15)
        option2 = tk.Label(proximity, text= nameArray[1] + " is " +  str(milesArray[1]) + " miles away.", font = ("Times New Roman", 20), borderwidth=5, relief="ridge").pack(pady=15)
        option3 = tk.Label(proximity, text= nameArray[2] + " is " +  str(milesArray[2]) + " miles away.", font = ("Times New Roman", 20), borderwidth=5, relief="ridge").pack(pady=15)
    elif len(nameArray) == 4:
        option1 = tk.Label(proximity, text= nameArray[0] + " is " +  str(milesArray[0]) + " miles away.", font = ("Times New Roman", 20), borderwidth=5, relief="ridge").pack(pady=15)
        option2 = tk.Label(proximity, text= nameArray[1] + " is " +  str(milesArray[1]) + " miles away.", font = ("Times New Roman", 20), borderwidth=5, relief="ridge").pack(pady=15)
        option3 = tk.Label(proximity, text= nameArray[2] + " is " +  str(milesArray[2]) + " miles away.", font = ("Times New Roman", 20), borderwidth=5, relief="ridge").pack(pady=15)
        option4 = tk.Label(proximity, text= nameArray[3] + " is " +  str(milesArray[3]) + " miles away.", font = ("Times New Roman", 20), borderwidth=5, relief="ridge").pack(pady=15)
    else:
        option1 = tk.Label(proximity, text= nameArray[0] + " is " +  str(milesArray[0]) + " miles away.", font = ("Times New Roman", 20), borderwidth=5, relief="ridge").pack(pady=15)
        option2 = tk.Label(proximity, text= nameArray[1] + " is " +  str(milesArray[1]) + " miles away.", font = ("Times New Roman", 20), borderwidth=5, relief="ridge").pack(pady=15)
        option3 = tk.Label(proximity, text= nameArray[2] + " is " +  str(milesArray[2]) + " miles away.", font = ("Times New Roman", 20), borderwidth=5, relief="ridge").pack(pady=15)
        option4 = tk.Label(proximity, text= nameArray[3] + " is " +  str(milesArray[3]) + " miles away.", font = ("Times New Roman", 20), borderwidth=5, relief="ridge").pack(pady=15)
        option5 = tk.Label(proximity, text= nameArray[4] + " is " +  str(milesArray[4]) + " miles away.", font = ("Times New Roman", 20), borderwidth=5, relief="ridge").pack(pady=15)
    
    total = 0
    for num in milesArray:
        total += num
    average = total/(len(milesArray))
    
    chances = (len(milesArray) / 10) * (1 - (average / 20))
    
    result = tk.Label(proximity, text= "Your Liklihood of Flooding by Region Is: " + str(round(chances*100, 2)) + "%", font = ("Times New Roman", 30), fg="#73628A", bg = "#CBC5EA", borderwidth=5, relief="ridge").pack(pady=30)
        
    
    gameBtn1 = tk.Button(proximity, text="Close Window", command = proximity.destroy, relief="ridge").pack()

def resultsCalculation():
    percent = count

def proximityOpen():
  #All throughout the program I use the global declaration to dismiss any variable locality errors and it allows me to chnage values across functions
  global gameLabel1, startGameB, gameBtn1, proximity, addressEntry, gameBtn0
  proximity = tk.Toplevel(bg ="#EAEAEA")
  proximity.title("Home Screen")
  proximity.geometry("800x800")
  gameLabel1 = tk.Label(proximity, text="Find out your liability towards flooding!\nPlease input your address below:", font = ("Times New Roman", 40), bg = '#313D5A', borderwidth=5, relief="ridge").pack(pady=15)
  addressEntry = tk.Entry(proximity, width = 30, bg = "#CBC5EA", fg ="black", borderwidth = 2)
  addressEntry.pack(pady=15)
 
  addressEntry.insert(0, "Enter your address")
  gameBtn0 = tk.Button(proximity, text="Enter Data", command = userInput, relief="ridge").pack(pady = 10)
  
def objectOpen():
  global object, objectLabel, objectBtn, objectActionBtn
  object = tk.Toplevel(bg ="#EAEAEA")
  object.title("Object Recognition Screen")
  object.geometry("800x800")
  objectLabel = tk.Label(object, text="Find out your assets' liability against flooding!", font = ("Times New Roman", 40), bg = '#313D5A', borderwidth=5, relief="ridge").pack(pady=15)
  objectActionBtn = tk.Button(object, text="Activate Recognizer", command = ObjectAnalysis, relief="ridge").pack(pady = 10)
  
  objectBtn = tk.Button(object, text="Close Window", command = object.destroy, relief="ridge").pack()

def resultsOpen():
  global results, resultsLabel, resultsBtn
  results = tk.Toplevel(bg ="#EAEAEA")
  results.title("Reccomentation Screen")
  results.geometry("800x800")
  resultsLabel = tk.Label(results, text="View your recommended insurance plan!", font = ("Times New Roman", 40), bg = '#313D5A', borderwidth=5, relief="ridge").pack(pady=15)
  resultsBtn = tk.Button(results, text="Close Window", command = results.destroy, relief="ridge").pack()
  
#floodIMG = tk.PhotoImage(file = 'flood.png', width = 525, height = 485)
#flood = tk.Label(window, image = floodIMG).pack(pady = 5)

#Creating a base frame to use for buttons on the home screen
frame = tk.LabelFrame(text="", padx=50, pady = 50, borderwidth = 5)
frame.pack(padx = 5, pady=5)

#Making the buttons for the home screen each calling upon the function to open their according windows
infoB = tk.Button(frame, text = "Flood Proximity", font = ("Times New Roman", 13), height= 8, width=22, command = proximityOpen)
quizB = tk.Button(frame, text = "Object Recognition", font = ("Times New Roman", 13), height= 8, width=22, command = objectOpen)
gameB = tk.Button(frame, text = "Recommended Insurance", font = ("Times New Roman", 13), height= 8, width=22, command  =resultsOpen)
#Organizing the buttons to adaptively fit on the screen using the grid system, making them organized
infoB.grid(row=0, column=0, sticky="NESW")
quizB.grid(row=0, column=1, sticky="NESW")
gameB.grid(row=0, column=2, sticky="NESW")
 
# Execute Tkinter
tk.mainloop()



