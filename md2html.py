#!/usr/bin/env python
# vim: set fileencoding=utf-8 ts=4 sw=4 tw=79 noet :

import time
import argparse
import os
import tempfile
import urllib2
from subprocess import call
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from jinja2 import Template

parser = argparse.ArgumentParser(
	description='Renders Github Flavored Markdown files to HTML, optionally ' + \
		'using a custom Jinja2 template. Can also watch given path for ' + \
		'changes, using the --watch option. Uses the "marked" Markdown ' + \
		'parser (https://github.com/chjj/marked.')

parser.add_argument(
	'infile',
	type=str,
	default='.'
)
parser.add_argument(
	'--verbose',
	action='store_true',
	help='Be verbose?'
)
parser.add_argument(
	'--watch',
	action='store_true',
	default='',
	help='Watch filesystem for changes (infile is treated as path).'
)
parser.add_argument(
	'--template',
	type=str,
	default='https://raw.github.com/dfh/md2html.py/dev/templates/default.html',
	help='Jinja2 template file to wrap the rendered Markdown in. ' + \
		'Available context: content, timestamp, program_name.'
)
parser.add_argument(
	'--output-dir',
	type=str,
	default='.',
	help='Directory to write HTML output to, if using the --watch option.'
)

args = parser.parse_args()

template = None
if (args.template):
	# no, this isn't very pretty, but i don't know how to do it properly yet
	# (just started learning Python!)
	if (args.template[:4] == 'http'):
		template = Template(urllib2.urlopen(args.template).read())
	else:
		with open(args.template, 'r') as template_file:
			template = Template(template_file.read())


def markdown2html(in_fname, template=None, verbose=False):
	"""
	Returns HTML given input filename, optionally wrapped in given template.
	"""
	tmp = tempfile.NamedTemporaryFile()
	if verbose:
		print('Rendering {} -> {}...'.format(in_fname, tmp.name))

	# renders markdown using 'marked':
	# marked --output="foo.html" --input="foo.md"
	call(['marked', '--gfm', '--tables',
		'--smart-lists', '--lang-prefix=language-',
		'-o', tmp.name, '-i', in_fname])

	with open(tmp.name, 'r') as content_file:
		content = content_file.read().decode('utf-8')
		if (template):
			content = template.render(content=content,
				timestamp=time.asctime(), program_name='md2html')
	return content


class RenderMarkdownEventHandler(FileSystemEventHandler):
	def on_any_event(self, event):
		if args.verbose:
			print('{} ({}) @ {}'.format(event.event_type, event.src_path,
				time.asctime()))

		if event.is_directory:
			if (args.verbose):
				print('Is directory, skipping...')
		else:
			in_fname, in_ext = os.path.splitext(event.src_path)
			if (in_ext == '.md' or in_ext == '.markdown'):
				out_fname = os.path.join(args.output_dir, os.path.basename(in_fname) + '.html')
				with open(out_fname, 'w') as out_file:
					content = markdown2html(event.src_path, template=template,
						verbose=args.verbose)
					out_file.write(content.encode('utf-8'))
					print('Wrote {}'.format(out_fname))
			else:
				if args.verbose:
					print('Probably not Markdown, skipping...')


if __name__ == '__main__':
	if args.watch:
		event_handler = RenderMarkdownEventHandler()
		observer = Observer()
		observer.schedule(event_handler, path=args.infile, recursive=False)
		observer.start()
		print('Watching "{}" for changes...'.format(args.infile))
		try:
			while True:
				time.sleep(1)
		except KeyboardInterrupt:
			print('Aborting on user interrupt...')
			observer.stop()
		observer.join()
	else:
		print(markdown2html(args.infile, template=template,
			verbose=args.verbose))
