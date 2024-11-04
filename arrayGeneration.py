from openai import OpenAI
from random import randint
from math import sqrt
import re
from Correction import correction #importer la fonction correction


## Set the API key
#insert key
client = OpenAI(api_key="")
MODEL="gpt-4o"


def find_first_number(input_string):
    # Regular expression to find the first occurrence of a number in the string
    match = re.search(r'\d+', input_string)
    if match:
        return match.group()
    return -1

def find_second_number(input_string):
    # Regular expression to find all occurrences of numbers in the string
    matches = re.findall(r'\d+', input_string)
    # Return the second number if it exists
    if len(matches) > 1:
        return matches[1]
    return -1


    

def array_generating(sizeIndex = 2): 
    if sizeIndex < 0 or sizeIndex > 5: 
        sizeIndex = 2
    sizeArray = [5,10,15,20,25,30]
    user_prompt = f"Give me a {sizeArray[sizeIndex]} by {sizeArray[sizeIndex]} two dimensional array that satisfies the following conditions. 1) there are two possible values for each element: 0, 1. 3) The central element of the first row is a 0. 4) O's must be in groups of at least 7 0s."
    user_prompt = f"You are going to generate dungeon 2d maps. They will be represented as two dimensional arrays of size {sizeArray[sizeIndex]}x{sizeArray[sizeIndex]} elements. For each element you'll have to pick bet<een different values that mean different things : 0 means air, 1 means wall!; For every air tile you must be sure it is connected vertically or horizontally to at least one other air tile (except if it's on the borders). This is to be sure that correct paths are generated. Additionally, you will have to replace valid air tiles with map objects : 10 would be a treasure chest, 11 would be an enemy monster and 12 would be a trap. I am not asking you to give me code to generate the array. Try to have multiple paths but not too many as the map should mostly be made of walls, I'm not asking for a labyrinth. Only give the final map without any intermediary map."
    labyrinth = client.chat.completions.create(
    model=MODEL,
    messages=[
        {"role": "system", "content": "You are a helpful assistant that designs dungeons for me!"},
        {"role": "user", "content": user_prompt}
        ]
    )
    text = labyrinth.choices[0].message.content
    #print(text)
    testSeperated = text.split("```")

    arraySeperated = testSeperated[1].split("\n")

    array = []
    for i in range(1, len(arraySeperated) - 1):
        temptext = arraySeperated[i].strip()
        temptext = temptext.replace('[', '').replace(']', '').replace(',', '')
        tempArray = temptext.split()
        tempArray = [int(value) for value in tempArray]
        array.append(tempArray)
    return array


def eventsGenerating(diffIndx, sizeIndx):

    difficultyTable = ["Easy", "Medium", "Hard", "Extreme"]
    sizeTable = ["Tiny", "Small", "Medium", "Large", "Huge", "Gigantic"]

    difficulty = "Easy"
    size = "Small"
    if diffIndx >= 0 and diffIndx < 4: 
        difficulty = difficultyTable[diffIndx]
    if sizeIndx >= 0 and sizeIndx < 6: 
        size = sizeTable[sizeIndx]
    user_message = f"My dungeon's difficulty should be {difficulty}, and its size {size}. How many different rooms, traps, treasures, and monsters should it have? return this in a python dictionary format"
    events = client.chat.completions.create(
        model=MODEL, 
        messages=[
            {"role": "system", "content": "You are a helpful assistant that adds events to my dungeons"}, 
            {"role": "user", "content": user_message}
        ]
    )
    #print(events.choices[0].message.content)
    #print("Assistant123: " + events.choices[0].message.content)
    dictText = events.choices[0].message.content.split("```")[1]
    dictText = dictText.split(",")
    numberArray = []
    for i in range(len(dictText)): 
        numberArray.append(int(find_first_number(dictText[i])))
        #print("hi im the", i, "element in the split dicttext", dictText[i], "and my associated number is", dictText[i][-2:], "\n\n")

    #print("here is my dictText", dictText)
    #print("here is the number array", numberArray)
    while -1 in numberArray: 
        numberArray.remove(-1)
    return numberArray
    
