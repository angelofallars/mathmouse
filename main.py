import discord
import os
import random
import asyncio
import csv
from dotenv import load_dotenv

# Get token
load_dotenv()
TOKEN = os.getenv('TOKEN')


def add_user(user_id, score=0):
    '''Check if user is in the scores.csv file.
    If not, add them to the scores.csv file.

    user_id - The Discord user's ID
    '''

    with open('scores.csv', mode='r') as csv_file:
        reader = csv.reader(csv_file)
        rows = list(reader)

        # Check if the user is already in the database just in case
        for row in rows:
            if row[0] == user_id:
                return True

        rows.append([user_id, score])

        # Commit changes to csv file
        with open('scores.csv', mode='w', newline='') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerows(rows)
        return False


def update_score(user_id, score=0):
    '''Update user's score by 'score' amount in scores.csv

    user_id - The Discord user's ID
    score - The amount by which to change their score
    '''

    # Add the user if not in database yet
    add_user(user_id)

    with open('scores.csv', mode='r') as csv_file:
        reader = csv.reader(csv_file)
        rows = list(reader)

        # Find the user's id
        for row in rows:
            if row[0] == user_id:
                # Update the user's score
                row[1] = int(row[1]) + score
                break

    # Commit changes to csv file
    with open('scores.csv', mode='w', newline='') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerows(rows)


class MathQuiz(discord.Client):
    async def on_ready(self):
        print('Logged in as')
        print(self.user.name)
        print(self.user.id)
        print('------')

    async def on_message(self, message):
        # Don't make the bot reply to itself
        if message.author.id == self.user.id:
            return

        print('Message from {0.author} {0.author.id}: {0.content}'.format(message))
        chnl = message.channel

        # Split the message into a list of args like a command line arg
        args = message.content.split()

        # COMMAND: Addition quiz
        if args[0] == 'm.add':
            timeout = 5
            question_count = 5
            score = 0

            # Send the pre-quiz messages for the user
            await chnl.send("Starting quiz for {}..."
                            .format(message.author))
            await chnl.send("You have {} seconds each to answer {} question(s)!"
                            .format(timeout, question_count))

            # Iterate through all of the questions
            for i in range(1, question_count + 1):

                # Initialize the values for one question
                a = random.randint(1, 20)
                b = random.randint(1, 20)
                answer = a + b

                await chnl.send('**{}.** What is {} + {}?'.format(i, a, b))

                def is_correct(m):
                    return m.author == message.author and m.content.isdigit()

                try:
                    guess = await self.wait_for('message',
                                                check=is_correct,
                                                timeout=timeout)
                except asyncio.TimeoutError:
                    await chnl.send('Sorry, you took too long it was {}.'
                                    .format(answer))
                    continue

                if int(guess.content) == answer:
                    await chnl.send('🎉You are right🎉!')
                    score += 1

                else:
                    await chnl.send('Oops. The answer is {}.'
                                    .format(answer))

            await chnl.send("Your score was **{}**/**{}**, {}!"
                            .format(score, question_count,
                                    message.author))

            # Send a message for perfect scores
            if score >= question_count:
                await chnl.send("You answered all questions perfectly! Great job! 😍")

            # Update user's score in scores.csv
            update_score(str(message.author.id), score)

        # COMMAND: Check score
        if args[0] == 'm.score':
            user_id = str(message.author.id)

            # Add the user if not in database yet
            add_user(user_id)

            with open('scores.csv', mode='r') as csv_file:
                csv_reader = csv.reader(csv_file)

                for row in csv_reader:
                    if row[0] == user_id:
                        await chnl.send("<@{}>'s score is {}."
                                        .format(row[0], row[1]))
                        break


client = MathQuiz()

client.run(TOKEN)
