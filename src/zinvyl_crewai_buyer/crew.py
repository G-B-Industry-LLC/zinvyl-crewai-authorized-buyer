from __future__ import annotations

from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task


MCP_SERVER = {
    "url": "https://zinvyl.com/marketplace/agent-mcp",
    "transport": "streamable-http",
}


class _ZinvylCrewTools:
    """Limit each crew to the smallest tool set needed for its authority level."""

    mcp_server_params = [MCP_SERVER]
    mcp_connect_timeout = 30

    def _tools(self, allowed_names: set[str]):
        return [tool for tool in self.get_mcp_tools() if tool.name in allowed_names]


@CrewBase
class ZinvylPreviewCrew(_ZinvylCrewTools):
    """Read-only product matching. This crew cannot create a purchase intent."""

    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    @agent
    def procurement_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["procurement_agent"],
            tools=self._tools({"qualify_task", "list_offers", "get_acceptance_tests", "get_purchase_requirements"}),
            verbose=True,
        )

    @task
    def preview_task(self) -> Task:
        return Task(config=self.tasks_config["preview_task"])

    @crew
    def crew(self) -> Crew:
        return Crew(agents=self.agents, tasks=self.tasks, process=Process.sequential, verbose=True)


@CrewBase
class ZinvylAuthorizedBuyerCrew(_ZinvylCrewTools):
    """One-call purchase path enabled only after deterministic local preflight."""

    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    @agent
    def procurement_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["procurement_agent"],
            tools=self._tools({"get_purchase_requirements", "buy_matching_service"}),
            verbose=True,
        )

    @task
    def purchase_task(self) -> Task:
        return Task(config=self.tasks_config["purchase_task"])

    @crew
    def crew(self) -> Crew:
        return Crew(agents=self.agents, tasks=self.tasks, process=Process.sequential, verbose=True)