def fullArrayGenerating(difficultyIndex = 2, sizeIndex = 3): 
    array = array_generating(sizeIndex)
    #for a in array:
        #print(a)
    # convertir en int pour la fonction correction
    array = [[int(element) for element in row] for row in array]
    
    #appliquer la correction
    array = correction(array)
    
    #remettre en string après
    #array = [[str(element) for element in row] for row in array]

     #index to differentiate path and rock from events
     #rooms is +0, traps is +1, treasures is +2, monsters is +3
    eventStartIndx = 10
    arrayOfZeroes = []
    arrayOfOnes = []
    for i in range(len(array)):
        for j in range(len(array[i])):
            if array[i][j] == 0:
                arrayOfZeroes.append([i,j])
            else:
                arrayOfOnes.append([i,j])
        nbZeroes = len(arrayOfZeroes)
    usedZeroes = 0
    nbOnes = len(arrayOfOnes)
    usedOnes = 0
    
    
    eventTable = eventsGenerating(difficultyIndex, sizeIndex)
    
    #print("this is my event table", eventTable)
    
    
    for typesOfEvents in range(len(eventTable)):
        for numberPerEvent in range(eventTable[typesOfEvents]):
            #print("im at the {numberPerEvent} step", numberPerEvent)
            if(nbZeroes - usedZeroes - 1 > 0):
                 #print("still on zeroes, remaining are", nbZeroes - usedZeroes - 1)
                elementToReplace = randint(0, nbZeroes - usedZeroes - 1)
                array[ arrayOfZeroes[elementToReplace][0] ][arrayOfZeroes[elementToReplace][1]] = eventStartIndx + typesOfEvents
                arrayOfZeroes.pop(elementToReplace)
                usedZeroes += 1
            #elif (nbOnes - usedOnes - 1 > 0):
                 #print("now on ones, remaining are", nbOnes - usedOnes - 1)
                #elementToReplace = randint(0, nbOnes - usedOnes - 1)
                 #array[ arrayOfOnes[elementToReplace][0] ][arrayOfOnes[elementToReplace][1]] = eventStartIndx + typesOfEvents
                #arrayOfOnes.pop(elementToReplace)
                #usedOnes += 1
            
                 #print("saturated, stop counting from here")
    #
    #
    #
    array.pop(0)
    array.pop(len(array)-1)
    #for a in array:
        #print(a)
    # print("starting room creation")
    # roomCreation(array, eventStartIndx)
    # print("done with array")

    #print("done with events")
    return array




def topLoop(start, end, size, yValue, array): 
    going = min(size, abs(end-start))
    for i in range(going): 
        if testIfInArray(array, yValue, start+i): 
            if (array[yValue][start+i] == 1 or array[yValue][start+i] == 2):
                array[yValue][start+i] = 0

    #size -= going

def rightSideLoop(start,end,size, xValue, array): 
    going = min(size, abs(end-start))
    for i in range(going): 
        if testIfInArray(array, start+i, xValue): 
            if (array[start+i][xValue] == 1 or array[start+i][xValue] == 2): 
                array[start+i][xValue] = 0

    #size -= going

def bottomLoop(start,end,size,yValue, array): 
    going = min(size, abs(end-start))
    for i in range(going): 
        if testIfInArray(array, yValue, start-i): 
            if (array[yValue][start-i] == 1 or array[yValue][start-i] == 2): 
                array[yValue][start-i] = 0

    #size -= going

def leftSideLoop(start, end, size, xValue, array): 
    going = min(size, abs(end-start))
    for i in range(going): 
        if testIfInArray(array, start-i, xValue): 
            if(array[start-i][xValue] == 1 or array[start-i][xValue] == 2):
                array[start-i][xValue] = 0

    #size -= going  

def testIfInArray(twoDarray, y, x): 
    
    if y >= 0 and y < len(twoDarray) and len(twoDarray) > 0 and x >= 0 and x < len(twoDarray[0]): 
        return True
    return False



def createRoom(xAxis, yAxis, inputSize, array): 
    minX = xAxis - 1
    maxX = xAxis + 1
    minY = yAxis - 1
    maxY = yAxis + 1
    currentX = xAxis
    currentY = yAxis - 1
    size = inputSize

    #spirals around the origin of the room until all 'tiles' are added,
    #if a tile is not a rock tile, it already 'is' in the room, so will nto be replaced
    while size > 0: 
        #print("size is", size)
        if currentX >= minX and currentX < maxX and currentY == minY: 
            topLoop(currentX, maxX, size, currentY, array)
            #print("in toploop, min is", min(size, abs(maxX-currentX)))
            size -= min(size, abs(maxX-currentX))
            currentX = maxX
            

        elif currentX == maxX and currentY < maxY and currentY >= minY: 
            rightSideLoop(currentY, maxY, size, currentX, array)
            #print("in rightSide loop, min is", min(size, abs(maxY-currentY)))
            size -= min(size, abs(maxY-currentY))
            currentY = maxY
            
        
        elif currentX == maxX and currentY == maxY: 
            bottomLoop(currentX, minX, size, currentY, array)
            #print("bottomLoop min is", min(size, abs(minX-currentX)))
            size -= min(size, abs(minX-currentX))
            currentX = minX
            
                 
        elif currentX == minX and currentY == maxY:
            leftSideLoop(currentY, minY, size, currentX, array)
            #print("left side loop, min is", min(size, abs(minY - currentY)))
            size -= min(size, abs(minY - currentY))
            currentY = minY
        elif currentX == minX and currentY == minY: 
            #print("not in a loop, size is", size)
            minX -= 1
            maxX += 1
            minY -= 1
            maxY += 1


def roomCreation(inputArrayWithEvents, roomValue): 
    sizeOfArray = len(inputArrayWithEvents)
    minRoomSize = 1
    maxRoomSize = int(sqrt(sizeOfArray))
    for i in range(sizeOfArray): 
        for j in range(sizeOfArray): 
            if inputArrayWithEvents[i][j] == roomValue: 
                sizeOfRoom = randint(minRoomSize, maxRoomSize)
                createRoom(i,j,sizeOfRoom, inputArrayWithEvents)