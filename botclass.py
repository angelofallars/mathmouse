import discord
import random
import asyncio
import csv
import csv_funcs


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

        print('Message from {0.author} {0.author.id}: {0.content}'
              .format(message))

        # Split the message into a list of args like a command line arg
        args = message.content.split()
        chnl = message.channel

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

                # Wait for the answer
                try:
                    guess = await self.wait_for('message',
                                                check=is_correct,
                                                timeout=timeout)
                # Timeout
                except asyncio.TimeoutError:
                    await chnl.send('Sorry, you took too long it was {}.'
                                    .format(answer))
                    continue

                # Correct Answer
                if int(guess.content) == answer:
                    await chnl.send('🎉You are right🎉!')
                    score += 1
                # Wrong Answer
                else:
                    await chnl.send('Oops. The answer is {}.'
                                    .format(answer))

            # Send the user's score
            await chnl.send("Your score was **{}**/**{}**, {}!"
                            .format(score, question_count,
                                    message.author))

            # Send a message for perfect scores
            if score >= question_count:
                await chnl.send
                ("You answered all questions perfectly! Great job! 😍")

            # Send a message for perfect scores
            if score == 0:
                await chnl.send
                ("Better luck next time!")

            # Update user's score in scores.csv
            csv_funcs.update_score(str(message.author.id), score)

        # COMMAND: Check score
        if args[0] == 'm.score':
            user_id = str(message.author.id)

            # Add the user if not in database yet
            csv_funcs.add_user(user_id)

            with open('scores.csv', mode='r') as csv_file:
                csv_reader = csv.reader(csv_file)

                for row in csv_reader:
                    if row[0] == user_id:
                        await chnl.send("<@{}>'s score is {}."
                                        .format(row[0], row[1]))
                        break
