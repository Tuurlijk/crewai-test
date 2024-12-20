from crewai_tools import ScrapeWebsiteTool, SerperDevTool

from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task


@CrewBase
class WebExtensionDevelopmentCrew:
    """WebExtensionDevelopment crew"""

    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    @agent
    def webextension_developer(self) -> Agent:
        return Agent(
            config=self.agents_config["webextension_developer"],
            tools=[SerperDevTool(), ScrapeWebsiteTool()],
            allow_delegation=False,
            verbose=True,
        )

    @agent
    def webextension_tester(self) -> Agent:
        return Agent(
            config=self.agents_config["webextension_tester"],
            tools=[SerperDevTool(), ScrapeWebsiteTool()],
            allow_delegation=False,
            verbose=True,
        )

    @task
    def webextension_developer_task(self) -> Task:
        return Task(
            config=self.tasks_config["webextension_developer_task"],
            agent=self.webextension_developer(),
        )

    @task
    def webextension_tester_task(self) -> Task:
        return Task(
            config=self.tasks_config["webextension_tester_task"],
            agent=self.webextension_tester(),
        )

    @crew
    def crew(self) -> Crew:
        """Creates the WebExtension crew"""
        return Crew(
            agents=self.agents,  # Automatically created by the @agent decorator
            tasks=self.tasks,  # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
            # process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
        )
