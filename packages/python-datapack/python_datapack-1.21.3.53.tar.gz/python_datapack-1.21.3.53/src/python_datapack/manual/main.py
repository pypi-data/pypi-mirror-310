
# Imports
from ..utils.io import *
from ..utils.print import *
from .utils import *
from .shared_import import *
from .book_optimizer import *
from ..constants import *
from ..resource_pack.item_models import handle_item		# Handle new items models (used for the manual and the heavy workbench)

# Utility functions
def deepcopy(x: list|dict) -> list|dict:
	return json.loads(json.dumps(x))

def main(config: dict):
	# Copy everything in the manual assets folder to the templates folder
	os.makedirs(TEMPLATES_PATH, exist_ok = True)
	shutil.copytree(MANUAL_ASSETS_PATH + "assets", TEMPLATES_PATH, dirs_exist_ok = True)

	# Copy the manual_overrides folder to the templates folder
	if config.get("manual_overrides") and os.path.exists(config["manual_overrides"]):
		shutil.copytree(config["manual_overrides"], TEMPLATES_PATH, dirs_exist_ok = True)

	# Launch the routine
	try:
		routine(config)

	# Remove the temporary templates folder
	finally:
		shutil.rmtree(TEMPLATES_PATH, ignore_errors = True)

def routine(config: dict):
	database: dict[str, dict] = config["database"]
	namespace: str = config["namespace"]

	# If smithed crafter is used, add it to the manual (last page that we will move to the second page)
	if OFFICIAL_LIBS["smithed.crafter"]["is_used"]:
		super_copy(f"{TEMPLATES_PATH}/heavy_workbench.png", f"{config['build_resource_pack']}/assets/{namespace}/textures/item/heavy_workbench.png")
		database["heavy_workbench"] = {
			"id": CUSTOM_BLOCK_VANILLA,
			"item_name": "'Heavy Workbench'",
			"category": HEAVY_WORKBENCH_CATEGORY,
			OVERRIDE_MODEL: {
				"parent":"minecraft:block/cube",
				"texture_size":[64,32],
				"textures":{"0":f"{namespace}:item/heavy_workbench"},
				"elements":[{"from":[0,0,0],"to":[16,16,16],"faces":{"north":{"uv":[4,8,8,16],"texture":"#0"},"east":{"uv":[0,8,4,16],"texture":"#0"},"south":{"uv":[12,8,16,16],"texture":"#0"},"west":{"uv":[8,8,12,16],"texture":"#0"},"up":{"uv":[4,0,8,8],"texture":"#0"},"down":{"uv":[8,0,12,8],"texture":"#0"}}}],
				"display":{"thirdperson_righthand":{"rotation":[75,45,0],"translation":[0,2.5,0],"scale":[0.375,0.375,0.375]},"thirdperson_lefthand":{"rotation":[75,45,0],"translation":[0,2.5,0],"scale":[0.375,0.375,0.375]},"firstperson_righthand":{"rotation":[0,45,0],"scale":[0.4,0.4,0.4]},"firstperson_lefthand":{"rotation":[0,225,0],"scale":[0.4,0.4,0.4]},"ground":{"translation":[0,3,0],"scale":[0.25,0.25,0.25]},"gui":{"rotation":[30,225,0],"scale":[0.625,0.625,0.625]},"head":{"translation":[0,-30.43,0],"scale":[1.601,1.601,1.601]},"fixed":{"scale":[0.5,0.5,0.5]}}
			},
			RESULT_OF_CRAFTING: [
				{"type":"crafting_shaped","shape":["###","#C#","SSS"],"ingredients":{"#":ingr_repr("minecraft:oak_log"),"C":ingr_repr("minecraft:crafting_table"),"S":ingr_repr("minecraft:smooth_stone")}}
			]
		}
		handle_item(config, "heavy_workbench", database["heavy_workbench"], set(), ignore_textures = True)
		write_all_files(contains="item/heavy_workbench")

	# Prework
	os.makedirs(f"{config['manual_path']}/font/page", exist_ok=True)
	os.makedirs(f"{config['manual_path']}/font/wiki_icons", exist_ok = True)
	os.makedirs(f"{config['manual_path']}/font/high_res", exist_ok = True)
	generate_all_iso_renders(config)

	# Constants
	FONT = namespace + ':' + FONT_FILE
	MAX_ITEMS_PER_PAGE = config['max_items_per_row'] * config['max_rows_per_page'] # (for showing up all items in the categories pages)

	# Calculate left padding for categories pages depending on config['max_items_per_row']: higher the value, lower the padding
	LEFT_PADDING = 6 - config['max_items_per_row']

	# Copy assets in the resource pack
	if not config['debug_mode']:
		super_copy(f"{TEMPLATES_PATH}/none_release.png", f"{config['build_resource_pack']}/assets/{namespace}/textures/font/none.png")
		super_copy(f"{TEMPLATES_PATH}/invisible_item_release.png", f"{config['build_resource_pack']}/assets/{namespace}/textures/font/invisible_item.png")
	else:
		super_copy(f"{TEMPLATES_PATH}/none.png", f"{config['build_resource_pack']}/assets/{namespace}/textures/font/none.png")
		super_copy(f"{TEMPLATES_PATH}/invisible_item.png", f"{config['build_resource_pack']}/assets/{namespace}/textures/font/invisible_item.png")
	super_copy(f"{TEMPLATES_PATH}/wiki_information.png", f"{config['build_resource_pack']}/assets/{namespace}/textures/font/wiki_information.png")
	super_copy(f"{TEMPLATES_PATH}/wiki_result_of_craft.png", f"{config['build_resource_pack']}/assets/{namespace}/textures/font/wiki_result_of_craft.png")
	super_copy(f"{TEMPLATES_PATH}/wiki_ingredient_of_craft.png", f"{config['build_resource_pack']}/assets/{namespace}/textures/font/wiki_ingredient_of_craft.png")
	if config['manual_high_resolution']:
		super_copy(f"{TEMPLATES_PATH}/furnace.png", f"{config['build_resource_pack']}/assets/{namespace}/textures/font/furnace.png")
		super_copy(f"{TEMPLATES_PATH}/shaped_2x2.png", f"{config['build_resource_pack']}/assets/{namespace}/textures/font/shaped_2x2.png")
		super_copy(f"{TEMPLATES_PATH}/shaped_3x3.png", f"{config['build_resource_pack']}/assets/{namespace}/textures/font/shaped_3x3.png")

	# If the manual cache is enabled and we have a cache file, load it
	if config['cache_manual_pages'] and os.path.exists(config['manual_debug']) and os.path.exists(f"{config['manual_path']}/font/manual.json"):
		with super_open(config['manual_debug'], "r") as f:
			book_content = json.load(f)

	# Else, generate all
	else:

		# Generate categories list
		categories: dict[str, list] = {}
		for item, data in database.items():

			if CATEGORY not in data:
				warning(f"Item '{item}' has no category key. Skipping.")
				continue

			category = data[CATEGORY]
			if category not in categories:
				categories[category] = []
			categories[category].append(item)

		# Error message if there is too many categories
		if len(categories) > MAX_ITEMS_PER_PAGE:
			error(f"Too many categories ({len(categories)}). Maximum is {MAX_ITEMS_PER_PAGE}. Please reduce the number of item categories.")

		# Debug categories and sizes
		s = ""
		for category, items in categories.items():
			if category == HEAVY_WORKBENCH_CATEGORY:
				continue
			s += f"\n- {category}: {len(items)} items"
			if len(items) > MAX_ITEMS_PER_PAGE:
				s += f" (splitted into {len(items) // MAX_ITEMS_PER_PAGE + 1} pages)"
		nb_categories: int = len(categories) - (1 if HEAVY_WORKBENCH_CATEGORY in categories else 0)
		debug(f"Found {nb_categories} categories:{s}")

		# Split up categories into pages
		categories_pages = {}
		for category, items in categories.items():
			if category != HEAVY_WORKBENCH_CATEGORY:
				i = 0
				while i < len(items):
					page_name = category.title()
					if len(items) > MAX_ITEMS_PER_PAGE:
						number = i // MAX_ITEMS_PER_PAGE + 1
						page_name += f" #{number}"
					new_items = items[i:i + MAX_ITEMS_PER_PAGE]
					categories_pages[page_name] = new_items
					i += MAX_ITEMS_PER_PAGE

		## Prepare pages (append categories first, then items depending on categories order)
		i = 2 # Skip first two pages (introduction + categories)
		
		# Append categories
		for page_name, items in categories_pages.items():
			i += 1
			manual_pages.append({"number": i, "name": page_name, "raw_data": items, "type": CATEGORY})
		
		# Append items (sorted by category)
		items_with_category = [(item, data) for item, data in database.items() if CATEGORY in data]
		category_list = list(categories.keys())
		sorted_database_on_category = sorted(items_with_category, key = lambda x: category_list.index(x[1][CATEGORY]))
		for item, data in sorted_database_on_category:
			i += 1
			manual_pages.append({"number": i, "name": item, "raw_data": data, "type": "item"})

		# Encode pages
		book_content = []
		os.makedirs(f"{config['manual_path']}/font/category", exist_ok=True)
		simple_case = load_simple_case_no_border(config['manual_high_resolution'])	# Load the simple case image for later use in categories pages
		for page in manual_pages:
			content = []
			number = page["number"]
			raw_data: dict = page["raw_data"]
			page_font = ""
			if not config['manual_high_resolution']:
				page_font = get_page_font(number)
			name = str(page["name"])
			titled = name.replace("_", " ").title() + "\n"

			# Encode categories {'number': 2, 'name': 'Material #1', 'raw_data': ['adamantium_block', 'adamantium_fragment', ...]}
			if page["type"] == CATEGORY:
				file_name = name.replace(" ", "_").replace("#", "").lower()
				page_font = get_page_font(number)
				font_providers.append({"type":"bitmap","file":f"{namespace}:font/category/{file_name}.png", "ascent": 0, "height": 130, "chars": [page_font]})
				content.append({"text": "", "font": FONT, "color": "white"})	# Make default font for every next component
				content.append({"text": "➤ ", "font": "minecraft:default", "color": "black"})
				content.append({"text": titled, "font": "minecraft:default", "color": "black", "underlined": True})
				content.append(SMALL_NONE_FONT * LEFT_PADDING + page_font + "\n")

				# Prepare image and line list
				page_image = Image.new("RGBA", (256, 256), (0, 0, 0, 0))
				x, y = 2, 2	# Prevision for global border and implicit border
				line = []

				# For each item in the category, get its page number and texture, then add it to the image
				for item in raw_data:

					# Get item texture
					texture_path = f"{config['manual_path']}/items/{namespace}/{item}.png"
					if os.path.exists(texture_path):
						item_image = Image.open(texture_path)
					else:
						warning(f"Missing texture at '{texture_path}', using empty texture")
						item_image = Image.new("RGBA", (1, 1), (0, 0, 0, 0))
					if not config['manual_high_resolution']:
						resized = careful_resize(item_image, 32)
					else:
						resized = Image.new("RGBA", (1, 1), (0, 0, 0, 0))	# Empty texture to use for category page
						high_res_font = generate_high_res_font(config, item, item_image)

					# Paste the simple case and the item_image
					page_image.paste(simple_case, (x, y))
					mask = resized.convert("RGBA").split()[3]
					page_image.paste(resized, (x + 2, y + 2), mask)
					x += simple_case.size[0]

					# Add the clickEvent part to the line and add the 2 times the line if enough items
					component = get_item_component(config, item, ["custom_model_data", "item_name", "custom_name"])
					component["text"] = MEDIUM_NONE_FONT if not config['manual_high_resolution'] else high_res_font
					line.append(component)
					if len(line) == config['max_items_per_row']:
						line.insert(0, SMALL_NONE_FONT * LEFT_PADDING)
						content += deepcopy(line)
						for i in range(1, len(line)):
							line[-i]["text"] = MEDIUM_NONE_FONT
						content += ["\n"] + line + ["\n"]
						line = []
						x = 2
						y += simple_case.size[1]
				
				# If remaining items in the line, add them
				if len(line) > 0:
					line.insert(0, SMALL_NONE_FONT * LEFT_PADDING)
					content += deepcopy(line)
					for i in range(1, len(line)):
						line[-i]["text"] = MEDIUM_NONE_FONT
					content += ["\n"] + line + ["\n"]
				
				# Add the 2 pixels border
				is_rectangle_shape = len(raw_data) % config['max_items_per_row'] == 0
				page_image = add_border(page_image, BORDER_COLOR, BORDER_SIZE, is_rectangle_shape)
				
				# Save the image
				page_image.save(f"{config['manual_path']}/font/category/{file_name}.png")

			# Encode items
			else:
				# Get all crafts
				crafts: list[dict] = list(raw_data.get(RESULT_OF_CRAFTING,[]))
				crafts += list(raw_data.get(USED_FOR_CRAFTING,[]))
				crafts += generate_otherside_crafts(config, name)
				crafts = [craft for craft in crafts if craft["type"] not in ["blasting", "smoking", "campfire_cooking"]]	# Remove smelting dupes
				crafts = remove_unknown_crafts(crafts)
				crafts = unique_crafts(crafts)

				# If there are crafts, generate the content for the first craft
				if crafts:
					first_craft = crafts[0]
					l = generate_craft_content(config, first_craft, name, page_font)
					if l:
						content += l
				
				# Else, generate the content for the single item in a big box
				else:
					if not page_font:
						page_font = get_page_font(number)
					generate_page_font(config, name, page_font, craft = None)
					component = get_item_component(config, name)
					component["text"] = NONE_FONT
					component["text"] *= 2
					content.append({"text": "", "font": FONT, "color": "white"})	# Make default font for every next component
					content.append({"text": titled, "font": "minecraft:default", "color": "black", "underlined": True})
					content.append(MEDIUM_NONE_FONT * 2 + page_font + "\n")
					for _ in range(4):
						content.append(MEDIUM_NONE_FONT * 2)
						content.append(component)
						content.append("\n")

				## Add wiki information if any
				wiki_buttons = []
				if name == "heavy_workbench":
					content.append([
						{"text":"\nEvery recipe that uses custom items ", "font":"minecraft:default","color":"black"},
						{"text":"must","color":"red","underlined":True},
						{"text":" be crafted using the Heavy Workbench."}
					])
				else:
					if raw_data.get(WIKI_COMPONENT):
						wiki_buttons.append({"text": WIKI_INFO_FONT + VERY_SMALL_NONE_FONT * 2, "hoverEvent": {"action": "show_text", "contents": raw_data[WIKI_COMPONENT]}})
					
					# For each craft (except smelting dupes),
					for i, craft in enumerate(crafts):
						if craft["type"] == "crafting_shapeless":
							craft = convert_shapeless_to_shaped(craft)

						# Get breaklines
						breaklines = 3
						if "shape" in craft:
							breaklines = max(2, max(len(craft["shape"]), len(craft["shape"][0])))

						if not config['manual_high_resolution']:
							craft_font = get_next_font()	# Unique used font for the craft
							generate_page_font(config, name, craft_font, craft, output_name = f"{name}_{i+1}")
							hover_text = [""]
							hover_text.append({"text": craft_font + "\n\n" * breaklines, "font": FONT, "color": "white"})
						else:
							l = generate_craft_content(config, craft, name, "")
							l = [l[0]] + l[2:]	# Remove craft title
							remove_events(l)
							for k, v in HOVER_EQUIVALENTS.items():
								l[1] = l[1].replace(k, v)
							hover_text = ["", l]

						# Append ingredients
						if craft.get("ingredient"):
							id = ingr_to_id(craft["ingredient"], False).replace("_", " ").title()
							hover_text.append({"text": f"\n- x1 ", "color": "gray"})
							hover_text.append({"text": id, "color": "gray"})
						elif craft.get("ingredients"):

							# If it's a shaped crafting
							if isinstance(craft["ingredients"], dict):
								for k, v in craft["ingredients"].items():
									id = ingr_to_id(v, False).replace("_", " ").title()
									count = sum([line.count(k) for line in craft["shape"]])
									hover_text.append({"text": f"\n- x{count} ", "color": "gray"})
									hover_text.append({"text": id, "color": "gray"})
							
							# If it's shapeless
							elif isinstance(craft["ingredients"], list):
								ids = {}	# {id: count}
								for ingr in craft["ingredients"]:
									id = ingr_to_id(ingr, False).replace("_", " ").title()
									if id not in ids:
										ids[id] = 0
									ids[id] += 1
								for id, count in ids.items():
									hover_text.append({"text": f"\n- x{count} ", "color": "gray"})
									hover_text.append({"text": id, "color": "gray"})

						# Add the craft to the content
						result_or_ingredient = WIKI_RESULT_OF_CRAFT_FONT if "result" not in craft else generate_wiki_font_for_ingr(config, name, craft)
						wiki_buttons.append({"text": result_or_ingredient + VERY_SMALL_NONE_FONT * 2, "hoverEvent": {"action": "show_text", "contents": hover_text}})

						# If there is a result to the craft, try to add the clickEvent that change to that page
						if "result" in craft:
							result_item = ingr_to_id(craft["result"], False)
							if result_item in database:
								wiki_buttons[-1]["clickEvent"] = {"action": "change_page", "value": str(get_page_number(result_item))}
				
				# Add wiki buttons 5 by 5
				if wiki_buttons:

					# Add a breakline only if there aren't too many breaklines already
					content.append("\n")

					last_i = 0
					for i, button in enumerate(wiki_buttons):
						last_i = i
						# Duplicate line and add breakline
						if i % 5 == 0 and i != 0:
							# Remove VERY_SMALL_NONE_FONT from last button to prevent automatic break line
							content[-1]["text"] = content[-1]["text"].replace(VERY_SMALL_NONE_FONT, "")

							# Re-add last 5 buttons (for good hoverEvent) but we replace the wiki font by the small font
							content += ["\n"] + [x.copy() for x in content[-5:]]
							for j in range(5):
								content[-5 + j]["text"] = WIKI_NONE_FONT + VERY_SMALL_NONE_FONT * (2 if j != 4 else 0)
							content.append("\n")
						content.append(button)
					
					# Duplicate the last line if not done yet
					if last_i % 5 != 0 or last_i == 0:
						last_i = last_i % 5 + 1

						# Remove VERY_SMALL_NONE_FONT from last button to prevent automatic break line
						content[-1]["text"] = content[-1]["text"].replace(VERY_SMALL_NONE_FONT, "")

						content += ["\n"] + [x.copy() for x in content[-last_i:]]
						for j in range(last_i):
							content[-last_i + j]["text"] = WIKI_NONE_FONT + VERY_SMALL_NONE_FONT * (2 if j != 4 else 0)

			# Add page to the book
			book_content.append(content)

		## Add categories page
		content = []
		file_name = "categories_page"
		page_font = get_page_font(1)
		font_providers.append({"type":"bitmap","file":f"{namespace}:font/category/{file_name}.png", "ascent": 0, "height": 130, "chars": [page_font]})
		content.append({"text": "", "font": FONT, "color": "white"})	# Make default font for every next component
		content.append({"text": "➤ ", "font": "minecraft:default", "color": "black"})
		content.append({"text": "Category browser\n", "font": "minecraft:default", "color": "black", "underlined": True})
		content.append(SMALL_NONE_FONT * LEFT_PADDING + page_font + "\n")

		# Prepare image and line list
		page_image = Image.new("RGBA", (256, 256), (0, 0, 0, 0))
		x, y = 2, 2	# Prevision for global border and implicit border
		line = []

		# For each item in the category, get its page number and texture, then add it to the image
		for page in manual_pages:
			if page["type"] == CATEGORY:
				item = page["raw_data"][0]

				# Get item texture TODO
				texture_path = f"{config['manual_path']}/items/{namespace}/{item}.png"
				if os.path.exists(texture_path):
					item_image = Image.open(texture_path)
				else:
					warning(f"Missing texture at '{texture_path}', using empty texture")
					item_image = Image.new("RGBA", (1, 1), (0, 0, 0, 0))
				if not config['manual_high_resolution']:
					resized = careful_resize(item_image, 32)
				else:
					resized = Image.new("RGBA", (1, 1), (0, 0, 0, 0))	# Empty texture to use for category page
					high_res_font = generate_high_res_font(config, item, item_image)

				# Paste the simple case and the item_image
				page_image.paste(simple_case, (x, y))
				mask = resized.convert("RGBA").split()[3]
				page_image.paste(resized, (x + 2, y + 2), mask)
				x += simple_case.size[0]

				# Add the clickEvent part to the line and add the 2 times the line if enough items
				component = get_item_component(config, item, ["custom_model_data"])
				component["hoverEvent"]["contents"]["components"]["item_name"] = str({"text": page["name"], "color": "white"})
				component["clickEvent"]["value"] = str(page["number"])
				if not config['manual_high_resolution']:
					component["text"] = MEDIUM_NONE_FONT
				else:
					component["text"] = high_res_font
				line.append(component)
				if len(line) == config['max_items_per_row']:
					line.insert(0, SMALL_NONE_FONT * LEFT_PADDING)
					content += deepcopy(line) + ["\n"]
					for i in range(1, len(line)):
						line[-i]["text"] = MEDIUM_NONE_FONT
					content += line + ["\n"]
					line = []
					x = 2
					y += simple_case.size[1]
		
		# If remaining items in the line, add them
		if len(line) > 0:
			line.insert(0, SMALL_NONE_FONT * LEFT_PADDING)
			content += deepcopy(line) + ["\n"]
			for i in range(1, len(line)):
				line[-i]["text"] = MEDIUM_NONE_FONT
			content += line + ["\n"]
		
		# Add the 2 pixels border
		is_rectangle_shape = len(categories_pages) % config['max_items_per_row'] == 0
		page_image = add_border(page_image, BORDER_COLOR, BORDER_SIZE, is_rectangle_shape)
		
		# Save the image and add the page to the book
		page_image.save(f"{config['manual_path']}/font/category/{file_name}.png")
		book_content.insert(0, content)


		## Append introduction page
		content = [""]
		page_font = get_page_font(0)
		font_providers.append({"type":"bitmap","file":f"{namespace}:font/page/_logo.png", "ascent": 0, "height": 40, "chars": [page_font]})
		content.append({"text": config['manual_name'] + "\n", "underlined": True})
		content.append({"text": MEDIUM_NONE_FONT * 2 + page_font, "font": FONT, "color": "white"})
		
		# Create the image and load Minecraft font
		icon_path = f"{config['assets_folder']}/original_icon.png"
		if not os.path.exists(icon_path):
			error(f"Missing icon path at '{icon_path}' (needed for the manual)")
		logo = Image.open(icon_path)
		logo = careful_resize(logo, 256)

		# Write the introduction text
		content.append("\n" * 6)
		content.append(config['manual_first_page_text'])

		# Save image and insert in the manual pages
		logo.save(f"{config['manual_path']}/font/page/_logo.png")
		book_content.insert(0, content)

		## Optimize the book size
		book_content_deepcopy = json.loads(json.dumps(book_content))	# Deepcopy to avoid sharing same components (such as clickEvent)
		book_content = optimize_book(book_content_deepcopy)

		## Insert at 2nd page the heavy workbench
		if "heavy_workbench" in database:
			heavy_workbench_page = book_content.pop(-1)
			book_content.insert(1, heavy_workbench_page)

			# Increase every change_page click event by 1
			for page in book_content:
				for component in page:
					if isinstance(component, dict) and "clickEvent" in component and component["clickEvent"].get("action") == "change_page":
						current_value: int = int(component["clickEvent"]["value"])
						component["clickEvent"]["value"] = str(current_value + 1)

		# Add fonts
		font_providers.append({"type":"bitmap","file":f"{namespace}:font/none.png", "ascent": 8, "height": 20, "chars": [NONE_FONT]})
		font_providers.append({"type":"bitmap","file":f"{namespace}:font/none.png", "ascent": 8, "height": 18, "chars": [MEDIUM_NONE_FONT]})
		font_providers.append({"type":"bitmap","file":f"{namespace}:font/none.png", "ascent": 7, "height": 7, "chars": [SMALL_NONE_FONT]})
		font_providers.append({"type":"bitmap","file":f"{namespace}:font/none.png", "ascent": 0, "height": 2, "chars": [VERY_SMALL_NONE_FONT]})
		font_providers.append({"type":"bitmap","file":f"{namespace}:font/none.png", "ascent": 0, "height": 1, "chars": [MICRO_NONE_FONT]})
		font_providers.append({"type":"bitmap","file":f"{namespace}:font/none.png", "ascent": 7, "height": 16, "chars": [WIKI_NONE_FONT]})
		font_providers.append({"type":"bitmap","file":f"{namespace}:font/invisible_item.png", "ascent": 7, "height": 16, "chars": [INVISIBLE_ITEM_FONT]})
		font_providers.append({"type":"bitmap","file":f"{namespace}:font/wiki_information.png", "ascent": 8, "height": 16, "chars": [WIKI_INFO_FONT]})
		font_providers.append({"type":"bitmap","file":f"{namespace}:font/wiki_result_of_craft.png", "ascent": 8, "height": 16, "chars": [WIKI_RESULT_OF_CRAFT_FONT]})
		font_providers.append({"type":"bitmap","file":f"{namespace}:font/wiki_ingredient_of_craft.png", "ascent": 8, "height": 16, "chars": [WIKI_INGR_OF_CRAFT_FONT]})
		if config['manual_high_resolution']:
			font_providers.append({"type":"bitmap","file":f"{namespace}:font/shaped_3x3.png", "ascent": 1, "height": 58, "chars": [SHAPED_3X3_FONT]})
			font_providers.append({"type":"bitmap","file":f"{namespace}:font/shaped_2x2.png", "ascent": 1, "height": 58, "chars": [SHAPED_2X2_FONT]})
			font_providers.append({"type":"bitmap","file":f"{namespace}:font/furnace.png", "ascent": 1, "height": 58, "chars": [FURNACE_FONT]})
			font_providers.append({"type":"bitmap","file":f"{namespace}:font/shaped_3x3.png", "ascent": -4, "height": 58, "chars": [HOVER_SHAPED_3X3_FONT]})
			font_providers.append({"type":"bitmap","file":f"{namespace}:font/shaped_2x2.png", "ascent": -2, "height": 58, "chars": [HOVER_SHAPED_2X2_FONT]})
			font_providers.append({"type":"bitmap","file":f"{namespace}:font/furnace.png", "ascent": -3, "height": 58, "chars": [HOVER_FURNACE_FONT]})
		fonts = {"providers": font_providers}
		with super_open(f"{config['manual_path']}/font/manual.json", "w") as f:
			f.write(super_json_dump(fonts).replace("\\\\", "\\"))
				
		# Debug book_content
		with super_open(config['manual_debug'], "w") as f:
			f.write(super_json_dump(book_content))
			debug(f"Debug book_content at '{config['manual_debug']}'")


	# Copy the font provider and the generated textures to the resource pack
	super_copy(f"{config['manual_path']}/font/manual.json", f"{config['build_resource_pack']}/assets/{namespace}/font/manual.json")
	super_copy(f"{config['manual_path']}/font/category/", f"{config['build_resource_pack']}/assets/{namespace}/textures/font/category/")
	super_copy(f"{config['manual_path']}/font/page/", f"{config['build_resource_pack']}/assets/{namespace}/textures/font/page/")
	super_copy(f"{config['manual_path']}/font/wiki_icons/", f"{config['build_resource_pack']}/assets/{namespace}/textures/font/wiki_icons/")
	if config['manual_high_resolution']:
		super_copy(f"{config['manual_path']}/font/high_res/", f"{config['build_resource_pack']}/assets/{namespace}/textures/font/high_res/")

	# Verify font providers and textures
	for fp in font_providers:
		if "file" in fp:
			path: str = fp["file"]
			path = path.replace(namespace + ':', f"{config['build_resource_pack']}/assets/{namespace}/textures/")
			if not os.path.exists(path):
				error(f"Missing font provider at '{path}' for {fp})")
			if len(fp["chars"]) < 1 or (len(fp["chars"]) == 1 and not fp["chars"][0]):
				error(f"Font provider '{path}' has no chars")

	# Finally, prepend the manual to the database
	manual_already_exists: bool = "manual" in database
	manual_database = {
		"manual": {
			"id": "minecraft:written_book",
			"written_book_content": {
				"title": config.get("manual_name", "Manual"),
				"author": config['author'],
				"pages": [str(i).replace("\\\\", "\\") for i in book_content],
			},
			"lore": [json.dumps(config['source_lore']).replace('"', "'")],
			"item_model": f"{namespace}:manual",
			"enchantment_glint_override": False,
			"max_stack_size": 1
		}
	}
	if not database.get("manual"):
		database["manual"] = manual_database["manual"]
	database["manual"].update(manual_database["manual"])

	# Add the model to the resource pack if it doesn't already exist
	if not manual_already_exists:
		handle_item(config, "manual", database["manual"])

	# Remove the heavy workbench from the database
	if OFFICIAL_LIBS["smithed.crafter"]["is_used"]:
		del database["heavy_workbench"]
		delete_file(f"{config['build_resource_pack']}/assets/{namespace}/textures/item/heavy_workbench.png")
		delete_file(f"{config['build_resource_pack']}/assets/{namespace}/models/item/heavy_workbench.json")

	info(f"Added manual to the database")

