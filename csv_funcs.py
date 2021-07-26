import csv


def save_file(rows):
    '''Save changes to the csv file using the input rows
    '''
    with open('scores.csv', mode='w', newline='') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerows(rows)


def add_user(user_id, score=0):
    '''Check if user is in the scores.csv file.
    Return True if user in database.
    Return False and add user to database if not existing already.

    user_id - The Discord user's ID
    score - The score to initialize the user with
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
        save_file(rows)


def update_score(user_id, n=0):
    '''Update user's score by 'n' amount in scores.csv

    user_id - The Discord user's ID
    n - The amount by which to change their score
    '''

    # Add the user if not in database yet
    add_user(user_id, n)

    with open('scores.csv', mode='r') as csv_file:
        reader = csv.reader(csv_file)
        rows = list(reader)

        # Find the user's id
        for row in rows:
            if row[0] == user_id:
                # Update the user's score
                row[1] = int(row[1]) + n
                break

    # Commit changes to csv file
    save_file(rows)
