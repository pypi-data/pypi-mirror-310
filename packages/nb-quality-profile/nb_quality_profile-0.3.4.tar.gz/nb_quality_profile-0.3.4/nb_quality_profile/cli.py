import click
from .nb_visualiser import nb_vis_parse_nb, nb_imports_parse_nb, nb_text_parse_nb

from pathlib import Path
import urllib

@click.group()
def cli():
	pass

# In the click path arguments, setting: type=click.Path(exists=True)
# fails if ther is a glob * in the provided path. Ideally, we would
# be able to check for whether any path exists on the supplied path

@cli.command()
@click.argument('path')
@click.option('--out', '-o', default='nb_quality_review.png',  help='Image outfile')
@click.option('--gap', '-g', default=0, type=float, help='Gap')
@click.option('--gapcolor', '-G', default='lightgrey', help='Gap colour')
@click.option('--linewidth', '-l', default=5, type=int, help='Line width')
@click.option('--text-formats/--no-text-formats', default=True, help="Enable/disable Jupytext support.")
@click.option('--path-filter', '-p', default=None,help="Filter phrase for directory path")
def chart(path, out, gap, gapcolor, linewidth, text_formats, path_filter):
	"""Display notebook profile chart from provided file or directory path."""
	click.echo('Using file/directory: {}'.format(path))
	#nb_vis_parse_nb('../Documents/GitHub/tm351-undercertainty/notebooks/tm351/Part 02 Notebooks',
    #        linewidth=10, gap=0, img_file='test-nbvis.png')
	nb_vis_parse_nb(path, img_file=out,  linewidth = linewidth,
					w=20, gap=gap, gap_boost=1, gap_colour=gapcolor,
					text_formats=text_formats, path_filter=path_filter)


@cli.command()
@click.argument('path')
@click.option('--text-formats/--no-text-formats', default=True, help="Enable/disable Jupytext support.")
def imports(path, text_formats):
	"""Display notebook imports from provided file or directory path."""
	click.echo('Using file/directory: {}'.format(path))
	nb_imports_parse_nb(path, text_formats)

@cli.command()
@click.argument('path')
@click.option('--text-formats/--no-text-formats', default=True,
			   help="Enable/disable Jupytext support.")
@click.option('--reading-rate', '-r', default=100, type=int, help='Words per minute.')
@click.option('--rounded-minutes', '-R', is_flag=True, help='Round up to minutes.')
def text_analysis(path, text_formats, reading_rate, rounded_minutes):
	"""Report on text / markdown content."""
	click.echo('Using file/directory: {}'.format(path))
	nb_text_parse_nb(path, text_formats, reading_rate, rounded_minutes)

@cli.command()
@click.argument('path')
@click.option('--grab-images', is_flag=True, help="Grab images.")
@click.option('--report', is_flag=True, help="Save image report.")
def alt_tags(path, grab_images, report):
	"""Check image alt text."""
	from .notebook_profiler import nb_md_links_and_images

	click.echo('\nChecking image alt text for documents in file/directory: {}'.format(path))
	
	retvals = nb_md_links_and_images(path)
	missing_alt_text=[]
	if not retvals:
		click.echo('\nNo images found in any of the notebooks.')
		return
	
	grab_images = grab_images or report

	if grab_images:
		img_path = Path("grab_images")
		img_path.mkdir(parents=True, exist_ok=True)

	biglist = []
	for nb in retvals:
		_missing_alt_text = [(nb["notebook"], i) for i in nb["images"] if not i[1]]
		missing_alt_text.extend(_missing_alt_text)
		if grab_images:
			nb_path = Path(nb["notebook"]).resolve().parent
			for i in nb["images"]:
				src = nb_path / i[0]
				dest = img_path / i[0]
				if i[0].startswith("http"):
					urllib.urlretrieve(i[0], dest)
				else:
					if src.is_file():
						# We could also check it is an image file
						dest.write_bytes(src.read_bytes())

		if report:
			for i in nb["images"]:
				biglist.append([nb["notebook"], i[1], src, dest,
				 f'![{i[1]}]({dest})'])
			report_fn = "nb_images_report.html"

	if report:
		from tabulate import tabulate
		with open(report_fn, 'w') as f:
			f.write(tabulate(biglist,
					headers=["notebook", "path", "src", "dest", "img" ],
					tablefmt='html'))
		click.echo(f"\nReport saved to: {report_fn}")

	if missing_alt_text:
		click.echo('\nMissing alt text:')
		for i in missing_alt_text:
			click.echo(f"- {i[0]}: {i[1]}")
	else:
		click.echo('\nAll images have alt text.')

