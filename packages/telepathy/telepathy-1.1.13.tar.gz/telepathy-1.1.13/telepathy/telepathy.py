#!/usr/bin/python3

"""Telepathy cli interface:
    A toolkit for investigating Telegram.
"""

from telethon.tl.functions.messages import GetDialogsRequest
from telethon.errors import SessionPasswordNeededError, ChannelPrivateError
from telethon.tl.types import InputPeerEmpty, PeerUser, PeerChat, PeerChannel
from datetime import date, datetime, timedelta
from telethon.utils import get_display_name
from telethon.sync import TelegramClient
from telethon import TelegramClient, functions, types, utils
import datetime, requests, json, random, glob, csv, os, getpass, click, re
import pandas as pd

__author__ = "Jordan Wildon (@jordanwildon)"
__license__ = "MIT License"
__version__ = "1.1.13"
__maintainer__ = "Jordan Wildon"
__email__ = "j.wildon@pm.me"
__status__ = "Development"

@click.command()
@click.option('--verbose', is_flag=True, help="Prints output to the terminal.")
@click.option('--name', '-n', default=["json"], multiple=True, help='Specifies a chat to investigate.')
@click.option('--archive', '-a', is_flag=True, help='Archives the specified chat.')
@click.option('--media', '-m', is_flag=True, help='Archives media in the specified chat.')
@click.option('--forwards', '-f', is_flag=True, help='Scrapes forwarded messages.')
@click.option('--participants', '-p', is_flag=True, help='Scrapes members from the specified group.')
@click.option('--user', '-u', default='', help='Looks up a specified user ID.')
@click.option('--info', '-i', default='', help='Looks up a specified channel by ID.')
@click.option('--location', '-l', default='', help='Finds users near to specified coordinates.')

