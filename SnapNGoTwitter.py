import twitter, re, json, csv
from datetime import *

class Task:
    def __init__(self, id, location, datetime, compensation):
        self.id = id
        self.location = location
        self.datetime = datetime
        self.compensation = compensation
        self.tweetSent = False
        self.tweetSentTime = 0
        self.assignedTo = ''
        self.taskSubmitted = False
        self.submissionPhotoLink = ''
        self.submissionTime = 0

    def toString(self):
        return 'Task ID: ' + str(self.id) + '\t Location: ' + self.location + '\t Date: ' + self.datetime.strftime("%B %d, %Y %I:%M%p") + '\t Compensation:' + str(self.compensation) + '\n'

    def scheduleTweet(self, tweet_time):
        # TODO: add threading to schedule task (this methond doesn't do anything right now
        now = datetime.now()
        delay = (tweet_time - now).total_seconds()
        print('Delay: ' + delay)

    def sendTaskTweet(self, api):
        if(not self.tweetSent):
            api.PostUpdate(self.toString())
            self.tweetSent = True
            self.tweetSentTime = datetime.now()

    def getFileRow(self):
        return [self.id, self.location, self.datetime.strftime("%B %d, %Y %I:%M%p"), self.compensation, self.tweetSent, self.tweetSentTime, self.assignedTo, self.taskSubmitted, self.submissionPhotoLink, self.submissionTime]

class SnapNGo:
    def __init__(self):
        self.task_ID = 1
        self.task_dictionary = {}

        keys = json.load(open('keys.json'))
        self.consumer_key = keys['consumer_key']
        self.consumer_key_secret = keys['consumer_key_secret']

        self.access_token = keys['access_token']
        self.access_token_secret = keys['access_token_secret']

        self.api = twitter.Api(
            consumer_key=self.consumer_key,
            consumer_secret=self.consumer_key_secret,
            access_token_key=self.access_token,
            access_token_secret=self.access_token_secret)

    def selectAction(self):
        print("Type '1' to add new tasks")
        print("Type '2' to tweet unsent tasks")
        print("Type '3' to print all tasks")
        print("Type '4' to write tasks to a file")
        print("Type 'EXIT' to exit the program")
        action = raw_input('>')

        while(action != 'EXIT'):
            if(action == '1'):
                print('Type 1 to enter tasks via command line, Type 2 to input tasks through a file')
                enter_tasks = raw_input('>>')
                if(enter_tasks == '1'):
                    self.addTasksViaCommandLine()
                if(enter_tasks == '2'):
                    print('Type the name of the file')
                    file_name = raw_input('>>>')
                    self.addTasksViaFile(file_name)
            if(action == '2'):
                self.sendUnsentTweets()
            if (action == '3'):
                self.printTasks()
            if (action == '4'):
                print('Write the name of the file to write tasks to:')
                file_name = raw_input('>>')
                self.writeTasksToFile(file_name)

            print("Type '1' to add new tasks")
            print("Type '2' to tweet unsent tasks")
            print("Type '3' to print all tasks")
            print("Type '4' to write tasks to a file")
            print("Type 'EXIT' to exit the program")
            action = raw_input('>')

    def addTasksViaCommandLine(self):
        input = raw_input('Please enter a task in the following format: location, month, day, year, hour, minutes\n>')
        while(input != 'end'):
            #check to see if input has correct length and is otherwise correct format
            input_array = re.sub(r'\s', '', input).split(',')
            task_date = date(int(input_array[3]), int(input_array[1]), int(input_array[2]))
            task_time = time(int(input_array[4]), int(input_array[5]))
            task_datetime = datetime.combine(task_date, task_time)

            self.task_dictionary[self.task_ID] = Task(self.task_ID, input_array[0], task_datetime, input_array[6])
            print('New task created: ' + self.task_dictionary[self.task_ID].toString())
            self.task_ID += 1

            input = raw_input('>')

        print 'All tasks: \n'
        self.printTasks()

    def addTasksViaFile(self, file_name):
        with open(file_name, 'rb') as task_file:
            reader = csv.reader(task_file)
            skip_header = 0
            for row in reader:
                if skip_header > 0:
                    location = row[0]
                    compensation = row[6]
                    task_date = date(int(row[3]), int(row[1]), int(row[2]))
                    task_time = time(int(row[4]), int(row[5]))
                    task_datetime = datetime.combine(task_date, task_time)
                    self.task_dictionary[self.task_ID] = Task(self.task_ID, location, task_datetime, compensation)
                    self.task_ID += 1
                skip_header += 1
            print "Completed. " + str(skip_header) + " tasks read from " + file_name

    def sendUnsentTweets(self):
        send_tweet = raw_input('Are you sure you would like to send tweets for tasks not already sent? Type Y for yes and N for no')
        if (send_tweet == 'Y'):
            tweets_sent = 0
            for i in range(self.task_ID - 1):
                if(not self.task_dictionary[i + 1].tweetSent):
                    self.task_dictionary[i + 1].sendTaskTweet(self.api)
                    tweets_sent += 1

        print("Finished. " + str(tweets_sent) + " were sent.")

    def printTasks(self):
        s = ''
        for i in range(self.task_ID-1):
            s += self.task_dictionary[i+1].toString()
        print('All Tasks:\n' + s)

    def writeTasksToFile(self, file_name):
        with open(file_name, 'wb') as file:
            file_writer = csv.writer(file)
            file_writer.writerow(['Task ID', 'Location', 'Date', 'Compensation', 'Tweet Sent', 'Tweet Sent Time', 'Assigned To', 'Task Submitted', 'Submission Photo Link', 'Submission Time'])
            for id in range(1, self.task_ID):
                file_writer.writerow(self.task_dictionary[id].getFileRow())

        print "Completed. " + str(self.task_ID -1) + " tasks written to " + file_name

if __name__ == '__main__':
    SnapNGo().selectAction()