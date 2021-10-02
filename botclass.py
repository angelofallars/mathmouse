import discord
import random
import asyncio
import csv
import csv_funcs
import embeds as emb
import os
from quiz import Question
from quiz import Quiz


class QuizBot(discord.Client):
    async def on_ready(self):
        print('Logged in as')
        print(self.user.name)
        print(self.user.id)
        print('------')

        # Create a scores.csv if it doesn't exist
        if not os.path.isfile('scores.csv'):
            file = open('scores.csv', 'w')
            file.close()

    async def on_message(self, message):
        # Don't make the bot reply to itself
        if message.author.id == self.user.id:
            return

        print('Message from {0.author} {0.author.id}: {0.content}'
              .format(message))

        # Split the message into a list of args like a command line arg
        args = message.content.split()
        chnl = message.channel

        # COMMAND: Start quiz
        if args[0] == 'm.quiz':

            # Check quiz type
            if len(args) >= 2:
                if args[1] == 'addition':
                    quiz_type = 'addition'
                elif args[1] == 'subtraction':
                    quiz_type = 'subtraction'
                elif args[1] == 'multiplication':
                    quiz_type = 'multiplication'
                elif args[1] == 'division':
                    quiz_type = 'division'
                else:
                    return
            else:
                return

            timeout = 5
            question_count = 5
            score = 0

            # Send the pre-quiz messages for the user
            await chnl.send("Starting quiz for {}..."
                            .format(message.author))
            await chnl.send("You have {} seconds each to answer {} question(s)!"
                            .format(timeout, question_count))

            # Initialize the quiz and questions variables
            questions = [Question(q_type=quiz_type) for i in range(question_count)]
            quiz = Quiz(questions=questions,
                        name="{} Quiz".format(quiz_type.title()))

            # Iterate through all of the questions
            for i in range(len(quiz.questions)):
                answer = quiz.questions[i].answer

                # Print the question
                title = "question #{}/{}".format(i + 1, len(quiz.questions))
                description = "What is {}?".format(quiz.questions[i].text)
                footer = "{}".format(quiz.name)

                embed = emb.print_embed(title, description, footer)
                await chnl.send(embed=embed)

                def is_correct(m):
                    return m.author == message.author

                # Wait for the answer
                try:
                    guess = await self.wait_for('message',
                                                check=is_correct,
                                                timeout=timeout)
                # Timeout
                except asyncio.TimeoutError:
                    embed = emb.print_embed(title=title,
                                            description='Timeout! The answer is {}.'.format(quiz.questions[i].answer))
                    await chnl.send(embed=embed)
                    continue

                # Correct Answer
                if int(guess.content) == answer:
                    embed = emb.print_embed(title=title,
                                            description='🎉You are right🎉!')
                    await chnl.send(embed=embed)
                    score += 1
                # Wrong Answer
                else:
                    embed = emb.print_embed(title=title,
                                            description='Oops, the answer is {}.'.format(quiz.questions[i].answer))
                    await chnl.send(embed=embed)

            # Send the user's score
            await chnl.send("Your score was **{}**/**{}**, {}!"
                            .format(score, question_count,
                                    message.author))

            # Send a message for perfect scores
            if score >= question_count:
                await chnl.send("You answered all questions perfectly! Great job! 😍")

            # Send a message for zero scores
            if score == 0:
                await chnl.send("Better luck next time!")

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
