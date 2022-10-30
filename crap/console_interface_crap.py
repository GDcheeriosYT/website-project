from crap import match_crap, player_crap
import os
import json
import shutil

async def main_process():
	'''
	manages console interface code
	'''
	while True:
		#ask user what they want to do
		task = input("1.create new match\n2.end match\n3.edit match\n4.test async interface\n5.refresh\n6.exit\n")
		
		#start match
		if task == "1":
			task2 = input("teams or free for all?\nT|F\n")
			
			#FFA
			if task2 == "f" or task2 == "F":
				task3 = input("match name\n")
				
				#match default name
				if task3 == "":
					await match_crap.start_match(False)
					
				#match name
				else:
					await match_crap.start_match(False, match_name=task3)
					
					
			#TEAMS 
			elif task2 == "t" or task2 == "T":
				task3 = input("amount of teams\n")
				
				#team default amount
				if task3 == "":
					task4 = input("match name\n")
					
					#match default name
					if task4 == "":
						await match_crap.start_match(True)
					
					#match name
					else:
						await match_crap.start_match(True, match_name=task3)
				
				#team amount
				else:
					task4 = input("match name\n")
					
					#match default name
					if task4 == "":
						await match_crap.start_match(True, team_amount=int(task3))
						
					#match name
					else:
						await match_crap.start_match(True, team_amount=int(task3), match_name=task4)
						
				
			#TEAMS default
			else:
				task3 = input("amount of teams\n")
				
				#team default amount
				if task3 == "":
					task4 = input("match name\n")
					
					#match default name
					if task4 == "":
						await match_crap.start_match(True)
					
					#match name
					else:
						await match_crap.start_match(True, match_name=task3)
				
				#team amount
				else:
					task4 = input("match name\n")
					
					#match default name
					if task4 == "":
						await match_crap.start_match(True, team_amount=task3)
						
					#match name
					else:
						await match_crap.start_match(True, team_amount=task3, match_name=task4)
			
				
	
		#end match
		elif task == "2":
			i = 0 #counting variable
			player_playcount = []
			player_score = []
			matches = []
			
			#append all matches into matches
			for match in os.listdir("matches/"):
				matches.append(match)
				print(f"{i} {match[:-5]}")
				i += 1
	
			match_end = int(input("\nwhich match will you end?\n")) #pick the match to end
	
			with open(f"matches/{matches[match_end]}") as file: # Open the file in read mode
				ending_match = json.load(file) # Set the variable to the dict version of the json file
			# The file is now closed
	
			with open("player_data.json")as player_data:
				player_data = json.load(player_data)
	
			for user in ending_match["users"]:
								
				player_playcount.append(player_data[user]["user data"]["playcount"])
				player_score.append(player_data[user]["user data"]["score"])
	
			ending_match["final playcount"] = player_playcount
			ending_match["final score"] = player_score
	
			with open(f"matches/{matches[match_end]}", "w") as file: # Open the file in write mode
				json.dump(ending_match, file, indent = 4, sort_keys = False) # Write the variable out to the file, json formatted
			# The file is now closed
			
			try:
				shutil.move(f"matches/{matches[match_end]}", f"match_history/")
			except FileNotFoundError:
				print("\nfile not found...")
	
		elif task == "3":
	
			i = 0
	
			matches = []
	
			for match in os.listdir("matches/"):
				matches.append(match)
				print(f"{i} {match[:-5]}")
				i += 1
	
			match_end = int(input("\nwhich match will you edit?\n"))
	
			print(matches[match_end])
	
			task2 = input("1.add user\n2.remove user\n3.edit match name\n")
			
			if task2 == "1": #add player
	
				with open(f"matches/{matches[match_end]}") as match_edit:
					match_edit = json.load(match_edit)
	
				x = 0
				
				player = player_crap.player_list()
				player_match_info = player_crap.user_data_grabber(player, specific_data=["score", "playcount"])
	
				match_edit["users"].append(player)
				match_edit["initial score"].append(player_match_info[0])
				match_edit["initial playcount"].append(player_match_info[1])
				
				with open(f"matches/{matches[match_end]}", "w") as file:
					json.dump(match_edit, file, indent = 4, sort_keys = False)
	
			elif task2 == "2": #remove player
	
				with open(f"matches/{matches[match_end]}") as match_edit:
					match_edit = json.load(match_edit)
	
				x = 0
	
				for user in match_edit["users"]:
	
					print(f"{x} {player_crap.user_data_grabber(user, specific_data=['name'])[0]} | {user}")
	
					x += 1
				
				task3 = int(input("who to remove?\n"))
	
				match_edit["initial score"].pop(task3)
				match_edit["initial playcount"].pop(task3)
				
				match_edit["users"].pop(task3)
				
				with open(f"matches/{matches[match_end]}", "w") as file:
					json.dump(match_edit, file, indent = 4, sort_keys = False)
	
			elif task2 == "3": #change match name
				
				with open(f"matches/{matches[match_end]}") as match_edit:
					match_edit = json.load(match_edit)
	
				task3 = input("new match name?\n")
	
				match_edit["match name"] = task3
				
	
				with open(f"matches/{matches[match_end]}", "w") as file:
					json.dump(match_edit, file, indent = 4, sort_keys = False)
				
				os.rename(f"matches/{matches[match_end]}", f"matches/{task3}.json")
			
			else:
	
				print("I don't know...")
	
		elif task == "4":
			print("testing")
	
		elif task == "5":
	
			task2 = input("1.refresh all data\n2.refresh certain player data\n3.refresh all users in a match\n")
	
			if task2 == "1":
	
				print("refreshing player data...\n")
				await player_crap.refresh_all_players()
			
			if task2 == "2":
	
				x = 0
	
				player = player_crap.player_list()
	
				await player_crap.player_refresh(player)
			
			if task2 =="3":
				
				i = 0
	
				matches = []
	
				for match in os.listdir("matches/"):
					matches.append(match)
					print(f"{i} {match[:-5]}")
					i += 1
					
				match_refresh = int(input("\nwhich match's users will you refresh?\n"))
				
				with open(f"matches/{matches[match_refresh]}") as match_data:
					match_data = json.load(match_data)
					
				for user in match_data["users"]:
					
					await(player_crap.player_refresh(user))
	
		elif task == "6":
			exit()
		
		else:
			print("I don't know...")