"""
Find and apply to jobs.

@dev You need to add OPENAI_API_KEY to your environment variables.

Also you have to install PyPDF2: pip install PyPDF2
"""

import csv
import os
import sys
from pathlib import Path

from PyPDF2 import PdfReader

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import asyncio
from typing import List, Optional

from langchain_openai import ChatOpenAI
from pydantic import BaseModel

from browser_use.agent.service import Agent
from browser_use.browser.service import Browser
from browser_use.controller.service import Controller

controller = Controller(keep_open=True)


class Job(BaseModel):
	title: str
	link: str
	company: str
	salary: Optional[str] = None
	location: Optional[str] = None


class Jobs(BaseModel):
	jobs: List[Job]


@controller.action('Save jobs to file', param_model=Jobs)
def save_jobs(params: Jobs):
	with open('jobs.csv', 'a', newline='') as f:
		writer = csv.writer(f)
		for job in params.jobs:
			writer.writerow([job.title, job.company, job.salary, job.link])


@controller.action('Read jobs from file')
def read_jobs():
	with open('jobs.csv', 'r') as f:
		return f.read()


@controller.action('Ask me for help')
def ask_human(question: str) -> str:
	return input(f'\n{question}\nInput: ')


@controller.action('Read my cv for context to fill forms')
def read_cv():
	pdf = PdfReader('your_cv.pdf')
	text = ''
	for page in pdf.pages:
		text += page.extract_text() or ''
	return text


@controller.action('Upload cv to index', requires_browser=True)
async def upload_cv(index: int, browser: Browser):
	await close_file_dialog(browser)
	element = await browser.get_element_by_index(index)
	my_cv = Path.cwd() / 'your_cv.pdf'
	if not element:
		raise Exception(f'Element with index {index} not found')

	await element.set_input_files(str(my_cv.absolute()))
	return f'Uploaded cv to index {index}'


@controller.action('Close file dialog', requires_browser=True)
async def close_file_dialog(browser: Browser):
	page = await browser.get_current_page()
	await page.keyboard.press('Escape')


async def main():
	task = (
		'Read my cv & find machine learning engineer jobs for me. '
		'Save them to a file'
		'then start applying for them in new tabs - please not via job portals like linkedin, indeed, etc. '
		'If you need more information or help, ask me.'
	)
	model = ChatOpenAI(model='gpt-4o')
	agent = Agent(task=task, llm=model, controller=controller)

	await agent.run()


if __name__ == '__main__':
	asyncio.run(main())
