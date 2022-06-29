import os
import json
from matplotlib.cbook import simple_linear_interpolation
import pandas
import matplotlib.pyplot as plt

# Getting Snapchat JSON Files
jsonFolder = input("Enter directory where Snapchat data is located: ")
os.chdir(jsonFolder + "/json")

'''
Function returns array of Pandas dataframes of each category given in parameters
'''
def extract( file, category, objects ):
    jsonFile = open(file)
    jsonText = json.load(jsonFile)

    dict = jsonText[category]
    dFrame = pandas.DataFrame.from_dict(dict)
    dFrame = dFrame[objects]
    return dFrame

'''
Function prints out total number of friends, five most recently added friends, and five oldest friends 
within the given data timeframe
'''
def friendStats():
    # friend.json extraction
    cols = ["Username", "Display Name", "Creation Timestamp"]
    categories = ["Friends"]
    dFrame = extract("friends.json", categories[0], cols)
    
    # Parsing dataframe for print
    dFrame.rename(columns = {"Creation Timestamp":"Date Added"}, inplace = True )
    dFrame["Date Added"] = pandas.to_datetime(dFrame["Date Added"], format="%Y-%m-%d %H:%M:%S %Z")
    dFrame.sort_values(by=["Date Added"], inplace=True, ascending=False)
    dFrame["Date Added"] = dFrame["Date Added"].dt.strftime("%m/%d/%Y")
    startDate = dFrame.iloc[-1]['Date Added']
    endDate = dFrame.iloc[0]['Date Added']

    # Printing Results
    print('\033[1m', "Total Number of Friends: ", '\033[0m', dFrame.shape[0], "\n")
    print('\033[1m', "Five Most Recent Friends:\n",'\033[0m', dFrame.head())
    print('\033[1m', "\nFive Oldest Friends:\n",'\033[0m', dFrame.tail(), "\n")
    print('\033[1m', "Date Range for Data Values: ", '\033[0m', startDate, " to ", endDate, "\n")


'''
Function prints out message counts, media type counts, most messages sent to/from a user, 
monthly average of messages, yearly totals of messages, and favorite word sent in chat
'''
def chatStats():
    # chat_history.json extraction
    cols = [["From", "Media Type", "Created", "Text"], ["To", "Media Type", "Created", "Text"]]
    categories = ["Received Saved Chat History", "Sent Saved Chat History", 
                  "Received Unsaved Chat History", "Sent Unsaved Chat History"]
    dFrames = [ extract("chat_history.json", categories[0], cols[0]), 
                extract("chat_history.json", categories[1], cols[1]), 
                extract("chat_history.json", categories[2], cols[0]), 
                extract("chat_history.json", categories[3], cols[1])]
    
    # Parsing dataframes for print
    # TODO

    # Printing Results
    for i in dFrames:
        print( i.head())


'''
Function prints out snap counts, media type counts, most snaps sent to/from a user,
monthly average of snaps, and yearly totals of snaps
'''
def snapStats():
    # snap_history.json extracation
    cols = [["From", "Media Type", "Created"], ["To", "Media Type", "Created"]]
    categories = ["Received Snap History", "Sent Snap History"]
    dFrames = [ extract("snap_history.json", categories[0], cols[0]), 
                extract("snap_history.json", categories[1], cols[1])]

    # Parsing dataframes for print
    # TODO

    # Printing Results
    for i in dFrames:
        print( i.head())

'''
Function prints out most / least stories viewed and total number of stories viewed within the given data timeframe
'''
def storyStats():
    # story_history.json extraction
    cols = ["View", "Media Type", "View Date"]
    categories = ["Friend and Public Story Views"]
    dFrame = extract("story_history.json", categories[0], cols)

    # Parsing dataframes for print
    dFrame["View Date"] = pandas.to_datetime(dFrame["View Date"], format="%Y-%m-%d %H:%M:%S %Z")
    dFrame.sort_values(by=["View Date"], inplace=True, ascending=False)
    dFrame["View Date"] = dFrame["View Date"].dt.strftime("%m/%d/%Y")
    startDate = dFrame.iloc[-1]['View Date']
    endDate = dFrame.iloc[0]['View Date']

    storyViews = {}
    totalStories = 0
    for index, row in dFrame.iterrows():
        if row["Media Type"] == "STORY" or row["Media Type"] == "VIDEO":
            key = row["View"]
            storyViews[key] = storyViews.get(key, 0) + 1
            totalStories += 1
    dFrame = pandas.DataFrame(list(storyViews.items()), columns=['Username', 'Views'])
    dFrame.sort_values(by=["Views"], inplace=True, ascending=False)

    # Printing Results
    print('\033[1m', "Total Number of User Stories Viewed: ", '\033[0m', totalStories, "\n")
    print('\033[1m', "Five Most Viewed User Stories:\n",'\033[0m', dFrame.head())
    print('\033[1m', "\nFive Least Viewed User Stories:\n",'\033[0m', dFrame.tail(), "\n")
    print('\033[1m', "Date Range for Data Values: ", '\033[0m', startDate, " to ", endDate, "\n")


'''
Function prints out breakdown of time spent on app and creates pie chart of values
'''
def timeStats():
    # user_profile.json extraction 
    # cannot use extract function with different file structure
    jsonFile = open("user_profile.json")
    jsonText = json.load(jsonFile)
    jsonString = jsonText["Breakdown of Time Spent on App"]
    categories = []
    percentSpent = []

    # Printing time breakdown values while storing into dataframe
    print('\033[1m', "Breakdown of Time Spent on App:", '\033[0m')
    for i in jsonString:
        print("  ", i)
        temp = i.split(": ", 1)
        categories.append(temp[0])
        percentSpent.append(float(temp[1].strip('%')))
    
    # Displaying pie chart of time breakdown
    dFrame = pandas.DataFrame({'percentages': percentSpent}, index=categories)
    plot = dFrame.plot.pie(y='percentages', figsize=(5,5))
    plt.show()
    print("\n")


# Main loop for analyzer
userInput = ''
while userInput != '0':
    print("=======================================================================\n") # Divider

    # Choices for which data to print and provide information for
    print("[1] View Snapchat friend statistics")                     # friends.json
    print("[2] View chat message statistics")                          # chat_history.json
    print("[3] View snap message statistics")                          # snap_history.json
    print("[4] View story history statistics")                         # story_history.json
    print("[5] View time breakdown of time spent on Snapchat")         # user_profile.json
    print("[0] Exit the Snapchat Analyzer Program")                    # Exit program
    userInput = input("\n\nWhat statistic would you like to see: ")    # Input

    print("\n=======================================================================\n") # Divider

    if userInput == '1':
        friendStats()
    elif userInput == '2':
        chatStats()
    elif userInput == '3':
        snapStats
    elif userInput == '4':
        storyStats()
    elif userInput == '5':
        timeStats()
    elif userInput == '0':
        print("Exiting program now...\n")
    else:
        print("Sorry, you could you provide a valid choice.\n")