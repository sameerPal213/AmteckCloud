from django.core.management.base import BaseCommand
import json

class Command(BaseCommand):
	help = "update project with old information"

	def handle(self, *args, **kwargs):
		with open('full_project_data.json') as file1:
			first_list = json.load(file1)

		with open('project_data.json') as file2:
			second_list = json.load(file2)

		# Convert the first list into a dictionary for quick lookup by `pij_num`
		first_list_dict = {item["fields"]["pij_num"]: item for item in first_list}

		# List to hold items from the second list that are not found in the first list
		not_found_items = []

		# Iterate over items in the second list
		for second_item in second_list:
			# Extract proj_num from the second item
			proj_num = second_item["pk"]
			
			# Check if proj_num exists in the first list dictionary
			if proj_num in first_list_dict:
				# If found, update the boxID of the corresponding item in the first list
				matching_item = first_list_dict[proj_num]
				matching_item["fields"]["boxID"] = second_item["fields"]["boxID"]
				print(f"Updated boxID for proj_num={proj_num}")
			else:
				# If not found, add the item to the not_found_items list
				not_found_items.append(second_item)

		# Save the updated first list back to a file
		with open('updated_first_list.json', 'w') as file_out:
			json.dump(first_list, file_out, indent=4)

		# Save the list of items not found to a separate file
		with open('not_found_items.json', 'w') as not_found_file:
			json.dump(not_found_items, not_found_file, indent=4)

		# Optionally, print out the items not found
		if not_found_items:
			print("Items in second list not found in the first list:")
			for item in not_found_items:
				print(item)