@cli.command()
@click.argument('path')
@click.option('--all-links', is_flag=True, help="Display all links.")
@click.option('--grab-screenshots', is_flag=True, help="Grab screenshots.")
def link_check(path, all_links, grab_screenshots):
	"""Check links."""
	click.echo('\nChecking links in documents in file/directory: {}'.format(path))

	if all_links:
		click.echo("Displaying reports for all links.\n")
	else:
		click.echo("Only displaying reports for none 200-OK  links. To display reports for all links, use --all-links\n")

	from .notebook_profiler import nb_md_links_and_images

	retvals = nb_md_links_and_images(path)
	# Returns list of (text, href) tuples

	from ouxml_link_checker import link_checker as olc

	reps = {}
	for nb in retvals:
		# Generate report of form: nb, linktext, link, report
		reps[nb["notebook"]] = [(l[0], l[1], olc.link_reporter(l[1])) for l in nb["links"]]

	for nb in reps:
		if all_links:
			click.echo(f"{nb}:")
			links = reps[nb]
			for l in links:
				click.echo(f"- [{l[0]}] {l[1]} {l[2]}")
		else:
			# Make the decision based on resolution of last part of any redirect
			links = [l for l in reps[nb] if l[2][-1][2] != 200]
			if links:
				click.echo(f"\nBroken links in {nb}:")
				for l in links:
					click.echo(f"- [{l[0]}] {l[1]} {l[2]}")

	if grab_screenshots:
		click.echo("\nGrabbing screenshots for reported links.")
		"""
		Url: https://gist.github.com/wassname/1393c4a57cfcbf03641dbc31886123b8
		"""
		import unicodedata
		import string

		valid_filename_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)
		char_limit = 255

		def clean_filename(filename, whitelist=valid_filename_chars, replace=' '):
			# replace spaces
			filename = filename.split("://")[-1]
			for r in replace:
				filename = filename.replace(r, '_')
			
			# keep only valid ascii chars
			cleaned_filename = unicodedata.normalize('NFKD', filename).encode('ASCII', 'ignore').decode()
			
			# keep only whitelisted chars
			cleaned_filename = ''.join(c for c in cleaned_filename if c in whitelist)
			if len(cleaned_filename)>char_limit:
				print("Warning, filename truncated because it was over {}. Filenames may no longer be unique".format(char_limit))
			return cleaned_filename[:char_limit]

		shot_urls = list({l[1] for l in links})

		from playwright.sync_api import sync_playwright
		img_path = "grab_link_screenshots"
		p = Path(img_path)
		p.mkdir(parents=True, exist_ok=True)
		with sync_playwright() as p:
			browser = p.webkit.launch()
			page = browser.new_page()
			for shot_url in shot_urls:
				try:
					page.goto(shot_url)
					page.screenshot(path=Path(img_path) / clean_filename(f"{shot_url}.png"))
				except:
					click.echo(f"\t- failed to grab screenshot for {shot_url}")
				browser.close()
			click.echo(f"\nScreenshots saved to {img_path}")

@cli.command()
@click.argument('path')
@click.option('--out', '-o', default="warnings_report.html",  help='Report outfile')
def check_warnings(path, out):
	"""Check code output cells for warnings."""
	from .notebook_profiler import get_warnings

	if out:
		from tabulate import tabulate
		with Path(out).open('w') as f:
			f.write(tabulate(get_warnings(path), 
					headers=["path", "cell", "source", "warning"],
					tablefmt='unsafehtml'))
		click.echo(f"Report saved to: {out}")
	else:
		click.echo(get_warnings(path))