def cli(verbose,name,archive,media,forwards,participants,user,info,location):
    """Telepathy is an OSINT toolkit for investigating Telegram chats."""

    telepathy_file = './telepathy_files/'

    try:
        os.makedirs(telepathy_file)
    except FileExistsError:
        pass

    login = telepathy_file + 'login.txt'

    if os.path.isfile(login) == False:
        api_id = input('Please enter your API ID:\n')
        api_hash = input("Please enter your API Hash:\n")
        phone_number = input("Please enter your phone number:\n")

        with open(login, 'w+') as f:
            f.write(api_id + ',' + api_hash + ',' + phone_number )

    else:
        with open(login) as f:
            details = f.read()
            api_id, api_hash, phone_number = details.split(sep=',')

    client = TelegramClient(phone_number, api_id, api_hash)

    name_clean = name
    alphanumeric = ""

    for character in name_clean:
        if character.isalnum():
            alphanumeric += character


    filetime = datetime.datetime.now().strftime("%Y_%m_%d-%H_%M")
    filetime_clean = str(filetime)

    directory = telepathy_file + alphanumeric

    try:
        os.makedirs(directory)
    except FileExistsError:
        pass

    output_print = False
    media_archive = False
    last_date = None

    client.connect()
    if not client.is_user_authorized():
        client.send_code_request(phone_number)
        client.sign_in(phone_number)
        try:
            client.sign_in(code=input('Enter code: '))
        except SessionPasswordNeededError:
            client.sign_in(password=getpass.getpass(prompt='Password: ', stream=None))
        chats = []
        chunk_size = 200
        groups=[]

        result = client(GetDialogsRequest(
                     offset_date=last_date,
                     offset_id=0,
                     offset_peer=InputPeerEmpty(),
                     limit=chunk_size,
                     hash = 0
                 ))
        chats.extend(result.chats)

        for chat in chats:
            groups.append(chat)

    if verbose:
        click.echo('Output will print to the terminal')
        output_print = True

    if media:
        click.echo("Media content will be archived")
        media_archive = True
        media_directory = directory + '/media'
        try:
            os.makedirs(media_directory)
        except FileExistsError:
            pass

    if archive:
        for n in name:
            async def main():
                click.echo('Archiving {0}'.format(n))
                message_list = []
                try:
                    async for message in client.iter_messages(n):
                        if message is not None:
                            try:
                                df = pd.DataFrame(message_list, columns = ['Chat name','message ID','Name','ID','Message text','Timestamp','Reply to','Views','Forward Peer ID','Forwarded From','Post Author','Forward post ID'])

                                file = directory + '/'+ alphanumeric + '_' + filetime_clean +'_archive.csv'

                                with open(file, 'w+') as f:
                                    df.to_csv(f, sep=';')

                                display_name = get_display_name(message.sender)
                                nameID = message.from_id
                                year = str(format(message.date.year, '02d'))
                                month = str(format(message.date.month, '02d'))
                                day = str(format(message.date.day, '02d'))
                                hour = str(format(message.date.hour, '02d'))
                                minute = str(format(message.date.minute, '02d'))
                                reply = message.reply_to_msg_id
                                views = int(message.views)
                                forward_ID = message.fwd_from.from_id
                                forward_name = message.fwd_from.from_name
                                forward_post_ID = int(message.fwd_from.channel_post)
                                post_author = message.fwd_from.post_author

                                date = year + "-" + month + "-" + day
                                time = hour + ":" + minute
                                timestamp = date + ', ' + time

                                if output_print == True:
                                    print(n,':','"' + message.text + '"',timestamp)
                                else:
                                    pass

                                if media_archive == True:
                                    if message.media:
                                        path = await message.download_media(file=media_directory)
                                        if output_print == True:
                                            print('File saved to', path)
                                    else:
                                        pass

                                message_list.append([n,message.id,display_name,nameID,'"' + message.text + '"',timestamp,reply,views,forward_ID,forward_name,post_author,forward_post_ID])

                            except:
                                continue
                        else:
                            message_list.append(['None','None','None','None','None','None','None','None','None','None','None','None','None'])
                            continue

                    jsons = './json_files'
                    try:
                        os.makedirs(jsons)
                    except FileExistsError:
                        pass

                    df.to_json(jsons+'/'+alphanumeric+'_archive.json',orient='split',compression='infer',index='true')

                    print("Scrape completed for",name,", file saved")

                    df = pd.DataFrame(None)

                except Exception as e:
                    print("An exception occurred.", e)

            with client:
                client.loop.run_until_complete(main())

    if forwards:
        f_directory = directory + alphanumeric + '/edgelists/'
        try:
            os.makedirs(f_directory)
        except FileExistsError:
            pass

        file = f_directory + alphanumeric + '_edgelist.csv'
        for n in name:
            async def main():
                click.echo('Listing forwards from {0}'.format(n))
                forwards_list = []
                to_ent = await client.get_entity(n)
                to_title = to_ent.title
                async for message in client.iter_messages(n):
                    if message.forward is not None:
                        try:
                            id = message.forward.original_fwd.from_id
                            if id is not None:
                                ent = await client.get_entity(id)
                                nameID = message.from_id
                                username = ent.username
                                year = format(message.date.year, '02d')
                                month = format(message.date.month, '02d')
                                day = format(message.date.day, '02d')
                                hour = format(message.date.hour, '02d')
                                minute = format(message.date.minute, '02d')

                                date = str(year) + "/" + str(month) + "/" + str(day)
                                time = str(hour) + ":" + str(minute)
                                timestamp = date + ", " + time

                                substring = "PeerUser"
                                if substring in str(id):
                                    user_id = re.sub("[^0-9]", "", str(id))
                                    user_id = await client.get_entity(PeerUser(int(user_id)))
                                    result = 'User named ' + str(user_id.first_name) + ' with ID ' + str(user_id.id)
                                else:
                                    result = ent.title

                                if output_print == True:
                                    print(result,">>>",to_title)
                                else:
                                    pass

                                df = pd.DataFrame(forwards_list, columns = ['To username','To name','From','From ID','From_username','timestamp'])

                                with open(file,'w+') as f:
                                    df.to_csv(f, sep=';')

                                forwards_list.append([n,to_title,result,id,username,timestamp])

                        except Exception as e:
                            if output_print == True:
                                print("An exception occurred with " + str(id) + " " + str(e))
                                #append not founds to a logfile for further investigation

            with client:
                client.loop.run_until_complete(main())

            print('Forwards scraped successfully.')

        next = input('Do you also want to scrape forwards from the discovered channels? (y/n)')
        if next == 'y':
            print('Scraping forwards from channels discovered in', n, '...')
            for n in name:
                async def main():
                    df = pd.read_csv(file, sep=';', keep_default_na=False)
                    df = df.From_username.unique()
                    forwards_list = []
                    net_file = directory + alphanumeric + '_net.csv'
                    for i in df:
                        if i != "":
                            to_ent = await client.get_entity(i)
                            to_title = to_ent.title
                            async for message in client.iter_messages(i):
                                if message.forward is not None:
                                    try:
                                        id = message.forward.original_fwd.from_id
                                        if id is not None:
                                            ent = await client.get_entity(id)
                                            username = ent.username
                                            year = format(message.date.year, '02d')
                                            month = format(message.date.month, '02d')
                                            day = format(message.date.day, '02d')
                                            hour = format(message.date.hour, '02d')
                                            minute = format(message.date.minute, '02d')

                                            date = str(year) + "/" + str(month) + "/" + str(day)
                                            time = str(hour) + ":" + str(minute)
                                            timestamp = date + ", " + time

                                            substring = "PeerUser"
                                            if substring in str(id):
                                                user_id = re.sub("[^0-9]", "", str(id))
                                                user_id = await client.get_entity(PeerUser(int(user_id)))
                                                result = 'User named ' + str(user_id.first_name) + ' with ID ' + str(user_id.id)
                                            else:
                                                result = ent.title

                                            if output_print == True:
                                                print(result,">>>",to_title)
                                            else:
                                                pass

                                            df = pd.DataFrame(forwards_list, columns = ['To username','To name','From','From ID','From_username','timestamp'])

                                            with open(net_file,'w+') as f:
                                                df.to_csv(f)

                                            forwards_list.append([n,to_title,result,id,username,timestamp])
                                    except Exception as e:
                                        if output_print == True:
                                            print("An exception occurred with " + str(id) + " " + str(e))
                                            #append not founds to a logfile for further investigation

                            print("Forward scrape complete for:", i,)

                with client:
                    client.loop.run_until_complete(main())
                print('Forwards scraped successfully.')
            else:
                pass

    if participants:

        p_directory = directory + 'memberlists'
        try:
            os.makedirs(directory)
        except FileExistsError:
            pass

        file_name = p_directory + alphanumeric + "_members.csv"
        for n in name:
            click.echo('Fetching members for {0}'.format(n))
            async def main():
                all_participants = []
                all_participants = await client.get_participants(n)

                with open(file_name,"w",encoding='UTF-8') as f:
                    writer = csv.writer(f,delimiter=",",lineterminator="\n")
                    writer.writerow(['username','full name','user id','group name','group id'])
                    for user in all_participants:
                        if user.username:
                            username= user.username
                        else:
                            username= ""
                        if user.first_name:
                            first_name= user.first_name
                        else:
                            first_name= ""
                        if user.last_name:
                            last_name= user.last_name
                        else:
                            last_name= ""
                        full_name= (first_name + ' ' + last_name).strip()
                        writer.writerow([username,full_name,user.id,name])

                        if output_print == True:
                            print(username,',',full_name,',',user.id,',',n)

                found = len(all_participants)
                print('Members scraped successfully. ' + str(found) + ' users found.')

            with client:
                client.loop.run_until_complete(main())

    if user:
        click.echo(f'Searching for {user}...')
        name = int(user)
        my_user = str(client.get_entity(PeerUser(name)))
        my_user = my_user.replace(",", "\n")
        click.echo(my_user)

    if info:
        click.echo('Looking up {0}...'.format(info))
        async def main():
            try:
                ent = await client.get_entity(int(info))
                username = ent.username
                id = ent.id
                print("https://t.me/" + username + " " + username + " " + str(id))

            except Exception as e:
                substring = "Cannot find any entity"
                if substring in str(e):
                    print("Entity not found for " + info)
                else:
                    print("An exception occurred.", e)
        with client:
            client.loop.run_until_complete(main())

    if location:
        client.connect()
        click.echo('Searching for users near: {0}'.format(location))
        latitude, longitude = location.split(sep=',')

        with client:
            result = client(functions.contacts.GetLocatedRequest(
                geo_point=types.InputGeoPoint(
                    lat=float(latitude),
                    long=float(longitude),
                    accuracy_radius=42
                ),
                self_expires=42
            ))
            output = result.stringify()

            f = open('locations.txt', 'w')
            click.echo(output, file = f)

        l = []
        with open("locations.txt", "r") as searchfile:
          for user in searchfile:
            if "user_id=" in user:
                numeric_filter = filter(str.isdigit, user)
                ids = "".join(numeric_filter)
                l.append(ids)
                f1 = open('ids.txt', 'w')
                click.echo(ids, file = f1)
            if "distance=" in user:
                numeric_filter = filter(str.isdigit, user)
                distance = "".join(numeric_filter)

        for account in l:
            dialogs = client.get_dialogs()
            account = int(account)
            my_user = client.get_entity(PeerUser(account))
            click.echo(my_user.first_name + ' with ID: ' + str(my_user.id) + ' is ' + distance + 'm from the specified coordinates.')
            f = open('userlookup.txt', 'w')
            click.echo(my_user, file = f)

        total = len(l)
        click.echo(total,'users found')

if __name__ == '__main__':
    cli()
